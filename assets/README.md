# assets/ — logo & favicon

## Cần bạn thả 2 file gốc vào đây

Môi trường chạy script đang lỗi nên mình chưa chép được file ảnh vào. Kéo 2 file KH gửi vào thư mục này và **đổi tên đúng như bảng dưới**:

| File KH gửi | Đổi tên thành | Dùng làm |
|---|---|---|
| `logo homi-01.png` | `homi365-logo-horizontal.png` | Logo header — cả 3 khung buyer / seller / admin |
| `Icon_viewweb_final.jpg` | `homi365-mark-source.jpg` | File nguồn để xuất favicon |

## Mình sẽ xử lý tiếp ở bước P4

1. Tách nền kem (`#F5F4EE`) của `homi365-mark-source.jpg` → PNG trong suốt.
2. Xuất bộ favicon: `favicon-16.png` · `favicon-32.png` · `favicon-48.png` · `favicon-180.png` (apple-touch) · `favicon-256.png` · `favicon.ico`.
3. Lấy chính xác mã màu navy và teal từ logo bằng eyedropper, chỉnh lại `css/tokens.css` cho khớp.
4. Nhúng vào cả 19 file màn hình:

```html
<link rel="icon" href="../assets/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="../assets/favicon-180.png">
<meta name="theme-color" content="#1E3A66">
```

## Còn thiếu — nên xin thêm KH

- **File vector** (`.ai` / `.eps` / `.svg`) của logo ngang. Bản PNG dùng tạm được cho prototype, nhưng đặt trên header sẽ vỡ ở màn Retina và dev sẽ cần vector khi làm thật.
- **Bản icon nền trong suốt** — để khỏi phải tách nền thủ công, tránh viền răng cưa quanh đường cong.
- **Bản logo một màu trắng** — dùng cho header admin nền navy, nếu sau này cần.

## Không dùng

`prototype-v2/brandingGuideline/logo/*.svg` là **bản vẽ tay ước lượng**, không phải logo chính thức: thiếu ăng-ten/sóng wifi, đường nhịp tim và hai đầu tròn kiểu ống nghe; chữ chưa outline. Đã đánh dấu deprecated — đừng dùng cho `prototype-v3/`.
