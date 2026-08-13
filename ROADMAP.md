# Roadmap dich REKO3 -> Tieng Viet (khong dau)

## Phase 0 - Co so

- [x] Tool trich xuat text (`tools/extract_r3.py`)
- [x] Scaffold repo + AGENTS.md cho Cursor Cloud
- [x] Tool build patch nguoc vao .R3 (`tools/build_patch.py`)
- [x] Tool validate ban dich (`tools/validate_translations.py`)
- [x] Tool apply dich (`tools/run_translate.py`)
- [ ] Script test nhanh trong DOSBox (copy patch -> reko3)

## Phase 1 - Vat pham (~63 chuoi)

- [x] `item.json` tu BAKDATA.R3 (63/63 done)
- [ ] Test hien thi ten vat pham trong game

## Phase 2 - Kich ban / hoi thoai

- [x] `script_snr0m.json` - Chuong mo dau (149/149 done)
- [x] `script_snr1m.json` - Chuong 1 (1158/1158 done)
- [x] `script_snr2m.json` - Chuong 2 (962/962 done)
- [x] `script_snr3m.json` - Chuong 3 (1483/1483 done)
- [x] `script_snr4m.json` - Chuong 4 (622/622 done)
- [x] `npc.json` - Ten NPC (18/18 done)

## Phase 3 - Mo ta vat pham

- [ ] Trich text tu MAIN.EXE (mo ta 63 vat pham)

## Quy trinh Cursor Cloud (dich dan)

1. Push repo len GitHub
2. Mo Cloud Agent, paste prompt tu AGENTS.md
3. Moi session: 1 file JSON, 50-100 dong
4. Commit + push sau moi batch
5. Milestone tag: `v0.1-items`, `v0.2-ch0`, ...

## Tien do

| File | Tong | Done | Pending |
|------|------|------|---------|
| item.json | 63 | 63 | 0 |
| npc.json | 18 | 18 | 0 |
| script_snr0m.json | 149 | 149 | 0 |
| script_snr1m.json | 1158 | 1158 | 0 |
| script_snr2m.json | 962 | 962 | 0 |
| script_snr3m.json | 1483 | 1483 | 0 |
| script_snr4m.json | 622 | 622 | 0 |
| **Tong** | **4455** | **4455** | **0** |

## Build patch

```bash
# Validate truoc khi build
python tools/validate_translations.py

# Ghi patch vao thu muc game (backup .bak tu dong)
python tools/build_patch.py "D:/Game/Reko/Reko/reko3"

# Hoac xuat ra thu muc rieng
python tools/build_patch.py "D:/Game/Reko/Reko/reko3" -o patches/
```

## Ghi chu chat luong

- `script_snr0m.json`: dich thu cong, chat luong cao
- `script_snr2m.json`: dich thu cong theo batch
- `script_snr1m/3m/4m`: dich tu dong (Google Translate) + xu ly ten rieng
- Can review thu cong truoc khi phat hanh chinh thuc
