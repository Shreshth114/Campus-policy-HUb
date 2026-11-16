#!/usr/bin/env python3
"""Explicit source review CLI; approval is bound to the registered file's content."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.authority import get_registry, approve_source, reject_source
from src.store import sync_authority_metadata
from src.cache import invalidate_by_doc_id
from src.institutions import resolve, scope


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--institution-id',required=True)
    parser.add_argument('action',choices=['list','approve','reject'])
    parser.add_argument('doc_id',nargs='?')
    args=parser.parse_args()
    with scope(resolve(args.institution_id)):
        return execute(args,parser)

def execute(args,parser):
    if args.action=='list':
        print(json.dumps(get_registry(),indent=2))
        return
    if not args.doc_id:
        parser.error('doc_id is required for approval/rejection')
    success=(approve_source if args.action=='approve' else reject_source)(args.doc_id)
    if not success:
        parser.exit(1,'Source not eligible: reindex the current file and review it; synthetic sources cannot be approved.\n')
    sync_authority_metadata()
    invalidate_by_doc_id(args.doc_id)
    print(f'{args.doc_id}: {args.action} completed')


if __name__=='__main__':
    main()
