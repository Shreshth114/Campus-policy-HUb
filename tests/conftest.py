"""Every test uses temporary storage; never write production data or download models."""
import importlib
import pytest


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    paths = {
        "DATA_RAW_DIR": tmp_path / "raw",
        "DATA_DECOYS_DIR": tmp_path / "decoys",
        "DATA_PROCESSED_DIR": tmp_path / "processed",
        "MANIFEST_PATH": tmp_path / "processed" / "manifest.json",
        "CACHE_PATH": tmp_path / "processed" / "cache.json",
        "REGISTRY_PATH": tmp_path / "processed" / "source_registry.json",
        "HYDE_CACHE_PATH": tmp_path / "processed" / "hyde_cache.json",
    }
    for name in ("DATA_RAW_DIR", "DATA_DECOYS_DIR", "DATA_PROCESSED_DIR"):
        paths[name].mkdir(parents=True)
    for name in ("config", "ingest", "reindex", "cache", "authority", "hyde"):
        module = importlib.import_module("src." + name)
        for key, value in paths.items():
            if hasattr(module, key):
                monkeypatch.setattr(module, key, value)
    from src import store, cache
    monkeypatch.setattr(store, "CHROMA_DIR", str(tmp_path / "chroma"))
    monkeypatch.setattr(store, "_client", None)
    monkeypatch.setattr(store, "_collection", None)
    monkeypatch.setattr(cache, "_cache", [])
    monkeypatch.setattr(cache, "_loaded", False)
    monkeypatch.setattr(cache, "CACHE_SEMANTIC_ENABLED", False)

    from src import institutions
    monkeypatch.setattr(institutions,'DATA_ROOT',tmp_path/'institution-data')
    entry=institutions.create_institution('Synthetic test institution','fixture')
    institutions.update_institution(entry['institution_id'],published=True)
    ctx=institutions.resolve(entry['institution_id'])
    paths.update(DATA_RAW_DIR=ctx.raw,DATA_DECOYS_DIR=ctx.path('decoys'),DATA_PROCESSED_DIR=ctx.processed,
                 MANIFEST_PATH=ctx.path('manifest'),CACHE_PATH=ctx.path('cache'),REGISTRY_PATH=ctx.path('registry'),HYDE_CACHE_PATH=ctx.path('hyde'))
    for name in ('config','ingest','reindex','cache','authority','hyde'):
        module=importlib.import_module('src.'+name)
        for key,value in paths.items():
            if hasattr(module,key):monkeypatch.setattr(module,key,value)
    monkeypatch.setenv('ADMIN_API_TOKEN','isolated-test-admin')
    with institutions.scope(ctx):
        yield ctx

    # Close any ChromaDB PersistentClient created during this test.
    # monkeypatch.setattr(store, "_client", None) set the global to None at fixture
    # setup, but any _get_client() call during the test overwrites it with a new
    # client pointing at tmp_path.  Without an explicit close() those clients leak
    # ~10 file descriptors each; at 313 tests that is ~3,200 FDs, which exhausts
    # the macOS default limit of 256 and causes "OSError: Too many open files".
    # We close the client here, before monkeypatch.undo() restores the global,
    # so the reference is still accessible.
    test_client = store._client
    if test_client is not None and hasattr(test_client, 'close'):
        try:
            test_client.close()
        except Exception:
            pass

