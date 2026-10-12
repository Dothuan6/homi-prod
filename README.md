# prototype-v3 — HOMI365

Re-skin mockup của khách hàng (`../Prototypev-v3/Homi365_Mockup-0409.html`) theo brand HOMI365.

**Phạm vi:** chỉ đổi màu + logo. Giữ nguyên 100% fields, layout, font (Nunito / Roboto) của mockup KH.

Kế hoạch đầy đủ: [`../PLAN-prototype-v3.md`](../PLAN-prototype-v3.md)

## Trạng thái — 08/09/2026

| Bước | Việc | Trạng thái |
|---|---|---|
| P0 | Giải nén bundle mockup KH | 🔴 **cần bạn chạy `python prototype-v3\tools\extract-bundle.py`** |
| P1 | Khử runtime riêng (`<sc-if>`, `style-hover`, `{{biến}}`) | ⏸ chặn bởi P0 |
| P2 | Preview 2 phương án màu màn A1 → KH chốt `--c6` | ⏸ chặn bởi P0 |
| P3 | Apply bảng map màu | 🟢 `css/tokens.css` đã viết xong, chờ markup |
| P4 | Logo & favicon | 🟢 file gốc đã có trong `assets/` |
| P5 | Tách 19 file + `index.html` + `js/ui.js` | — |
| P6 | QA đối chiếu | — |
| P7 | Đóng gói bàn giao | — |

## Cấu trúc (sẽ dựng ở P5)

```
index.html      chuyển thẳng tới màn mua hàng A1 (bản prod không còn trang danh sách màn hình)
screens/        19 file .html — mỗi màn 1 file
css/            tokens.css · base.css · fonts/
js/             ui.js — modal, chuyển bước, copy link
assets/         logo & favicon  ← xem assets/README.md
```

Không dùng server, không build step, không framework. Double-click file nào cũng chạy.
