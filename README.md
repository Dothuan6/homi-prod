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
index.html      màn mua hàng A1 (bản prod không còn trang danh sách màn hình)
screens/        19 file .html — mỗi màn 1 file
css/            tokens.css · base.css · fonts/
js/             ui.js — modal, chuyển bước, copy link
assets/         logo & favicon  ← xem assets/README.md
```

Không dùng server, không build step, không framework. Double-click file nào cũng chạy.

## URL trên GitHub Pages (12/10/2026)

Các trang ở thư mục gốc được sinh từ `screens/` bằng `python tools/build-routes.py`
(`build-v3.py` tự gọi ở cuối). **Sửa ở `screens/` rồi chạy lại script, không sửa tay các trang sinh ra.**

| URL | Màn | File |
|---|---|---|
| `/<MÃ>` — vd `https://homi365.com.vn/SA2237` | A1 Form mua hàng, ô Mã giới thiệu lấy theo URL | `404.html` → `index.html` |
| `/`, `/<mã sai>`, đường dẫn sai | Màn thông báo "Vui lòng dùng liên kết giới thiệu của thành viên HOMI365…" | `index.html` |
| `/policy?s=dieu-khoan-thanh-vien` | Chính sách | `policy.html` |
| `/agent/dang-nhap` | C1 Đăng nhập thành viên | `agent/dang-nhap.html` |
| `/agent/dang-ky` | A2 Đăng ký thành viên | `agent/dang-ky.html` |
| `/agent` | A3 Dashboard thành viên | `agent.html` (+ `agent/index.html`) |
| `/admin/dang-nhap` | B1 Đăng nhập quản trị | `admin/dang-nhap.html` |
| `/admin/thanh-vien` · `/admin` | B2 Thành viên | `admin/thanh-vien.html` |
| `/admin/xet-hang` | B9 Xét thăng / hạ cấp | `admin/xet-hang.html` |
| `/admin/doi-diem` | B3 Yêu cầu đổi điểm | `admin/doi-diem.html` |
| `/admin/don-hang` | B6 Đơn hàng | `admin/don-hang.html` |
| `/admin/kho-hang` | B4 Kho hàng | `admin/kho-hang.html` |
| `/admin/san-pham` | B5 Sản phẩm | `admin/san-pham.html` |
| `/admin/nhat-ky` | B8 Nhật ký hệ thống | `admin/nhat-ky.html` |
| `/admin/tai-khoan` | B7 Tài khoản admin | `admin/tai-khoan.html` |

Trạng thái xem thử vẫn mở bằng `#hash`, vd `/admin/thanh-vien#chi-tiet`.
Link hiển thị/copy trong giao diện dùng full URL: link giới thiệu `https://homi365.com.vn/<MÃ>`,
link đăng nhập `https://homi365.com.vn/agent/dang-nhap`.
Chạy được cả khi gắn domain riêng (gốc `/`) lẫn `dothuan6.github.io/homi-prod/`.

Mã giới thiệu hợp lệ là danh sách cố định `VALID_REF` trong `tools/build-routes.py`
(site tĩnh, không có database). Thêm/bớt mã: sửa danh sách, chạy lại script, deploy lại.
Netlify dùng `_redirects` (trả 200); GitHub Pages dùng `404.html`.
