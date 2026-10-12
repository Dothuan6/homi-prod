# DIFF — prototype-v3 so với mockup của khách hàng

Sinh tự động bởi `tools/build-v3.py`. Ngoài 13 mục dưới đây, **không có thay đổi nào khác**: layout, khoảng cách, bo góc, font giữ nguyên 100%.

## 1. Đổi giá trị màu

| Màu cũ (mockup KH) | Màu mới (HOMI365) |
|---|---|
| `#00ADEE` | `#1E3A66` |
| `#00adee` | `#1E3A66` |
| `#0099d1` | `#1B3358` |
| `#0088ba` | `#122544` |
| `#00728f` | `#0F7F96` |
| `rgba(0,173,238,.14)` | `rgba(15,127,150,.14)` |
| `rgba(0,173,238,` | `rgba(30,58,102,` |
| `#EE0000` | `#1E3A66` |
| `#84BE52` | `#2F7A48` |
| `#4c7a2e` | `#2F7A48` |
| `#73aa45` | `#2F7A48` |
| `rgba(132,190,82,` | `rgba(47,122,72,` |
| `#FFA500` | `#965C0A` |
| `#FBAE40` | `#965C0A` |
| `#FFBC40` | `#E0B15F` |
| `#a36400` | `#965C0A` |
| `rgba(255,165,0,` | `rgba(150,92,10,` |
| `#D9342B` | `#C0392B` |
| `#E20707` | `#C0392B` |
| `rgba(217,52,43,` | `rgba(192,57,43,` |
| `rgba(226,7,7,` | `rgba(192,57,43,` |
| `#1F1F1F` | `#2B303A` |
| `#424242` | `#5B6472` |
| `#414445` | `#5B6472` |
| `#939393` | `#8A93A3` |
| `#AAAAAA` | `#C9CED4` |
| `#5c5c5c` | `#5B6472` |
| `rgba(31,31,31,` | `rgba(43,48,58,` |
| `rgba(170,170,170,` | `rgba(154,163,176,` |
| `rgba(204,204,204,.9)` | `rgba(18,37,68,.16)` |
| `#344557` | `#1B3358` |
| `#2a3745` | `#122544` |
| `rgba(52,69,87,` | `rgba(27,51,88,` |

## 2. Màu giữ nguyên — logo bên thứ ba

| Màu | Lý do |
|---|---|
| `#ED1C24` | logo Techcombank |
| `#00A19A` | logo napas247 |
| `#003DA5` | logo napas247 |

## 3. Thanh trên

Chữ `Homi365 ●` đổi thành ảnh logo chính thức (`assets/logo homi-01.png`), bấm vào về trang mục lục. Favicon dùng `assets/Icon_viewweb_final.jpg`.

Bỏ hai thành phần vốn là khung điều khiển của bản mockup, không thuộc sản phẩm:

- Dòng chú thích `WhiteCoat Việt Nam · 7 màn hình MVP`.
- Dãy nút chuyển màn `A1 · Thông tin nhận hàng … B4 · Kho hàng`. Việc chuyển màn giờ nằm ở `index.html`.

Vì thanh chỉ còn một phần tử, logo nâng lên 71px và đệm dọc nới từ 12px lên 16px — thanh cao 104px thay vì 65px. Mọi phép `calc(100vh - 65px)` trong mockup đã được sửa theo (3 chỗ) để màn quản trị không dư thanh cuộn.

Thêm nút **Đăng nhập Agent** ở góc phải thanh trên, chỉ trên 2 màn công khai A1 và A2 (trỏ sang `c1-login.html`). Không đặt ở C1 vì đang đứng sẵn ở đó, không đặt ở A3 vì đã đăng nhập, không đặt ở khung quản trị. Đây là thành phần mới so với mockup KH — cần nêu khi gửi.

Logo canh thẳng hàng với nội dung bên dưới: màn người mua và thành viên dùng chung khung 1160px canh giữa; màn quản trị canh theo mép trái các mục sidebar. Đây là thay đổi layout duy nhất của bản này, và chỉ ở thanh trên.

### 3b. Responsive

Mockup KH chỉ có bản desktop. Bổ sung `css/responsive.css` — **mọi quy tắc bố cục đều nằm trong media query**, nên từ 901px trở lên giao diện KH đã duyệt không đổi một pixel nào (ngoài media query chỉ có đúng một dòng `img{max-width:100%}`, ở desktop không ảnh nào chạm ngưỡng đó).

| Bề ngang | Thay đổi |
|---|---|
| ≤ 900px | A1 bỏ cột tóm tắt đơn 380px, xếp dọc · footer 1 cột · khung quản trị: cột điều hướng 220px thành dải nút ngang cuộn được · thẻ tổng hợp 4 cột → 2 |
| ≤ 720px | Nút *Đăng nhập thành viên HOMI365* xuống hàng riêng, rộng hết khung; logo thanh trên còn 40px |
| ≤ 640px | Cặp ô nhập trong form A1/A2 về 1 cột · thẻ tổng hợp về 1 cột · ngăn chi tiết quản trị rộng hết màn |
| ≤ 420px | Logo thanh trên còn 34px |

Bảng quản trị **vẫn cuộn ngang** trong khung của nó thay vì ép về một cột: 9–10 cột số liệu mà nén lại thì dính vào nhau, đọc còn khó hơn vuốt ngang.

Lưu ý kỹ thuật cho dev: markup KH không có class nào, style viết inline hết, nên các quy tắc phải nhắm bằng `[style*="…"]` kèm `!important`. Runtime của mockup ghi lại style qua `el.style.cssText` nên chuỗi bị trình duyệt chuẩn hoá (`1fr 1fr;gap:` → `1fr 1fr; gap: `); selector viết cả hai dạng. Khi dựng thật bằng React/Vue thì bỏ hết mẹo này, dùng class bình thường.

Đã kiểm tra ở 360 · 390 · 768 · 1024px trên cả 12 màn: không màn nào bị tràn ngang ngoài các khung cố ý cho cuộn.

## 4. Bỏ trường Quận/Huyện

Hàng địa chỉ trong form mua hàng (A1) và form đăng ký (A2) đi từ **3 ô** `Tỉnh/Thành phố · Quận/Huyện · Phường/Xã` xuống **2 ô** `Tỉnh/Thành phố · Phường/Xã`. Đã bỏ 2 ô, lưới đổi từ 3 cột sang 2 cột.

Đây là **thay đổi trường nhập liệu duy nhất** so với mockup KH — cần nêu rõ khi gửi, vì các trường còn lại đều giữ nguyên như đã duyệt. Lý do: từ 01/07/2025 Việt Nam bỏ cấp huyện, địa chỉ hành chính chỉ còn tỉnh/thành → phường/xã.

Kéo theo: dữ liệu địa chỉ lưu xuống chỉ còn 2 cấp — cần thống nhất với dev trước khi thiết kế bảng, và chốt xem đơn hàng cũ (nếu có dữ liệu chuyển đổi) xử lý cấp huyện thế nào.

## 5. Nền trang

Nền trang đổi sang `--warm-50` = `#FAF8F3` (lấy từ `prototype-v2/css/tokens.css`), thẻ và ô nhập giữ trắng `#FFFFFF` — tạo nhịp xen kẽ ấm / trắng thay vì trắng trên trắng.

| Màn | Trước | Sau |
|---|---|---|
| A1 · C1 | `rgba(170,170,170,.05)` | `#FAF8F3` |
| A3 | `#FFFFFF` | `#FAF8F3` |
| A2 · B2 · B3 · B4 | `#FFFFFF` | `#FAF8F3` |
| Thanh trên · thẻ · ô nhập | `#FFFFFF` | giữ nguyên |
| B1 đăng nhập quản trị | `--c3` navy | giữ nguyên |

Kéo theo: 30 thẻ trong mockup KH **chỉ khai báo viền, không khai báo nền** — trên nền trắng cũ thì không lộ, trên nền ấm sẽ bị chìm. Đã cho về trắng (A3 5 thẻ · B2/B3/B4 mỗi màn 8 · A2 1).

Cột biểu đồ hoa hồng đổi sang teal `#1BA3BE` để tách khỏi navy của nút và link — navy là màu hành động, teal là màu dữ liệu.

## 6. Thêm link bán hàng vào A3

