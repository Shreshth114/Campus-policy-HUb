from tests import scoped_metadata, mark_indexed
"""Production isolation and fusion regressions; no models or APIs required."""

import ast
import importlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import chromadb
from chromadb.config import Settings
import pytest

from src import authority, store
from src.answer import ABSTAIN_MESSAGE, confidence_gate
from src.ingest import ingest_file
from src.pipeline import ask
from src.retrieve import RetrievalResult, retrieve
from src.trace import ChunkTrace, Trace
from tests.test_guardrails import make_chunk


@pytest.fixture
def policy_collection(tmp_path, monkeypatch):
    """Use real cosine search, isolated from the project's persistent index."""
    client = chromadb.PersistentClient(
        path=str(tmp_path / "chroma"),
        settings=Settings(anonymized_telemetry=False),
    )
    collection = client.create_collection(
        "guardrail_policies", metadata={"hnsw:space": "cosine"},
    )
    monkeypatch.setattr(store, "_collection", collection)
    # Emulate reviewed sources only in a temporary test registry/index.
    for doc_id in ("approved", "approved_decoy"):
        path = tmp_path / (doc_id + ".txt")
        path.write_text("Isolated synthetic source-authority test fixture; not a university policy.")
        authority.register_source(doc_id, "Isolated fixture", source_path=str(path))
        mark_indexed(doc_id)
        assert authority.approve_source(doc_id)
    digest = authority.get_registry()["approved"]["file_hash"]
    collection.upsert(
        ids=["approved", "pending", "decoy", "approved_decoy", "legacy"],
        documents=["Policy excerpt"] * 5,
        embeddings=[[1.0, 0.0]] * 5,
        metadatas=scoped_metadata([
            {"doc_id": "approved", "file_hash": digest, "approved": True, "is_decoy": False},
            {"doc_id": "pending", "approved": False, "is_decoy": False},
            {"doc_id": "decoy", "approved": False, "is_decoy": True},
            {"doc_id": "approved_decoy", "file_hash": digest, "approved": True, "is_decoy": True},
            {"doc_id": "legacy", "is_decoy": False},
        ]),
    )
    yield collection
    client.delete_collection(collection.name)
    # Explicitly close the PersistentClient to release its file descriptors.
    # Without this, the ~10 FDs per client accumulate across the test suite and
    # trigger "Too many open files" on systems with fd limit <= 256.
    if hasattr(client, 'close'):
        try:
            client.close()
        except Exception:
            pass


