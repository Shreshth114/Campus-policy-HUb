"""
chunking.py — Section-aware text chunker for policy documents.

Splits PDF-extracted text into chunks suitable for embedding:
- Detects section headings (numbered clauses, article headers)
- Targets CHUNK_MAX_TOKENS tokens with CHUNK_OVERLAP_FRACTION overlap
- Prepends context header: "{doc_title} > {section_title}\n{text}"
- Generates deterministic chunk IDs via SHA-256
"""

import hashlib
import re
import unicodedata
from dataclasses import dataclass

from src.config import CHUNK_MAX_TOKENS, CHUNK_OVERLAP_FRACTION


@dataclass
class Chunk:
    """A single chunk of policy text with metadata."""
    chunk_id: str
    text: str                # context header + chunk text
    raw_text: str            # chunk text without header
    doc_id: str
    doc_title: str
    section: str
    page: int
    chunk_index: int
    file_hash: str
    source_path: str
    is_decoy: bool

    workspace_id: str = ""
    institution_id: str = ""
    version_id: str = ""
    is_synthetic: bool = False
    extraction_method: str = "unknown"
    approved: bool = False       # set True only via authority registry

    def to_metadata(self) -> dict:
        """Metadata dict for ChromaDB storage."""
        return {
            "workspace_id": self.workspace_id,
            "institution_id": self.institution_id,
            "version_id": self.version_id,
            "doc_id": self.doc_id,
            "doc_title": self.doc_title,
            "section": self.section,
            "page": self.page,
            "chunk_index": self.chunk_index,
            "file_hash": self.file_hash,
            "approved": self.approved,
            "source_path": self.source_path,
            "is_decoy": self.is_decoy,
            "is_synthetic": self.is_synthetic,
            "extraction_method": self.extraction_method,
        }