Dashboard thành viên trong mockup KH **không có link bán hàng nào**. Agent rời màn "Kích hoạt thành công" (A2 bước 5) là mất đường lấy link, không có chỗ xem lại. Đã thêm thẻ **Link bán hàng của bạn** ngay dưới phần chào, gồm 1 link + nút copy, dùng lại đúng link và hàm `copyLink` sẵn có của A2 bước 5.

**Đã chốt 08/09: 2 link**, đúng theo requirement 8.1.C-4 — agent nhận cả hai ngay lúc kích hoạt (A2 bước 5) và xem lại được ở dashboard (A3), mỗi link một nút copy riêng:

| Link | Giá trị | Dùng để |
|---|---|---|
| Giới thiệu · ref_code | `homi365.vn/san-pham/CN02?aff_id=923983` | gán tuyến trên / tuyển thành viên |
| Mua hàng cá nhân · alias | `homi365.com.vn/NVA1111` | chia sẻ để khách mua trực tiếp |

`ref_code = 923983` là mã chính thức của agent. Alias sinh đúng cú pháp **8.1.C-4**: `Homi365.com.vn/[EEEE][PPPP]` — EEEE là chữ cái đầu (viết hoa, bỏ dấu) của mỗi từ trong họ tên, PPPP là 4 số cuối SĐT. *Nguyễn Văn A* · `0901111111` → `NVA1111`.

Còn treo — **hai link của admin ở màn B2 chưa khớp mô hình này.** B2 hiện hiện *link form* `portal.homi365.com.vn/TTB4123` và *link đăng nhập* `homi365.com.vn/dang-nhap/TTB4123`, cả hai dựng từ alias chứ không có link mua hàng lẫn ref_code. Cần chốt admin nhìn thấy những link nào của agent, và 4 dạng link này rốt cuộc là mấy thứ khác nhau. Prototype giữ nguyên phần B2 như mockup KH.

## 7. Tách hoa hồng theo trạng thái (A3)

Thẻ số dư trong mockup KH chỉ có **2 con số** — khả dụng và "đang chờ duyệt (đã khóa)"; "đã ghi nhận" nằm lẫn trong một dòng chữ nhỏ, "đã rút" nằm tận ô chỉ số phía trên. Đã tách thành **4 mục**:

| Mục | Giá trị mẫu |
|---|---|
| Đã ghi nhận | 6.000.000đ |
| Đang chờ duyệt · tạm giữ | 800.000đ |
| Đã rút | 1.200.000đ |
| **Số dư khả dụng** | **4.000.000đ** |

Số liệu mẫu khớp: `6.000.000 = 4.000.000 + 800.000 + 1.200.000`.

Bổ sung dòng giải thích cơ chế hold: yêu cầu rút ở trạng thái **chờ duyệt** hoặc **đã duyệt** bị tạm giữ và trừ khỏi số dư khả dụng, tới khi chi trả xong hoặc bị từ chối; từ chối thì hoàn lại khả dụng.

"Đã rút" hiển thị ở **2 nơi** — ô chỉ số phía trên (trường của mockup gốc) và thẻ hoa hồng này. **Đã chốt giữ cả hai** (BA quyết 08/09): ô chỉ số cho cái nhìn nhanh, thẻ hoa hồng cho quan hệ giữa 4 con số. Không phải lỗi trùng lặp.

## 8. Bổ sung màn Quản lý sản phẩm (B5)

Mockup KH không có màn này, dù requirement **7.7.1 Logic quản lý sản phẩm** là P0. Đã thêm màn `b5-products.html` trong khung quản trị, kèm mục **Quản lý sản phẩm** ở sidebar.

Nội dung: bảng sản phẩm với 3 cột theo đúng yêu cầu — **Tên · Hình ảnh · Mô tả** — cùng nút *Thêm sản phẩm* và nút *Sửa* trên từng dòng, cả hai mở cùng một hộp thoại 3 trường.

**Đã chốt 08–09/09** — phạm vi màn này đúng bằng 3 trường trên, không hơn: không quản lý giá, không quản lý gói, không có công tắc bật/tắt bán, mỗi sản phẩm **chỉ 1 ảnh**.

Danh sách chỉ có **1 sản phẩm CN02**, đúng theo **6.1.C-3** (*"cho 1 sản phẩm pilot (CN02)"*). Hai lựa chọn *Gói 1 năm 10.000.000đ* và *Gói nửa năm 6.000.000đ* ở màn mua hàng là **gói license của cùng sản phẩm đó**, không phải 2 sản phẩm — khớp với kho B4, nơi cả 1.200 thiết bị đều mang một dòng SKU `CN02-xxxx`.

## 9. Bổ sung Thêm hàng vào kho (B4)

Màn Quản lý kho hàng của mockup KH **chỉ xem, không nhập được hàng** — 1.200 mã trong bản demo là dữ liệu dựng sẵn. Đã thêm nút **+ Thêm hàng vào kho** cạnh nút xuất Excel, mở hộp thoại 2 trường theo yêu cầu: **Mã sản phẩm** và **Mã kích hoạt**. Hàng thêm vào mặc định ở trạng thái *Sẵn hàng*.

**Đã chốt 08/09** — thêm nút **Import hàng loạt** bên cạnh, mở hộp thoại cho chọn file Excel/CSV hoặc dán danh sách, mỗi dòng `mã sản phẩm, mã kích hoạt`.

**Chặn trùng ở cả hai đường nhập:**

- Nhập tay: trùng mã kích hoạt hoặc mã sản phẩm thì báo lỗi ngay trong hộp thoại, không cho lưu.
- Import: xử lý **từng phần** — dòng nào hợp lệ thì nhận, dòng nào trùng hoặc thiếu dữ liệu thì bỏ qua. Kết thúc hiện bảng tổng kết `tổng dòng / đã nhập / bỏ qua` kèm danh sách dòng bị bỏ và lý do.
- Chặn trùng tính cả với kho hiện có **lẫn trùng nhau trong chính danh sách đang dán** — dán 2 dòng cùng mã thì chỉ nhận dòng đầu.

## 10. Bổ sung màn Quản lý đơn hàng (B6)

Mockup KH **không có màn đơn hàng nào**, dù luồng mua của chính mockup là chuyển khoản + khách tự tải ảnh bill lên. Nghĩa là tiền về tài khoản nhưng không ai xác nhận được, đơn treo vĩnh viễn và khách không bao giờ nhận mã kích hoạt. Đây là mắt xích đứt, không phải tính năng phụ.

Màn `b6-orders.html` gồm: 4 ô thống kê (chờ đối soát · chờ Head Admin · đã thanh toán · doanh thu đã đối soát), bộ lọc theo trạng thái, ô tìm theo mã đơn / tên / SĐT, bảng đơn, và ngăn chi tiết bên phải với thông tin khách, thông tin đơn, ảnh chuyển khoản, lịch sử xử lý và nút hành động.

⚠ Bản 08/09 làm duyệt 2 cấp cho đơn hàng. **Đã bỏ ngày 09/09** — xem mục 13 để biết mô hình duyệt cuối cùng.

**Đã chốt 08/09:**

- **Tách vai theo bước, không tách theo người.** Specialist làm bước 1; bước 2 thuộc về Head Admin, và Head Admin làm luôn việc kích hoạt tài khoản. Khác luồng rút tiền ở chỗ rút tiền cấm cùng một người làm cả hai bước, còn ở đây phân quyền theo vai là đủ.
- **Mã kích hoạt do Head Admin chọn tay** từ danh sách thả xuống, chỉ liệt kê mã đang ở trạng thái *Sẵn hàng* trong kho (B4). Không chọn thì không xác nhận được. Xác nhận xong mã đó chuyển sang *Đã gán đơn hàng* và ghi vào lịch sử của cả đơn lẫn thiết bị.
- **Đơn bị từ chối là chấm dứt.** Phase 1 không mở lại đơn cũ; khách muốn mua thì đặt đơn mới qua link giới thiệu. Ngăn chi tiết hiển thị rõ dòng này để admin khỏi đi tìm nút mở lại.

- **Hoàn tiền nằm ngoài hệ thống.** Đơn bị từ chối nhưng tiền đã về tài khoản thì bộ phận kế toán xử lý thủ công bên ngoài; hệ thống không có màn hoàn tiền, không lưu trạng thái hoàn tiền, không đối soát khoản hoàn. Dev không cần làm gì cho phần này.

