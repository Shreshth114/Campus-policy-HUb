# Grounding verification output

Commands run in the project root. No live provider calls are made by these test suites.

## Initial reproduction (before implementation)

```text
FF...FFF                                                                 [100%]
=================================== FAILURES ===================================
______ test_complete_provision_and_second_rule_fit_existing_total_budget _______

    def test_complete_provision_and_second_rule_fit_existing_total_budget():
        c=make_chunk(text=PROVISION+'\nB12.1. A late request requires a processing fee of 43 credits.')
        sent=answer.answer_evidence(QUESTION+' What fee applies to a late request?', [c])
        assert PROVISION in sent[0].text
>       assert '43 credits' in sent[0].text
E       AssertionError: assert '43 credits' in 'B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for con...ven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.'
E        +  where 'B11.4. Those who have 80% or more attendance for the period other than their medical leave will be considered for con...ven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier.' = RetrievedChunk(chunk_id='c1', text='B11.4. Those who have 80% or more attendance for the period other than their medic...y=False, approved=True, rrf_score=None, is_synthetic=False, extraction_method='unknown', source_chunk_ids=[], pages=[]).text

tests/test_structured_grounding.py:24: AssertionError
_ test_other_institution_complete_rules_not_just_threshold[R7. Students may borrow three books. Approval by the librarian is required within five days.-True] _

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x120e550f0>
quote = 'R7. Students may borrow three books. Approval by the librarian is required within five days.'
ok = True

    @pytest.mark.asyncio
    @pytest.mark.parametrize('quote,ok',[
        ('R7. Students may borrow three books. Approval by the librarian is required within five days.',True),
        ('Students may borrow three books.',False),
        ('Students may borrow four books.',False),
        ('Students may borrow three',False),
    ])
    async def test_other_institution_complete_rules_not_just_threshold(monkeypatch,quote,ok):
        c=make_chunk(text='R7. Students may borrow three books. Approval by the librarian is required within five days.')
        monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
        chat=AsyncMock(side_effect=[SimpleNamespace(text=payload(quote)),SimpleNamespace(text=review())])
        monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=chat))
        result,reason,_,_=await answer.generate_answer('How many books can I borrow and what approval is needed?', [c])
>       assert (reason is None)==ok
E       AssertionError: assert ('citation_check_failed' is None) == True

tests/test_structured_grounding.py:41: AssertionError
_________ test_question_coverage_rejection_no_automatic_source_append __________

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x120e52350>

    @pytest.mark.asyncio
    async def test_question_coverage_rejection_no_automatic_source_append(monkeypatch):
        c=make_chunk(text='A1. General registration is required every semester.')
        monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
        chat=AsyncMock(side_effect=[SimpleNamespace(text=payload(c.text)),SimpleNamespace(text=review(False))])
        monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=chat))
        result,reason,_,response=await answer.generate_answer('How do I return after a temporary withdrawal?', [c])
>       assert reason=='question_coverage_failed' and result==answer.ABSTAIN_MESSAGE
E       AssertionError: assert ('citation_check_failed' == 'question_coverage_failed'
E         
E         - question_coverage_failed
E         + citation_check_failed)

tests/test_structured_grounding.py:53: AssertionError
________ test_review_proof_bound_to_question_answer_evidence_and_scope _________

    def test_review_proof_bound_to_question_answer_evidence_and_scope():
>       from src.grounding import make_proof, proof_matches
E       ModuleNotFoundError: No module named 'src.grounding'

tests/test_structured_grounding.py:58: ModuleNotFoundError
___ test_same_line_individual_exact_quotes_do_not_form_false_combined_claim ____

    def test_same_line_individual_exact_quotes_do_not_form_false_combined_claim():
        c=make_chunk(text='Calculators are prohibited. The Senate may grant an exception.')
>       assert answer.validate_answer('"Calculators are prohibited." [C1] "The Senate may grant an exception." [C1]',[c])[0] is None
E       AssertionError: assert 'unsupported_cited_claim' is None

tests/test_structured_grounding.py:71: AssertionError
=============================== warnings summary ===============================
../../../../../opt/miniconda3/lib/python3.14/site-packages/chromadb/telemetry/opentelemetry/__init__.py:128
  /opt/miniconda3/lib/python3.14/site-packages/chromadb/telemetry/opentelemetry/__init__.py:128: DeprecationWarning: 'asyncio.iscoroutinefunction' is deprecated and slated for removal in Python 3.16; use inspect.iscoroutinefunction() instead
    if asyncio.iscoroutinefunction(f):

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type SwigPyPacked has no __module__ attribute

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type SwigPyObject has no __module__ attribute

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type swigvarlink has no __module__ attribute

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
FAILED tests/test_structured_grounding.py::test_other_institution_complete_rules_not_just_threshold[R7. Students may borrow three books. Approval by the librarian is required within five days.-True]
FAILED tests/test_structured_grounding.py::test_question_coverage_rejection_no_automatic_source_append
FAILED tests/test_structured_grounding.py::test_review_proof_bound_to_question_answer_evidence_and_scope
FAILED tests/test_structured_grounding.py::test_same_line_individual_exact_quotes_do_not_form_false_combined_claim
5 failed, 3 passed, 6 warnings in 1.99s
```

