"""Small local-process locks and atomic JSON persistence."""
import json
import os
import tempfile
from pathlib import Path
from threading import RLock

INDEX_LOCK = RLock()
CACHE_LOCK = RLock()
AUTHORITY_LOCK = RLock()


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)