## 11. Bổ sung theo rà soát requirement 09/09

Nguồn: `docs/GAP-Requirement-vs-prototype-v3.md`. Sáu mục nhóm B đã làm xong:

| Mã YC | Bổ sung |
|---|---|
| **7.9.1** | Màn **B7 · Tài khoản admin** — danh sách 5 tài khoản mẫu, cột vai trò (Head Admin / Admin Specialist), khoá–mở khoá, thêm–sửa tài khoản, kèm bảng giải thích quyền của từng vai. |
| **7.1.3** | Đăng nhập bằng SĐT **đã mua hàng nhưng chưa là agent** → tự chuyển sang màn đăng ký và autofill từ đơn cũ (khớp luôn 7.2.8). Thêm dòng gợi ý ngay dưới nút Đăng nhập. |
| **7.5.2** | Thêm khối **Lịch sử thăng/giáng hạng** vào ngăn chi tiết thành viên. |
| **7.5.2** | Cây tuyến mở rộng lên **3 cấp** F0 → F1 → F2. |
| **7.3.2** | Dashboard thêm bộ chọn **Hôm nay / Tuần này / Tháng này / Tất cả**, số Tổng đơn hàng đổi theo. |
| **7.9.4** | Nhãn trạng thái duyệt hiện rõ số lượt: **Chờ duyệt (0/2)** · **Chờ Head Admin (1/2)** · **Đã duyệt (2/2)**. |

Chưa làm, chờ KH quyết — xem mục A3 của file rà soát: theo **7.9.2** agent đăng ký xong phải ở trạng thái *Chờ duyệt* chứ không vào thẳng dashboard như mockup KH. Sửa chỗ này kéo theo cả màn A2, luồng duyệt và cách tính hoa hồng lúc chờ, nên chưa đụng vào.

## 12. Sửa theo rà soát bản deploy 09/09

Nguồn: `docs/AUDIT-deploy-vs-requirement.md`.

| Mã YC | Đã sửa |
|---|---|
| **7.2.2** | **Autofill khi đăng ký ngay sau khi mua.** Nút *Đăng ký thành viên* ở modal thanh toán thành công giờ mang toàn bộ thông tin người mua sang màn A2 (họ tên, SĐT, email, CCCD, địa chỉ, ngày sinh, số tài khoản, mã đơn, hạng tuyến trên). Trước đó form mở ra trống trơn — lỗi phát sinh do tách mỗi màn một file. |
| **7.9.1** | **Chặn Admin Specialist khỏi màn Tài khoản admin.** Mục *Tài khoản admin* biến mất khỏi sidebar khi đang ở vai Specialist; vào thẳng URL thì ra màn **403**. |
| **7.3.3** | Thêm dòng **còn thiếu bao nhiêu đơn để lên hạng kế tiếp** ngay dưới ô *Hạng hiện tại*. |
| **7.3.2** | Thêm mốc **Khoảng ngày…** mở ra 2 ô chọn ngày và nút Áp dụng, cạnh 4 mốc có sẵn. |
| **7.5.2** | Cây tuyến **3 cấp** F0 → F1 → F2 giờ mới thật sự chạy — bản vá dữ liệu trước đó đặt nhầm vào nhóm xử lý markup nên chưa từng có hiệu lực. Tiêu đề đổi thành *Sơ đồ tuyến dưới (3 cấp)*. |
| — | Thay hết **Medigo** còn sót thành **HOMI365** (điều khoản T&C, câu chúc mừng ở A2, lời chào ở A3, tiêu đề đăng nhập quản trị). |
| — | Sửa nhãn **Bước 1/3 → Bước 1/5** ở màn đăng ký cho khớp số bước thật. |

### Ba điểm đã chốt 09/09 — requirement phải sửa theo

Cả ba quyết định đều **giữ nguyên hành vi prototype**, nhưng **trái với Acceptance Criteria trong sheet**. Không sửa sheet thì dev đọc spec sẽ code ra thứ khác với bản KH đã duyệt.

**1. Duyệt 2 lớp tách theo VAI TRÒ** (Specialist bước 1 · Head Admin bước 2). Cần sửa 3 dòng:

- `7.9.2 AC` đang ghi *"lượt 1: bất kỳ Admin Specialist hoặc Head Admin nào"* và *"lượt 2 phải do người KHÁC"* → viết lại thành tách theo vai trò.
- `7.9.3 AC` đang ghi *"2 người khác nhau, hoặc Head Admin tự chốt"* → bỏ vế Head Admin tự chốt.
- `7.9.4 AC` đang ghi *"nút Xác nhận của chính người đó bị vô hiệu hoá"* → đổi thành khoá theo vai trò.

Rủi ro vận hành cần KH biết trước: **Specialist nghỉ là mọi thứ nghẽn ở bước 1**, kể cả khi Head Admin đang trực. Requirement bản cũ thiết kế để tránh đúng chuyện này. Nếu KH muốn chặn rủi ro mà vẫn giữ tách vai trò, cách gọn nhất là thêm một câu: *Head Admin được phép làm thay bước 1 khi cần*.

**2. Tuyến trên hạng Đồng → báo lỗi** (không giấu lời mời). `7.2.1 AC` đang ghi ngược lại (*"không hiển thị thông báo cho đăng ký thành viên, mà chỉ báo đơn hàng thành công"*) → phải viết lại cho khớp dòng *Logic điều kiện đăng ký thành viên mới*.

Đã chỉnh prototype: báo lỗi **ngay khi bấm** nút Đăng ký thành viên, thay vì để khách điền hết 5 bước rồi mới chặn ở bước cuối.

**3. Agent sau đăng ký vào thẳng dashboard**, không qua *Chờ duyệt (0/2)*. `7.9.2` đang bắt hồ sơ đăng ký phải đủ 2 lượt xác nhận mới kích hoạt → phải bỏ phần đăng ký ra khỏi phạm vi duyệt 2 lớp, chỉ giữ cho rút tiền và đơn hàng.

**Cơ chế tạm giữ hoa hồng — chốt 09/09.** Đăng ký xong là **active ngay**, nhưng kích hoạt của admin mới mở khoá phần tiền:

| | Sau khi đăng ký | Sau khi admin kích hoạt |
|---|---|---|
| Link giới thiệu & link mua hàng | có, dùng được ngay | có |
| Bán hàng, ghi nhận đơn & tuyến dưới | bình thường | bình thường |
| Hoa hồng phát sinh | **tạm giữ** | được giải phóng |
| Điểm tích luỹ | **không cộng** (= 0) | cộng đủ, kể cả phần trước đó |
| Rút tiền | **không được** | được |

Đã dựng vào prototype:

- A2 bước 5: đổi *"Kích hoạt thành công · đã chính thức là seller"* → **"Đăng ký thành công"** kèm câu giải thích hoa hồng bị giữ.
- A3 agent mới: thay banner chào mừng bằng khối **CHỜ KÍCH HOẠT** — nêu rõ bán được ngay nhưng hoa hồng tạm giữ, chưa tính điểm, chưa rút được; hiện số **hoa hồng đang tạm giữ** và **số dư khả dụng 0đ**; nút rút tiền để trạng thái khoá.
- Điểm tích luỹ của agent chưa kích hoạt đổi từ 80 về **0**.

Nhờ vậy màn duyệt hồ sơ ở B2 vẫn có lý do tồn tại: nó là chỗ mở khoá tiền, không phải chỗ cho phép bán hàng.

**Chốt 09/09: cộng dồn toàn bộ về quá khứ.** Khi admin kích hoạt, hoa hồng đã tạm giữ và điểm tích luỹ được tính **từ đơn đầu tiên**, không phải từ thời điểm kích hoạt. Hộp xác nhận duyệt ở B2 đã ghi rõ điều này để admin biết mình đang mở khoá cái gì.

Kéo theo cho dev: bản ghi hoa hồng phải tồn tại **ngay khi đơn thanh toán**, mang một cờ *đang giữ*, chứ không phải sinh ra lúc kích hoạt — nếu sinh lúc kích hoạt thì không còn dữ liệu quá khứ để cộng dồn. Điểm tích luỹ cũng vậy.

## 13. Mô hình duyệt — bản chốt cuối 09/09

