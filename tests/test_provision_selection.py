"""Actual failed-context regressions; no providers, embeddings or production writes."""
import json
from pathlib import Path
from html import unescape
from src.answer import trim_chunk_span, _build_answer_prompt, answer_evidence
from tests.test_guardrails import make_chunk
from tests.test_answer_grounding_regressions import PAGE,PROVISION

Q='I was sick and missed classes. Is there a way to still write my finals?'


def test_informal_illness_selects_complete_medical_attendance_provision():
    result=trim_chunk_span('B11. Attendance\n'+PAGE[PAGE.index('B11.1.'):PAGE.index('B12.')],Q)
    assert ' '.join(result.split())==PROVISION


def test_actual_recorded_retrieved_block_reaches_answer_prompt():
    path=Path(__file__).parents[1]/'evaluation/ps1/runs/reliability-paced-2026-11-16/ps1-14-raw.json'
    record=json.loads(path.read_text());c=record['trace']['retrieved'][0]
    chunk=make_chunk(c['chunk_id'],text=c['text'],section=c['section'],page=c['page'])
    prompt=unescape(_build_answer_prompt(Q,[chunk])[1]['content'])
    assert PROVISION in ' '.join(prompt.split())
    assert 'p.10' in prompt and '<excerpt id="C1"' in prompt
    assert chunk.text==c['text']


def test_heading_only_is_not_sent_as_policy_evidence():
    assert trim_chunk_span('B11. Attendance',Q)==''


def test_missed_exam_is_not_reinterpreted_as_missed_classes():
    text='B15. Make-up examination\nB15.1. Students who miss examinations due to serious illness may apply for a make-up examination.\nB15.2. Students shall apply within five days.'
    result=trim_chunk_span(text,'I was sick and missed my exam. Can I take it later?')
    assert result.startswith('B15.1.')


def test_generic_other_institution_numbering_and_no_invented_policy():
    text='R7. Attendance\nR7.1. Teachers shall record attendance.\nR7.2. Medical absence may be considered for attendance relaxation with written permission.'
    result=trim_chunk_span(text,Q)
    assert result=='R7.2. Medical absence may be considered for attendance relaxation with written permission.'