class TestProductionSearch:
    def test_only_approved_nondecoys_are_retrievable(self, policy_collection):
        chunks = store.query([1.0, 0.0], top_k=10, production=True)
        assert [c.chunk_id for c in chunks] == ["approved"]
        assert chunks[0].approved is True
        assert chunks[0].is_decoy is False
        assert chunks[0].similarity == pytest.approx(1.0)

    def test_production_is_default(self, policy_collection):
        assert [c.chunk_id for c in store.query([1.0, 0.0])] == ["approved"]

    def test_evaluation_can_retrieve_all_sources(self, policy_collection):
        chunks = store.query([1.0, 0.0], top_k=10, production=False)
        assert {c.chunk_id for c in chunks} == {
            "approved", "pending", "decoy", "approved_decoy", "legacy",
        }

    @pytest.mark.parametrize("doc_id", ["pending", "decoy", "approved_decoy", "legacy"])
    def test_caller_filter_cannot_override_production(self, policy_collection, doc_id):
        assert store.query(
            [1.0, 0.0], where={"doc_id": doc_id}, production=True,
        ) == []

    def test_caller_filter_preserves_approved_source(self, policy_collection):
        chunks = store.query([1.0, 0.0], where={"doc_id": "approved"})
        assert [c.chunk_id for c in chunks] == ["approved"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("mode", ["raw", "hyde", "fusion"])
    @pytest.mark.parametrize("production", [True, False])
    async def test_modes_honor_production_flag(self, policy_collection, mode, production):
        with patch("src.retrieve.embed_single", return_value=[1.0, 0.0]), patch(
            "src.retrieve.generate_hyde", new=AsyncMock(
                return_value=("A hypothetical policy excerpt.", SimpleNamespace(provider="test")),
            ),
        ):
            result = await retrieve("policy?", mode=mode, top_k=10, production=production)
        expected = {"approved"} if production else {
            "approved", "pending", "decoy", "approved_decoy", "legacy",
        }
        assert {c.chunk_id for c in result.chunks} == expected

    @pytest.mark.asyncio
    @pytest.mark.parametrize("production", [True, False])
    async def test_hyde_fallback_preserves_production_flag(self, policy_collection, production):
        with patch("src.retrieve.embed_single", return_value=[1.0, 0.0]), patch(
            "src.retrieve.generate_hyde", new=AsyncMock(side_effect=RuntimeError("offline")),
        ):
            result = await retrieve("policy?", mode="hyde", top_k=10, production=production)
        assert result.hyde_failed
        assert len(result.chunks) == (1 if production else 5)


class TestAuthorityIngestion:
    @pytest.mark.parametrize("status", ["pending", "approved", "rejected"])
    def test_registration_preserves_explicit_status(self, tmp_path, monkeypatch, status):
        monkeypatch.setattr(authority, "REGISTRY_PATH", tmp_path / "registry.json")
        source = tmp_path / "policy.txt"
        source.write_text("Students must maintain sufficient attendance. " * 30)
        entry = authority.register_source("policy", "Policy", source_path=str(source))
        assert entry.authority_status == "pending"
        if status == "approved":
            mark_indexed("policy")
            assert authority.approve_source("policy")
        elif status == "rejected":
            assert authority.reject_source("policy")

        chunks = ingest_file(source)
        assert chunks
        assert authority.get_status("policy") == status
        assert all(c.approved == (status == "approved") for c in chunks)
        assert all(c.to_metadata()["approved"] == (status == "approved") for c in chunks)

        decoys = ingest_file(source, is_decoy=True)
        assert decoys
        assert all(c.is_decoy and not c.approved for c in decoys)


class TestFusionConfidence:
    @pytest.mark.asyncio
    async def test_top_rrf_rank_still_abstains_for_low_cosine(self):
        # The shared chunk ranks first in both lists: maximal two-list RRF.
        raw = [make_chunk("shared", similarity=0.1), make_chunk("raw", similarity=0.2)]
        hyde = [make_chunk("shared", similarity=0.15), make_chunk("hyde", similarity=0.25)]
        for chunk in raw + hyde:
            chunk.approved = True
        with patch("src.retrieve.retrieve_raw", new=AsyncMock(
            return_value=RetrievalResult(chunks=raw),
        )) as raw_search, patch("src.retrieve.retrieve_hyde", new=AsyncMock(
            return_value=RetrievalResult(chunks=hyde),
        )) as hyde_search, patch("src.answer.CONFIDENCE_THRESHOLD", 0.35), patch(
            "src.answer.get_llm_client",
        ) as llm, patch("src.pipeline.cache_store") as cache_store:
            trace = await ask("An unrelated question?", mode="fusion", use_cache=False)

        assert raw_search.await_args.kwargs["production"] is True
        assert hyde_search.await_args.kwargs["production"] is True
        assert trace.retrieved[0].chunk_id == "shared"
        assert trace.retrieved[0].rrf_score == pytest.approx(2 / 61)
        assert trace.retrieved[0].score == pytest.approx(0.15)
        assert trace.retrieved[0].approved is True
        assert trace.decision == "abstained"
        assert trace.abstain_reason.startswith("low_confidence")
        assert trace.answer == ABSTAIN_MESSAGE
        assert trace.citations == []
        llm.assert_not_called()
        cache_store.assert_not_called()

    def test_even_inflated_rrf_score_cannot_pass_gate(self):
        chunk = make_chunk(similarity=0.1)
        chunk.rrf_score = 1.0
        with patch("src.answer.CONFIDENCE_THRESHOLD", 0.35):
            passes, reason = confidence_gate([chunk])
        assert not passes
        assert reason.startswith("low_confidence")

    @pytest.mark.asyncio
    async def test_pipeline_explicitly_requests_production_and_traces_raw_scores(self):
        chunk = make_chunk(similarity=0.9)
        chunk.approved = True
        with patch("src.pipeline.valid_cached_citations", return_value=True), patch("src.pipeline.retrieve", new=AsyncMock(
            return_value=RetrievalResult(chunks=[chunk]),
        )) as search, patch("src.pipeline.generate_answer", new=AsyncMock(
            return_value=("Attendance policy [C1].", None, ["c1"], None),
        )):
            trace = await ask("attendance?", mode="raw", use_cache=False)
        search.assert_awaited_once_with("attendance?", mode="raw", production=True)
        assert trace.decision == "answered"
        assert trace.to_dict()["retrieved"][0]["approved"] is True
        assert trace.retrieved[0].rrf_score is None
        assert trace.retrieved[0].score == pytest.approx(0.9)

    def test_trace_defaults_are_fail_closed_and_serializable(self):
        chunk = ChunkTrace("c1", "Policy", "1", 1, 0.1, "Excerpt")
        data = Trace(question="policy?", mode="raw", retrieved=[chunk]).to_dict()
        assert data["retrieved"][0]["approved"] is False
        assert data["retrieved"][0]["rrf_score"] is None


def test_list_models_uses_modern_gemini_sdk():
    script = Path(__file__).resolve().parents[1] / "scripts" / "list_models.py"
    source = script.read_text()
    imports = [n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.ImportFrom)]
    assert any(n.module == "google" and any(a.name == "genai" for a in n.names) for n in imports)
    assert "google.generativeai" not in source
    module = importlib.import_module("scripts.list_models")
    assert module.genai.Client is not None
    with patch.dict(module.PROVIDERS, {"gemini": {"api_key": "test-key"}}), patch.object(
        module.genai, "Client",
    ) as client:
        client.return_value.models.list.return_value = [
            SimpleNamespace(name="models/example", supported_generation_methods=["generateContent"]),
        ]
        assert module.list_gemini_models() == ["example"]
    client.assert_called_once_with(api_key="test-key")