Mô hình duyệt đã đổi ba lần trong hai ngày. Đây là bản cuối, **ghi đè mọi mô tả duyệt ở các mục trên**:

| Luồng | Số lượt duyệt | Ai làm | Ghi chú |
|---|---|---|---|
| **Đơn hàng** (B6) | **1** | Admin bất kỳ (Specialist hoặc Head) | Xác nhận tiền về + chọn mã kích hoạt từ kho → đơn `Đã thanh toán`, mã sang `Đã gán đơn hàng`, hệ thống gửi email kèm mã cho khách ngay |
| **Thành viên** (B2) | **1** | Chỉ Manager / Head Admin | Chỉ duyệt được khi đơn của thành viên đó đã xác nhận thanh toán. Duyệt xong mở khoá điểm và ưu đãi đang tạm giữ |
| **Rút tiền** (B3) | **2** | Specialist bước 1, Head Admin bước 2 | Giữ nguyên duyệt 2 lượt — chốt 09/09, khác hai luồng trên |

Vòng đời hồ sơ thành viên: `Chờ xác nhận thanh toán` → `Chờ Manager duyệt` → `Đang hoạt động`. Bước một không nằm ở màn Thành viên mà ở màn Đơn hàng — đây là điểm dễ hiểu nhầm nhất, cần nói rõ khi bàn giao cho dev.

Kỹ thuật: hai trạng thái `pending` và `specialist_approved` dùng chung giữa thành viên và rút tiền, nhưng nhãn hiển thị khác nhau (thành viên có bảng nhãn riêng). Khi dev thiết kế bảng nên tách hẳn hai bộ trạng thái, đừng dùng chung enum.

## 14. Gỡ ô tra cứu đơn theo số điện thoại (11/09)

Mockup KH có một hộp thoại **Nhập số điện thoại → Tra cứu đơn hàng** trên A1. Từ khi luồng đăng nhập đổi (C1 tự đối chiếu SĐT rồi mở hộp thoại kèm sẵn kết quả), **không còn nút nào trên giao diện mở nhánh gõ số để tra** — nó chỉ còn vào được bằng cách gõ tay `a1-buy.html#tra-cuu-don`.

Đã gỡ hẳn: bỏ ô nhập, bỏ nút *Tra cứu đơn hàng*, bỏ khối modal khỏi A1 cùng mục `#tra-cuu-don` trong `index.html`. Phần thẻ **Đơn hàng tìm thấy** giữ nguyên và vẫn chạy trên C1.

Lý do không chỉ là dọn mã chết: nhánh đó nhận **một số điện thoại bất kỳ, không xác thực gì**, rồi trả về họ tên, email, số CCCD và địa chỉ của chủ đơn. Deploy lên là ai biết URL cũng tra được dữ liệu cá nhân của người khác. Nếu sau này KH muốn có tính năng tra cứu đơn thật thì phải kèm OTP về đúng số đó, và chỉ trả mã đơn + trạng thái, không trả thông tin định danh.

Kèm theo, sửa một lỗi lộ ra khi rà: modal **tuyến trên bị chặn** trước đây chỉ được nhúng vào A1, trong khi nhánh gọi nó (`lookupContinue`, khi người giới thiệu hạng Copper) lại nằm ở C1 — bấm xong không hiện gì. Đã chuyển khối này sang C1.

Build in cảnh báo `ô tra cứu SĐT còn sót` nếu bản vá gỡ markup không khớp neo, vì bản vá markup im lặng khi trượt.

## 15. Sửa hàng tiêu đề bảng Kho hàng (15/09)

Bảng kho ở B4 có **10 cột dữ liệu nhưng hàng tiêu đề chỉ có 7 ô** — ba nhãn *Ngày kích hoạt · Ngày hết hiệu lực · Mã vận đơn* bị thiếu, kéo theo nhãn *Trạng thái* nằm lệch ba cột so với ô trạng thái thật.

Nguyên nhân: bản vá thêm cột neo vào chuỗi `<div>Seller</div>`, nhưng bản vá đổi *Seller → Thành viên* đứng trước nó trong danh sách. Tới lượt bản vá thêm cột thì neo đã biến mất, `str.replace` không tìm thấy gì và **bỏ qua không báo lỗi**. Hàng dữ liệu vẫn được thêm cột (neo khác, không bị đụng) nên bảng lệch.

Đã sửa neo và bổ sung bộ soát: build giờ đếm bản vá markup nào không khớp ở bất kỳ khối nào rồi in cảnh báo kèm 60 ký tự đầu của neo. Dòng `bản vá markup: n/n khớp hết` là bình thường; thấy ⚠ thì có neo bị hỏng, phải xem lại trước khi gửi.

Dev lưu ý: đây là hạn chế của cách dựng bản mẫu (vá chuỗi trên markup của KH), không phải vấn đề nghiệp vụ. Bản dựng thật không có chuyện này.

## 16. Gửi yêu cầu thanh toán — chống đơn trùng & lỗi mạng (16/09)

Mockup KH bấm **Thanh toán** là mở ngay mã QR, không có trạng thái chờ. Thực tế gọi cổng thanh toán mất vài giây và có thể hỏng giữa chừng, nên bổ sung ba trạng thái cho nút:

| Trạng thái | Nút | Hiển thị thêm |
|---|---|---|
| `idle` | *Thanh toán*, bấm được | — |
| `sending` | *Đang gửi yêu cầu…*, **khoá** | — |
| `timeout` | *Gửi lại yêu cầu thanh toán*, bấm được | Dải đỏ *Lỗi đường truyền, vui lòng gửi lại yêu cầu* |

Đây là **thông báo duy nhất** của luồng này — chốt 16/09. Trường hợp bấm lại khi đơn đã tạo **không hiện thông báo**: hệ thống lặng lẽ mở lại mã thanh toán của đúng đơn cũ, người mua không cần biết chuyện gì vừa xảy ra. Chống trùng vẫn phải làm đủ ở tầng dưới, chỉ là không nói ra trên giao diện.

**Ba quy tắc dev phải làm đúng, không chỉ là giao diện:**

1. **Ngưỡng chờ 5 giây.** Quá 5s chưa nhận được phản hồi mở mã thanh toán thì chuyển nút sang `timeout`. Bản mẫu để 1,2s cho dễ xem, con số thật là 5s.
2. **Giữ nguyên form.** Gửi lại không được xoá hay nạp lại bất kỳ trường nào người mua đã nhập.
3. **Khoá chống trùng (idempotency key).** Mã đơn sinh **một lần** rồi dùng lại cho mọi lần gửi lại; server thấy khoá cũ thì trả về đơn cũ chứ không tạo đơn mới. Không có khoá này thì người mua mạng yếu bấm ba lần là ba đơn, ba mã kích hoạt bị giữ.

Trong lúc `sending` nút bị khoá hẳn — đó là lớp chặn bấm dồn thứ nhất; khoá chống trùng là lớp thứ hai, phòng khi người dùng tải lại trang rồi bấm tiếp.

Xem thử: `a1-buy.html#loi-duong-truyen`. Bấm *Gửi lại yêu cầu thanh toán* sẽ chạy hết luồng và mở mã QR bình thường.

Chưa làm, cần KH chốt: sau bao nhiêu lần gửi lại liên tiếp thì dừng và mời liên hệ hotline, và đơn đã tạo nhưng chưa thanh toán thì giữ hiệu lực bao lâu trước khi tự huỷ.

## 17. Cập nhật cấp thành viên (17/09)

Trước đây cấp chỉ do hệ thống gán theo doanh số, không ai sửa được. Bổ sung luồng cho phép sửa tay.

**Chốt 17/09: việc trình – xét – duyệt làm NGOÀI hệ thống** (email hoặc biểu mẫu nội bộ). Hệ thống không ra quyết định, chỉ ghi nhận quyết định đã có và áp dụng nó. Bản dựng trước đó có luồng *Admin đề nghị → Head duyệt* ngay trong hệ thống — đã gỡ bỏ.

