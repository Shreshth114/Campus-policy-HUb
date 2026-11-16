"""Opt-in local answer diagnostics; never part of a public API or production data."""
import json
import os
import re
import uuid
from pathlib import Path


def record_answer(messages, originals, excerpts, raw_answer, reason, failures, review=None):
    directory = os.getenv('ANSWER_DIAGNOSTICS_DIR')
    if os.getenv('ANSWER_DIAGNOSTICS_ENABLED', '').lower() != 'true' or not directory:
        return
    from src.config import PROVIDERS
    from src.institutions import current
    secrets = [current().workspace_id, os.getenv('ADMIN_API_TOKEN', '')] + [c.get('api_key', '') for c in PROVIDERS.values()]
    payload = {'coverage_review':review, 'messages':messages, 'excerpts':[
        {'label':f'C{i+1}', 'chunk_id':c.chunk_id, 'source_chunk_ids':c.source_chunk_ids or [c.chunk_id],
         'document_id':c.doc_id, 'page':c.page, 'pages':c.pages or [c.page], 'section':c.section,
         'text':c.text, 'selection':'complete_provision' if c.text != originals[i].text else 'whole_chunk',
         'original_characters':len(originals[i].text), 'sent_characters':len(c.text)}
        for i,c in enumerate(excerpts)],
        'rejected_answer':raw_answer if reason else None, 'result':reason or 'accepted', 'failures':failures}
    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    for secret in secrets:
        if secret:
            serialized = serialized.replace(secret, '[REDACTED]')
    serialized = re.sub(r'(?<![\w-])(?:gsk_[A-Za-z0-9_-]+|sk-[A-Za-z0-9_-]+|AIza[A-Za-z0-9_-]+|[A-Za-z0-9_-]{43})(?![\w-])', '[REDACTED]', serialized)
    serialized = re.sub(r'(?i)(bearer\s+)[A-Za-z0-9._-]+', r'\1[REDACTED]', serialized)
    serialized = re.sub(r'(?i)(?:authorization|api[_ -]?key|password|secret|token)\s*[:=]\s*(?:Bearer\s+)?[^\s"\\,]+', '[REDACTED]', serialized)
    try:
        root = Path(directory).expanduser().resolve()
        from src.config import PROJECT_ROOT
        if any(root.is_relative_to((PROJECT_ROOT / name).resolve())
               for name in ('data', '.chroma', '.chroma-institutions', 'web')):
            return  # Never write diagnostics into production storage or served files.
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        path = root / (uuid.uuid4().hex + '.json')
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            stream.write(serialized)
    except OSError:
        # Diagnostics must never change the answering/abstention outcome.
        pass
