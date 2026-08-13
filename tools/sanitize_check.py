#!/usr/bin/env python3
"""Small pre-publication scanner for obvious secrets/site-specific leftovers."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git'}
PATTERNS = {
    'password assignment': re.compile(r'(?i)\b(password|passwd|pwd)\s*[:=]\s*["\']?(?!<|example|changeme)[^\s"\']{6,}'),
    'private key': re.compile(r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----'),
    'github token': re.compile(r'\bgh[pousr]_[A-Za-z0-9_]{20,}\b'),
    'mqtt uri with credentials': re.compile(r'(?i)mqtts?://[^\s/:]+:[^\s/@]+@'),
}

bad = []
for path in ROOT.rglob('*'):
    if not path.is_file() or any(part in SKIP for part in path.parts):
        continue
    if path.suffix.lower() in {'.zip', '.png', '.jpg', '.jpeg', '.gif', '.pdf'}:
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    for name, pattern in PATTERNS.items():
        if pattern.search(text):
            bad.append((str(path.relative_to(ROOT)), name))
if bad:
    for path, name in bad:
        print(f'FAIL {path}: {name}')
    raise SystemExit(1)
print('sanitize_check: OK')