## Second reproduction (before block/parenthetical fixes)

```text
..........................FF                                             [100%]
=================================== FAILURES ===================================
___ test_semantically_related_provision_not_dropped_for_zero_keyword_overlap ___

    def test_semantically_related_provision_not_dropped_for_zero_keyword_overlap():
        c=make_chunk(text='R1. A temporary withdrawal is permitted for one semester.\nR2. On resumption, the adviser determines the creditable courses with the departmental head.')
        sent=answer.answer_evidence('How do I return after a temporary withdrawal?', [c])
>       assert 'R2.' in sent[0].text
E       AssertionError: assert 'R2.' in 'R1. A temporary withdrawal is permitted for one semester.'
E        +  where 'R1. A temporary withdrawal is permitted for one semester.' = RetrievedChunk(chunk_id='c1', text='R1. A temporary withdrawal is permitted for one semester.', doc_id='attendance_pol...y=False, approved=True, rrf_score=None, is_synthetic=False, extraction_method='unknown', source_chunk_ids=[], pages=[]).text

tests/test_structured_grounding.py:140: AssertionError
_________ test_complete_rule_with_trailing_parenthetical_is_preserved __________

    def test_complete_rule_with_trailing_parenthetical_is_preserved():
        from src.grounding import provisions
        text='F4. The fee is 43 credits. The council may revise it. (Amended at the fifth meeting)'
>       assert provisions(text)==[text]
E       AssertionError: assert [] == ['F4. The fee...fth meeting)']
E         
E         Right contains one more item: 'F4. The fee is 43 credits. The council may revise it. (Amended at the fifth meeting)'
E         Use -v to get more diff

tests/test_structured_grounding.py:146: AssertionError
=============================== warnings summary ===============================
../../../../../opt/miniconda3/lib/python3.14/site-packages/chromadb/telemetry/opentelemetry/__init__.py:128
  /opt/miniconda3/lib/python3.14/site-packages/chromadb/telemetry/opentelemetry/__init__.py:128: DeprecationWarning: 'asyncio.iscoroutinefunction' is deprecated and slated for removal in Python 3.16; use inspect.iscoroutinefunction() instead
    if asyncio.iscoroutinefunction(f):

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type SwigPyPacked has no __module__ attribute

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type SwigPyObject has no __module__ attribute

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type swigvarlink has no __module__ attribute

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_structured_grounding.py::test_semantically_related_provision_not_dropped_for_zero_keyword_overlap
FAILED tests/test_structured_grounding.py::test_complete_rule_with_trailing_parenthetical_is_preserved
2 failed, 26 passed, 6 warnings in 4.09s
```

## Final targeted grounding tests

```text
...................................................................      [100%]
=============================== warnings summary ===============================
../../../../../opt/miniconda3/lib/python3.14/site-packages/chromadb/telemetry/opentelemetry/__init__.py:128
  /opt/miniconda3/lib/python3.14/site-packages/chromadb/telemetry/opentelemetry/__init__.py:128: DeprecationWarning: 'asyncio.iscoroutinefunction' is deprecated and slated for removal in Python 3.16; use inspect.iscoroutinefunction() instead
    if asyncio.iscoroutinefunction(f):

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type SwigPyPacked has no __module__ attribute

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type SwigPyObject has no __module__ attribute

tests/test_structured_grounding.py::test_complete_provision_and_second_rule_fit_existing_total_budget
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type swigvarlink has no __module__ attribute

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
67 passed, 6 warnings in 3.60s
```

## Final full Python suite

```text
........................................................................ [ 15%]
........................................................................ [ 31%]
........................................................................ [ 47%]
........................................................................ [ 63%]
........................................................................ [ 79%]
........................................................................ [ 95%]
...................                                                      [100%]
=============================== warnings summary ===============================
../../../../../opt/miniconda3/lib/python3.14/site-packages/chromadb/telemetry/opentelemetry/__init__.py:128
  /opt/miniconda3/lib/python3.14/site-packages/chromadb/telemetry/opentelemetry/__init__.py:128: DeprecationWarning: 'asyncio.iscoroutinefunction' is deprecated and slated for removal in Python 3.16; use inspect.iscoroutinefunction() instead
    if asyncio.iscoroutinefunction(f):

<frozen importlib._bootstrap>:491
<frozen importlib._bootstrap>:491
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type SwigPyPacked has no __module__ attribute

<frozen importlib._bootstrap>:491
<frozen importlib._bootstrap>:491
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type SwigPyObject has no __module__ attribute

<frozen importlib._bootstrap>:491
  <frozen importlib._bootstrap>:491: DeprecationWarning: builtin type swigvarlink has no __module__ attribute

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
451 passed, 6 warnings in 12.74s
<sys>:0: DeprecationWarning: builtin type swigvarlink has no __module__ attribute
```

Four frontend suites passed: personal, sidebar, dashboard (19 DOM checks) and what-if. Exact commands and scope appear in the implementation report.