| Bước | Ở đâu | Ai làm | Ra cái gì |
|---|---|---|---|
| 1. Trình tăng cấp | Ngoài | Người phụ trách | Phiếu trình: thành viên, cấp hiện tại, cấp đề xuất, lý do, số liệu |
| 2. Review nội dung | Ngoài | Người duyệt | Ý kiến, yêu cầu bổ sung |
| 3. Quyết định | Ngoài | Người duyệt | Duyệt · Sửa rồi duyệt · Từ chối. Kết quả là phiếu/email chốt có **mã phiếu, người duyệt, ngày duyệt, cấp cuối cùng** |
| 4. Cập nhật | **Trong** | Admin | Mở hồ sơ → *Cập nhật cấp* → chọn cấp đã duyệt + nhập minh chứng → Lưu |
| 5. Áp dụng | **Trong** | Hệ thống | Cấp mới hiệu lực ngay, ghi lịch sử. Không duyệt lại |

**Bị từ chối thì không thao tác gì trong hệ thống** — chốt 17/09: ngoài core xem như chưa từng đề xuất, nên hệ thống không ghi nhận gì cả. Hệ quả cần biết: nhìn vào hồ sơ sẽ không thấy dấu vết đã từng trình rồi bị bác; muốn tra thì phải tìm ở nguồn ngoài.

**Quyền cập nhật: Admin** — chốt 17/09. Admin tự cập nhật và tự đính kèm minh chứng, không cần Head thao tác. Head vẫn làm được vì là vai cao hơn.

**Giao diện.** Ngăn chi tiết thành viên (B2) có nút **Cập nhật cấp**, kèm dòng nhắc *việc trình và duyệt làm ngoài hệ thống*. Hộp thoại gồm: danh sách 6 cấp, và **ba trường minh chứng bắt buộc** — số phiếu / mã email, ngày duyệt, người duyệt — cộng ô **tải file minh chứng** (ảnh, PDF, hoặc file email `.eml`/`.msg`). Thiếu một trong ba trường bắt buộc thì nút *Lưu & áp dụng* vẫn xám; file không bắt buộc.

Không có ô nhập lý do — chốt 17/09. Lý do nằm trong phiếu duyệt ngoài, gõ lại vào đây chỉ sinh ra một bản chép tay có thể sai khác với bản gốc.

Ba trường kia chỉ là số hiệu do người nhập gõ vào — **file mới là bằng chứng thật**. Khuyến nghị KH quy định bắt buộc đính kèm file trong quy chế nội bộ, kể cả khi hệ thống không chặn. Bản mẫu chỉ giữ tên file; bản thật phải tải lên kho lưu trữ, gắn với bản ghi và không cho xoá.

**Hai ràng buộc khi chọn cấp.** Cấp vi phạm bị làm mờ kèm dòng giải thích:

- **Trần:** không cao hơn cấp của người giới thiệu trực tiếp.
- **Sàn:** không thấp hơn cấp của tuyến dưới trực tiếp. Ràng buộc này KH chưa nêu nhưng bắt buộc phải có — vì chỉ sửa cấp của riêng một người, hạ người trên xuống cũng làm tuyến dưới vượt tuyến trên, đúng cái điều mà trần đang cấm.

Ràng buộc vẫn áp **kể cả khi phiếu ngoài đã duyệt**. Gặp trường hợp bị chặn thì Admin không tự phá rào, phải trình lại bên ngoài. Cần nói rõ điều này với bộ phận duyệt, nếu không họ sẽ duyệt ra thứ hệ thống không nhận.

Sửa cấp **chỉ đổi đúng thành viên đó**, tuyến dưới giữ nguyên.

**Lưu vết:** mỗi lượt ghi cấp cũ → cấp mới, mã phiếu, ngày duyệt, người duyệt, tên file minh chứng, thời điểm cập nhật. Hiện ở mục *Lịch sử điều chỉnh cấp* trong hồ sơ.

Xem thử: `b2-members.html#cap-nhat-cap` và `#da-cap-nhat-cap`.

**Rủi ro khi đưa duyệt ra ngoài — cần bù lại bằng quy trình:**

1. **Mất dấu vết ai duyệt.** Quyết định nằm trong hộp thư cá nhân. Ba trường minh chứng là sợi dây duy nhất nối số liệu trong hệ thống với phiếu ngoài — vì vậy để bắt buộc.
2. **Không còn cơ chế hai người.** Trước phải Admin trình + Head duyệt mới đổi được cấp; giờ một Admin gõ là xong. Đề xuất bù: log chỉ thêm, không sửa/xoá, và định kỳ xuất báo cáo các lượt đổi cấp để đối chiếu với phiếu ngoài.

**Còn chờ KH chốt:**

1. Hướng của ràng buộc — em hiểu là *tuyến dưới không được vượt tuyến trên*; nếu KH muốn ngược lại thì phải đảo cả trần lẫn sàn.
2. Có hồi tố không — đơn đã chốt theo cấp cũ có tính lại ưu đãi, hay chỉ áp cấp mới từ lúc cập nhật.

Hai câu còn lại đã chốt 17/09, xem ở trên: không ghi nhận lượt bị từ chối; Admin là người cập nhật.

## 18. Bổ sung màn Nhật ký hệ thống (B8) — 17/09

Màn mới, **phạm vi toàn hệ thống**, không riêng phân hệ nào. Hai tab:

**Tab 1 — Thay đổi dữ liệu.** 9 cột: thời điểm · người thực hiện (kèm vai) · phân hệ · đối tượng · hành động · giá trị trước · giá trị sau · minh chứng · địa chỉ IP. Lọc theo phân hệ, hành động, khoảng ngày, và tìm theo người thực hiện / đối tượng / mã phiếu.

Sáu phân hệ được ghi: Thành viên · Đơn hàng · Kho hàng · Sản phẩm · Rút tiền · Tài khoản admin. Sáu nhóm hành động: Tạo mới · Cập nhật · Duyệt · Từ chối · Khoá/mở khoá · Tải file lên. Cả thao tác của **hệ thống tự động** (gán mã kích hoạt khi xác nhận đơn) lẫn của **thành viên** (đăng ký, chấp thuận T&C) đều vào nhật ký, không chỉ thao tác của admin.

**Tab 2 — File đã tải lên.** Tên file · loại · gắn với đối tượng nào · người tải · thời điểm · dung lượng · nút tải về. Gom mọi file trong hệ thống: ảnh CCCD, phiếu duyệt điều chỉnh cấp, file import kho, ảnh sản phẩm, uỷ nhiệm chi.

**Hai nguyên tắc ghi rõ trên màn:**

- Nhật ký **chỉ ghi thêm** — không sửa, không xoá, kể cả Head.
- File đã tải lên **không xoá được**. Nộp nhầm thì tải bản đúng lên rồi ghi chú, bản cũ vẫn giữ.

Không có hai điều này thì nhật ký vô nghĩa: ai xoá được dấu vết thì dấu vết không còn là bằng chứng.

Xem thử: `b8-audit-log.html` và `#file`.

**Cần chốt với dev:**

1. **Thời gian lưu.** Giữ bao lâu rồi chuyển sang lưu trữ lạnh? Nhật ký toàn hệ thống phình rất nhanh.
2. **Ai được xem.** Bản mẫu cho cả Admin lẫn Head. Nhật ký chứa IP và thao tác của mọi người — KH cân nhắc có nên giới hạn ở Head không.
3. Dữ liệu trong bản mẫu là **dựng sẵn**, không nối với thao tác thật trên các màn khác — bản thật backend ghi vào bảng `audit_log` ngay trong cùng giao dịch với thay đổi dữ liệu, không ghi sau bằng job riêng.

## 19. Cập nhật sau UAT 02/10 — đợt 06/10

Nguồn: sheet `Plan Update` trong Google Sheet `[Homi] - Change Request`. Đợt này chỉ làm các mục **không bị chặn** bởi câu hỏi H2–H5. Toàn bộ bản vá nằm ở `tools/update_uat0210.py`, neo không khớp là dừng build.

