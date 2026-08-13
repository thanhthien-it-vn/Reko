#!/usr/bin/env python3
"""Generate snr3m_data.py / snr4m_data.py from extracted JSON via translation."""
from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
from pathlib import Path

from deep_translator import GoogleTranslator

# Character / place name replacements (Traditional Chinese -> ASCII Vietnamese)
NAME_MAP: list[tuple[str, str]] = [
    # Main characters
    ("諸葛亮", "Gia Cat Luong"),
    ("诸葛亮", "Gia Cat Luong"),
    ("關羽", "Quan Vu"),
    ("关羽", "Quan Vu"),
    ("張飛", "Truong Phi"),
    ("张飞", "Truong Phi"),
    ("劉備", "Luu Bi"),
    ("刘备", "Luu Bi"),
    ("趙雲", "Trieu Van"),
    ("赵云", "Trieu Van"),
    ("曹操", "Tao Thao"),
    ("呂布", "Lu Bo"),
    ("吕布", "Lu Bo"),
    ("孫權", "Ton Quyen"),
    ("孙权", "Ton Quyen"),
    ("周瑜", "Chu Du"),
    ("黃忠", "Hoang Trung"),
    ("黄忠", "Hoang Trung"),
    ("馬超", "Ma Sieu"),
    ("马超", "Ma Sieu"),
    ("魏延", "Vi Yan"),
    ("姜維", "Tuong Vi"),
    ("姜维", "Tuong Vi"),
    ("龐統", "Bong Thong"),
    ("庞统", "Bong Thong"),
    ("法正", "Phap Chinh"),
    ("徐庶", "Tu Thu"),
    ("關平", "Quan Binh"),
    ("关平", "Quan Binh"),
    ("關興", "Quan Hung"),
    ("关兴", "Quan Hung"),
    ("張苞", "Truong Bao"),
    ("张苞", "Truong Bao"),
    ("曹仁", "Tao Nhan"),
    ("曹洪", "Tao Hong"),
    ("夏侯惇", "Ha Hau Don"),
    ("夏侯渊", "Ha Hau Nguyen"),
    ("許褚", "Hu Thu"),
    ("许褚", "Hu Thu"),
    ("典韋", "Dien Vi"),
    ("典韦", "Dien Vi"),
    ("張遼", "Truong Lieu"),
    ("张辽", "Truong Lieu"),
    ("曹丕", "Tao Phi"),
    ("司馬懿", "Tu Ma Y"),
    ("司马懿", "Tu Ma Y"),
    ("陸遜", "Luc Ton"),
    ("陆逊", "Luc Ton"),
    ("魯肅", "Lo Tuc"),
    ("鲁肃", "Lo Tuc"),
    ("呂蒙", "Lu Mong"),
    ("吕蒙", "Lu Mong"),
    ("甘寧", "Cam Ninh"),
    ("甘宁", "Cam Ninh"),
    ("太史慈", "Thai Su Tu"),
    ("董卓", "Dong Trac"),
    ("袁紹", "Vien Thieu"),
    ("袁绍", "Vien Thieu"),
    ("袁術", "Vien Thu"),
    ("袁术", "Vien Thu"),
    ("華佗", "Hoa Da"),
    ("华佗", "Hoa Da"),
    ("貂蟬", "Dieu Thuyen"),
    ("貂蝉", "Dieu Thuyen"),
    ("糜竺", "Mi Truc"),
    ("糜夫人", "Phu nhan Mi"),
    ("孫尚香", "Ton Thuong Huong"),
    ("孙尚香", "Ton Thuong Huong"),
    ("劉禪", "Luu Thien"),
    ("刘禅", "Luu Thien"),
    ("劉璋", "Luu Chuong"),
    ("刘璋", "Luu Chuong"),
    # Places
    ("荊州", "Kinh Chau"),
    ("荆州", "Kinh Chau"),
    ("徐州", "Xu Chau"),
    ("益州", "Ich Chau"),
    ("洛陽", "Lac Duong"),
    ("洛阳", "Lac Duong"),
    ("許昌", "Hu Xu"),
    ("许昌", "Hu Xu"),
    ("新野", "Tan Da"),
    ("成都", "Thanh Do"),
    ("襄陽", "Tuong Duong"),
    ("襄阳", "Tuong Duong"),
    ("江陵", "Giang Lang"),
    ("赤壁", "Xich Bich"),
    ("長坂坡", "Truong Ban"),
    ("长坂坡", "Truong Ban"),
    ("漢中", "Han Trung"),
    ("汉中", "Han Trung"),
    ("長安", "Truong An"),
    ("长安", "Truong An"),
    ("建業", "Kien Nghiep"),
    ("建业", "Kien Nghiep"),
    ("宛城", "Uan Thanh"),
    ("小沛", "Tieu Bai"),
    ("下邳", "Ha Bi"),
    ("白帝城", "Bach De Thanh"),
    ("夷陵", "Di Lang"),
    ("麥城", "Mai Thanh"),
    ("麦城", "Mai Thanh"),
    ("街亭", "Giai Dinh"),
    ("祁山", "Ky Son"),
    ("五丈原", "Ngu Truong Nguyen"),
    ("博望坡", "Bac Vong Pho"),
    ("華容道", "Hoa Dung Dao"),
    ("华容道", "Hoa Dung Dao"),
    ("樊城", "Phan Thanh"),
    ("新亭", "Tan Dinh"),
    ("合肥", "Hop Phi"),
    ("濡須口", "Nhu Tu Khau"),
    ("濡须口", "Nhu Tu Khau"),
    ("陳倉", "Tran Tang"),
    ("陈仓", "Tran Tang"),
    ("天水", "Thien Thuy"),
    ("安定", "An Dinh"),
    ("武都", "Vo Do"),
    ("陰平", "Am Binh"),
    ("阴平", "Am Binh"),
    ("劍閣", "Kiem Cac"),
    ("剑阁", "Kiem Cac"),
    ("涪城", "Phu Thanh"),
    ("雒城", "Lac Thanh"),
    ("雒城", "Lac Thanh"),
    # Factions / terms
    ("蜀國", "nuoc Thuc"),
    ("蜀国", "nuoc Thuc"),
    ("魏國", "nuoc Nguoi"),
    ("魏国", "nuoc Nguoi"),
    ("吳國", "nuoc Ngo"),
    ("吴国", "nuoc Ngo"),
    ("東吳", "Dong Ngo"),
    ("东吴", "Dong Ngo"),
    ("曹魏", "Tao Nguoi"),
    ("漢室", "nha Han"),
    ("汉室", "nha Han"),
]

