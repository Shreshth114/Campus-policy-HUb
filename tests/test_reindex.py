"""
test_reindex.py — Tests for incremental re-indexing.

Tests:
1. No changes → 0 chunks re-embedded
2. Single file update → only that file re-indexed
3. File deletion → chunks removed
4. Manifest consistency
"""

import json
import pytest
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.reindex import reindex, _load_manifest, _save_manifest


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory structure."""
    from src.institutions import workspace_path
    raw_dir=workspace_path('raw');decoys_dir=workspace_path('decoys');processed_dir=workspace_path('processed')
    manifest_path=workspace_path('manifest')
    return tmp_path, raw_dir, decoys_dir, manifest_path


class TestManifest:

    def test_load_empty_manifest(self, tmp_path):
        """Non-existent manifest returns empty dict."""
        with patch("src.reindex.MANIFEST_PATH", tmp_path / "nope.json"):
            m = _load_manifest()
        assert m == {}

    def test_save_and_load_manifest(self, tmp_path):
        manifest_path = tmp_path / "manifest.json"
        with patch("src.reindex.MANIFEST_PATH", manifest_path), \
             patch("src.reindex.DATA_PROCESSED_DIR", tmp_path):
            _save_manifest({"file1.pdf": "abc123"})
            m = _load_manifest()
        assert m == {"file1.pdf": "abc123"}


class TestReindexLogic:
    """Test the diff logic of reindex (without actual PDF parsing)."""

    def test_no_changes_zero_reembeds(self, temp_data_dir):
        """When nothing changed, nothing should be re-embedded."""
        tmp_path, raw_dir, decoys_dir, manifest_path = temp_data_dir

        # Create a dummy file and pre-populate manifest
        dummy = raw_dir / "test.pdf"
        dummy.write_bytes(b"%PDF-1.4 test content for hashing")

        import hashlib
        file_hash = hashlib.sha256(dummy.read_bytes()).hexdigest()
        manifest = {str(dummy): file_hash}
        manifest_path.write_text(json.dumps(manifest))

        with patch("src.reindex.DATA_RAW_DIR", raw_dir), \
             patch("src.reindex.DATA_DECOYS_DIR", decoys_dir), \
             patch("src.reindex.MANIFEST_PATH", manifest_path), \
             patch("src.reindex.DATA_PROCESSED_DIR", manifest_path.parent), \
             patch("src.reindex.ingest_file") as mock_ingest, \
             patch("src.reindex.embed_texts") as mock_embed, \
             patch("src.reindex.upsert_chunks") as mock_upsert, \
             patch("src.reindex.delete_by_doc_id") as mock_delete, \
             patch("src.reindex.invalidate_by_doc_id", return_value=0), \
             patch("src.reindex.get_collection_count", return_value=10):

            report = reindex()

        # Nothing should have been ingested or deleted
        mock_ingest.assert_not_called()
        mock_embed.assert_not_called()
        mock_upsert.assert_not_called()
        mock_delete.assert_not_called()
        assert report["chunks_added"] == 0
        assert report["chunks_deleted"] == 0

    def test_new_file_triggers_ingest(self, temp_data_dir):
        """A new file should trigger ingestion."""
        tmp_path, raw_dir, decoys_dir, manifest_path = temp_data_dir

        # Empty manifest, one new file
        manifest_path.write_text("{}")
        dummy = raw_dir / "new_policy.pdf"
        dummy.write_bytes(b"%PDF-1.4 new content")

        from src.chunking import Chunk
        fake_chunk = Chunk(
            chunk_id="abc", text="test", raw_text="test",
            doc_id="new_policy", doc_title="New Policy",
            section="1", page=1, chunk_index=0,
            file_hash="xxx", source_path=str(dummy), is_decoy=False,
        )

        with patch("src.reindex.DATA_RAW_DIR", raw_dir), \
             patch("src.reindex.DATA_DECOYS_DIR", decoys_dir), \
             patch("src.reindex.MANIFEST_PATH", manifest_path), \
             patch("src.reindex.DATA_PROCESSED_DIR", manifest_path.parent), \
             patch("src.reindex.ingest_file", return_value=[fake_chunk]) as mock_ingest, \
             patch("src.reindex.embed_texts", return_value=[[0.1]*384]) as mock_embed, \
             patch("src.reindex.upsert_chunks") as mock_upsert, \
             patch("src.reindex.delete_by_doc_id", return_value=0), \
             patch("src.reindex.invalidate_by_doc_id", return_value=0), \
             patch("src.reindex.get_collection_count", return_value=1):

            report = reindex()

        mock_ingest.assert_called_once()
        mock_embed.assert_called_once()
        mock_upsert.assert_called_once()
        assert report["chunks_added"] == 1

