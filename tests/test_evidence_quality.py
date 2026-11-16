import pytest
from src.chunking import clean_personal_text,chunk_personal
from src.evidence import merge_blocks,verify_quotes,unsupported_claims
from tests.test_guardrails import make_chunk

def test_personal_cleanup_boundaries_and_page_fallback():
    assert clean_personal_text('data sto-\nrage\ncontinues\n•\n\nNext.')=='data storage continues\n\nNext.'
    text=' '.join(['data storage device.']*300)
    chunks=chunk_personal(text,'d','Title','hash','path',7)
    assert chunks and all(c.section=='Page 7' for c in chunks)
    assert all(c.raw_text.startswith(('data','storage','device.')) for c in chunks)
    assert all(c.raw_text.split()[-1] in {'data','storage','device.'} for c in chunks)

def test_adjacent_evidence_merges_without_duplicate_sentence():
    a=make_chunk('a',text='Attendance must be 75 percent. Appeals require written permission.');b=make_chunk('b',text='Appeals require written permission. Submit the form in three days.')
    a.version_id=b.version_id='hash';a.chunk_index=0;b.chunk_index=1
    blocks=merge_blocks([a,b]);assert len(blocks)==1 and blocks[0].source_chunk_ids==['a','b']
    assert blocks[0].text.count('Appeals require written permission.')==1

@pytest.mark.parametrize('text',[ 'The rule says "Attendance must be 95 percent" [C1].','The rule says "fabricated permission" [C1].','"Attendance must be 75 percent" [C2].'])
def test_fabricated_altered_or_foreign_quote_rejected(text):
    chunks=[make_chunk('a',text='Attendance must be 75 percent.'),make_chunk('b',text='The hostel closes at 10 pm.')]
    assert verify_quotes(text,chunks)[1]

def test_normalized_quote_ellipsis_and_correct_attribution():
    chunks=[make_chunk(text='Attendance   MUST be 75 percent. Permission requires written approval.')]
    ok,bad=verify_quotes('“attendance must be 75 percent … permission requires written approval” [C1].',chunks)
    assert len(ok)==1 and not bad

def test_unrelated_and_altered_numeric_cited_claims_rejected():
    chunks=[make_chunk(text='Attendance must be 75 percent.')]
    assert unsupported_claims('Residence accommodation is completely free [C1].',chunks)
    assert unsupported_claims('Attendance must be 95 percent [C1].',chunks)