# Vietnamese-side corrections after machine translation (with/without diacritics)
VI_NAME_MAP: list[tuple[str, str]] = [
    ("Gia Cat Luong", "Gia Cat Luong"),
    ("Gia Cát Lương", "Gia Cat Luong"),
    ("Quan Vu", "Quan Vu"),
    ("Quan Vũ", "Quan Vu"),
    ("Truong Phi", "Truong Phi"),
    ("Trương Phi", "Truong Phi"),
    ("Luu Bi", "Luu Bi"),
    ("Lưu Bị", "Luu Bi"),
    ("Trieu Van", "Trieu Van"),
    ("Triệu Vân", "Trieu Van"),
    ("Tao Thao", "Tao Thao"),
    ("Tào Tháo", "Tao Thao"),
    ("Lu Bo", "Lu Bo"),
    ("Lữ Bố", "Lu Bo"),
    ("Ton Quyen", "Ton Quyen"),
    ("Tôn Quyền", "Ton Quyen"),
    ("Chu Du", "Chu Du"),
    ("Chu Du", "Chu Du"),
    ("Chu Du", "Chu Du"),
    ("Hoang Trung", "Hoang Trung"),
    ("Hoàng Trung", "Hoang Trung"),
    ("Ma Sieu", "Ma Sieu"),
    ("Mã Siêu", "Ma Sieu"),
    ("Kinh Chau", "Kinh Chau"),
    ("Kinh Châu", "Kinh Chau"),
    ("Xu Chau", "Xu Chau"),
    ("Từ Châu", "Xu Chau"),
    ("Ich Chau", "Ich Chau"),
    ("Ích Châu", "Ich Chau"),
    ("Lac Duong", "Lac Duong"),
    ("Lạc Dương", "Lac Duong"),
    ("Hu Xu", "Hu Xu"),
    ("Hứa Xương", "Hu Xu"),
    ("Tan Da", "Tan Da"),
    ("Tân Dã", "Tan Da"),
    ("Thanh Do", "Thanh Do"),
    ("Thành Đô", "Thanh Do"),
    ("Tuong Duong", "Tuong Duong"),
    ("Tương Dương", "Tuong Duong"),
    ("Giang Lang", "Giang Lang"),
    ("Giang Lăng", "Giang Lang"),
    ("Chua cong", "Chua oi"),
    ("Chúa công", "Chua oi"),
    ("Chua oi", "Chua oi"),
    ("Chúa ơi", "Chua oi"),
]

