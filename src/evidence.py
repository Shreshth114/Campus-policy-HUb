"""Evidence blocks and conservative quote/numeric attribution checks; no inferred authority."""
import copy
import re
import unicodedata
from difflib import SequenceMatcher

def normalize(text):
    text=unicodedata.normalize('NFKC',text).translate(str.maketrans({'“':'"','”':'"','‘':"'",'’':"'"}))
    return ' '.join(text.casefold().split())

def sentences(text):return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+',text) if s.strip()]

def relevant_sentence(text,question):
    body=text.split('\n',1)[-1] if ' > ' in text.split('\n',1)[0] else text
    rows=sentences(body)
    terms=set(re.findall(r'\b\w{4,}\b',question.casefold()))
    if not rows:return body
    return max(rows,key=lambda s:len(terms&set(re.findall(r'\b\w{4,}\b',s.casefold()))))

def ids(chunks):return list(dict.fromkeys(cid for c in chunks for cid in (c.source_chunk_ids or [c.chunk_id])))

def merge_blocks(chunks):
    blocks=[]
    for original in chunks:
        chunk=copy.deepcopy(original)
        chunk.source_chunk_ids=chunk.source_chunk_ids or [chunk.chunk_id]
        chunk.pages=chunk.pages or [chunk.page]
        body=chunk.text.split('\n',1)[-1] if ' > ' in chunk.text.split('\n',1)[0] else chunk.text
        target=None
        for candidate in blocks:
            if not chunk.version_id or (candidate.doc_id,candidate.version_id,candidate.workspace_id,candidate.institution_id)!=(chunk.doc_id,chunk.version_id,chunk.workspace_id,chunk.institution_id):continue
            same_page=set(candidate.pages)&set(chunk.pages)
            common=SequenceMatcher(None,normalize(candidate.text),normalize(body),autojunk=False).find_longest_match()
            if same_page and (abs(candidate.chunk_index-chunk.chunk_index)==1 or common.size>=max(60,min(len(candidate.text),len(body))*.45)):
                target=candidate;break
        if target is None:blocks.append(chunk);continue
        # Retain exact original passages as components; suppress duplicate sentences for display/context.
        seen={normalize(s) for s in sentences(target.text)}
        additions=[s for s in sentences(body) if normalize(s) not in seen]
        if additions:target.text+='\n'+' '.join(additions)
        target.source_chunk_ids=list(dict.fromkeys(target.source_chunk_ids+chunk.source_chunk_ids))
        target.pages=sorted(set(target.pages+chunk.pages));target.similarity=max(target.similarity,chunk.similarity)
    return blocks

def connect_continuations(chunks):
    """Join only retrieved, adjacent page continuations in the same source.

    No additional index reads, invented continuation or sentence deduplication.
    A dangling clause plus lower-case continuation is required. Other layouts
    remain separate and may require abstention.
    """
    remaining=[copy.deepcopy(c) for c in chunks]
    changed=True
    while changed:
        changed=False
        for a in remaining:
            if re.search(r'[.!?;][\)\]"”]*$',a.text.strip()):continue
            for b in remaining:
                if a is b or not a.version_id:continue
                if (a.doc_id,a.version_id,a.institution_id,a.workspace_id,a.section)!=(b.doc_id,b.version_id,b.institution_id,b.workspace_id,b.section):continue
                if b.chunk_index!=a.chunk_index+1 or b.page!=max(a.pages or [a.page])+1:continue
                body=b.text.split('\n',1)[-1] if ' > ' in b.text.split('\n',1)[0] else b.text
                if not re.match(r'[a-z]',body.strip()):continue
                a.text=a.text.rstrip()+' '+body.lstrip()
                a.source_chunk_ids=list(dict.fromkeys((a.source_chunk_ids or [a.chunk_id])+(b.source_chunk_ids or [b.chunk_id])))
                a.pages=sorted(set((a.pages or [a.page])+(b.pages or [b.page])))
                a.similarity=max(a.similarity,b.similarity)
                a.chunk_index=b.chunk_index
                remaining.remove(b);changed=True;break
            if changed:break
    return remaining