| Mục | Màn | Thay đổi | Xem thử |
|---|---|---|---|
| 1 | A1, C1 | Thêm **bước nhập số điện thoại** trước form mua hàng. Số đã có tài khoản thì hiện khối gợi ý với hai nút Đăng nhập / Bỏ qua và tự điền; số mới vào thẳng form, điền sẵn số vừa nhập. Hệ thống chỉ trả lời có hay chưa có tài khoản. Đăng nhập đi qua C1 rồi **quay lại form mua hàng** (đã chốt). | `a1-buy.html`, `#sdt-da-co`, `#form`, `c1-login.html#tu-mua-hang` |
| 2 | A1 | Sau đăng nhập form **tự điền theo đơn gần nhất**, sửa trực tiếp được. (08/10: bỏ dòng nhắc "Đã điền theo đơn…" và nút Mua cho người khác — không có trong yêu cầu KH.) | `#form-tu-dien` |
| 3 | A1 | Ô Ngày sinh kiểm tra tuổi **18–100**, báo lỗi ngay dưới ô và khoá nút Thanh toán. Chỉ xét khi đã gõ đủ `dd/mm/yyyy`. | `#loi-tuoi` |
| 4 | A1 | Bỏ dấu (*) ở Tỉnh/Thành phố và Phường/Xã. Nút Thanh toán vốn không phụ thuộc hai ô này nên không có điều kiện nào phải gỡ. Bổ sung cùng ngày: ba ô **Ngân hàng, Số tài khoản, Tên chủ tài khoản** ở form mua hàng cũng bỏ dấu (*) — vẫn giữ ô, chỉ không bắt buộc nhập. Form đăng ký thành viên A2 giữ nguyên bắt buộc. | `#form` |
| 5 | A1 | Ô đồng ý chính sách **mờ và khoá**, bấm một trong hai link chính sách thì mở. Hai link đổi sang mở tab mới — trước đây mở cùng tab, bấm là mất dữ liệu đang nhập. Dùng lại cơ chế của A2 bước 4 trong `js/otp.js`. | `#form` |
| 6 | A2, A3 | **Bỏ trạng thái chờ kích hoạt.** A2 bước 5 và nút bước 4 không còn chữ "kích hoạt", "tạm giữ". A3 gỡ banner CHỜ KÍCH HOẠT; khối số dư và nút đổi điểm hiện cho cả thành viên mới, số dư là số thật. Đơn chưa duyệt hiện dòng "điểm được ghi nhận sau khi đơn được duyệt" (H1 đã chốt). Sửa câu tương ứng ở Điều khoản mục 2. | `a2-register.html#buoc-5`, `a3-dashboard.html` |
| 7 | mọi màn | Đổi toàn bộ **"rút tiền" → "đổi điểm"**: tiêu đề, nút, cột bảng, bộ lọc, sidebar, phân hệ trong nhật ký, tên trạng thái ở `index.html`. Hash `#rut-tien` đổi thành `#doi-diem`. | — |
| 10 | B3 | Nút **Xuất danh sách chi trả** mở hộp thoại chọn kỳ, liệt kê 5 cột của file, xem trước các dòng và tổng chi của kỳ. | `b3-withdrawals.html#xuat-chi-tra` |
| 11 | B3, B8 | Hai trạng thái mới **Chi không thành công** và **Đã hoàn điểm**, có bộ lọc riêng. Yêu cầu đã duyệt có thêm nút ghi nhận ngân hàng trả về; sau đó nút **Hoàn điểm** với lý do bắt buộc và dòng nhắc hệ thống gửi email. B8 thêm hành động Hoàn điểm. | `#bao-chi-loi`, `#chi-khong-thanh-cong`, `#hoan-diem`, `#da-hoan-diem` |
| 22 | B2, B8 | Form sửa hồ sơ có dòng nhắc **hệ thống sẽ gửi email báo thay đổi**; đổi email thì nêu cả địa chỉ cũ và mới. Lưu xong hiện dòng xác nhận. B8 thêm dòng mẫu. | `b2-members.html#sua-ho-so`, `#sua-ho-so-doi-email` |

**Hai mục không có gì phải sửa trên giao diện:**

- **Mục 19** (bỏ từ "tách nhánh"): prototype không dùng từ này ở màn nào.
- **Mục 16** (email khi thăng/hạ cấp): không có giao diện, xem danh sách email dưới đây.

**Email hệ thống phát sinh từ đợt này** — nội dung do team HOMI365 biên soạn:

| Email | Gửi cho | Khi nào | Mục |
|---|---|---|---|
| Báo thăng / hạ cấp | Thành viên | Mỗi khi cấp thay đổi | 16 |
| Báo tài khoản nhận tiền có vấn đề | Thành viên | Admin bấm Hoàn điểm | 11 |
| Báo hồ sơ được sửa, nêu giá trị mới | Thành viên (đổi email thì cả địa chỉ cũ lẫn mới) | Admin lưu hồ sơ | 22 |

**Giả định của bản mẫu — cần xác nhận khi làm thật:**

1. **Thế nào là "đã có tài khoản" (mục 1).** Bản mẫu coi là số đã đăng ký thành viên, vì chỉ thành viên mới đăng nhập được. Khách từng mua nhưng chưa đăng ký thành viên được coi như khách mới.
2. **Mua cho người khác (mục 2)** xoá hết phần tự điền, kể cả số điện thoại và tài khoản ngân hàng. Ai là người giới thiệu của đơn mua lần 2 trở đi đang chờ trả lời câu hỏi H5 ở sheet Change Request.
3. **Chi không thành công (mục 11)** được ghi nhận từ trạng thái Đã duyệt, trước khi đánh dấu đã chi trả. Nếu ngân hàng trả về sau khi đã đánh dấu thì cần thêm nhánh từ Đã chi trả.
4. **Cột của file chi trả (mục 10)** là 5 cột theo sheet; danh sách cuối cùng còn chờ phía HOMI365 xác nhận.
5. **Nội dung chuyển khoản** ở chi tiết yêu cầu đổi từ `Rut khoan thuong…` sang `Doi diem thuong…` cho khớp mục 7.
6. **Điều khoản mục 2** (bước 4 đăng ký và trang chính sách) đã sửa một câu cho khớp mục 6 — cần Pháp lý đọc lại.

**Chưa làm, chờ khách hàng:** mục 8, 9 (H2, H3) · 12, 13, 14 (màn đề xuất thăng/hạ cấp) · 15, 20, 21 (H4) · 17, 18 (H5) · 23 (xác nhận đảo quyết định về B5).

**Còn lệch, nằm ngoài phạm vi đợt này:** ngăn chi tiết thành viên ở B2 và hộp thoại Head duyệt hồ sơ vẫn ghi "ưu đãi đang tạm giữ", "kích hoạt". Sau mục 6 các câu này không còn đúng, nhưng ý nghĩa mới của bước Head duyệt hồ sơ chưa được chốt nên chưa sửa.

## 20. Cập nhật theo phản hồi KH ở sheet Change Request — đợt 08/10

KH đã trả lời các câu hỏi H1–H5 và chốt từng mục; đợt này làm hết, kể cả các thay đổi lớn. Bản vá vẫn nằm trong `tools/update_uat0210.py` (mục 7), neo không khớp là dừng build.

