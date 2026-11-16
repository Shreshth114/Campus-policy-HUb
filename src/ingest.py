"""
ingest.py — Parse PDFs, chunk, embed, and upsert into the vector DB.

Usage:
    python -m src.ingest              # ingest data/raw/ and data/decoys/
    python -m src.ingest --reset      # wipe collection first

Returns counts, per-file errors, changed paths and elapsed time.
"""

import hashlib
import sys
import time
from pathlib import Path

import pymupdf
import pdfplumber

from src.config import MANIFEST_PATH
from src.institutions import current, workspace_path
from src.chunking import chunk_text, Chunk
from src.authority import register_source, is_approved
from src.persistence import INDEX_LOCK, write_json


def _file_hash(path: Path) -> str:
    """SHA-256 hash of file contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()


def _doc_id_from_path(path: Path, is_decoy: bool = False) -> str:
    """Generate a stable doc_id from filename (without extension)."""
    from src.authority import get_registry
    for did, entry in get_registry().items():
        if not is_decoy and entry.get('source_path') == str(path): return did
    stem = hashlib.sha256((current().scope_id + '|' + str(path)).encode()).hexdigest()
    return "decoy__" + stem if is_decoy else stem


def _doc_title_from_path(path: Path) -> str:
    """Generate a human-readable title from filename."""
    return path.stem.replace("_", " ").replace("-", " ").title()


def extract_pages(path: Path):
    """Return actual page numbers and parser provenance; fallback per file."""
    if path.suffix.lower() == ".txt":
        return [(0, path.read_text(encoding="utf-8", errors="replace"), "text")]
    if path.suffix.lower() != ".pdf":
        raise ValueError("Only .pdf and .txt sources are supported")
    pages = []
    try:
        with pymupdf.open(str(path)) as doc:
            pages = [(i + 1, page.get_text(), "pymupdf") for i, page in enumerate(doc)]
    except Exception:
        pass
    average = sum(len(text.strip()) for _, text, _ in pages) / max(len(pages), 1)
    if not pages or average < 50:
        print(f"  [extract] Low PDF text yield for {path.name}; trying pdfplumber", flush=True)
        try:
            with pdfplumber.open(str(path)) as pdf:
                fallback = [(i + 1, page.extract_text() or "", "pdfplumber")
                            for i, page in enumerate(pdf.pages)]
            if sum(len(t) for _, t, _ in fallback) > sum(len(t) for _, t, _ in pages):
                pages = fallback
        except Exception:
            pass
    return pages


def extract_text(path: Path) -> str:
    return "\n\n".join(text for _, text, _ in extract_pages(path))


def ingest_file(path: Path, is_decoy: bool = False, is_synthetic: bool = False) -> list[Chunk]:
    """
    Parse, chunk, and return chunks for a single file.

    Registers the source in the authority registry (as pending).
    Sets approved=True on chunks only if the source is explicitly approved.
    Decoys are never approved.
    """
    doc_id = _doc_id_from_path(path, is_decoy=is_decoy)
    doc_title = _doc_title_from_path(path)
    fhash = _file_hash(path)
    from src.authority import get_registry
    is_synthetic = is_synthetic or bool(get_registry().get(doc_id,{}).get('is_synthetic'))

    # Register in authority registry (does not auto-approve)
    if not is_decoy:
        register_source(
            doc_id=doc_id,
            doc_title=doc_title,
            source_path=str(path),
            is_synthetic=is_synthetic,
        )

    approved = (not is_decoy) and (not is_synthetic) and is_approved(doc_id)

    print(f"  Parsing: {path.name} (doc_id={doc_id}, approved={approved})", flush=True)
    started = time.perf_counter()
    pages = extract_pages(path)
    short_pages = sum(len(text.strip()) < 20 for _, text, _ in pages)
    print(f"    Extraction: {len(pages)} pages, {sum(len(text) for _, text, _ in pages)} chars; "
          f"{short_pages} short/empty pages; parsers={','.join(sorted({method for _, _, method in pages})) or 'none'}; "
          f"{time.perf_counter() - started:.2f}s", flush=True)
    started = time.perf_counter()
    chunks = []
    from src.chunking import _make_chunk_id
    if current().personal:
        from src.chunking import chunk_personal_pages
        chunks = chunk_personal_pages(pages, doc_id, doc_title, fhash, str(path), approved=approved, is_synthetic=is_synthetic)
    else:
        for page, text, method in pages:
            if not text or len(text.strip()) < 20:
                continue
            page_chunks = chunk_text(text, doc_id, doc_title, fhash, str(path), is_decoy=is_decoy)
            for chunk in page_chunks:
                chunk.chunk_index = len(chunks)
                chunk.chunk_id = _make_chunk_id(doc_id, chunk.section, chunk.chunk_index)
                chunk.workspace_id = current().workspace_id
                chunk.institution_id = current().institution_id
                chunk.version_id = fhash
                chunk.chunk_id = hashlib.sha256(f"{current().scope_id}|{doc_id}|{fhash}|{chunk.section}|{chunk.chunk_index}".encode()).hexdigest()
                chunk.page = page
                chunk.approved = approved
                chunk.is_synthetic = is_synthetic
                chunk.extraction_method = method
                chunks.append(chunk)
    print(f"    Chunking: {len(chunks)} chunks (approved={approved}); "
          f"{time.perf_counter() - started:.2f}s", flush=True)
    return chunks


def ingest_all(reset: bool = False) -> dict:
    """
    Ingest all PDFs from data/raw/ and data/decoys/.

    Returns a report dict with counts and timing.
    """
    if reset:
        raise ValueError('Global reset is disabled; use scoped document removal')
    from src.reindex import reindex
    return reindex()


if __name__ == "__main__":
    import argparse
    from src.institutions import resolve, scope
    parser=argparse.ArgumentParser();parser.add_argument('--institution-id',required=True)
    args=parser.parse_args()
    with scope(resolve(args.institution_id)):ingest_all()
