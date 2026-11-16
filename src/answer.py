"""
answer.py — Grounded answer generation with guardrails.

Guardrail layers (explained in the video):
1. Structural isolation: generate_answer(question, chunks) — no HyDE parameter.
2. Confidence gate: abstain if best similarity < CONFIDENCE_THRESHOLD.
3. Grounded prompt: answer only from chunks, cite as [C1].
4. Citation check: every [Cn] must map to a retrieved chunk.
5. Abstain response: safe fallback with no invented permissions.
"""

import re
import json
import math
import copy
from typing import Optional

from src.llm import get_llm_client, LLMResponse, ProviderUnavailableError
from src.prompts import ANSWER_SYSTEM_PROMPT, ANSWER_USER_TEMPLATE, format_chunks_for_prompt
from src.config import CONFIDENCE_THRESHOLD, ANSWER_MAX_TOKENS, ANSWER_CHUNKS_LIMIT
from src.store import RetrievedChunk
from src.institutions import current

# The abstain message — no invented permissions
ABSTAIN_MESSAGE = (
    "I couldn't find a policy that covers this. "
    "Please contact the Department office or Academic section for clarification."
)


def confidence_gate(chunks: list[RetrievedChunk]) -> tuple[bool, Optional[str]]:
    """
    Check if the best chunk score meets the confidence threshold.

    Returns:
        (passes, reason) — True if retrieval is confident enough.
    """
    institution_id = current().institution_id
    if any(not current().owns(c) for c in chunks): return False, "foreign_evidence"
    if not chunks:
        return False, "no_chunks_retrieved"
    if any(c.is_decoy or c.is_synthetic or (not current().personal and not c.approved) for c in chunks):
        return False, "unapproved_evidence"

    if any(not math.isfinite(c.similarity) for c in chunks):
        return False, "invalid_similarity"
    best_score = max(c.similarity for c in chunks)
    if best_score < CONFIDENCE_THRESHOLD:
        return False, f"low_confidence (best={best_score:.3f}, threshold={CONFIDENCE_THRESHOLD})"

    return True, None


def trim_chunk_span(text: str, question: str) -> str:
    """Select an entire numbered provision, not a sentence and its neighbours.

    Use the existing ingestion chunk-size budget. Unstructured passages must fit
    whole; a rule that exceeds the budget is withheld rather than cut mid-rule.
    """
    from src.config import CHUNK_MAX_TOKENS
    from src.evidence import sentences
    budget = CHUNK_MAX_TOKENS * 4
    boundaries = list(re.finditer(r'(?<!\w)(?:[A-Z]\d+(?:\.\d+)*|\d+\.\d+(?:\.\d+)*)\.\s+', text))
    if boundaries:
        provisions = [text[m.start():boundaries[i+1].start() if i+1 < len(boundaries) else len(text)].strip()
                      for i, m in enumerate(boundaries)]
        # Section labels such as B11. Attendance are not substantive rules.
        # A heading may precede rules in a merged retrieval block; never let an
        # exact-word tie choose that heading as the only answer context.
        provisions = [p for p in provisions if re.search(
            r'\b(?:shall|must|may|should|will|is|are|has|have|cannot|permitted|required|allowed|eligible)\b',
            re.sub(r'^\S+\s+', '', p), re.I)]
        if not provisions:
            return ''
        from src.query_intent import provision_terms
        terms = provision_terms(question)
        selected = max(provisions, key=lambda p: len(terms & set(re.findall(r'\b\w{4,}\b', p.casefold()))))
    else:
        selected = text.split('\n', 1)[-1] if ' > ' in text.split('\n', 1)[0] else text.strip()
        if len(selected) > budget:
            # Retrieval blocks can repeat identical overlapping sentences. Keep
            # every distinct sentence, including all qualifiers; never crop them.
            selected = ' '.join(dict.fromkeys(sentences(selected)))
    return selected if len(selected) <= budget else ''


def answer_evidence(question, chunks):
    """Pack whole provisions into the existing total input budget.

    Consider every retrieved block; preserve original unit order and source
    mappings. Never truncate a provision to fit and never reconstruct PDF text.
    """
    from src.config import CHUNK_MAX_TOKENS
    from src.grounding import provisions
    from src.query_intent import provision_terms
    budget = ANSWER_CHUNKS_LIMIT * CHUNK_MAX_TOKENS * 4
    terms = provision_terms(question) - {'what','which','when','where','does','have','this','that','according','uploaded','required'}
    candidates = []
    for rank, c in enumerate(chunks):
        units = provisions(c.text)
        scored = [(len(terms & set(re.findall(r'\b\w{4,}\b',unit.casefold()))),index,unit)
                  for index,unit in enumerate(units)]
        if scored:
            candidates.append((max(row[0] for row in scored),rank,scored))
    result = []; used = 0
    for _,rank,scored in sorted(candidates,key=lambda row:(-row[0],row[1])):
        if len(result)>=ANSWER_CHUNKS_LIMIT:break
        whole = '\n'.join(unit for _,_,unit in scored)
        if len(whole)<=budget-used:
            chosen = [(index,unit) for _,index,unit in scored]
        else:
            # Atomic fallback only when the full block cannot fit. Keep
            # neighbouring units ahead of distant ones after choosing the anchor.
            anchor = max(scored,key=lambda row:row[0])[1]
            chosen = []
            remaining = budget-used
            for score,index,unit in sorted(scored,key=lambda row:(abs(row[1]-anchor),-row[0])):
                cost = len(unit)+(1 if chosen else 0)
                if cost<=remaining:
                    chosen.append((index,unit));remaining-=cost
        if chosen:
            c = copy.copy(chunks[rank])
            c.text = '\n'.join(unit for _,unit in sorted(chosen))
            result.append(c);used+=len(c.text)
    return result


