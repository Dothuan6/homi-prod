# Rà soát bản deploy ↔ Requirement

*Ngày rà: 09/09/2026 · Bản deploy: https://homi-ui-final.netlify.app · Nguồn: `Homi365_CNTT - Requirement_092026` sheet **2. Functional Requirement** (48 dòng, update 04/09/2026), đọc cả cột **Mô tả** lẫn cột **Acceptance Criteria**.*

Đi qua toàn bộ 11 màn và 41 trạng thái trên bản deploy. Lần này đọc kỹ cột **Acceptance Criteria** — chỗ chứa nhiều ràng buộc mà cột Mô tả không nói, và là nơi lộ ra phần lớn lỗi bên dưới.

---

## 0. Bản deploy đang CŨ hơn bản build tại máy

Trước khi đọc tiếp, cần biết điều này để khỏi sửa nhầm thứ đã sửa rồi:

| Thay đổi | Local | Deploy |
|---|---|---|
| Cây tuyến 3 cấp (vòng lặp F2) | có | **không** |
| Cột `Nội dung` (đã đổi tên) | có | vẫn là `Nội dung chuyển khoản` |

Cần **build lại rồi deploy lại** trước khi rà lần sau.

---

## A. Sai so với Acceptance Criteria — cần sửa

### A1 · Autofill khi đăng ký ngay sau khi mua — **hỏng** · 7.2.2 · P0

> AC: *"khi form đăng ký hiển thị, lúc đó toàn bộ thông tin đã có sẵn (autofill) từ dữ liệu đơn hàng, **không hiển thị trống**"*

Bấm **Đăng ký thành viên** ở modal thanh toán thành công → sang màn A2 với form **trống hoàn toàn**. Khách vừa nhập họ tên, SĐT, email, CCCD, địa chỉ ở A1 xong phải gõ lại từ đầu.

Nguyên nhân: đây là **lỗi do tách file**. Trong mockup gốc mọi màn nằm chung một trang nên dữ liệu còn nguyên trong state. Khi tách mỗi màn một file, nút đó chỉ mang sang mỗi `regStep`, không mang dữ liệu người mua.

Điều buồn cười: đường **tra cứu đơn hàng** lại autofill đúng, vì luồng đó có truyền dữ liệu. Tức là khách đi vòng thì được, đi thẳng thì không.

### A2 · Tuyến trên hạng Đồng vẫn được mời đăng ký — 7.2.1 · P0

> AC: *"Hệ thống nhận diện được agent thuộc cấp nào, trường hợp là cấp Copper sẽ **không hiển thị thông báo cho đăng ký thành viên**, mà chỉ báo đơn hàng thành công"*

Modal thanh toán thành công **luôn** hiện *"Bạn có muốn đăng ký làm seller… / Đăng ký thành viên / Không, thoát ra"*, bất kể người giới thiệu hạng nào. Modal chặn chỉ bật ở luồng tra cứu đơn, không bật ở luồng mua thẳng.

⚠ **Requirement tự mâu thuẫn ở điểm này** — cần KH chốt trước khi sửa:
- **7.2.1 AC**: hạng Đồng → *không hiện lời mời*, chỉ báo đơn thành công.
- Dòng *"Logic điều kiện đăng ký thành viên mới"*: hạng Đồng → *hiển thị báo lỗi không đủ điều kiện*.

Một bên là giấu đi, một bên là hiện rồi báo lỗi. Bản deploy đang làm cách thứ hai.

### A3 · Cây tuyến dưới chỉ có 2 cấp — 7.5.2 · P0

> Mô tả: *"sơ đồ/cây tuyến dưới (**ít nhất 2-3 cấp** cho MVP)"*

Deploy chỉ vẽ F0 → F1. Tiêu đề ghi *"SƠ ĐỒ TUYẾN DƯỚI (2 CẤP)"*.

Local đã có vòng lặp F2 nhưng **vẫn không hiện**, vì dữ liệu `tree` thiếu nhánh con — bản vá dữ liệu đặt nhầm vào nhóm xử lý markup nên chưa từng chạy. Đã sửa trong `tools/build-v3.py`, chạy lại build là ra.

### A4 · Admin Specialist vào được màn Tài khoản admin — 7.9.1 · P0

> AC: *"Chỉ Head Admin có quyền tạo mới/chỉnh sửa/vô hiệu hoá tài khoản… **Admin Specialist không có quyền truy cập màn hình quản lý**"*

Mở `b7-admin-users.html` với vai mặc định **Admin Specialist**: thấy đủ danh sách, bấm được *Thêm tài khoản*, *Sửa*, *Khoá*. Không có chặn, không có màn 403.

### A5 · Duyệt 2 lớp đang tách theo VAI TRÒ, requirement nói tách theo NGƯỜI — 7.9.2 · 7.9.3 · 7.9.4 · P0

Đây là lệch **nặng nhất về nghiệp vụ**, vì nó khác hẳn cách hệ thống được xây.

