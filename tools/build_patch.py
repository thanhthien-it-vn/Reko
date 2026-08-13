#!/usr/bin/env python3
"""Ghi ban dich ASCII (abbrev) nguoc vao file .R3 cua REKO3."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

DEFAULT_GAME = Path(r"D:\Game\Reko\Reko\reko3")
DEFAULT_JSON = Path("translations/extracted")
ITEM_BASE = 0x0D00
ITEM_SLOT = 16
ITEM_NAME_MAX = 13


def load_json(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def patch_bytes(data: bytearray, offset: int, text: str, max_len: int) -> None:
    """Write ASCII text null-padded into data at offset, up to max_len bytes."""
    encoded = text.encode("ascii", errors="replace")
    if len(encoded) > max_len:
        raise ValueError(f"Text too long ({len(encoded)} > {max_len}): {text!r}")
    chunk = encoded + b"\x00" * (max_len - len(encoded))
    data[offset : offset + max_len] = chunk


def patch_null_string(data: bytearray, offset: int, text: str, budget: int) -> None:
    """Replace null-terminated string at offset with ASCII text."""
    end = offset
    while end < len(data) and data[end] != 0:
        end += 1
    # Include trailing nulls up to budget
    limit = min(end + 1, offset + budget)
    while limit < len(data) and data[limit] == 0 and limit - offset < budget:
        limit += 1
    max_len = limit - offset
    patch_bytes(data, offset, text, max_len)


def patch_items(data: bytearray, entries: list[dict]) -> int:
    count = 0
    for entry in entries:
        if entry.get("status") != "done" or not entry.get("abbrev"):
            continue
        off = entry["offset"]
        patch_bytes(data, off, entry["abbrev"], ITEM_NAME_MAX)
        count += 1
    return count


def patch_npcs(data: bytearray, entries: list[dict]) -> int:
    count = 0
    for entry in entries:
        if entry.get("status") != "done" or not entry.get("abbrev"):
            continue
        off = entry["offset"]
        patch_bytes(data, off, entry["abbrev"], 13)
        count += 1
    return count


def patch_script(data: bytearray, entries: list[dict]) -> int:
    count = 0
    for entry in entries:
        if entry.get("status") != "done" or not entry.get("abbrev"):
            continue
        off = entry["offset"]
        budget = entry.get("ascii_max", entry.get("raw_bytes", 0) + 8)
        patch_null_string(data, off, entry["abbrev"], budget)
        count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Build REKO3 R3 patch from translated JSON")
    parser.add_argument("game_dir", nargs="?", default=str(DEFAULT_GAME))
    parser.add_argument("-j", "--json-dir", default=str(DEFAULT_JSON))
    parser.add_argument("-o", "--output", help="Output dir (default: game_dir)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    game = Path(args.game_dir)
    json_dir = Path(args.json_dir)
    out_dir = Path(args.output) if args.output else game

    patches: list[tuple[str, str, callable]] = [
        ("BAKDATA.R3", "item.json", patch_items),
        ("BAKDATA.R3", "npc.json", patch_npcs),
    ]
    for snr in sorted(json_dir.glob("script_snr*m.json")):
        r3_name = snr.stem.replace("script_", "").upper() + ".R3"
        patches.append((r3_name, snr.name, patch_script))

    # Group by R3 file
    by_r3: dict[str, list[tuple[str, callable]]] = {}
    for r3, json_name, fn in patches:
        by_r3.setdefault(r3, []).append((json_name, fn))

    for r3_name, jobs in sorted(by_r3.items()):
        src = game / r3_name
        if not src.exists():
            print(f"SKIP (missing): {src}")
            continue
        data = bytearray(src.read_bytes())
        total = 0
        for json_name, fn in jobs:
            jpath = json_dir / json_name
            if not jpath.exists():
                continue
            entries = load_json(jpath)
            n = fn(data, entries)
            print(f"  {json_name}: {n} strings patched")
            total += n
        if total == 0:
            print(f"{r3_name}: nothing to patch")
            continue
        if args.dry_run:
            print(f"{r3_name}: would patch {total} strings (dry-run)")
            continue
        dst = out_dir / r3_name
        if dst.resolve() != src.resolve():
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.copy2(src, dst)
            dst.write_bytes(data)
        else:
            backup = src.with_suffix(".R3.bak")
            if not backup.exists():
                shutil.copy2(src, backup)
            src.write_bytes(data)
        print(f"{r3_name}: patched {total} strings -> {dst}")


if __name__ == "__main__":
    main()
