"""Exact development-response regression, not a held-out question or fake success."""
import json,re,html
from pathlib import Path
import pytest
from src.answer import canonicalize_citations,validate_answer,complete_source_conditions
from src.evidence import verify_quotes,quote_in_source
from tests.test_guardrails import make_chunk

RECORD=json.loads((Path(__file__).parent/'fixtures/quotation_attribution/ps1_14_fusion.json').read_text())

def original_chunks():
    return [make_chunk(str(i),text=html.unescape(text)) for i,text in enumerate(re.findall(r'<excerpt[^>]*>\n(.*?)\n</excerpt>',RECORD['messages'][1]['content'],re.S))]


def test_exact_failed_response_is_missing_attribution_not_altered_text():
    raw=RECORD['raw_response'];cs=original_chunks()
    assert len(re.findall('“([^”]+)”',raw))==5
    assert all(quote_in_source(q,cs[0].text) for q in re.findall('“([^”]+)”',raw))
    answer=canonicalize_citations(raw)
    ok,bad=verify_quotes(answer,cs)
    assert len(ok)==1 and len(bad)==4
    assert {f['reason'] for f in bad}=={'missing_quote_citation'}
    assert validate_answer(answer,cs)[0]=='quote_verification_failed'
    assert complete_source_conditions(answer,cs)==(answer,False)


def test_each_exact_quote_with_adjacent_citation_passes():
    text='\n'.join('“'+q+'” [C1]' for q in re.findall('“([^”]+)”',RECORD['raw_response']))
    assert validate_answer(text,original_chunks())[0] is None


@pytest.mark.parametrize('text,expected',[
 ('“Attendance is 75%.” “Approval is required.” [C1]','missing_quote_citation'),
 ('[C1] “Attendance is 75%.”','missing_quote_citation'),
 ('“Attendance is 75%.”\n[C1]','missing_quote_citation'),
 ('“Attendance is 60%.” [C1]','quote_mismatch'),
 ('“Attendance is 75%.” [C99]','invalid_quote_citation'),
 ('“Attendance is 75%.” [C0]','invalid_quote_citation'),
 ('“Attendance is 75%.” [Cfoo]','invalid_quote_citation'),
 ('“Attendance is 75%.” explanation [C1]','missing_quote_citation'),
])
def test_failure_categories_and_no_retroactive_attribution(text,expected):
    _,failed=verify_quotes(text,[make_chunk(text='Attendance is 75%. Approval is required.')])
    assert failed and failed[0]['reason']==expected
