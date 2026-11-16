# Verification output

Final full Python command: `python -m pytest tests/ -q`.

```text
........................................................................ [ 15%]
........................................................................ [ 30%]
........................................................................ [ 45%]
........................................................................ [ 60%]
........................................................................ [ 75%]
........................................................................ [ 90%]
............................................                             [100%]
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
476 passed, 6 warnings in 11.96s
<sys>:0: DeprecationWarning: builtin type swigvarlink has no __module__ attribute
```

All four frontend suites passed: personal, sidebar, dashboard (19 DOM checks), and what-if. These use mocked requests and are not live visual QA.