def _normalize_text(text: str) -> str:
    """Normalize Unicode (ligatures, non-breaking spaces) and collapse whitespace."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[^\S\n]+", " ", text).strip()
    return text


def _make_chunk_id(doc_id: str, section: str, chunk_index: int) -> str:
    """Deterministic chunk ID: SHA-256 of doc_id + section + chunk_index."""
    key = f"{doc_id}|{section}|{chunk_index}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


# Patterns to detect section headings in policy documents
_SECTION_PATTERNS = [
    # "4.2 Title" or "4.2. Title"
    re.compile(r"^(\d+(?:\.\d+)*\.?\s+.{3,80})$", re.MULTILINE),
    # "Article 7: Title" or "ARTICLE VII"
    re.compile(r"^((?:Article|ARTICLE|Section|SECTION|Chapter|CHAPTER)\s+[\dIVXLCDM]+[:\.\s].{0,80})$", re.MULTILINE),
    # "A. Title" or "B. Title" (uppercase letter sections)
    re.compile(r"^([A-Z]\.\s+.{3,80})$", re.MULTILINE),
    # ALL CAPS headings (at least 4 chars, common in policy docs)
    re.compile(r"^([A-Z][A-Z\s]{3,80})$", re.MULTILINE),
]


def _detect_sections(text: str) -> list[tuple[str, str, int]]:
    """
    Split text into (section_title, section_text, approx_page) tuples.
    Falls back to paragraph-based splitting if no headings detected.
    """
    # Find all heading positions
    headings: list[tuple[int, str]] = []
    for pattern in _SECTION_PATTERNS:
        for m in pattern.finditer(text):
            title = m.group(1).strip()
            # Skip very short matches or pure whitespace
            if len(title) > 3:
                headings.append((m.start(), title))

    # Deduplicate overlapping matches (keep earliest per position)
    headings.sort(key=lambda x: x[0])
    deduped: list[tuple[int, str]] = []
    for pos, title in headings:
        if not deduped or pos > deduped[-1][0] + len(deduped[-1][1]):
            deduped.append((pos, title))
    headings = deduped

    if not headings:
        # No headings found — split on double newlines (paragraphs)
        paragraphs = re.split(r"\n\s*\n", text)
        return [("General", p.strip(), 0) for p in paragraphs if p.strip()]

    sections: list[tuple[str, str, int]] = []
    preamble = text[:headings[0][0]].strip()
    if preamble:
        sections.append(("Preamble", preamble, 1))
    for i, (pos, title) in enumerate(headings):
        start = pos + len(title)
        end = headings[i + 1][0] if i + 1 < len(headings) else len(text)
        section_text = text[start:end].strip()
        if section_text:
            # Rough page estimate (assuming ~3000 chars per page)
            page_est = pos // 3000 + 1
            sections.append((title, section_text, page_est))

    return sections


def chunk_text(
    text: str,
    doc_id: str,
    doc_title: str,
    file_hash: str,
    source_path: str,
    is_decoy: bool = False,
) -> list[Chunk]:
    """
    Split document text into overlapping, section-aware chunks.

    Args:
        text: Full document text (already extracted from PDF).
        doc_id: Unique identifier for the document.
        doc_title: Human-readable document title.
        file_hash: SHA-256 hash of the source file.
        source_path: Path to the source file.
        is_decoy: Whether this is a decoy/fabricated document.

    Returns:
        List of Chunk objects ready for embedding and storage.
    """
    text = _normalize_text(text)
    sections = _detect_sections(text)
    if not sections:
        sections = [("General", text, 0)]
    chunks = []
    max_chars = CHUNK_MAX_TOKENS * 4
    overlap = int(max_chars * CHUNK_OVERLAP_FRACTION)
    if max_chars < 4 or not 0 <= overlap < max_chars:
        raise ValueError("Invalid chunk size or overlap")
    for section, body, page in sections:
        start = 0
        while start < len(body):
            end = min(start + max_chars, len(body))
            if end < len(body):
                boundary = body.rfind(" ", start + max_chars // 2, end)
                if boundary > start:
                    end = boundary
            raw = body[start:end].strip()
            if raw:
                index = len(chunks)
                chunks.append(Chunk(
                    chunk_id=_make_chunk_id(doc_id, section, index),
                    text=f"{doc_title} > {section}\n{raw}", raw_text=raw,
                    doc_id=doc_id, doc_title=doc_title, section=section,
                    page=page, chunk_index=index, file_hash=file_hash,
                    source_path=source_path, is_decoy=is_decoy,
                ))
            if end == len(body):
                break
            start = max(start + 1, end - overlap)
    return chunks


_VERB_PATTERN = re.compile(
    r'\b(shall|must|will|is|are|was|were|has|have|had|can|could|may|might|should|would|does|do|did|being|having)\b',
    re.IGNORECASE,
)


def _personal_heading(line: str) -> bool:
    line = line.strip()
    if not line or len(line) > 75 or len(line) < 3:
        return False
    if line.endswith((',', ';')):
        return False
    if line.endswith('.') and not re.match(r'^(?:Section|Chapter|[A-Z]?\d+(?:\.\d+)*\.?)\s+[A-Z][\w\s]{2,40}\.$', line):
        return False
    if _VERB_PATTERN.search(line):
        return False
    if line.endswith(':'):
        return len(line.split()) <= 7
    if re.match(r'^(?:Section\s+\d+|Chapter\s+\d+|[A-Z]?\d+(?:\.\d+)*\.?)\s+[A-Za-z]', line):
        return len(line.split()) <= 10
    if line.isupper() and len(line) >= 4 and len(line.split()) <= 7:
        if re.match(r'^(?:PAGE\s+\d+|\d+\s*\|\s*P\s*A\s*G\s*E)$', line, re.IGNORECASE):
            return False
        return True
    if len(line.split()) <= 6 and re.match(r'^[A-Z][a-zA-Z0-9\s/&()\-–—]+$', line):
        if re.search(r'\b(Credits?|semesters?|hours?|marks?|days?|months?)\b', line, re.IGNORECASE):
            return False
        return True
    return False


def clean_personal_text(text: str) -> str:
    """New personal ingestion only: repair common PDF line artefacts, retaining words."""
    text = unicodedata.normalize('NFKC', text).replace('\r\n', '\n')
    text = re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '', text)
    text = re.sub(r'(?m)^\s*[•●▪◦‣]\s*$', '', text)
    text = re.sub(r'[^\S\n]+', ' ', text)
    # PDF text layers may put the section number and title on separate lines.
    # Join only a standalone number followed by a recognized heading, never a rule.
    lines = text.splitlines()
    joined = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.fullmatch(r'(?:[A-Z]?\d+(?:\.\d+)*\.)', line):
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and _personal_heading(lines[j]):
                joined.append(line + ' ' + lines[j].strip())
                i = j + 1
                continue
        joined.append(line)
        i += 1
    lines = joined
    out = []
    for line in lines:
        line = line.strip()
        if re.match(r'^(?:PAGE\s+\d+|\d+\s*\|\s*P\s*a\s*g\s*e|\d+)$', line, re.IGNORECASE):
            continue
        if re.match(r'^[-=_~*]{3,}$', line):
            continue
        if out and line and out[-1] and not re.search(r'[.!?:;]$', out[-1]) and not _personal_heading(out[-1]) and not _personal_heading(line):
            out[-1] += ' ' + line
        else:
            out.append(line)
    return '\n'.join(out).strip()


def _clean_chunk_edges(raw: str) -> str:
    raw = raw.strip()
    while raw and raw[-1] in '-—–~^/\\([{':
        raw = raw[:-1].rstrip()
    if raw and not (raw[-1] in '.!?;:)]"\'0123456789' or raw.split()[-1].isalnum()):
        raw += '.'
    return raw


def _merge_personal_chunks(raw_chunks: list[dict]) -> list[dict]:
    """Combine continuations using source offsets, never guessed text overlap.

    Offsets refer to one page/section body. Re-slicing that body preserves real
    repetitions while removing only overlap introduced by the splitter. Never
    merge across sections or pages (a Chunk has only one source page).
    """
    merged: list[dict] = []
    for original in raw_chunks:
        c = dict(original)
        raw = c["raw_text"].strip()
        if not raw:
            continue
        starts_lowercase = bool(raw[0].isalpha() and raw[0].islower()
                                and len(raw.split()[0]) > 1
                                and raw.split()[0] not in {'e.g.', 'i.e.', 'etc.', 'v.', 'vs.'})
        prev = merged[-1] if merged else None
        same_body = (prev is not None and '_body' in c and '_body' in prev
                     and c['_body_key'] == prev['_body_key'])
        if same_body and (starts_lowercase or len(raw.split()) < 10
                          or len(prev['raw_text'].split()) < 10):
            prev['_end'] = c['_end']
            prev['raw_text'] = c['_body'][prev['_start']:prev['_end']].strip()
        else:
            merged.append(c)
    for c in merged:
        c["raw_text"] = _clean_chunk_edges(c["raw_text"])
        c["text"] = f"{c['doc_title']} > {c['section']}\n{c['raw_text']}"
    return merged


def chunk_personal(text: str, doc_id: str, doc_title: str, file_hash: str, source_path: str, page: int, fallback_heading: Optional[str] = None) -> list[Chunk]:
    text = clean_personal_text(text)
    heading = fallback_heading or f"Page {page}"
    sections = []
    body_lines = []
    for line in text.splitlines():
        if _personal_heading(line):
            if body_lines:
                sections.append((heading, "\n".join(body_lines)))
                body_lines = []
            heading = line
        elif line:
            body_lines.append(line)
    if body_lines:
        sections.append((heading, "\n".join(body_lines)))

    limit = CHUNK_MAX_TOKENS * 4
    overlap = int(limit * CHUNK_OVERLAP_FRACTION)
    raw_chunks = []
    for section_index, (h, body) in enumerate(sections):
        start = 0
        while start < len(body):
            end = min(start + limit, len(body))
            if end < len(body):
                sentence = max((m.end() for m in re.finditer(r'[.!?]\s+', body[start:end]) if m.end() > limit // 2), default=0)
                boundary = start + sentence if sentence else body.rfind(' ', start, end)
                if boundary > start:
                    end = boundary
                else:
                    next_space = body.find(' ', end)
                    end = len(body) if next_space < 0 else next_space
            raw = body[start:end].strip()
            if raw:
                raw_chunks.append({
                    "doc_title": doc_title,
                    "section": h,
                    "page": page,
                    "raw_text": raw,
                    "_body": body, "_body_key": (page, section_index),
                    "_start": start, "_end": end,
                })
            if end >= len(body):
                break
            next_start = max(start + 1, end - overlap)
            while next_start < end and next_start > 0 and not body[next_start - 1].isspace():
                next_start += 1
            start = next_start if next_start < end else end
            while start < len(body) and body[start].isspace():
                start += 1

    merged = _merge_personal_chunks(raw_chunks)
    result = []
    for idx, c in enumerate(merged):
        cid = _make_chunk_id(doc_id, c["section"], idx)
        result.append(Chunk(cid, c["text"], c["raw_text"], doc_id, doc_title, c["section"], page, idx, file_hash, source_path, False))
    return result


def chunk_personal_pages(pages: list[tuple[int, str, str]], doc_id: str, doc_title: str, file_hash: str, source_path: str, approved: bool = False, is_synthetic: bool = False) -> list[Chunk]:
    current_heading = None
    limit = CHUNK_MAX_TOKENS * 4
    overlap = int(limit * CHUNK_OVERLAP_FRACTION)
    raw_chunks = []

    for page_num, raw_text, method in pages:
        if not raw_text or len(raw_text.strip()) < 20:
            continue
        page_text = clean_personal_text(raw_text)
        if not page_text or len(page_text.strip()) < 20:
            continue
        sections = []
        body_lines = []
        heading = current_heading or f"Page {page_num}"
        for line in page_text.splitlines():
            line = line.strip()
            if not line:
                continue
            if _personal_heading(line):
                if body_lines:
                    sections.append((heading, "\n".join(body_lines)))
                    body_lines = []
                heading = line
                current_heading = line
            else:
                body_lines.append(line)
        if body_lines:
            sections.append((heading, "\n".join(body_lines)))

        for section_index, (h, body) in enumerate(sections):
            start = 0
            while start < len(body):
                end = min(start + limit, len(body))
                if end < len(body):
                    sentence = max((m.end() for m in re.finditer(r'[.!?]\s+', body[start:end]) if m.end() > limit // 2), default=0)
                    boundary = start + sentence if sentence else body.rfind(' ', start, end)
                    if boundary > start:
                        end = boundary
                    else:
                        next_space = body.find(' ', end)
                        end = len(body) if next_space < 0 else next_space
                raw = body[start:end].strip()
                if raw:
                    raw_chunks.append({
                        "doc_title": doc_title,
                        "section": h,
                        "page": page_num,
                        "raw_text": raw,
                        "method": method,
                        "_body": body, "_body_key": (page_num, section_index),
                        "_start": start, "_end": end,
                    })
                if end >= len(body):
                    break
                next_start = max(start + 1, end - overlap)
                while next_start < end and next_start > 0 and not body[next_start - 1].isspace():
                    next_start += 1
                start = next_start if next_start < end else end
                while start < len(body) and body[start].isspace():
                    start += 1

    merged = _merge_personal_chunks(raw_chunks)
    from src.institutions import current
    result = []
    for idx, c in enumerate(merged):
        cid = hashlib.sha256(f"{current().scope_id}|{doc_id}|{file_hash}|{c['section']}|{idx}".encode()).hexdigest()
        chunk = Chunk(
            chunk_id=cid,
            text=c["text"],
            raw_text=c["raw_text"],
            doc_id=doc_id,
            doc_title=doc_title,
            section=c["section"],
            page=c.get("page", 1),
            chunk_index=idx,
            file_hash=file_hash,
            source_path=source_path,
            is_decoy=False,
        )
        chunk.workspace_id = current().workspace_id
        chunk.institution_id = current().institution_id
        chunk.version_id = file_hash
        chunk.approved = approved
        chunk.is_synthetic = is_synthetic
        chunk.extraction_method = c.get("method", "fitz")
        result.append(chunk)
    return result