> **7.9.2 AC**: *"Lượt xác nhận thứ 1: **bất kỳ Admin Specialist hoặc Head Admin nào** thực hiện → Chờ duyệt (1/2). Lượt xác nhận thứ 2 phải do **người KHÁC** với người đã xác nhận lượt 1"*
> **7.9.3 AC**: *"…khi đủ 2 xác nhận hợp lệ (**2 người khác nhau, hoặc Head Admin tự chốt**)"*
> **7.9.4 AC**: *"Admin Specialist đã xác nhận 1 yêu cầu thì nút Xác nhận **của chính người đó** trên yêu cầu đó bị vô hiệu hoá"*

Bản deploy làm: **Specialist luôn làm bước 1, Head Admin luôn làm bước 2**, khoá theo vai trò.

Ba điểm khác nhau thực chất:

| | Requirement | Deploy |
|---|---|---|
| Ai làm bước 1 | Specialist **hoặc** Head Admin | chỉ Specialist |
| Điều kiện bước 2 | người khác người bước 1 | phải là Head Admin |
| Head Admin đơn độc | được **tự chốt** cả 2 lượt (7.9.3) | không thể |
| Khoá nút | theo **từng người** | theo vai trò |

Hệ quả thực tế: theo bản deploy, nếu Specialist nghỉ thì không đơn nào qua được bước 1 — dù Head Admin đang ngồi đó. Requirement thiết kế để tránh đúng tình huống này.

Lưu ý: quyết định ngày 08/09 chọn "hai cấp như rút tiền" là nói về **màn Đơn hàng (B6)** — màn này requirement chưa có dòng nào. Nhưng cách hiện thực đã áp luôn lên cả duyệt hồ sơ và duyệt rút tiền, là hai chỗ requirement có nói rõ.

### A6 · Nhãn bước sai ở màn đăng ký — 7.2.x

Màn A2 bước 1 ghi *"**Bước 1/3** · Thông tin cá nhân & nhận hoa hồng"* trong khi luồng có **5 bước** (thông tin → OTP → mật khẩu → T&C → hoàn tất). Số bước hiển thị không khớp thực tế. Lỗi có sẵn từ mockup KH.

### A7 · Còn tên thương hiệu "Medigo" trong sản phẩm HOMI365

Sau khi đã re-skin toàn bộ sang HOMI365, các chỗ sau vẫn ghi Medigo:

- A2 bước 4: *"Điều khoản chương trình affiliate **Medigo** — Homi365"*, *"…điều khoản tham gia chương trình affiliate **Medigo**"*
- A2 bước 5: *"Bạn đã chính thức là seller **Medigo**"*
- A3 agent mới: *"Chào mừng bạn đến với **Medigo**!"*

Gửi KH mà còn tên đối thủ/tên cũ trong màn là mất điểm.

---

## B. Thiếu nội dung so với Acceptance Criteria

| # | Mã YC | AC yêu cầu | Deploy |
|---|---|---|---|
| B1 | **7.3.3** · P0 | *"Hiển thị **số đơn còn thiếu để lên hạng kế tiếp**"* | Chỉ có *Hạng hiện tại*, không có gợi ý còn thiếu bao nhiêu đơn |
| B2 | **7.3.2** · P1 | *"Cho phép chọn **khoảng ngày tùy chỉnh**"* | Chỉ có 4 mốc cố định Hôm nay / Tuần này / Tháng này / Tất cả |
| B3 | **7.2.3** · P0 | OTP **hết hạn 5 phút**; sai 3 lần → lần 4 **khoá tạm** và admin cấp lại mật khẩu | Màn OTP tĩnh, chỉ có *"Gửi lại (30s)"*, không đếm ngược hết hạn, không có trạng thái khoá |
| B4 | **7.5.4** · P1 | *"Khi khoá thì **link bán hàng, giới thiệu cũng sẽ bị khoá**"* | Có nút Khoá/Mở khoá, nhưng không thể hiện link bị vô hiệu |
| B5 | **8.1.C-5** · P0 | Trùng alias → tự thêm hậu tố `-2`, `-3` (VD `HTMT0083-2`) | Không có màn/trạng thái nào thể hiện |
| B6 | **7.2.6** · P0 | Lưu bản ghi chấp thuận T&C: **agent id, phiên bản T&C, thời điểm** | Chỉ có checkbox đồng ý, không hiện phiên bản điều khoản |
| B7 | **7.2.4** · P0 | *"Hạng khởi điểm mặc định là **Copper**"* | Màn hoàn tất không nói hạng khởi điểm (A3 có hiện *Đồng*, coi như gián tiếp đạt) |

---

## C. Lệch mô hình dữ liệu — cần chốt trước khi dev code

**Form mua hàng đang hỏi số tài khoản ngân hàng của người mua.** A1 có nguyên khối *"Thông tin nhận hoa hồng — Ngân hàng (*) / Số tài khoản (*)"*, đánh dấu bắt buộc.

