# Roadmap dich REKO3 -> Tieng Viet (khong dau)

## Phase 0 - Co so

- [x] Tool trich xuat text (`tools/extract_r3.py`)
- [x] Scaffold repo + AGENTS.md cho Cursor Cloud
- [ ] Tool build patch nguoc vao .R3 (`tools/build_patch.py`)
- [ ] Script test nhanh trong DOSBox (copy patch -> reko3)

## Phase 1 - Vat pham (~63 chuoi)

- [ ] `item.json` tu BAKDATA.R3
- [ ] Test hien thi ten vat pham trong game

## Phase 2 - Kich ban / hoi thoai

- [ ] `script_snr0m.json` - Chuong mo dau
- [ ] `script_snr1m.json` - Chuong 1
- [ ] `script_snr2m.json` - Chuong 2
- [ ] `script_snr3m.json` - Chuong 3
- [ ] `script_snr4m.json` - Chuong 4

## Phase 3 - Mo ta vat pham

- [ ] Trich text tu MAIN.EXE (mo ta 63 vat pham)

## Quy trinh Cursor Cloud (dich dan)

1. Push repo len GitHub
2. Mo Cloud Agent, paste prompt tu AGENTS.md
3. Moi session: 1 file JSON, 50-100 dong
4. Commit + push sau moi batch
5. Milestone tag: `v0.1-items`, `v0.2-ch0`, ...

## Uoc luong

| Phase | Chuoi (uoc) | Ghi chu |
|-------|-------------|---------|
| 0 | - | 1 tuan (tool + test) |
| 1 | 63 | 1 ngay |
| 2 | ~2000+ | 1-2 thang (dich dan qua Cloud) |
| 3 | ~200 | 1 tuan |

**Ket luan: Kha thi — cung mo hinh GSE-VN.**

## Tien do

| File | Tong | Done | Pending |
|------|------|------|---------|
| item.json | 63 | 0 (4 sample) | 59 |
| npc.json | 18 | 0 | 18 |
| script_snr0m.json | 149 | 0 | 149 |
| script_snr1m.json | 1158 | 0 | 1158 |
| script_snr2m.json | 962 | 0 | 962 |
| script_snr3m.json | 1483 | 0 | 1483 |
| script_snr4m.json | 622 | 0 | 622 |
| **Tong** | **3455** | **0** | **3455** |
