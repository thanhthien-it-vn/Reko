#!/usr/bin/env python3
"""Apply translation data modules to extracted JSON files."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from translations.item_data import ITEM_TRANSLATIONS
from translations.npc_data import NPC_TRANSLATIONS
from translations.snr0m_data import SNR0M_TRANSLATIONS
from translations.snr1m_data import SNR1M_TRANSLATIONS
from translations.snr2m_data import SNR2M_TRANSLATIONS
from translations.snr3m_data import SNR3M_TRANSLATIONS
from translations.snr4m_data import SNR4M_TRANSLATIONS

ASCII_RE = re.compile(r"^[a-zA-Z0-9 .,!?;:'\"()-]+$")


def is_valid_abbrev(abbrev: str) -> bool:
    """ASCII text, optionally prefixed by 1-2 game control bytes."""
    body = abbrev
    if len(abbrev) >= 2 and ord(abbrev[1]) < 32:
        body = abbrev[2:]
    elif len(abbrev) >= 1 and ord(abbrev[0]) < 32:
        body = abbrev[1:]
    return bool(body) and bool(ASCII_RE.match(body))

DATA_MAP = {
    "item.json": ITEM_TRANSLATIONS,
    "npc.json": NPC_TRANSLATIONS,
    "script_snr0m.json": SNR0M_TRANSLATIONS,
    "script_snr1m.json": SNR1M_TRANSLATIONS,
    "script_snr2m.json": SNR2M_TRANSLATIONS,
    "script_snr3m.json": SNR3M_TRANSLATIONS,
    "script_snr4m.json": SNR4M_TRANSLATIONS,
}


def fit_abbrev(translated: str, ascii_max: int) -> str:
    """Generate abbrev from translated text within ascii_max."""
    if len(translated) <= ascii_max:
        return translated
    # Try initials: "Dao Thanh Long" -> "D.T.Long" or "T.Long"
    words = translated.split()
    if len(words) >= 2:
        init = ".".join(w[0].upper() for w in words if w)
        if len(init) <= ascii_max:
            return init
        # First word abbreviated + rest
        short = words[0][:3] + "." + words[-1][:3] if len(words) > 1 else words[0][:ascii_max]
        if len(short) <= ascii_max:
            return short
    return translated[:ascii_max]


def apply_file(path: Path, translations: dict[str, tuple[str, str]]) -> dict:
    entries = json.loads(path.read_text(encoding="utf-8"))
    applied = 0
    missing = []
    errors = []
    for entry in entries:
        orig = entry.get("original", "")
        if orig in translations:
            translated, abbrev = translations[orig]
            entry["translated"] = translated
            entry["abbrev"] = abbrev
            if len(abbrev) > entry.get("ascii_max", 999):
                entry["abbrev"] = fit_abbrev(translated, entry["ascii_max"])
            entry["status"] = "done"
            applied += 1
        elif entry.get("status") != "done":
            missing.append(orig[:40])
        abbrev = entry.get("abbrev", "")
        if entry.get("status") == "done":
            if len(abbrev) > entry.get("ascii_max", 999):
                errors.append(f"{entry['id']}: abbrev {len(abbrev)} > {entry['ascii_max']}")
            if abbrev and not is_valid_abbrev(abbrev):
                errors.append(f"{entry['id']}: non-ASCII abbrev {abbrev!r}")
    path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"applied": applied, "total": len(entries), "missing": len(missing), "errors": errors}


def main() -> None:
    base = Path("translations/extracted")
    target = sys.argv[1] if len(sys.argv) > 1 else None
    files = [target] if target else list(DATA_MAP.keys())
    for fname in files:
        path = base / fname if not Path(fname).exists() else Path(fname)
        data = DATA_MAP.get(path.name, {})
        if not data:
            print(f"SKIP {path.name}: no data module")
            continue
        result = apply_file(path, data)
        print(f"{path.name}: {result['applied']}/{result['total']} done, missing={result['missing']}")
        for e in result["errors"]:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    main()
