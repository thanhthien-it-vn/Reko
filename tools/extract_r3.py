#!/usr/bin/env python3
"""Trich xuat chuoi Big5/ASCII tu file .R3 cua REKO3 (San Guo Zhi Ying Jie Zhuan)."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HAN_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
DEFAULT_GAME = Path(r"D:\Game\Reko\Reko\reko3")

# 63 vat pham, moi entry 16 byte, ten bat dau offset 0x0D00
ITEM_BASE = 0x0D00
ITEM_COUNT = 63
ITEM_NAME_MAX = 13  # 6 chu Han + null


def decode_big5(data: bytes) -> str:
    return data.split(b"\x00")[0].decode("big5", errors="replace").strip()


def extract_items(path: Path) -> list[dict]:
    data = path.read_bytes()
    entries: list[dict] = []
    for i in range(ITEM_COUNT):
        off = ITEM_BASE + i * 16
        raw = data[off : off + ITEM_NAME_MAX]
        name = decode_big5(raw)
        if not name or "\ufffd" in name:
            continue
        raw_len = len(name.encode("big5", errors="replace"))
        # 6 chu Han full-width ~ 12 byte; ASCII 1 byte/char
        ascii_max = 12
        entries.append(
            {
                "id": f"ITEM_{i:02d}",
                "file": path.name,
                "offset": off,
                "item_index": i,
                "raw_hex": raw[:raw_len].hex(),
                "raw_bytes": raw_len,
                "ascii_max": ascii_max,
                "original": name,
                "translated": "",
                "abbrev": "",
                "status": "pending",
            }
        )
    return entries


def extract_big5_runs(data: bytes) -> list[tuple[int, bytes, str]]:
    out: list[tuple[int, bytes, str]] = []
    i = 0
    while i < len(data):
        b = data[i]
        if b == 0:
            i += 1
            continue
        if 0x20 <= b < 0x7F:
            start = i
            buf = bytearray()
            while i < len(data) and 0x20 <= data[i] < 0x7F:
                buf.append(data[i])
                i += 1
            text = bytes(buf).decode("ascii").strip()
            if len(text) >= 2:
                out.append((start, bytes(buf), text))
            continue
        if 0xA1 <= b <= 0xF9 and i + 1 < len(data) and data[i + 1] >= 0x40:
            start = i
            buf = bytearray()
            while i + 1 < len(data) and 0xA1 <= data[i] <= 0xF9 and data[i + 1] >= 0x40:
                buf.extend(data[i : i + 2])
                i += 2
            try:
                text = bytes(buf).decode("big5").strip()
            except UnicodeDecodeError:
                continue
            if len(text) >= 2 and HAN_RE.search(text):
                out.append((start, bytes(buf), text))
            continue
        i += 1
    return out


def extract_null_strings(data: bytes) -> list[tuple[int, bytes, str]]:
    """Trich chuoi null-terminated Big5 (dung cho SNR?M.R3)."""
    out: list[tuple[int, bytes, str]] = []
    i = 0
    while i < len(data):
        if data[i] == 0:
            i += 1
            continue
        start = i
        j = i
        while j < len(data) and data[j] != 0:
            j += 1
        chunk = data[start:j]
        if len(chunk) >= 4:
            try:
                text = chunk.decode("big5").strip()
                if len(text) >= 2 and HAN_RE.search(text) and "\ufffd" not in text:
                    out.append((start, chunk, text))
            except UnicodeDecodeError:
                pass
        i = j + 1
    return out


def ascii_budget(data: bytes, start: int, raw_len: int) -> int:
    end = start + raw_len
    budget = raw_len
    while end < len(data) and data[end] == 0:
        end += 1
        budget += 1
    return max(raw_len // 2, min(budget, raw_len + 8))


def extract_script_text(path: Path) -> list[dict]:
    data = path.read_bytes()
    entries: list[dict] = []
    seen: set[str] = set()
    chapter = path.stem.replace("SNR", "").replace("M", "")
    # Uu tien null-terminated (dung format SNR?M.R3)
    runs = extract_null_strings(data)
    if len(runs) < 5:
        runs = extract_big5_runs(data)
    for offset, raw, text in runs:
        if text in seen:
            continue
        seen.add(text)
        entries.append(
            {
                "id": f"{path.stem}_{offset:06X}",
                "file": path.name,
                "chapter": chapter,
                "offset": offset,
                "raw_hex": raw.hex(),
                "raw_bytes": len(raw),
                "ascii_max": ascii_budget(data, offset, len(raw)),
                "original": text,
                "translated": "",
                "abbrev": "",
                "status": "pending",
            }
        )
    return entries


def extract_npc_names(path: Path) -> list[dict]:
    """Ten NPC o dau file BAKDATA (offset 0x0000, moi entry 13 byte)."""
    data = path.read_bytes()
    entries: list[dict] = []
    seen: set[str] = set()
    for off in range(0, 0x0C00, 13):
        raw = data[off : off + 13]
        name = decode_big5(raw)
        if not name or "\ufffd" in name or name in seen:
            continue
        if not HAN_RE.search(name):
            continue
        seen.add(name)
        raw_len = len(name.encode("big5", errors="replace"))
        entries.append(
            {
                "id": f"NPC_{off:04X}",
                "file": path.name,
                "offset": off,
                "raw_hex": raw[:raw_len].hex(),
                "raw_bytes": raw_len,
                "ascii_max": 8,
                "original": name,
                "translated": "",
                "abbrev": "",
                "status": "pending",
            }
        )
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract REKO3 R3 strings to JSON")
    parser.add_argument(
        "game_dir",
        nargs="?",
        default=str(DEFAULT_GAME),
        help="Thu muc reko3",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="translations/extracted",
        help="Thu muc output JSON",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="Chi trich file cu the",
    )
    parser.add_argument(
        "--npc",
        action="store_true",
        help="Trich them ten NPC tu BAKDATA.R3",
    )
    args = parser.parse_args()

    game = Path(args.game_dir)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    targets: list[Path] = []
    if args.files:
        targets = [game / f for f in args.files]
    else:
        bak = game / "BAKDATA.R3"
        if bak.exists():
            targets.append(bak)
        targets.extend(sorted(game.glob("SNR*M.R3")))

    for path in targets:
        if not path.exists():
            print(f"SKIP (missing): {path}")
            continue
        if path.name == "BAKDATA.R3":
            entries = extract_items(path)
            out_name = "item.json"
            out_path = out_dir / out_name
            out_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"{path.name}: {len(entries)} vat pham -> {out_path}")
            if args.npc or not args.files:
                npc = extract_npc_names(path)
                npc_path = out_dir / "npc.json"
                npc_path.write_text(json.dumps(npc, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"{path.name}: {len(npc)} NPC -> {npc_path}")
            continue
        if path.name.endswith("M.R3"):
            entries = extract_script_text(path)
            out_name = f"script_{path.stem.lower()}.json"
        else:
            print(f"SKIP (unknown): {path.name}")
            continue
        out_path = out_dir / out_name
        out_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{path.name}: {len(entries)} chuoi -> {out_path}")


if __name__ == "__main__":
    main()
