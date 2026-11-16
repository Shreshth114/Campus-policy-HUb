def scoped_metadata(values):
    from src.institutions import current
    from src.authority import get_registry
    registry=get_registry()
    return [{**m,'institution_id':current().institution_id,'version_id':m.get('file_hash',registry.get(m.get('doc_id'),{}).get('file_hash',''))} for m in values]

def mark_indexed(did):
    from src.documents import set_index_status
    set_index_status(did,'indexed',1)
