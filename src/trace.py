"""
trace.py — Trace dataclass for full pipeline observability.

Every pipeline run produces a Trace that the UI and benchmark consume.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ChunkTrace:
    """Lightweight chunk info for the trace (not full text)."""
    chunk_id: str
    doc_title: str
    section: str
    page: int
    score: float
    text_preview: str
    workspace_id: str = ""
    institution_id: str = ""
    doc_id: str = ""
    version_id: str = ""
    is_decoy: bool = False
    rrf_score: Optional[float] = None
    approved: bool = False
    is_synthetic: bool = False
    extraction_method: str = "unknown"
    source_chunk_ids: list[str] = field(default_factory=list)
    pages: list[int] = field(default_factory=list)
    text: str = ""
    matched_sentence: str = ""
    answer_excerpt: Optional[str] = None


@dataclass
class Trace:
    """Full pipeline trace — returned by every /ask call."""
    question: str
    mode: str                                           # raw | hyde | fusion
    workspace_id: str = ""
    institution_id: str = ""
    trust_level: str = "institutional"
    trust_notice: str = ""
    cache_hit: bool = False
    cache_similarity: Optional[float] = None
    hyde_text: Optional[str] = None
    hyde_failed: bool = False
    retrieved: list[ChunkTrace] = field(default_factory=list)
    decision: str = "pending"                           # answered | abstained | provider_unavailable
    abstain_reason: Optional[str] = None                # low_confidence | no_policy_found | citation_check_failed
    answer: Optional[str] = None
    citations: list[str] = field(default_factory=list)  # chunk_ids cited
    timings_ms: dict = field(default_factory=dict)      # {cache, hyde, embed, retrieve, answer, total}
    provider: Optional[str] = None                      # groq | gemini
    error: Optional[str] = None
    llm_usage: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    validation_failures: list[dict] = field(default_factory=list)
    question_requirements: list[dict] = field(default_factory=list)
    evidence_coverage: list[dict] = field(default_factory=list)
    verified_quotes: list[dict] = field(default_factory=list)
    citations_verified: bool = False
    confidence_passed: bool = False
    synthetic_demo: bool = False
    retry_after_s: Optional[float] = None
    tokens_estimated_before: Optional[int] = None
    tokens_estimated_after: Optional[int] = None
    failovers: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

