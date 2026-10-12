# Rà soát Requirement ↔ prototype-v3

*Ngày rà: 09/09/2026 · Nguồn: `Homi365_CNTT - Requirement_092026` sheet **2. Functional Requirement** (48 dòng, update đến 04/09/2026) đối chiếu toàn bộ `prototype-v3/screens/`.*

Chỉ liệt kê chỗ **thiếu, sai, hoặc lệch**. Phần đã khớp không nhắc (chiếm phần lớn: luồng mua A1, đăng ký 5 bước, đăng nhập + quên mật khẩu, dashboard, kho 3 trạng thái, rút tiền duyệt 2 lớp, phân quyền 2 vai, export, lọc/tìm).

---

## A. Sai — cần sửa

| # | Mã YC | Requirement nói | Prototype đang làm | Mức |
|---|---|---|---|---|
| A1 | **8.1.C-4** | Link mua hàng cá nhân cú pháp `Homi365.com.vn/[EEEE][PPPP]`, ví dụ `Homi365.com.vn/HTMT0083` | Đã sửa hôm nay thành `homi365.com.vn/NVA1111` ✅ | — |
| A2 | **7.7.1** | "Logic lưu thông tin sp trong DB **(ko có giao diện quản lý)**" | Vừa dựng hẳn màn **B5 Quản lý sản phẩm** theo yêu cầu 08/09 | **Cao** |
| A3 | **7.9.2** | Đăng ký thành viên ở trạng thái **Chờ duyệt** cho tới khi đủ **2 lượt xác nhận** mới kích hoạt chính thức — áp cho cả 7.2.x và LP-6 | A2 bước 5 báo thẳng *"Kích hoạt thành công · Bạn đã chính thức là seller"* rồi vào dashboard | **Cao** |
| A4 | — | Tên miền | Mockup dùng lẫn lộn: `homi365.vn/san-pham/...` (link ref), `homi365.com.vn/...` (link cá nhân), `portal.homi365.com.vn/...` (link form B2) | Trung bình |

**A2 — mâu thuẫn requirement vs quyết định mới.** Requirement ghi rõ sản phẩm *không có giao diện quản lý*, nhưng ngày 08/09 đã chốt làm màn B5. Không phải lỗi prototype — là **requirement cần cập nhật**, nếu không dev đọc spec sẽ bỏ qua màn này.

**A3 — lệch nghiệp vụ nặng nhất.** Theo 7.9.2, agent đăng ký xong phải ở trạng thái *Chờ duyệt (0/2)*, chưa được coi là seller. Mockup KH cho vào thẳng dashboard với thông báo đã kích hoạt. Hai cách hiểu khác hẳn nhau về thời điểm agent bắt đầu bán được hàng. Cần chốt trước khi dev làm — ảnh hưởng cả engine hoa hồng (hoa hồng phát sinh trong lúc chờ duyệt tính thế nào).

---

## B. Thiếu — chưa có trong prototype

| # | Mã YC | Ưu tiên | Thiếu gì |
|---|---|---|---|
| B1 | **7.9.1** | P0 | **Màn quản lý tài khoản admin.** Requirement yêu cầu mỗi tài khoản admin được gán đúng 1 trong 2 vai (Specialist / Head Admin) — nhưng không có màn nào tạo, sửa, gán vai hay khoá tài khoản admin. Hiện chỉ có nút *Vai trò (demo)* để đổi vai lúc trình diễn. |
| B2 | **7.1.3** | P0 | **Redirect sang màn đăng ký agent** khi tài khoản đã mua hàng nhưng chưa kích hoạt vai trò agent. C1 hiện chỉ có 2 nhánh: đúng mật khẩu → dashboard, sai → OTP. |
| B3 | **7.5.2** | P0 | **Lịch sử thăng/giáng hạng** trong ngăn chi tiết agent. Đã có cây tuyến và lịch sử đơn/hoa hồng, thiếu mỗi lịch sử hạng. |
| B4 | **7.5.2** | P0 | Cây tuyến yêu cầu **2–3 cấp**, prototype mới vẽ **2 cấp** (F0 → F1). |
| B5 | **7.3.2** | P1 | **Lọc số đơn theo thời gian** (hôm nay / tuần / tháng / khoảng ngày tuỳ chọn) ở dashboard. Ô *Tổng đơn hàng* đang là số tĩnh; bộ chọn khoảng thời gian chỉ tác động lên biểu đồ. |
| B6 | **7.9.4** | P0 | Hiển thị tiến trình duyệt đúng dạng **`0/2` · `1/2` · Đã duyệt · Từ chối**. Prototype diễn đạt bằng chữ (*"Chờ Head Admin xác nhận"*, *"bước 1/2"*) và có audit log đủ vai + thời gian, nhưng nhãn trạng thái không theo dạng đếm lượt. |