Nhưng LP-2 chỉ yêu cầu *"họ tên, số điện thoại, email, địa chỉ nhận hàng (nếu cần) và thông tin thanh toán"*. Thông tin **nhận hoa hồng** thuộc về 7.2.2 — form đăng ký agent, không phải form mua hàng. Bắt một người chỉ muốn mua đồng hồ phải khai số tài khoản để "nhận hoa hồng" là vừa khó hiểu vừa thu thập dư dữ liệu tài chính.

Đây là trường có sẵn trong mockup KH nên tôi giữ nguyên, nhưng nên hỏi lại.

---

## D. Đã đạt — không cần đụng

Ghi lại để khỏi rà lại lần sau: LP-1, LP-3, LP-6, 7.1.1 *(báo lỗi chung, không lộ SĐT tồn tại)*, 7.1.2, 7.1.3, 7.2.5, 7.2.7, 7.2.8, 7.3.4 *(4 trạng thái hoa hồng + cơ chế hold)*, 7.3.6 *(chặn vượt số dư, chặn 1 lần/tháng)*, 7.3.10, 7.4.1, 7.5.1 *(đủ 9 cột)*, 7.5.3 *(lọc hạng + trạng thái + tìm)*, 7.5.5, 7.6.1, 7.6.2, 7.6.3 *(bắt buộc lý do, cảnh báo vượt số dư)*, 7.6.4 *(nút chi trả chỉ hiện khi đã duyệt)*, 7.6.5 *(timeline đủ ai/khi nào)*, 7.8.1 → 7.8.5 *(3 summary cộng đúng 24, lọc, phân trang, trạng thái rỗng)*.

Nhãn `0/2 · 1/2 · 2/2` của 7.9.4 đã hiển thị đúng trên cả B2 và B3.

---

## E. Ngoài phạm vi prototype — dev tự thiết kế

`6.1.C-1` ref code không đoán được *(dữ liệu mẫu đang là số 6 chữ số dễ đoán)* · `6.1.C-2` tracking click, 0% lỗi gán tuyến · `6.1.C-3` engine hoa hồng, tổng 6 hạng = 3.850.000đ/đơn · `6.1.C-5` idempotency · `7.7.1` kiến trúc dữ liệu mở rộng thêm sản phẩm.

---

## F. Thứ tự xử lý đề xuất

**Đã chốt 09/09 — cả ba giữ nguyên hành vi prototype, nhưng requirement phải sửa:**

1. **A5 → tách theo VAI TRÒ.** Specialist bước 1, Head Admin bước 2. Sửa `7.9.2 AC`, `7.9.3 AC`, `7.9.4 AC` — cả ba đang mô tả tách theo *người*. Rủi ro cần KH biết: Specialist nghỉ là nghẽn bước 1 dù Head Admin đang trực; muốn chặn rủi ro mà vẫn giữ tách vai trò thì thêm câu *"Head Admin được làm thay bước 1 khi cần"*.
2. **A2 → hạng Đồng thì BÁO LỖI.** Sửa `7.2.1 AC` (đang ghi ngược: không hiện lời mời). Prototype đã chỉnh để báo lỗi **ngay khi bấm** nút Đăng ký thành viên, thay vì bắt khách điền hết 5 bước rồi mới chặn.
3. **7.9.2 → agent vào thẳng dashboard.** Bỏ phần đăng ký thành viên ra khỏi phạm vi duyệt 2 lớp, chỉ giữ cho rút tiền và đơn hàng.

⚠ **Mâu thuẫn còn lại bên trong sản phẩm, cần chốt nốt.** A2 báo *"đã chính thức là seller"*, nhưng B2 vẫn có thành viên ở trạng thái *Chờ duyệt (0/2)* kèm nút Duyệt / Từ chối. Nếu ai đăng ký cũng active ngay thì màn duyệt hồ sơ ở B2 không còn lý do tồn tại.

Cách dung hoà (prototype-v2 đã làm): agent **hoạt động ngay** — có link, bán được hàng — nhưng **hoa hồng tạm giữ** tới khi đủ 2 lượt duyệt. Giữ được cả "vào thẳng dashboard" lẫn màn duyệt.

**Sửa được ngay, không cần hỏi:**

4. **A1** — truyền dữ liệu người mua sang màn đăng ký. Lỗi nặng nhất về trải nghiệm, sửa nhanh nhất.
5. **A7** — thay hết "Medigo" thành "HOMI365".
6. **A6** — sửa nhãn `Bước 1/3` cho khớp số bước thật.
7. **A3** — build lại để cây 3 cấp có hiệu lực.
8. **A4** — chặn Specialist vào màn B7, thêm màn 403.
9. **B1, B2** — thêm "còn thiếu N đơn để lên hạng" và bộ chọn khoảng ngày tuỳ chỉnh.

**Build lại và deploy lại** sau khi xong, vì bản trên server đang cũ hơn bản tại máy.
