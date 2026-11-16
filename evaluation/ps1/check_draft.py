"""Offline integrity check only. No models, embeddings, Chroma, approvals or scores."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check(root=ROOT):
    manifest = json.loads((root/'manifest.json').read_text())
    path = root/'questions.draft.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest['question_set_sha256'], 'Draft changed: update its manifest before freezing a run'
    rows = json.loads(path.read_text())
    assert len(rows) == 30 and len({r['id'] for r in rows}) == 30
    assert {t: sum(r['type']==t for r in rows) for t in {r['type'] for r in rows}} == {
        'direct':10, 'informal':10, 'multi_condition':5, 'out_of_scope':5}
    assert not manifest['labels_verified']
    for r in rows:
        assert r['labels_verified'] is False and r['review_status']=='pending'
        assert r['proposed_split'] in {'development','holdout'}
        if r['expect']=='answer':
            assert r['source_quote'] and r['source_pages'] and r['proposed_gold_chunk_ids']
        else:
            assert not r['proposed_gold_chunk_ids']
    return {'status':'awaiting_human_review', 'questions':len(rows),
            'development':sum(r['proposed_split']=='development' for r in rows),
            'holdout':sum(r['proposed_split']=='holdout' for r in rows),
            'fragment_mappings_to_review':[r['id'] for r in rows if r.get('mapping_status')=='fragment_matches_review_required'],
            'verified_labels':0, 'accuracy_measured':False}


if __name__=='__main__':
    print(json.dumps(check(),indent=2))
