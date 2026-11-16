"""
test_cache.py — Tests for semantic cache.

Tests:
1. Exact match hit
2. Miss on different question
3. Invalidation by doc_id
4. Normalized matching (case, punctuation, whitespace)
5. Clear cache
"""

import pytest
from src.cache import (
    cache_lookup,
    cache_store,
    invalidate_by_doc_id,
    clear_cache,
    _normalize_question,
    _cache,
    _loaded,
)


@pytest.fixture(autouse=True)
def clean_cache(tmp_path, monkeypatch):
    """Clear cache before and after each test."""
    import src.cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_PATH", tmp_path / "cache.json")
    # These unit tests exercise cache mechanics; provenance is tested separately.
    monkeypatch.setattr("src.store.valid_cached_citations", lambda ids: True)
    monkeypatch.setattr("src.store.citation_fingerprint", lambda ids: ["fixture-version"])
    cache_mod._cache.clear()
    cache_mod._loaded = True  # skip file loading
    yield
    cache_mod._cache.clear()


class TestCacheNormalization:

    def test_lowercase(self):
        assert _normalize_question("Can I Skip Lab?") == "can i skip lab"

    def test_punctuation_removal(self):
        assert _normalize_question("can i skip lab???") == "can i skip lab"

    def test_whitespace_collapse(self):
        assert _normalize_question("  can   i  skip  lab  ") == "can i skip lab"

    def test_equivalent_questions_match(self):
        q1 = "Can I skip lab?"
        q2 = "can i skip lab"
        assert _normalize_question(q1) == _normalize_question(q2)


class TestCacheLookup:

    def test_exact_match_hit(self):
        cache_store("Can I skip lab?", "You need 75% attendance.", ["c1"], ["attendance"])
        result = cache_lookup("Can I skip lab?")
        assert result is not None
        assert result["answer"] == "You need 75% attendance."
        assert result["similarity"] == 1.0

    def test_normalized_match_hit(self):
        cache_store("Can I skip lab?", "Answer here.", ["c1"], ["attendance"])
        result = cache_lookup("can i skip lab")
        assert result is not None

    def test_miss_different_question(self):
        cache_store("Can I skip lab?", "Answer here.", ["c1"], ["attendance"])
        result = cache_lookup("What is the exam schedule?")
        assert result is None

    def test_miss_on_empty_cache(self):
        result = cache_lookup("anything")
        assert result is None


class TestCacheInvalidation:

    def test_invalidate_removes_matching_entries(self):
        cache_store("q1", "a1", ["c1"], ["attendance_policy"])
        cache_store("q2", "a2", ["c2"], ["exam_policy"])
        cache_store("q3", "a3", ["c3"], ["attendance_policy"])

        removed = invalidate_by_doc_id("attendance_policy")
        assert removed == 2

        assert cache_lookup("q1") is None
        assert cache_lookup("q3") is None
        assert cache_lookup("q2") is not None

    def test_invalidate_no_match(self):
        cache_store("q1", "a1", ["c1"], ["attendance"])
        removed = invalidate_by_doc_id("nonexistent_doc")
        assert removed == 0
        assert cache_lookup("q1") is not None


class TestCacheClear:

    def test_clear_all(self):
        cache_store("q1", "a1", ["c1"], ["d1"])
        cache_store("q2", "a2", ["c2"], ["d2"])
        count = clear_cache()
        assert count == 2
        assert cache_lookup("q1") is None
        assert cache_lookup("q2") is None