# Sort by length descending so longer names match first
NAME_MAP.sort(key=lambda x: len(x[0]), reverse=True)
VI_NAME_MAP.sort(key=lambda x: len(x[0]), reverse=True)

VIET_MAP = str.maketrans({
    "à": "a", "á": "a", "ả": "a", "ã": "a", "ạ": "a",
    "ă": "a", "ằ": "a", "ắ": "a", "ẳ": "a", "ẵ": "a", "ặ": "a",
    "â": "a", "ầ": "a", "ấ": "a", "ẩ": "a", "ẫ": "a", "ậ": "a",
    "è": "e", "é": "e", "ẻ": "e", "ẽ": "e", "ẹ": "e",
    "ê": "e", "ề": "e", "ế": "e", "ể": "e", "ễ": "e", "ệ": "e",
    "ì": "i", "í": "i", "ỉ": "i", "ĩ": "i", "ị": "i",
    "ò": "o", "ó": "o", "ỏ": "o", "õ": "o", "ọ": "o",
    "ô": "o", "ồ": "o", "ố": "o", "ổ": "o", "ỗ": "o", "ộ": "o",
    "ơ": "o", "ờ": "o", "ớ": "o", "ở": "o", "ỡ": "o", "ợ": "o",
    "ù": "u", "ú": "u", "ủ": "u", "ũ": "u", "ụ": "u",
    "ư": "u", "ừ": "u", "ứ": "u", "ử": "u", "ữ": "u", "ự": "u",
    "ỳ": "y", "ý": "y", "ỷ": "y", "ỹ": "y", "ỵ": "y",
    "đ": "d", "Đ": "D",
    "À": "A", "Á": "A", "Ả": "A", "Ã": "A", "Ạ": "A",
    "Ă": "A", "Ằ": "A", "Ắ": "A", "Ẳ": "A", "Ẵ": "A", "Ặ": "A",
    "Â": "A", "Ầ": "A", "Ấ": "A", "Ẩ": "A", "Ẫ": "A", "Ậ": "A",
    "È": "E", "É": "E", "Ẻ": "E", "Ẽ": "E", "Ẹ": "E",
    "Ê": "E", "Ề": "E", "Ế": "E", "Ể": "E", "Ễ": "E", "Ệ": "E",
    "Ì": "I", "Í": "I", "Ỉ": "I", "Ĩ": "I", "Ị": "I",
    "Ò": "O", "Ó": "O", "Ỏ": "O", "Õ": "O", "Ọ": "O",
    "Ô": "O", "Ồ": "O", "Ố": "O", "Ổ": "O", "Ỗ": "O", "Ộ": "O",
    "Ơ": "O", "Ờ": "O", "Ớ": "O", "Ở": "O", "Ỡ": "O", "Ợ": "O",
    "Ù": "U", "Ú": "U", "Ủ": "U", "Ũ": "U", "Ụ": "U",
    "Ư": "U", "Ừ": "U", "Ứ": "U", "Ử": "U", "Ữ": "U", "Ự": "U",
    "Ỳ": "Y", "Ý": "Y", "Ỷ": "Y", "Ỹ": "Y", "Ỵ": "Y",
})

ASCII_RE = re.compile(r"^[a-zA-Z0-9 .,!?;:'\"()\-]+$")


def to_ascii_vn(text: str) -> str:
    """Remove Vietnamese diacritics; keep ASCII punctuation."""
    return text.translate(VIET_MAP)


