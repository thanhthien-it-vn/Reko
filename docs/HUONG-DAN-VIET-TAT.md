# Huong dan viet tat - REKO3 (San Guo Zhi Ying Jie Zhuan) tieng Viet khong dau

Muc tieu: text trong game ngan hon ban dich day du, tranh tran o man hinh DOS.

## Quy tac chung

1. **Khong dau** - chi dung a-z, A-Z, 0-9, space
2. **Uu tien viet tat da thong nhat** - xem bang duoi
3. **Do dai** - cot `ascii_max` trong file JSON = so ky tu toi da nen dung
4. **Neu van dai** - cat tu, bo danh tu, chi giu y chinh
5. **Ten rieng** - giu am Han-Viet quen thuoc (Luu Bi, Quan Vu, Tao Thao)

## Bang viet tat co dinh (dung lai xuyen suot)

### Nhan vat chinh

| Goc | Viet tat game |
|-----|---------------|
| 刘备 | Luu Bi |
| 关羽 | Quan Vu |
| 张飞 | Truong Phi |
| 赵云 | Trieu Van |
| 诸葛亮 | Gia Cat Luong |
| 曹操 | Tao Thao |
| 吕布 | Lu Bo |

### Vat pham (63 loai)

| Goc | Viet tat |
|-----|----------|
| 短剑 | K.Ngan |
| 长剑 | K.Dai |
| 矛 | Thuong |
| 战斧 | R.Chien |
| 青龙偃月刀 | Thanh Long |
| 丈八蛇矛 | Xa Mao |
| 药 | Thuoc |
| 恢复 | Hoi |
| 攻击 | Tan cong |
| 防御 | Phong thu |

### Menu / he thong

| Goc | Viet tat |
|-----|----------|
| 购买 | Mua |
| 卖出 | Ban |
| 装备 | Trang bi |
| 使用 | Dung |
| 撤退 | Rut lui |
| 结束 | Ket thuc |
| 攻击 | Tan cong |
| 策略 | Ke luoc |
| 待机 | Cho |

### Dia danh

| Goc | Viet tat |
|-----|----------|
| 徐州 | Xu Chau |
| 荆州 | Kinh Chau |
| 益州 | Ich Chau |
| 洛阳 | Lac Duong |
| 许昌 | Hu Xu |
| 新野 | Tan Da |

## Vi du xu ly tran chu

| Goc | ascii_max | Ban dich | Viet tat trong game |
|-----|-----------|----------|---------------------|
| 青龙偃月刀 | 6 | Dao Thanh Long | T.Long |
| 群雄起兵讨伐董卓 | 12 | Quan hung khoi binh | Q.Hung |
| 好像很慌张似地... | (talk) | ... | (tach cau ngan) |

## Ghi chu cho nguoi dich

- File `translations/extracted/*.json`: dien cot `translated` (day du) va `abbrev` (vao game)
- Ten vat pham: toi da **6 ky tu hien thi** (ascii_max thuong = 6-12)
- Danh dau `"status": "done"` khi da review
- **Khong** doi file .R3 khi chua test patch trong DOSBox