---

## C. Có trong prototype nhưng requirement chưa nhắc

| # | Màn / chức năng | Ghi chú |
|---|---|---|
| C1 | **B6 Quản lý đơn hàng** | Requirement **không có dòng nào** về màn đơn hàng, dù luồng mua là chuyển khoản + khách tự tải ảnh bill. Không có màn này thì không ai xác nhận được tiền về, đơn treo vĩnh viễn. Cần bổ sung requirement. |
| C2 | **Import kho hàng loạt** + chặn trùng mã | Chốt 08/09, requirement 7.8.x chưa có. |
| C3 | **B5 Quản lý sản phẩm** | Xem A2 ở trên — trái với 7.7.1. |
| C4 | Modal **Tra cứu đơn hàng** ở A1 | Thực ra là hiện thực của **7.2.8** (tra theo SĐT cũ để autofill khi khách quay lại đăng ký). Trước đây tôi kết luận "không có requirement" — **kết luận đó sai**, 7.2.8 chính là nó. Nhưng cách hiện thực vẫn có lỗ hổng: nhập SĐT bất kỳ là ra họ tên, email, CCCD, địa chỉ người khác. 7.2.8 không nói phải mở tra cứu công khai — cần thêm OTP xác thực chính chủ. |

---

## D. Prototype không mô phỏng được — dev tự thiết kế

| Mã YC | Nội dung |
|---|---|
| **6.1.C-5** | Idempotency chặn tạo Order trùng khi bấm Thanh toán nhiều lần |
| **6.1.C-1** | Ref code không trùng, không đoán được (mockup dùng số 6 chữ số dễ đoán: 923983, 118820…) |
| **6.1.C-2** | Tracking click link giới thiệu, yêu cầu **0% lỗi gán tuyến** |
| **6.1.C-3** | Engine tính điểm / hoa hồng theo tầng / xếp hạng |
| **8.1.C-5** | Xử lý trùng alias khi 2 agent ra cùng mã `initials + 4 số cuối SĐT` |

---

## E. Việc đề xuất, theo thứ tự

1. **Chốt A3 (7.9.2)** — agent sau đăng ký là *Chờ duyệt* hay *Đã kích hoạt*? Đây là câu hỏi chặn, ảnh hưởng cả luồng mua, màn duyệt và engine hoa hồng.
2. **Cập nhật requirement cho 3 mục mới**: bỏ mệnh đề "ko có giao diện quản lý" ở 7.7.1, viết mới cho màn Đơn hàng, viết mới cho Import kho.
3. **Thống nhất tên miền** — chọn `homi365.com.vn` hay `homi365.vn`, và chốt `portal.` dùng làm gì.
4. **Bổ sung vào prototype** (nhanh, mỗi cái dưới nửa ngày): màn tài khoản admin (B1), redirect 7.1.3 (B2), lịch sử hạng + cây 3 cấp (B3–B4), bộ lọc thời gian ở dashboard (B5), nhãn `0/2 · 1/2` (B6).
5. **Thêm OTP cho modal tra cứu đơn** trước khi trả dữ liệu cá nhân.
