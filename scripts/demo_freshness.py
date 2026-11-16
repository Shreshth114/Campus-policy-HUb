#!/usr/bin/env python3
"""Storage-only freshness smoke test in a temporary, synthetic corpus. Never edits PDFs."""
import importlib
from contextlib import ExitStack
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import time
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))


def measure_freshness():
    from src import store, authority, cache
    from src.ingest import ingest_file
    indexer=importlib.import_module('src.reindex')
    with TemporaryDirectory(prefix='policy-synthetic-') as directory, ExitStack() as stack:
        root=Path(directory)
        from src.institutions import InstitutionContext, scope
        stack.enter_context(scope(InstitutionContext('synthetic-freshness-fixture',root)))
        for name in ('raw','decoys','processed'):
            (root/name).mkdir()
        for module in (indexer,):
            for key,value in {'DATA_RAW_DIR':root/'raw','DATA_DECOYS_DIR':root/'decoys',
                              'DATA_PROCESSED_DIR':root/'processed','MANIFEST_PATH':root/'processed/manifest.json'}.items():
                stack.enter_context(patch.object(module,key,value))
        for module,key,value in [(authority,'REGISTRY_PATH',root/'processed/registry.json'),
                                  (cache,'CACHE_PATH',root/'processed/cache.json'),
                                  (cache,'_cache',[]),(cache,'_loaded',False),
                                  (store,'CHROMA_DIR',str(root/'chroma')),
                                  (store,'_client',None),(store,'_collection',None)]:
            stack.enter_context(patch.object(module,key,value))
        stack.enter_context(patch.object(indexer,'ingest_file',lambda p,is_decoy=False:ingest_file(p,is_decoy,is_synthetic=True)))
        stack.enter_context(patch.object(indexer,'embed_texts',lambda texts:[
            [0.,1.] if 'fresh-marker-v2' in text else [1.,0.] for text in texts]))
        target=root/'raw/synthetic_marker.txt'
        target.write_text('SYNTHETIC STORAGE FIXTURE. old-marker-v1. '*20)
        indexer.reindex()
        started=time.perf_counter()
        target.write_text('SYNTHETIC STORAGE FIXTURE. fresh-marker-v2. '*20)
        report=indexer.reindex()
        found=store.query([0.,1.],production=False)
        verified=bool(found) and any('fresh-marker-v2' in c.text for c in found)
        if not verified or report['errors'] or store.query([0.,1.],production=True):
            raise RuntimeError('Synthetic freshness/isolation verification failed')
        result={'scope':'synthetic_storage_only','deterministic_fixture_embeddings':True,
                'freshness_ms':round((time.perf_counter()-started)*1000,3),
                'marker_verified':verified,'production_leakage':False}
        print(result)
        return result


if __name__=='__main__':
    measure_freshness()
