"""Generic synthetic text/PDF fixtures verify parser pages and chunk boundaries."""
import pymupdf
import pytest
from src.chunking import chunk_text,_normalize_text
from src.ingest import ingest_file,extract_pages
from src import chunking


def chunks(text):
    return chunk_text(text,'fixture','Synthetic fixture','hash','/test-only',is_decoy=False)


def test_section_headings_and_preamble_preserved():
    result=chunks('This is a synthetic preamble.\n\n1. Alpha Heading\nFixture marker alpha.\n\n2. Beta Heading\nFixture marker beta.')
    assert {c.section for c in result}=={'Preamble','1. Alpha Heading','2. Beta Heading'}
    assert 'synthetic preamble' in result[0].text


def test_long_sentence_is_bounded_without_losing_tail(monkeypatch):
    monkeypatch.setattr(chunking,'CHUNK_MAX_TOKENS',20)
    text='fixturetoken '*100+'unique_final_marker'
    result=chunks(text)
    assert len(result)>1 and all(len(c.raw_text)<=80 for c in result)
    assert 'unique_final_marker' in result[-1].raw_text
    assert len({c.chunk_id for c in result})==len(result)
    assert [c.chunk_id for c in result]==[c.chunk_id for c in chunks(text)]


def test_unicode_normalization_preserves_line_structure():
    assert _normalize_text('ﬁxture\u00a0alpha\n\nFixture beta')=='fixture alpha\n\nFixture beta'


def test_short_text_is_not_discarded():
    assert chunks('Short synthetic fixture marker.')[0].raw_text=='Short synthetic fixture marker.'
    assert chunks('')==[]


def test_actual_pdf_page_numbers_are_preserved(tmp_path):
    path=tmp_path/'synthetic_fixture.pdf'
    with pymupdf.open() as document:
        for marker in ('alpha','beta'):
            page=document.new_page()
            page.insert_text((40,40),f'SYNTHETIC FIXTURE {marker}. This is parser test data and not a university policy. '*2)
        document.save(path)
    result=ingest_file(path,is_synthetic=True)
    assert {c.page for c in result}=={1,2}
    assert all(c.is_synthetic and not c.approved for c in result)
    assert len({c.chunk_id for c in result})==len(result)
    assert all(c.extraction_method=='pymupdf' for c in result)


def test_unreadable_pdf_returns_no_chunks(tmp_path):
    path=tmp_path/'broken.pdf'
    path.write_bytes(b'SYNTHETIC broken PDF fixture')
    assert ingest_file(path,is_synthetic=True)==[]


def test_pdf_fallback_is_recorded(monkeypatch,tmp_path):
    from types import SimpleNamespace
    from unittest.mock import MagicMock
    from src import ingest
    path=tmp_path/'fallback.pdf'
    path.write_bytes(b'SYNTHETIC parser fixture')
    primary=MagicMock()
    primary.__enter__.return_value=[SimpleNamespace(get_text=lambda:'tiny')]
    fallback=MagicMock()
    fallback.__enter__.return_value=SimpleNamespace(pages=[SimpleNamespace(extract_text=lambda:'SYNTHETIC fallback fixture marker. '*10)])
    monkeypatch.setattr(ingest.pymupdf,'open',lambda *_:primary)
    monkeypatch.setattr(ingest.pdfplumber,'open',lambda *_:fallback)
    result=ingest_file(path,is_synthetic=True)
    assert result and all(c.extraction_method=='pdfplumber' for c in result)