def apply_name_map_cn(text: str) -> str:
    """Replace Chinese names in source before translation."""
    for cn, vn in NAME_MAP:
        text = text.replace(cn, f" {vn} ")
    return re.sub(r"  +", " ", text).strip()


def apply_name_map_vi(text: str) -> str:
    """Fix Vietnamese name spellings after translation."""
    for src, dst in VI_NAME_MAP:
        text = text.replace(src, dst)
    return text


def fit_abbrev(translated: str, ascii_max: int) -> str:
    if len(translated) <= ascii_max:
        return translated
    words = translated.split()
    if len(words) >= 2:
        init = ".".join(w[0].upper() for w in words if w)
        if len(init) <= ascii_max:
            return init
        short = words[0][:3] + "." + words[-1][: max(1, ascii_max - 5)]
        if len(short) <= ascii_max:
            return short
    return translated[:ascii_max]


def make_abbrev(translated: str, ascii_max: int) -> str:
    abbrev = translated
    if len(abbrev) > ascii_max:
        abbrev = fit_abbrev(translated, ascii_max)
    # Ensure ASCII-only
    abbrev = to_ascii_vn(abbrev)
    if not ASCII_RE.match(abbrev):
        abbrev = re.sub(r"[^a-zA-Z0-9 .,!?;:'\"()\-]", "", abbrev)
    if len(abbrev) > ascii_max:
        abbrev = fit_abbrev(abbrev, ascii_max)
    return abbrev


def translate_batch(texts: list[str], retries: int = 3) -> list[str]:
    for attempt in range(retries):
        try:
            return GoogleTranslator(source="zh-TW", target="vi").translate_batch(texts)
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    return texts  # unreachable


def process_entries(entries: list[dict], batch_size: int = 40) -> dict[str, tuple[str, str]]:
    """Return dict keyed by original Chinese."""
    originals = [e["original"] for e in entries]
    ascii_max_map = {e["original"]: e["ascii_max"] for e in entries}
    results: dict[str, tuple[str, str]] = {}

    for i in range(0, len(originals), batch_size):
        batch = [apply_name_map_cn(o) for o in originals[i : i + batch_size]]
        vi_batch = translate_batch(batch)
        for orig, vi in zip(originals[i : i + batch_size], vi_batch):
            vi = apply_name_map_vi(vi)
            translated = to_ascii_vn(vi)
            abbrev = make_abbrev(translated, ascii_max_map[orig])
            results[orig] = (translated, abbrev)
        done = min(i + batch_size, len(originals))
        print(f"  translated {done}/{len(originals)}", flush=True)
        time.sleep(0.3)

    return results


def write_data_py(out_path: Path, var_name: str, module_doc: str, data: dict[str, tuple[str, str]]) -> None:
    lines = [
        f'"""{module_doc}"""',
        "",
        f"{var_name}: dict[str, tuple[str, str]] = {{",
    ]
    for orig, (translated, abbrev) in data.items():
        o = json.dumps(orig, ensure_ascii=False)
        t = json.dumps(translated, ensure_ascii=False)
        a = json.dumps(abbrev, ensure_ascii=False)
        lines.append(f"    {o}: ({t}, {a}),")
    lines.append("}")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["snr1m", "snr3m", "snr4m"]
    base = Path("translations/extracted")
    out_dir = Path("tools/translations")

    configs = {
        "snr1m": ("script_snr1m.json", "SNR1M_TRANSLATIONS", "Vietnamese translations for script_snr1m.json"),
        "snr3m": ("script_snr3m.json", "SNR3M_TRANSLATIONS", "Vietnamese translations for script_snr3m.json"),
        "snr4m": ("script_snr4m.json", "SNR4M_TRANSLATIONS", "Vietnamese translations for script_snr4m.json"),
    }

    for key in targets:
        if key not in configs:
            print(f"Unknown target: {key}")
            continue
        json_name, var_name, doc = configs[key]
        json_path = base / json_name
        entries = json.loads(json_path.read_text(encoding="utf-8"))
        print(f"Processing {json_name} ({len(entries)} entries)...")
        data = process_entries(entries)
        out_path = out_dir / f"{key}_data.py"
        write_data_py(out_path, var_name, doc, data)
        print(f"Wrote {out_path} ({len(data)} entries)")


if __name__ == "__main__":
    main()
