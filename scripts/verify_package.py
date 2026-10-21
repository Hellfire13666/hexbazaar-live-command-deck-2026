#!/usr/bin/env python3
"""Checks exact packaged HEXBAZAAR Deck bytes without touching any engine."""
import hashlib,json,os,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MANIFEST.json').read_text())
files=manifest['files']
observed={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in str(p)}
if observed != set(files):
 print('[FAIL] Extra or missing release files',sorted(observed-set(files)),sorted(set(files)-observed))
 sys.exit(2)
for name,want in files.items():
 p=root/name
 if p.is_symlink():
  print('[FAIL] Symlink in release:',name);sys.exit(2)
 if hashlib.sha256(p.read_bytes()).hexdigest()!=want:
  print('[FAIL] Hash mismatch:',name);sys.exit(2)
print(f'[PASS] HEXBAZAAR Live Deck verified: {len(files)} authentic packaged files, no mismatches')
