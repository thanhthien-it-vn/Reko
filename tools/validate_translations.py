#!/usr/bin/env python3
"""Validate all extracted JSON translations meet project rules."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ASCII_RE = re.compile(r"^[a-zA-Z0-9 .,!?;:'\"()-]+$")


def is_valid_abbrev(abbrev: str) -> bool:
    body = abbrev
    if len(abbrev) >= 2 and ord(abbrev[1]) < 32:
        body = abbrev[2:]
    elif len(abbrev) >= 1 and ord(abbrev[0]) < 32:
        body = abbrev[1:]
    return bool(body) and bool(ASCII_RE.match(body))


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    entries = json.loads(path.read_text(encoding="utf-8"))
    for e in entries:
        eid = e.get("id", "?")
        if e.get("status") != "done":
            errors.append(f"{eid}: status={e.get('status')}")
            continue
        if not e.get("translated"):
            errors.append(f"{eid}: missing translated")
        abbrev = e.get("abbrev", "")
        if not abbrev:
            errors.append(f"{eid}: missing abbrev")
        elif len(abbrev) > e.get("ascii_max", 999):
            errors.append(f"{eid}: abbrev {len(abbrev)} > {e['ascii_max']}")
        elif not is_valid_abbrev(abbrev):
            errors.append(f"{eid}: non-ASCII abbrev")
    return errors


def main() -> None:
    base = Path("translations/extracted")
    total_done = 0
    total_all = 0
    all_errors: list[str] = []
    for path in sorted(base.glob("*.json")):
        entries = json.loads(path.read_text(encoding="utf-8"))
        done = sum(1 for e in entries if e.get("status") == "done")
        total_done += done
        total_all += len(entries)
        errs = validate_file(path)
        status = "OK" if not errs else f"{len(errs)} errors"
        print(f"{path.name}: {done}/{len(entries)} done - {status}")
        all_errors.extend(f"{path.name}: {e}" for e in errs[:5])
        if len(errs) > 5:
            all_errors.append(f"{path.name}: ... and {len(errs)-5} more")
    print(f"\nTOTAL: {total_done}/{total_all}")
    if all_errors:
        print("\nErrors:")
        for e in all_errors:
            print(f"  {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
