# REKO3 — 三国志英杰传 bản tiếng Việt không dấu

Repo GitHub: [thanhthien-it-vn/Reko](https://github.com/thanhthien-it-vn/Reko)

Game gốc: Koei 1992, bản DOS Trung Quốc (REKO3).  
Cài đặt tham chiếu: `D:\Game\Reko\Reko\reko3`

## Mục tiêu

- Dịch dần toàn bộ text trong file `.R3` (và sau này `MAIN.EXE`)
- **Tiếng Việt không dấu** (ASCII) — game hỗ trợ chữ Latin/ASCII
- **Tràn chữ → viết tắt** theo [docs/HUONG-DAN-VIET-TAT.md](docs/HUONG-DAN-VIET-TAT.md)

## Cấu trúc repo

```
REKO-VN/
  README.md
  ROADMAP.md
  AGENTS.md                    # Hướng dẫn Cursor Cloud Agent
  docs/HUONG-DAN-VIET-TAT.md
  tools/
    extract_r3.py              # Trích xuất chuỗi gốc → JSON
    build_patch.py             # (TODO) Gộp bản dịch → patch .R3
  translations/
    extracted/                 # JSON từ game gốc
    patches/                   # File .R3 đã dịch (khi build xong)
```

## Bắt đầu nhanh

```bat
cd D:\Game\REKO-VN
python tools\extract_r3.py
```

Mở `translations/extracted/item.json`, điền:

```json
{
  "original": "短剑",
  "translated": "Kiem ngan",
  "abbrev": "K.Ngan",
  "status": "done"
}
```

## File game chứa text

| File | Nội dung |
|------|----------|
| `BAKDATA.R3` | Tên 63 vật phẩm (tối đa 6 chữ Hán) |
| `SNR0M.R3`–`SNR4M.R3` | Kịch bản / hội thoại theo chương |
| `MAIN.EXE` | Mô tả vật phẩm (phase sau) |

## Cursor Cloud — dịch từ từ

1. Push repo lên GitHub
2. Mở **Cursor → Cloud Agent** trên repo `REKO-VN`
3. Prompt mẫu trong `AGENTS.md` — mỗi session dịch 50–100 dòng JSON
4. Agent commit + push; session sau `git pull` rồi tiếp tục

## Trạng thái

| Phase | Nội dung | Trạng thái |
|-------|----------|------------|
| 0 | Tool + scaffold | 🟡 Đang làm |
| 1 | Vật phẩm (63) | ⚪ Chưa |
| 2 | Kịch bản chương 0–4 | ⚪ Chưa |
| 3 | MAIN.EXE mô tả | ⚪ Chưa |

## Lưu ý pháp lý

- Chỉ fan patch / bản dịch cộng đồng — **không** phân phối game gốc
- Người chơi cần sở hữu bản game hợp lệ

## Liên quan

- Dự án tương tự: `D:\Game\GSE-VN` (Graystone Saga)
- Format `.R3`: [剧本初步解析](https://www.xycq.org.cn/forum/thread-239493-1-1.html)
