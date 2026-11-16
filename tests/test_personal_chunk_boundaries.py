"""Exact user-supplied page text is a test fixture, never production policy data."""
from pathlib import Path
import re
import pytest
from src import chunking

PAGE10 = (Path(__file__).parent / 'fixtures/chunking/nit_goa_page_10.txt').read_text()


def words(text):
    return ' '.join(text.split())


@pytest.mark.parametrize('entrypoint', ['single', 'pages'])
def test_exact_page10_preserves_complete_rules_and_numbered_sections(entrypoint):
    args = ('doc', 'Test document', 'hash', 'test-only.pdf')
    if entrypoint == 'single':
        chunks = chunking.chunk_personal(PAGE10, *args, page=10)
    else:
        chunks = chunking.chunk_personal_pages([(10, PAGE10, 'pymupdf')], *args)
    attendance = [c for c in chunks if c.section == 'B11. Attendance']
    assert len(attendance) == 1
    body = attendance[0].raw_text
    # Compare every word of B11.1 through B11.5, not only absence of duplication.
    expected = PAGE10[PAGE10.index('B11.1.'):PAGE10.index('B12.')]
    assert words(body) == words(expected)
    b114 = body[body.index('B11.4.'):body.index('B11.5.')]
    source_b114 = PAGE10[PAGE10.index('B11.4.'):PAGE10.index('B11.5.')]
    assert words(b114) == words(source_b114)
    assert body.count('may permit the student to appear') == 1
    assert '80%' in b114 and '75%' in b114
    assert 'seven days' in b114 and 'two' in b114
    assert 'B12.' not in body
    assessment = [c for c in chunks if c.section == 'B12. Assessment Procedure']
    assert len(assessment) == 1
    assert assessment[0].raw_text.startswith('B12.1.')
    assert words(assessment[0].raw_text) == words(PAGE10[PAGE10.index('B12.1.'):PAGE10.index('B13.')])
    assert all(c.page == 10 for c in chunks)


def segment(body, start, end, key=(10, 0)):
    return {'doc_title': 'Fixture', 'section': 'B11. Attendance', 'page': key[0],
            'raw_text': body[start:end], '_body': body, '_body_key': key,
            '_start': start, '_end': end}


@pytest.mark.parametrize('overlap', [0, 5, 18, 35])
def test_offset_merge_preserves_legitimate_repeated_sentences(overlap):
    body = 'A student must apply in seven days. A student must apply in seven days. Approval is required.'
    cut = 65
    parts = [segment(body, 0, cut), segment(body, cut-overlap, len(body))]
    result = chunking._merge_personal_chunks(parts)
    assert len(result) == 1
    assert result[0]['raw_text'] == body
    assert result[0]['raw_text'].count('A student must apply in seven days.') == 2
    assert parts[0]['raw_text'] == body[:cut]  # no mutation of input segments


def test_identical_text_without_source_offsets_is_not_deduplicated():
    parts = [dict(doc_title='Fixture', section='Rule', page=1, raw_text='approval is required.') for _ in range(2)]
    result = chunking._merge_personal_chunks(parts)
    assert len(result) == 2
    assert sum(c['raw_text'].count('approval is required.') for c in result) == 2


@pytest.mark.parametrize('key', [(10, 1), (11, 0)])
def test_short_lowercase_segments_never_cross_section_or_page(key):
    a = segment('prior approval is required.', 0, 27)
    b = segment('apply within seven days.', 0, 24, key)
    result = chunking._merge_personal_chunks([a, b])
    assert len(result) == 2
    assert [c['page'] for c in result] == [10, key[0]]


@pytest.mark.parametrize('heading', ['B12.\nAssessment Procedure', 'B12. Assessment Procedure', '12.\n\nAssessment Procedure'])
def test_short_sections_keep_own_heading_and_number(heading):
    text = 'B11.\nAttendance\nB11.1. Attendance must be at least 80%.\n'+heading+'\nB12.1. Approval is required.'
    chunks = chunking.chunk_personal(text, 'd', 'Fixture', 'hash', 'fixture', 10)
    assert len(chunks) == 2
    assert chunks[0].section == 'B11. Attendance'
    assert chunks[0].raw_text == 'B11.1. Attendance must be at least 80%.'
    assert chunks[1].section.endswith('Assessment Procedure')
    assert chunks[1].raw_text == 'B12.1. Approval is required.'


def test_number_before_rule_is_not_mistaken_for_heading():
    cleaned = chunking.clean_personal_text('B12.\nA student must obtain approval within seven days.')
    assert cleaned.startswith('B12.\nA student must')


def test_cross_page_rule_continuation_keeps_correct_source_page():
    chunks = chunking.chunk_personal_pages([
        (10, 'B13.\nInternal Evaluation\nB13.2. For laboratory practical, End-term exam is not', 'fixture'),
        (11, 'mandatory. If End-term exam is planned, approval is required.', 'fixture')
    ], 'doc', 'Fixture', 'hash', 'fixture')
    assert len(chunks) == 2
    assert [c.page for c in chunks] == [10, 11]
    assert all(c.section == 'B13. Internal Evaluation' for c in chunks)
    assert words(' '.join(c.raw_text for c in chunks)) == 'B13.2. For laboratory practical, End-term exam is not mandatory. If End-term exam is planned, approval is required.'