| Mục | Màn | Thay đổi | Xem thử |
|---|---|---|---|
| 1 (làm lại) | A1 | Bỏ màn nhập SĐT riêng của đợt 06/10. Vào trang thấy **form mua hàng nhưng bị khoá** (mờ, không bấm được); ô nhập SĐT nằm ở **đầu trang**. Xác định xong SĐT thì form mở khoá, đầu trang thu lại thành một dòng có nút Đổi số. | `a1-buy.html`, `#sdt-da-co`, `#form` |
| 5 (làm lại) | A1 | Không mở khoá bằng bấm link nữa. Form hiện **khung nội dung chính sách** cuộn được; khách **kéo xuống đọc hết** mới tick được ô đồng ý. Link bản đầy đủ vẫn mở tab mới nhưng không mở khoá. | `#form` |
| 8 | A3 | Thẻ **Yêu cầu đổi điểm kỳ 09/2026** dưới nút tạo yêu cầu: trạng thái, nút **Huỷ yêu cầu** + hộp xác nhận. Gửi / huỷ được tới 23:59 ngày liền trước ngày cuối tháng (Chính sách ưu đãi thành viên mục 4, chốt 08/10); ngày cuối tháng khoá sổ, nút mờ kèm giải thích. Đang có yêu cầu thì khoá nút tạo mới. | `a3-dashboard.html#co-yeu-cau`, `#huy-yeu-cau`, `#da-khoa-so` |
| 9 | B3 | **Đảo ngược mô hình duyệt 2 lớp**: bỏ bước Head, bỏ trạng thái Chờ Head. Luồng mới: Chờ duyệt → Admin duyệt → Đã duyệt → xuất file → ngân hàng chi → **tải lên file kết quả thanh toán** → Thanh toán thành công / Chi không thành công. Có ô chọn từng dòng, **Duyệt đã chọn** và **Duyệt tất cả Chờ duyệt** (H2). Không còn nhập mã giao dịch từng lệnh, không còn nút đánh dấu đã chi trả bằng tay. | `b3-withdrawals.html`, `#duyet-hang-loat`, `#tai-ket-qua` |
| 10 | B3 | Hộp thoại xuất danh sách chi trả lấy các yêu cầu **Đã duyệt** (bỏ điều kiện duyệt đủ 2 bước). | `#xuat-chi-tra` |
| 11 | B3 | Chi không thành công giờ sinh ra từ file kết quả (yêu cầu Đã duyệt không có trong file). Hoàn điểm giữ nguyên: lý do bắt buộc, gửi email, ghi nhật ký. Thêm trạng thái **Thành viên đã huỷ** cho mục 8. | `#chi-khong-thanh-cong`, `#hoan-diem`, `#thanh-vien-huy` |
| 12, 13, 14, 17, 18 | **B9 (màn mới)** | Màn **Xét thăng / hạ cấp**: danh sách đề xuất cuối kỳ (cấp hiện tại, gói xét cấp, gói tháng này đã quy đổi, cấp đề xuất chỉ ±1 bậc, lý do hệ thống), ô chọn, **Duyệt đã chọn / Duyệt tất cả**, **Từ chối bắt nhập lý do**, nút **Chạy lại xét cấp cho nhóm đã chọn**. Gói 6 tháng tính 0,5; dưới 1 gói / tháng thì đề xuất hạ; nửa gói lẻ không cộng dồn (H4). | `b9-rank-review.html`, `#tu-choi`, `#duyet-tat-ca`, `#da-xu-ly` |
| 14, 17 | A3, B2 | A3: dòng tiến độ đổi sang **gói xét cấp đã quy đổi** + dòng tháng này. B2: thêm khối Gói xét cấp / Gói tháng này. | `a3-dashboard.html`, `b2-members.html#chi-tiet` |
| 15 | B2 | **Bổ nhiệm đặc biệt** thay cho Cập nhật cấp: bỏ số phiếu, ngày duyệt, người duyệt, file minh chứng; thêm **Lý do** và **Người yêu cầu** (bắt buộc). Duyệt làm **ngoài hệ thống** (chốt 08/10): admin bấm **Xác nhận bổ nhiệm & gửi email** là cấp mới có hiệu lực ngay, hệ thống gửi email cho anh Phương (lưu làm bằng chứng) và email báo thành viên. **Không cho chọn cấp bằng tuyến trên** (H3). | `#cap-nhat-cap`, `#da-bo-nhiem` |
| 20 | B2 | Hiện **tuyến trên trực tiếp** và **tuyến trên hiệu lực** (đi ngược lên tới người đầu tiên có cấp cao hơn, không có thì là công ty) kèm ghi chú khi khác nhau. Trần của bổ nhiệm đặc biệt tính theo tuyến trên hiệu lực. | `#tuyen-tren-hieu-luc` |
| 21 | B2, B5 | **Super Lithium** hiện trong danh sách cấp nhưng không chọn được (tài khoản công ty), có dòng riêng trong bảng hoa hồng; A3 không bao giờ hiện. Giới hạn số tầng tuyến trên khi chia ưu đãi KHÔNG làm thành cấu hình trên giao diện (bỏ 09/10) — dev tự xử lý trong logic tính. | `b5-products.html` |
| 23 | B5 | Khối **Hoa hồng theo cấp**: mỗi cấp nhập **% trên giá trị gói**, tự quy ra tiền cho gói 1 năm và nửa năm, dòng tổng phân bổ tối đa, cảnh báo khi ngoài 0–100% hoặc cấp trên thấp hơn cấp dưới. Cột **chênh lệch cũng nhập %** (H6 trả lời 08/10), mặc định quy từ số tiền cũ trên gói 1 năm (Silver 10% … Lithium 0,5%). **09/10: mỗi gói một bộ % riêng** — chọn tab Gói 1 năm (10tr) / Gói nửa năm (6tr) để cấu hình, số tiền quy theo giá gói đang chọn; mặc định gói nửa năm lấy cùng số với gói 1 năm để admin chỉnh. | `b5-products.html`, `#hoa-hong-loi` |
| 24 | A1, B5, B6 | Đổi **tên hiển thị** gói thành **HOMI365-01**. Mã CN02 trong SKU kho và mã gói giữ nguyên. | — |

**Giả định của bản mẫu — cần xác nhận:**

1. **Bổ nhiệm đặc biệt (15)** — đã chốt 08/10: anh Phương duyệt ngoài hệ thống, admin vào xác nhận là có hiệu lực ngay; hệ thống chỉ cần gửi email cho anh Phương.
2. **Ngưỡng số gói từng cấp** — đã chốt 08/10 theo Chính sách ưu đãi thành viên: Silver 10, Gold 18, Diamond 24, Titanium 28, Lithium 30 (xem mục 21).
3. **Hoa hồng % mặc định** quy từ bảng tiền cũ của gói 1 năm (Copper 20% … Lithium 38,5%). Tính % trên gói nửa năm 6tr cho ra 1.200.000đ … 2.310.000đ, khác bản chốt 01/10 (ưu đãi gói nửa năm = 1/2 gói 1 năm). Cần KH xác nhận lại.
4. **Đối chiếu file kết quả thanh toán** theo số tài khoản + số tiền. Bản mẫu giả lập 1 yêu cầu không có trong file và 1 dòng file không khớp yêu cầu nào.
5. **Duyệt đổi điểm** cho cả Admin và Head bấm (Head có đủ quyền Admin).
6. **Mốc chi trả 5 ngày sau khoá sổ** (H1) KH chưa trả lời — chưa thể hiện trên giao diện.

**Còn lệch, chưa sửa:** ngăn chi tiết thành viên ở B2 và hộp thoại Head duyệt hồ sơ vẫn ghi "ưu đãi đang tạm giữ", "kích hoạt" (xem mục 19).

## 21. Văn bản chính sách chính thức (HOMI365 gửi 08/10, hiệu lực 01/10/2026)

Nguồn dữ liệu duy nhất: `tools/policy_docs.py` — sinh ra cả khung đọc trong form lẫn trang `policy.html`, nên hai nơi không lệch chữ.

| Văn bản | Hiện ở | Ghi chú |
|---|---|---|
| Chính sách mua hàng + Chính sách bảo mật và bảo vệ dữ liệu cá nhân (kèm Điều kiện giao dịch chung, Vận chuyển và giao nhận, Phương thức thanh toán) | A1 khung đọc trên ô đồng ý · `policy.html?s=chinh-sach-mua-hang` | Thay bản tóm tắt tự viết. "Ngày cập nhật 10/10/2026" đổi thành "Hiệu lực từ 01/10/2026". |
| Chính sách ưu đãi thành viên HOMI365, phiên bản 1.0 | A2 bước 4 · `policy.html?s=dieu-khoan-thanh-vien` (giữ id cũ) | Thay bản Điều khoản & Điều kiện cũ (còn chỗ trống ………). Sửa lỗi gõ "ngày cuối cũng" → "ngày cuối cùng". |

Cả A1 và A2: ô đồng ý chỉ mở khi **kéo đọc hết** khung; bấm link mở bản đầy đủ không còn mở khoá. Footer: thêm link Chính sách mua hàng & bảo mật dữ liệu, đổi tên "Điều khoản thành viên" → "Chính sách ưu đãi thành viên". Hai văn bản chính thức không còn dòng "Nội dung mẫu dựng giao diện" ở cuối trang.

**Bỏ 7 trang chính sách mẫu (HOMI365 chốt 08/10):** Quy chế hoạt động, Bảo mật thông tin, Thanh toán, Vận chuyển & giao nhận, Đổi trả & hoàn tiền, Bảo hành, Kiểm hàng — nội dung chép từ gocare.vn, mâu thuẫn với văn bản KH (thẻ/ví/cổng thanh toán, phí giao hàng). Trang chính sách và footer chỉ còn 2 văn bản; link cũ `?s=<id cũ>` tự chuyển về Chính sách mua hàng & bảo mật dữ liệu. Câu "Chính sách đổi trả và hoàn tiền" ở mục Phí giao hàng: HOMI365 xác nhận nội dung này nằm chung trang Chính sách mua hàng, không tách trang riêng.