def generation_budget(chunks):
    """Budget exact-source coverage plus reasoning/format overhead, with a cap.

    Input evidence size is unchanged. 2 chars/token is a conservative allowance
    for PDF punctuation, numbers and output quoting; reserve 160 for reasoning.
    """
    return max(ANSWER_MAX_TOKENS, min(1200, sum(len(c.text) for c in chunks)//2 + 160))


def complete_source_conditions(text, chunks):
    """Append exact missing source conditions only to otherwise supported claims.

    Never repair an invented claim, bad quote, missing citation or truncation.
    The addition is explicitly labelled as source text, not model generation.
    """
    from src.evidence import QUOTE_PATTERN
    outside = QUOTE_PATTERN.sub('', text)
    outside = re.sub(r'\[C\d+\]', '', outside)
    if re.sub(r'[\s.,;:]', '', outside):
        return text, False
    reason, _, failures = validate_answer(text, chunks)
    if not failures or any(f['reason'] != 'omitted_qualification' for f in failures):
        return text, False
    additions = []
    for f in failures:
        label = f['source_label']
        quote = f['qualification']
        # Avoid ambiguous quotation markup. Original wording remains literal.
        if any(c in quote for c in ('"','“','”')):
            return text, False
        additions.append('"' + quote + '" [' + label + ']')
    completed = text + '\n\n' + '\n'.join(additions)
    if validate_answer(completed, chunks)[0] is not None:
        return text, False
    return completed, True


def canonicalize_citations(text):
    return re.sub(r'【C([1-9]\d*)】', r'[C\1]', text)


def validate_answer(answer_text, chunks):
    """Shared, ordered validation for fresh responses and cache hits."""
    from src.evidence import verify_quotes, claim_failures
    answer_text = canonicalize_citations(answer_text)
    valid, cited = check_citations(answer_text, chunks)
    _, failed = verify_quotes(answer_text, chunks)
    claims = claim_failures(answer_text, chunks)
    failures = ([{'reason': 'missing_or_invalid_citation'}] if not valid else [])
    failures += failed
    failures += claims
    reason = ('citation_check_failed' if not valid else
              'quote_verification_failed' if failed else
              'unsupported_cited_claim' if claims else None)
    return reason, [] if reason else cited, failures


def _build_answer_prompt(question: str, chunks: list[RetrievedChunk], trim: bool = True) -> list[dict]:
    """
    Build the answer LLM prompt from question and retrieved chunks.

    This function is the structural isolation point — it takes ONLY
    the question and real chunks. No HyDE text parameter exists.
    """
    from src.question_coverage import question_requirements
    active_chunks = answer_evidence(question, chunks) if trim else chunks[:ANSWER_CHUNKS_LIMIT]
    chunk_dicts = [
        {
            "chunk_id": c.chunk_id,
            "text": c.text,
            "doc_title": c.doc_title,
            "section": c.section,
            "page": c.page,
            "pages": c.pages or [c.page],
        }
        for c in active_chunks
    ]

    labelled = format_chunks_for_prompt(chunk_dicts,provision_labels=True)

    return [
        {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
        {"role": "user", "content": ANSWER_USER_TEMPLATE.format(
            labelled_chunks=labelled,
            question=question,
        ) + '\nCoverage requirements (all retain the full question scope):\n' + json.dumps(question_requirements(question))},
    ]


def _extract_prompt_text(messages: list[dict]) -> str:
    """Extract all text from message list (for testing isolation)."""
    return "\n".join(m["content"] for m in messages)


def check_citations(answer_text: str, chunks: list[RetrievedChunk]) -> tuple[bool, list[str]]:
    """
    Verify that every [Cn] citation in the answer maps to a retrieved chunk.

    Returns:
        (valid, cited_chunk_ids) — True if all citations are valid.
    """
    if any(not current().owns(c) for c in chunks): return False, []
    # Extract all citation references [C1], [C2], etc.
    citations = re.findall(r"\[C(\d+)\]", answer_text)
    if not citations:
        return False, []  # Answer must have at least one citation

    cited_ids = []
    for c_num in citations:
        idx = int(c_num) - 1  # C1 -> index 0
        if idx < 0 or idx >= len(chunks):
            return False, cited_ids  # Citation references non-existent chunk
        cited_ids.append(chunks[idx].chunk_id)

    return True, list(dict.fromkeys(cited_ids))


async def generate_answer(
    question: str,
    chunks: list[RetrievedChunk],
) -> tuple[str, Optional[str], list[str], Optional[LLMResponse]]:
    """
    Generate a grounded answer from question + real policy chunks.

    This is the structural isolation point: NO HyDE text parameter.

    Args:
        question: Original student question.
        chunks: Retrieved real policy chunks.

    Returns:
        (answer_text, abstain_reason, cited_chunk_ids, llm_response)
    """
    # Layer 2: Confidence gate
    passes, gate_reason = confidence_gate(chunks)
    if not passes:
        return ABSTAIN_MESSAGE, gate_reason, [], None

    from src.store import valid_cached_citations
    from src.evidence import ids
    if not valid_cached_citations(ids(chunks)):
        return ABSTAIN_MESSAGE, 'source_changed', [], None

    # Estimate tokens before trimming (full text of all retrieved chunks)
    full_chunk_dicts = [
        {"chunk_id": c.chunk_id, "text": c.text, "doc_title": c.doc_title, "section": c.section, "page": c.page}
        for c in chunks
    ]
    full_prompt_text = ANSWER_SYSTEM_PROMPT + "\n" + ANSWER_USER_TEMPLATE.format(
        labelled_chunks=format_chunks_for_prompt(full_chunk_dicts),
        question=question,
    )
    est_before = max(1, len(full_prompt_text) // 4)

    # Layer 3: Build grounded prompt and call LLM
    active_chunks = answer_evidence(question, chunks)
    if not active_chunks or any(not c.text for c in active_chunks):
        return ABSTAIN_MESSAGE, 'incomplete_evidence_context', [], None
    messages = _build_answer_prompt(question, active_chunks, trim=False)
    actual_prompt_text = _extract_prompt_text(messages)
    est_after = max(1, len(actual_prompt_text) // 4)

    client = get_llm_client()
    response = await client.chat(
        messages=messages,
        max_tokens=generation_budget(active_chunks),
        temperature=0.1,  # low temperature for factual answers
    )
    response.tokens_estimated_before = est_before
    response.tokens_estimated_after = est_after

    from src.question_coverage import question_requirements,selected_references,coverage_failures
    response.question_requirements = question_requirements(question)
    response.answer_excerpts = {c.chunk_id: c.text for c in active_chunks}
    answer_text = canonicalize_citations(response.text)
    if getattr(response, 'finish_reason', None) == 'length':
        response.validation_failures = [{'reason':'output_token_limit'}]
        from src.answer_diagnostics import record_answer
        record_answer(messages, [next(c for c in chunks if c.chunk_id==a.chunk_id) for a in active_chunks], active_chunks, response.text,
                      'incomplete_generation', [{'reason':'output_token_limit'}])
        return ABSTAIN_MESSAGE, 'incomplete_generation', [], response

    from src.grounding import (parse_object, render_contract, review_messages,
                               review_passes, make_proof)
    contract = parse_object(response.text)
    answer_text, failures = render_contract(contract, active_chunks)
    reason = ('citation_check_failed' if any(f['reason']=='invalid_quote_citation' for f in failures)
              else 'invalid_answer_contract' if failures else None)
    if response.text.strip() == 'NO_POLICY_FOUND' or any(f['reason']=='model_abstained' for f in failures):
        reason = 'no_policy_found'
    cited_ids = []
    if not reason:
        reason, cited_ids, failures = validate_answer(answer_text, active_chunks)
    if not reason:
        review_prompt = review_messages(question,active_chunks,contract)
        reviewed = await client.chat(messages=review_prompt,max_tokens=400,temperature=0)
        review = parse_object(reviewed.text)
        response.coverage_review = {'messages':review_prompt,'raw':reviewed.text,'verdict':review}
        response.review_usage = {k:getattr(reviewed,k,None) for k in
                                ('provider','model','latency_ms','input_tokens','output_tokens','finish_reason','reasoning_tokens')}
        response.evidence_coverage = review.get('coverage',[]) if review else []
        coverage_errors = coverage_failures(response.evidence_coverage,response.question_requirements,selected_references(contract,active_chunks))
        if getattr(reviewed,'finish_reason',None)=='length' or not review_passes(review,response.question_requirements,selected_references(contract,active_chunks)):
            reason = 'question_coverage_failed'
            failures = [{'reason':reason,'details':review.get('reasons',[]) if review else ['invalid_review_contract']}] + coverage_errors
            cited_ids = []
        else:
            response.grounding_proof = make_proof(question,answer_text,active_chunks,contract,review)
    response.validation_failures = failures
    from src.answer_diagnostics import record_answer
    record_answer(messages, [next(c for c in chunks if c.chunk_id==a.chunk_id) for a in active_chunks],
                  active_chunks, response.text, reason, failures,
                  review=getattr(response,'coverage_review',None))
    if reason:
        return ABSTAIN_MESSAGE, reason, [], response
    return answer_text, None, cited_ids, response
