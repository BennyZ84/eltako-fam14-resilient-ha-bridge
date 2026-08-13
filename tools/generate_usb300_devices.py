#!/usr/bin/env python3
"""Generate outbound-only enocean-mqtt device sections from a CSV map.

CSV columns:
    kind,name,sender_suffix,cover_prefix

kind is 'switch' or 'cover'. sender_suffix is one hex byte (80..FF).
For covers, cover_prefix is two colon-separated hex bytes, stored as a comment
because raw_data should be set dynamically at send time.
"""
from __future__ import annotations
import argparse
import csv
import re
import sys
from pathlib import Path

HEX_BYTE = re.compile(r"^[0-9A-Fa-f]{2}$")
PREFIX = re.compile(r"^[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}$")
NAME = re.compile(r"^[a-z0-9_]+$")


def parse_base(value: str) -> str:
    cleaned = value.replace(":", "").replace("-", "").upper()
    if not re.fullmatch(r"[0-9A-F]{8}", cleaned):
        raise ValueError("base must be four hex bytes, e.g. FF:AA:BB:80")
    if not cleaned.endswith("80"):
        raise ValueError("this generator expects a TCM310-style ...80 base")
    return cleaned[:6]


def generate(rows, base_prefix: str) -> str:
    out = []
    seen = set()
    for line_no, row in enumerate(rows, start=2):
        kind = (row.get("kind") or "").strip().lower()
        name = (row.get("name") or "").strip().lower()
        suffix = (row.get("sender_suffix") or "").strip().upper()
        prefix = (row.get("cover_prefix") or "").strip().upper()
        if kind not in {"switch", "cover"}:
            raise ValueError(f"line {line_no}: kind must be switch or cover")
        if not NAME.fullmatch(name):
            raise ValueError(f"line {line_no}: invalid name {name!r}")
        if not HEX_BYTE.fullmatch(suffix):
            raise ValueError(f"line {line_no}: invalid sender_suffix {suffix!r}")
        if int(suffix, 16) < 0x80:
            raise ValueError(f"line {line_no}: suffix must be within Base_ID..Base_ID+127")
        sender = base_prefix + suffix
        if sender in seen:
            raise ValueError(f"line {line_no}: duplicate sender {sender}")
        seen.add(sender)
        section = f"usb300_backup_{name}" if kind == "switch" else f"usb300_backup_cover_{name}"
        out += [f"[{section}]", "address = 0xFFFFFFFF", "rorg = 0xA5"]
        if kind == "switch":
            out += ["func = 0x38", "type = 0x08", f"sender = 0x{sender}", "default_data = 0x01000008", "ignore = 1", ""]
        else:
            if not PREFIX.fullmatch(prefix):
                raise ValueError(f"line {line_no}: cover_prefix must be two hex bytes like 00:F5")
            out += ["func = 0x3F", "type = 0x7F", f"sender = 0x{sender}", "ignore = 1", f"# move_prefix = {prefix}", ""]
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("csv_file", type=Path)
    p.add_argument("--base", default="FF:AA:BB:80", help="USB300 Base ID; default is documentation-only")
    args = p.parse_args()
    base_prefix = parse_base(args.base)
    with args.csv_file.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    sys.stdout.write(generate(rows, base_prefix))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