**Văn bản lệch với prototype — kết quả chốt 08/10:**

1. **Ngưỡng hạng — ĐÃ CHỐT 08/10.** Ngưỡng theo văn bản: Silver 10, Gold 18, Diamond 24, Titanium 28, Lithium 30 — đã thay số minh hoạ ở B9/A3/B2. Đơn vị vẫn là *gói quy đổi* (gói 1 năm = 1, gói 6 tháng = 0,5 — Change Request mục 17) và lên cấp thì đếm lại từ 0, không nhảy bậc (mục 14) — HOMI365 xác nhận lại 08/10: Copper bán 12 gói thì tháng sau lên Silver, từ Silver đếm lại từ 0; bán bao nhiêu trong tháng cũng chỉ lên 1 cấp, phần dư bỏ. **Chốt 09/10:** số gói cần cho mỗi bậc = ngưỡng cấp đích trừ ngưỡng cấp hiện tại — Copper→Silver 10, Silver→Gold 8, Gold→Diamond 6, Diamond→Titanium 4, Titanium→Lithium 2 (ví dụ KH: Silver bán 1 gói 1 năm + 1 gói 6 tháng → "Gói xét cấp 1,5 / 8 · còn 6,5 gói để lên Gold"). A3 chỉ hiện đúng 1 dòng này. Văn bản ghi "số đơn giao dịch hợp lệ lũy kế", chưa nêu trọng số gói 6 tháng và việc đếm lại — nên đề nghị HOMI365 bổ sung câu chữ cho khớp.
2. **Hạ hạng — ĐÃ CHỐT 08/10: giữ logic prototype.** Trong tháng phải đạt tối thiểu 1 gói quy đổi mới giữ hạng: gói 1 năm = 1 gói, gói 6 tháng = 0,5 gói, nên cần 2 gói 6 tháng (hoặc 1 gói 1 năm). Tháng chỉ có 1 đơn gói 6 tháng vẫn bị đề xuất hạ 1 cấp. Văn bản mục 3 ("ít nhất 01 đơn mới trong mỗi tháng") đang lệch với quy tắc này — cần HOMI365 sửa câu chữ trong văn bản.
3. **Hạn gửi yêu cầu đổi điểm — ĐÃ CHỐT 08/10: theo văn bản.** Gửi và huỷ được tới 23:59 ngày liền trước ngày cuối tháng (kỳ 09/2026: 23:59 ngày 29/09); ngày cuối tháng khoá sổ. A3 đã sửa mốc, thêm trạng thái `#het-han-gui` (chưa có yêu cầu, qua hạn → nút tạo mờ, hẹn kỳ sau).
4. Văn bản không nhắc tới Super Lithium, bổ nhiệm đặc biệt, tỷ lệ hoa hồng % theo gói — giữ nguyên trên prototype.

## 22. Rà soát bản deploy — đợt 09/10

| Màn | Thay đổi |
|---|---|
| B2 duyệt hồ sơ | Còn **1 bước Head duyệt**; hồ sơ mới ở trạng thái "Chờ Head duyệt". Duyệt hay chưa **không chặn** thành viên dùng link bán hàng, nhận điểm, đổi điểm. Bỏ chữ "kích hoạt / tạm giữ / 2 lượt duyệt" trong modal. Vai Admin chỉ xem, không có nút duyệt. |
| B2 bổ nhiệm | Bổ nhiệm xong thì gói xét cấp về 0 (VD: 0 / 4 lên Titanium). |
| B2 chi tiết | "Lịch sử đơn hàng & ưu đãi"; số tiền = giá gói × % ưu đãi của cấp, tính riêng từng gói (Copper: gói 1 năm 2.000.000đ, gói nửa năm 1.200.000đ). |
| A2 | Tên màn "Đăng ký thành viên"; "Số tài khoản nhận ưu đãi"; SĐT + email tự điền từ đơn mua (chỉ đọc). |
| A1, A2 | Tỉnh/Phường/Ngân hàng/Giới tính để trống, không chọn sẵn; placeholder mẫu: dd/mm/yyyy, VD: NGUYEN VAN AN, VD: Nguyễn Văn A, VD: Cục Cảnh sát QLHC về TTXH. |
| A3 | Có yêu cầu đổi điểm đang mở thì số đó hiện ở "Đang chờ duyệt" và trừ khỏi "Số dư khả dụng"; không có yêu cầu thì "Đang chờ duyệt" = 0đ. |
| A1 header | Trước ô SĐT có câu "Vui lòng nhập số điện thoại để kiểm tra tài khoản". SĐT mới → dưới ô báo "Anh chị chưa có tài khoản, vui lòng nhập thông tin để mua hàng" và mở form (10/10). |
| B3 | Cột "Khoản thưởng hiện tại" → "Số dư khả dụng". |
| B6 | Cột Nội dung 1 dòng, cắt chữ, rê chuột xem đủ. |
| B7 | Mở mặc định với vai Head; thêm trạng thái vai Admin (không có quyền). Sửa mô tả vai trò. |
| B8 | Tab File: "Bổ nhiệm đặc biệt · Lê Văn Cường". |
| A1 header (10/10) | Bỏ tiêu đề "Anh chị đã có tài khoản" ở khung gợi ý (giữ hướng dẫn + nút Đăng nhập / Bỏ qua / Dùng số khác). Chỉ còn 2 câu: "Vui lòng nhập số điện thoại để kiểm tra tài khoản" trước ô SĐT và "Anh chị chưa có tài khoản, vui lòng nhập thông tin để mua hàng" khi SĐT mới. |
| A1, A2 · Ngân hàng (10/10) | Danh sách theo file Techcombank `DomesticBeneficiaryBank.xlsx` (sheet External batch payment, 111 ngân hàng, giữ nguyên tên để khớp file chi trả; bỏ Kho bạc, NHNN, Quỹ TDCS) — `tools/banks_tcb.py`; bỏ gọi API VietQR. Không có ô nhập tay (KH bỏ 12/10). |
| A1 · Sức khỏe (10/10) | Khung "Thông tin sức khỏe cá nhân" ngay dưới khung gói HOMI365-01: 4 mục, mỗi mục tick Không / Có (`#suc-khoe`). Đơn hàng lưu lại; B6 chi tiết đơn hiện từng mục, "Có" tô đỏ. |
| B6 · Chấp thuận điều khoản (10/10) | Chi tiết đơn có khung Chấp thuận điều khoản như hồ sơ thành viên: văn bản, Phiên bản HOMI365, thời điểm đồng ý, IP, định danh (mã đơn · SĐT). Đổi nhãn "Phiên bản T&C" → "Phiên bản HOMI365" ở cả B2. |
| A1 · QR (10/10) | Số tài khoản nhận: TECHCOMBANK - 79365 (CONG TY CO PHAN GIAI PHAP VA DICH VU HOMI365). |
| C1 (11/10) | Vào từ form mua hàng: nhập SĐT → mật khẩu → **màn OTP** → xác thực xong mới quay lại form A1 (tự điền) — `c1-login.html#tu-mua-hang-otp`. Bấm "Đăng nhập thành viên HOMI365" giữ flow cũ: đúng mật khẩu vào thẳng dashboard. |
| A1 · Thanh toán thành công (12/10) | SĐT đã có tài khoản: tiêu đề "Đơn hàng đã được ghi nhận", báo SĐT đã có tài khoản, nút **Đăng nhập thành viên** (sang C1, vào dashboard) + "Để sau" — `a1-buy.html#thanh-toan-ok-thanh-vien`. SĐT mới giữ lời mời đăng ký thành viên. |

## Ghi chú

- Nút **Thanh toán** ở màn A1 trong mockup KH đang để nền đỏ `#EE0000` nhưng màu hover lại là cyan `#0099d1` — gần như chắc chắn là lỗi sót. Bản này đưa về màu chính. Cần KH xác nhận.
- Điều hướng giữa các màn đổi từ `setState` sang chuyển file thật, vì mỗi màn giờ là một file `.html` riêng. Dữ liệu mang sang màn sau đi qua `sessionStorage`.
- Thêm vòng focus bàn phím (WCAG 2.4.7) — không ảnh hưởng layout.

## ⚠ Còn sót màu cũ

- `#00ADEE`
