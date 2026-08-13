#!/usr/bin/env python3
"""Build snr2m_data.py from translation batches."""
from __future__ import annotations

import json
import re
from pathlib import Path

BATCH_DIR = Path(__file__).parent / "translations" / "snr2m_batches"
OUTPUT = Path(__file__).parent / "translations" / "snr2m_data.py"
JSON_FILE = Path("translations/extracted/script_snr2m.json")

PREFIX_CHARS = set("{}|~nlbu")


def get_prefix(orig: str) -> str:
    if len(orig) >= 2 and orig[1] == "\x01" and orig[0] in PREFIX_CHARS:
        return orig[:2]
    return ""


def make_abbrev(translated: str, ascii_max: int, orig: str) -> str:
    prefix = get_prefix(orig)
    budget = ascii_max - len(prefix) if prefix else ascii_max
    # Game abbrev is single-line ASCII
    text = translated.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    text = text.strip()
    if len(text) <= budget:
        return text
    t = text[:budget]
    if " " in t:
        t = t.rsplit(" ", 1)[0]
    return t


def load_batches() -> dict[str, str]:
    merged: dict[str, str] = {}
    all_path = BATCH_DIR / "batch_all.json"
    if all_path.exists():
        return json.loads(all_path.read_text(encoding="utf-8"))
    for path in sorted(BATCH_DIR.glob("batch_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        merged.update(data)
    return merged


def emit_py(translations: dict[str, str]) -> None:
    entries = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    lines = [
        '"""Vietnamese translations for script_snr2m.json - keyed by original Chinese."""',
        "",
        "SNR2M_TRANSLATIONS: dict[str, tuple[str, str]] = {",
    ]
    for entry in entries:
        orig = entry["original"]
        if orig not in translations:
            raise KeyError(f"Missing translation for {entry['id']}: {orig[:40]!r}")
        tr = translations[orig]
        ab = make_abbrev(tr, entry["ascii_max"], orig)
        lines.append(f"    {orig!r}: ({tr!r}, {ab!r}),")
    lines.append("}")
    lines.append("")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(entries)} entries")


def main() -> None:
    translations = load_batches()
    entries = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    missing = [e["original"] for e in entries if e["original"] not in translations]
    print(f"Loaded {len(translations)} translations, missing {len(missing)}")
    if missing:
        for m in missing[:5]:
            print(f"  MISSING: {m[:50]!r}")
        raise SystemExit(1)
    emit_py(translations)


if __name__ == "__main__":
    main()