QUOTE_PATTERN=re.compile(r'"([^"\n]+)"|“([^”\n]+)”|(?<!\w)\x27([^\x27\n]{3,})\x27(?!\w)|‘([^’\n]{3,})’')

def quote_in_source(quote,source):
    position=0;source=normalize(source)
    segments=[normalize(s) for s in re.split(r'\.{3}|…',quote) if normalize(s)]
    if not segments:return False
    for segment in segments:
        found=source.find(segment,position)
        if found<0:return False
        position=found+len(segment)
    return True

def verify_quotes(answer,chunks):
    verified=[];failed=[]
    for match in QUOTE_PATTERN.finditer(answer):
        quote=next(g for g in match.groups() if g is not None)
        # Attribution belongs to this quotation only: same-line adjacent labels.
        # Do not scan forward through text/other quotes or inherit a prior label.
        after=answer[match.end():].split('\n',1)[0]
        attribution=re.match(r'[^\S\n]*[.,;:]?[^\S\n]*(\[[^\]\n]+\](?:[^\S\n]*[,;]?[^\S\n]*\[[^\]\n]+\])*)',after)
        labels=re.findall(r'\[([^\]]+)\]',attribution.group(1)) if attribution else []
        labels=list(dict.fromkeys(labels))
        indices=[int(label[1:])-1 for label in labels if re.fullmatch(r'C[1-9]\d*',label)]
        if not labels:
            reason='missing_quote_citation'
        elif len(indices)!=len(labels) or any(i>=len(chunks) for i in indices):
            reason='invalid_quote_citation'
        elif not all(quote_in_source(quote,chunks[i].text) for i in indices):
            reason='quote_mismatch'
        else:
            reason=None
        row={'quote':quote,'labels':labels}
        if reason:row['reason']=reason
        (failed if reason else verified).append(row)
    return verified,failed

def unsupported_claims(answer, chunks):
    """Compatibility wrapper using the same strict validator as generation."""
    return [f.get('claim') or f.get('qualification') or f['reason']
            for f in claim_failures(answer, chunks)]


# Conservative paraphrase vocabulary; no institution names or threshold constants.
_GROUNDING_STOP = set('a an the those who student students you your their they it its this that these for of in on to from by with be is are was were will shall must should have has need needs requires required requirement policy according states says says contains marker fixture document source course period at least as during'.split())


def _grounding_tokens(text):
    text = normalize(text)
    for pattern, replacement in [
        (r'\b(?:does not fall below|not less than|at least|or more)\b', ' minimum '),
        (r'\b(?:at most|no more than|not exceed)\b', ' maximum '),
        (r'\b(?:other than|outside|excluding)\b', ' excluding '),
        (r'\billness\b', ' medical leave '),
        (r'\b(?:on or before|no later than|not later than)\b', ' deadline '),
        (r'\b(?:percent|per cent)\b', '%'),
        (r'\b(?:require|requires|required|requirement)\b', ' '),
    ]:
        text = re.sub(pattern, replacement, text)
    numbers = {'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9','ten':'10'}
    return {numbers.get(t, t) for t in re.findall(r'\d+(?:\.\d+)?|[a-z]+|%', text)
            if t not in _GROUNDING_STOP}


def _answer_units(answer):
    # Do not split an attributed, multi-sentence quotation before its citation.
    quotes = []
    def hide(match):
        quotes.append(match.group());return f'QUOTEPLACEHOLDER{len(quotes)-1}'
    masked = QUOTE_PATTERN.sub(hide, answer)
    # Each individually attributed quote is a unit even on the same line.
    masked = re.sub(r'(QUOTEPLACEHOLDER\d+\s*\[C\d+\])\s+(?=QUOTEPLACEHOLDER)', r'\1\n', masked)
    units = re.split(r'\n+|(?<=[.!?])\s+(?!\[C\d+\])', masked)
    return [re.sub(r'QUOTEPLACEHOLDER(\d+)', lambda m: quotes[int(m[1])], u).strip()
            for u in units if u.strip()]


