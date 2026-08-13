# AGENTS — Huong dan cho Cursor Cloud / Agent

Du an: dich **三国志英杰传 (REKO3 / Sangokushi Eiketsuden)** sang **tieng Viet khong dau** (ASCII).

Game goc: `D:\Game\Reko\Reko\reko3` (khong commit vao repo)

## Muc tieu

1. Dich het text trong `translations/extracted/*.json`
2. Dung **viet tat** khi `len(abbrev) > ascii_max` — xem `docs/HUONG-DAN-VIET-TAT.md`
3. Khong commit file game goc (.EXE, .R3 patch chua test)

## Lenh / prompt mau (Cloud Agent)

Copy-paste khi tao Cloud Agent moi:

```
Doc AGENTS.md, ROADMAP.md, docs/HUONG-DAN-VIET-TAT.md.

Nhiem vu: dich file translations/extracted/<TEN_FILE>.json
- Dien translated (day du) va abbrev (vao game)
- abbrev phai <= ascii_max ky tu
- Chi dung a-z, A-Z, 0-9, space (KHONG dau tieng Viet)
- Dat status: "done" khi xong
- Commit + push len main

Uu tien: item.json -> script_snr0m.json -> script_snr1m.json -> ...
```

## Quy trinh moi session

1. `git pull`
2. Chon 1 file JSON phase chua xong (uu tien pending nhieu nhat)
3. Dich 50-100 dong / session
4. `git commit -m "dich <file>: batch N"` + `git push`
5. Ghi tien do vao ROADMAP.md neu can

## Quy tac dich

| Rule | Chi tiet |
|------|----------|
| Encoding | abbrev = ASCII only |
| Do dai | `len(abbrev) <= ascii_max` |
| Ten rieng | Giu am quen thuoc: Luu Bi, Quan Vu, Truong Phi, Tao Thao... |
| Dia danh | Xuzhou, Jingzhou, Yi Zhou... hoac viet tat 2-3 chu |
| Trung lap | Cung nghia = cung abbrev xuyen file |

## Pha con lai (ROADMAP)

- [x] Phase 0 partial: extract_r3.py + scaffold
- [ ] Phase 1: item.json (63 vat pham)
- [ ] Phase 2: script_snr0m .. script_snr4m (hoi thoai)
- [ ] Phase 0: build_patch.py
- [ ] Phase 3: MAIN.EXE mo ta vat pham

## KHONG lam

- Khong dau tieng Viet (á, ệ, ...)
- Khong push file binary game
- Khong doi offset/id trong JSON
- Khong dich khi chua doc HUONG-DAN-VIET-TAT

## Tool

```bash
python tools/extract_r3.py "D:/Game/Reko/Reko/reko3" -o translations/extracted
python tools/extract_r3.py --files BAKDATA.R3 SNR0M.R3
```
