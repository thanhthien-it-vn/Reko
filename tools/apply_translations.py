#!/usr/bin/env python3
"""Apply translation dict to JSON entries and validate abbrev constraints."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ASCII_RE = re.compile(r"^[a-zA-Z0-9 .,!?;:'\"()-]+$")


def validate_entry(entry: dict) -> list[str]:
    errs: list[str] = []
    abbrev = entry.get("abbrev", "")
    ascii_max = entry.get("ascii_max", 999)
    if not entry.get("translated"):
        errs.append("missing translated")
    if not abbrev:
        errs.append("missing abbrev")
    elif len(abbrev) > ascii_max:
        errs.append(f"abbrev too long: {len(abbrev)} > {ascii_max}")
    elif not ASCII_RE.match(abbrev):
        errs.append(f"abbrev not ASCII: {abbrev!r}")
    return errs


def apply_dict(path: Path, translations: dict[str, tuple[str, str]]) -> tuple[int, int]:
    """Apply translations keyed by original Chinese text. Returns (applied, errors)."""
    entries = json.loads(path.read_text(encoding="utf-8"))
    applied = 0
    errors = 0
    for entry in entries:
        orig = entry.get("original", "")
        if orig in translations:
            translated, abbrev = translations[orig]
            entry["translated"] = translated
            entry["abbrev"] = abbrev
            entry["status"] = "done"
            applied += 1
        errs = validate_entry(entry)
        if errs and entry.get("status") == "done":
            errors += 1
            print(f"  WARN {entry['id']}: {errs}")
    path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return applied, errors


def count_status(path: Path) -> dict[str, int]:
    entries = json.loads(path.read_text(encoding="utf-8"))
    done = sum(1 for e in entries if e.get("status") == "done")
    return {"total": len(entries), "done": done, "pending": len(entries) - done}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: apply_translations.py <json_file>")
        sys.exit(1)
    p = Path(sys.argv[1])
    print(count_status(p))