def _clauses(text):
    return [c for c in re.split(r',|;|\band\b|\bprovided(?: that)?\b', text, flags=re.I) if c.strip()]


def _supported_claim(claim, source):
    clean = re.sub(r'\s+', ' ', re.sub(r'^\s*(?:[-*•]|\d+\.)\s*', '', claim)).strip(' ."“”')
    if quote_in_source(clean, source):
        return True
    # Require every substantive word and every number in a paraphrased clause
    # to have support in ONE source clause. A number elsewhere is insufficient.
    candidates = [_grounding_tokens(c) for sentence in sentences(' '.join(source.split())) for c in _clauses(sentence)]
    for clause in _clauses(clean):
        tokens = _grounding_tokens(clause)
        if not tokens:
            continue
        numeric = {t for t in tokens if re.fullmatch(r'\d+(?:\.\d+)?', t)}
        # Ambiguous multi-value paraphrases require exact wording. Token sets
        # alone cannot prove which value belongs to which condition.
        if len(numeric) > 1:
            return False
        if not any(tokens <= candidate
                   and (not numeric or len({t for t in candidate if re.fullmatch(r'\d+(?:\.\d+)?', t)}) == 1)
                   and (tokens & {'not', 'no', 'never'}) == (candidate & {'not', 'no', 'never'})
                   for candidate in candidates):
            return False
    return True


def claim_failures(answer, chunks):
    """Fail closed on unsupported paraphrases, uncited claims and lost conditions.

    This is intentionally a restricted lexical/condition consistency validator,
    not general natural-language entailment. Exact source wording is preferred.
    """
    failures = []
    cited = set()
    supported_units = []
    for unit in _answer_units(answer):
        labels = [int(n)-1 for n in re.findall(r'\[C(\d+)\]', unit)]
        clean = re.sub(r'\[C\d+\]', '', unit).strip()
        if not clean.strip(' .:-*'):
            continue
        if not labels:
            failures.append({'reason':'uncited_claim', 'claim':clean});continue
        if any(i < 0 or i >= len(chunks) for i in labels):
            failures.append({'reason':'invalid_citation', 'claim':clean});continue
        # One cited excerpt must support the complete claim; do not combine
        # unrelated numbers from different sources into a new rule.
        if not any(_supported_claim(clean, chunks[i].text) for i in labels):
            failures.append({'reason':'unsupported_claim_or_condition', 'claim':clean});continue
        cited.update(labels)
        supported_units.append(clean)
    supported = ' '.join(supported_units)
    supported_tokens = _grounding_tokens(supported)
    for i in cited:
        source = chunks[i].text
        from src.grounding import provisions
        quotes = [next(g for g in m.groups() if g is not None) for m in QUOTE_PATTERN.finditer(supported)]
        units = provisions(source)
        matched = [u for u in units if any(quote_in_source(q,u) for q in quotes)]
        if matched and all(QUOTE_PATTERN.sub('', re.sub(r'\[C\d+\]', '', u)).strip(' .;,:') == '' for u in supported_units):
            source = '\n'.join(matched)
        # A selected provision is an atomic rule. Material qualifiers must not
        # disappear from the answer, even when its headline threshold is right.
        for sentence in sentences(' '.join(source.split())):
            if not re.search(r'\b(?:may|unless|provided|subject to|application|at most|whichever|approval|permission|except|only|deadline|within|before|after)\b', sentence, re.I):
                continue
            if quote_in_source(sentence, supported):
                continue
            qualifiers = _grounding_tokens(sentence) - {'provided', 'considered', 'shortage'}
            if not qualifiers <= supported_tokens:
                failures.append({'reason':'omitted_qualification', 'source_label':f'C{i+1}', 'qualification':sentence})
    return failures
