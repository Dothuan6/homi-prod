# -*- coding: utf-8 -*-
"""
policy_docs.py — toàn văn hai văn bản chính sách HOMI365 gửi 08/10/2026.

  * PURCHASE — "Chính sách mua hàng và Chính sách bảo mật và bảo vệ dữ liệu cá
    nhân" (file Word CHÍNH SÁCH MUA HÀNG VÀ ĐIỀU KHOẢN BẢO MẬT.docx). Hiện trong
    khung đọc ở form mua hàng A1.
  * MEMBER — "Chính sách ưu đãi thành viên HOMI365" (file Word cùng tên). Hiện
    trong khung đọc ở bước 4 form đăng ký A2.

Cả hai hiệu lực từ 01/10/2026 (HOMI365 chốt). Một nguồn dữ liệu, hai đầu ra:
html(doc) cho khung đọc trong form, policy_js(doc) cho trang policy.html — để
hai nơi không bao giờ lệch chữ.

Chuỗi trong items được phép chứa thẻ inline (<strong>, <a>…). Mục con không có
tiêu đề riêng thì viết thành đoạn <strong>…</strong>.

Chỉnh so với bản Word: "Ngày cập nhật: 10/10/2026" → "Hiệu lực từ 01/10/2026";
sửa lỗi gõ "ngày cuối cũng dương lịch" → "ngày cuối cùng dương lịch".
"""
import json

EFFECTIVE = "01/10/2026"

_CONTACT = [
    "CÔNG TY CỔ PHẦN GIẢI PHÁP VÀ DỊCH VỤ HOMI365",
    "Giấy chứng nhận đăng ký doanh nghiệp số 0319717698 cấp ngày 21 tháng 09 năm 2026",
    "Trụ sở chính tại: Số 36 đường 27A, Phường Bình Trưng, Thành Phố Hồ Chí Minh, Việt Nam",
    "Mã số thuế: 0319717698",
    "Hotline: 1900 9007",
    "Email: info@homi365.com.vn",
]

PURCHASE = {
    "id": "chinh-sach-mua-hang",
    "title": "Chính sách mua hàng &amp; bảo mật dữ liệu",
    "heads": ["CHÍNH SÁCH MUA HÀNG", "CHÍNH SÁCH BẢO MẬT VÀ BẢO VỆ DỮ LIỆU CÁ NHÂN"],
    "h1": "Chính sách mua hàng và Chính sách bảo mật và bảo vệ dữ liệu cá nhân",
    "intro": ("Áp dụng đối với khách hàng và người sử dụng sản phẩm, dịch vụ của HOMI365 · "
              "Hiệu lực từ " + EFFECTIVE),
    "sections": [
        {"h": "1. MỤC ĐÍCH VÀ CAM KẾT", "items": [
            "HOMI365 tôn trọng quyền riêng tư và cam kết bảo vệ dữ liệu cá nhân của khách hàng, người sử dụng dịch vụ và các cá nhân có liên quan.",
            "Chính sách này quy định cách HOMI365 thu thập, sử dụng, lưu trữ, bảo vệ và chia sẻ dữ liệu cá nhân trong quá trình cung cấp sản phẩm, dịch vụ và chăm sóc khách hàng.",
            "HOMI365 xử lý dữ liệu cá nhân theo Luật Bảo vệ dữ liệu cá nhân và các quy định pháp luật Việt Nam hiện hành.",
        ]},
        {"h": "2. DỮ LIỆU CÁ NHÂN CÓ THỂ ĐƯỢC THU THẬP", "items": [
            "Tùy từng sản phẩm, dịch vụ và phương thức tương tác, HOMI365 có thể thu thập các thông tin cần thiết, bao gồm:",
            {"list": [
                "Họ và tên; ngày, tháng, năm sinh;",
                "Số điện thoại, email, địa chỉ liên hệ hoặc địa chỉ sử dụng dịch vụ;",
                "Thông tin tài khoản, thông tin đăng nhập;",
                "Thông tin giao dịch, lịch sử sử dụng sản phẩm, dịch vụ;",
                "Hình ảnh, thông tin do khách hàng cung cấp;",
                "Thông tin thiết bị, địa chỉ IP và dữ liệu kỹ thuật khi sử dụng website/ứng dụng;",
                "Thông tin của người được khách hàng đăng ký sử dụng dịch vụ trong phạm vi cần thiết;",
                "Thông tin sức khỏe và thông tin liên quan đến chăm sóc sức khỏe khi dịch vụ có yêu cầu.",
            ]},
            "HOMI365 chỉ thu thập dữ liệu trong phạm vi cần thiết cho mục đích xử lý và theo căn cứ pháp luật áp dụng.",
        ]},
        {"h": "3. MỤC ĐÍCH XỬ LÝ DỮ LIỆU", "items": [
            "HOMI365 có thể xử lý dữ liệu cá nhân để:",
            {"steps": [
                "Đăng ký, xác thực và quản lý tài khoản;",
                "Cung cấp, vận hành và quản lý sản phẩm, dịch vụ;",
                "Tiếp nhận, xử lý yêu cầu sử dụng dịch vụ, thanh toán và chăm sóc khách hàng;",
                "Liên hệ với khách hàng về giao dịch, dịch vụ, hỗ trợ và các vấn đề liên quan;",
                "Cải thiện chất lượng sản phẩm, dịch vụ và trải nghiệm khách hàng;",
                "Bảo đảm an toàn hệ thống, phòng ngừa gian lận và bảo vệ quyền, lợi ích hợp pháp;",
                "Thực hiện hợp đồng và nghĩa vụ pháp lý của HOMI365;",
                "Thực hiện các mục đích khác khi khách hàng đã được thông báo và có sự đồng ý hợp pháp, nếu pháp luật yêu cầu.",
            ]},
            "Đối với dữ liệu sức khỏe và dữ liệu cá nhân nhạy cảm khác, HOMI365 áp dụng biện pháp bảo vệ phù hợp và chỉ xử lý trong phạm vi cần thiết, đúng mục đích và theo quy định pháp luật.",
        ]},
        {"h": "4. CHIA SẺ VÀ CUNG CẤP DỮ LIỆU CÁ NHÂN", "items": [
            "HOMI365 không bán dữ liệu cá nhân của khách hàng.",
            "Trong phạm vi cần thiết để cung cấp sản phẩm, dịch vụ, HOMI365 có thể cung cấp hoặc chia sẻ dữ liệu cá nhân với:",
            {"list": [
                "Đơn vị cung cấp dịch vụ công nghệ, lưu trữ và vận hành hệ thống;",
                "Đơn vị thanh toán, giao nhận hoặc đối tác trực tiếp tham gia cung cấp dịch vụ;",
                "Nhà cung cấp dịch vụ chăm sóc sức khỏe hoặc đối tác thực hiện dịch vụ cho khách hàng;",
                "Công ty, đơn vị có liên quan trong phạm vi cần thiết và phù hợp với mục đích xử lý;",
                "Cơ quan nhà nước có thẩm quyền khi pháp luật yêu cầu.",
            ]},
            "Các bên nhận dữ liệu có trách nhiệm bảo mật và chỉ xử lý dữ liệu trong phạm vi được phép.",
        ]},
        {"h": "5. THỜI GIAN LƯU TRỮ", "items": [
            "HOMI365 lưu trữ dữ liệu cá nhân trong thời gian cần thiết để thực hiện mục đích xử lý, cung cấp dịch vụ, thực hiện hợp đồng, giải quyết khiếu nại, tranh chấp hoặc đáp ứng nghĩa vụ lưu trữ theo pháp luật.",
            "Khi dữ liệu không còn cần thiết và pháp luật không yêu cầu tiếp tục lưu trữ, HOMI365 sẽ xóa, hủy hoặc áp dụng biện pháp xử lý phù hợp.",
        ]},
        {"h": "6. BẢO MẬT VÀ AN TOÀN DỮ LIỆU", "items": [
            "HOMI365 áp dụng các biện pháp quản lý, kỹ thuật và tổ chức phù hợp để bảo vệ dữ liệu cá nhân khỏi truy cập, sử dụng, tiết lộ, thay đổi, mất mát hoặc xử lý trái phép.",
            "Việc truy cập dữ liệu được phân quyền phù hợp với chức năng, nhiệm vụ và nhu cầu công việc. Đối với dữ liệu cá nhân nhạy cảm, HOMI365 áp dụng các biện pháp bảo vệ tăng cường theo quy định pháp luật.",
        ]},
        {"h": "7. QUYỀN CỦA KHÁCH HÀNG", "items": [
            "Theo quy định pháp luật, khách hàng có các quyền đối với dữ liệu cá nhân của mình, bao gồm quyền được biết; quyền đồng ý hoặc rút lại sự đồng ý trong trường hợp pháp luật yêu cầu; quyền truy cập, chỉnh sửa, xóa; quyền hạn chế hoặc phản đối việc xử lý trong các trường hợp luật định và các quyền khác theo quy định pháp luật.",
            "Khách hàng có thể liên hệ HOMI365 theo thông tin tại Mục 9 để thực hiện quyền của mình. HOMI365 tiếp nhận và xử lý yêu cầu theo quy định pháp luật.",
        ]},
        {"h": "8. DỮ LIỆU CỦA NGƯỜI KHÁC", "items": [
            "Trường hợp khách hàng cung cấp cho HOMI365 dữ liệu cá nhân của người khác để đăng ký hoặc sử dụng dịch vụ, khách hàng có trách nhiệm bảo đảm việc cung cấp dữ liệu đó phù hợp với quy định pháp luật và quyền của người có dữ liệu.",
        ]},
        {"h": "9. THÔNG TIN LIÊN HỆ VỀ DỮ LIỆU CÁ NHÂN", "items": [
            {"list": _CONTACT},
            "Khách hàng có thể liên hệ các thông tin trên để yêu cầu hỗ trợ, giải đáp hoặc thực hiện các quyền liên quan đến dữ liệu cá nhân.",
        ]},
        {"h": "10. CẬP NHẬT CHÍNH SÁCH", "items": [
            "HOMI365 có thể sửa đổi, bổ sung Chính sách này để phù hợp với hoạt động kinh doanh, sản phẩm, dịch vụ hoặc quy định pháp luật.",
            "Phiên bản cập nhật sẽ được công bố trên website, ứng dụng hoặc kênh chính thức của HOMI365 và áp dụng kể từ thời điểm được công bố hoặc thời điểm khác được thông báo theo quy định pháp luật.",
            "Chính sách này được xây dựng trên cơ sở Luật Bảo vệ dữ liệu cá nhân và các văn bản pháp luật có liên quan đang có hiệu lực tại Việt Nam.",
        ]},
        {"h": "ĐIỀU KIỆN GIAO DỊCH CHUNG HOMI365", "items": [
            {"list": [
                "<strong>Phạm vi áp dụng:</strong> Áp dụng đối với khách hàng đăng ký, mua hoặc sử dụng sản phẩm, dịch vụ của HOMI365 trên website, ứng dụng và các kênh chính thức của HOMI365.",
                "<strong>Thông tin giao dịch:</strong> Khách hàng có trách nhiệm cung cấp thông tin chính xác, đầy đủ và cập nhật. Giá, phí, nội dung và điều kiện dịch vụ được công bố hoặc thỏa thuận tại thời điểm giao dịch.",
                "<strong>Thanh toán:</strong> Khách hàng thanh toán theo phương thức và thời hạn được HOMI365 thông báo hoặc thỏa thuận.",
                "<strong>Hủy/đổi/hoàn tiền:</strong> Thực hiện theo chính sách áp dụng cho từng sản phẩm, dịch vụ và quy định pháp luật hiện hành.",
                "<strong>Trách nhiệm:</strong> HOMI365 cung cấp dịch vụ theo nội dung đã công bố hoặc thỏa thuận; khách hàng có trách nhiệm sử dụng dịch vụ đúng mục đích và tuân thủ hướng dẫn của HOMI365.",
                "<strong>Khiếu nại và tranh chấp:</strong> Mọi khiếu nại được tiếp nhận và giải quyết trên tinh thần thiện chí, hợp tác và phù hợp với quy định pháp luật Việt Nam."
                # (12/10) KH bổ sung thông tin pháp nhân ngay dưới mục khiếu nại.
                "<div style=\"margin-top:6px;padding:8px 12px;border-left:3px solid #1E3A66;background:rgba(30,58,102,.05);line-height:1.7\">"
                "<strong>CÔNG TY CỔ PHẦN GIẢI PHÁP VÀ DỊCH VỤ HOMI365</strong><br>"
                "Giấy chứng nhận đăng ký doanh nghiệp số 0319717698 cấp ngày 21 tháng 09 năm 2026<br>"
                "Trụ sở chính tại: Số 36 đường 27A, Phường Bình Trưng, Thành Phố Hồ Chí Minh, Việt Nam<br>"
                "Mã số thuế: 0319717698<br>"
                "Hotline: 1900 9007<br>"
                "Email: info@homi365.com.vn</div>",
                "<strong>Điều chỉnh:</strong> HOMI365 có quyền cập nhật Điều kiện giao dịch chung để phù hợp với hoạt động và quy định pháp luật. Phiên bản mới được công bố trên các kênh chính thức của HOMI365.",
            ]},
        ]},
        {"h": "VẬN CHUYỂN VÀ GIAO NHẬN", "items": [
            "Chính sách này quy định phạm vi, phí, thời gian giao hàng và trách nhiệm các bên khi khách hàng mua sản phẩm qua website homi365.com.vn.",
            "<strong>1. Phạm vi và phương thức giao hàng</strong>",
            "HOMI365 giao hàng toàn quốc, tới địa chỉ nhận hàng khách hàng cung cấp khi đặt hàng, thông qua đơn vị vận chuyển do HOMI365 lựa chọn tại từng thời điểm.",
            "Đơn hàng chỉ được giao sau khi HOMI365 xác nhận thanh toán. Mã kích hoạt phần mềm được gửi qua email ngay khi đơn hàng được xác nhận, không phụ thuộc thời điểm giao thiết bị.",
            "<strong>2. Phí giao hàng</strong>",
            "Số tiền khách hàng thanh toán là Thành tiền hiển thị tại bước thanh toán của đơn hàng. HOMI365 không thu thêm phí giao hàng ngoài số tiền này, trừ trường hợp giao lại theo yêu cầu của khách hàng hoặc gửi trả hàng do thay đổi nhu cầu theo Chính sách đổi trả và hoàn tiền.",
        ]},
        {"h": "PHƯƠNG THỨC THANH TOÁN", "items": [
            {"list": [
                "HOMI365 chỉ áp dụng hình thức chuyển khoản ngân hàng qua mã VietQR. HOMI365 không thu tiền mặt, không áp dụng thanh toán khi nhận hàng (COD), thẻ hay ví điện tử.",
                "Tại bước thanh toán, khách hàng quét mã VietQR bằng ứng dụng ngân hàng. Thông tin đơn vị thụ hưởng, số tài khoản, ngân hàng, số tiền và nội dung chuyển khoản được hiển thị cùng mã QR.",
                "Khách hàng chuyển đúng số tiền và giữ nguyên nội dung chuyển khoản do hệ thống tạo (có mã đơn hàng) để HOMI365 đối soát.",
                "Sau khi chuyển khoản, khách hàng tải ảnh chụp màn hình hoặc biên lai giao dịch lên website. Đơn hàng chuyển sang trạng thái Chờ đối soát.",
                "HOMI365 chỉ nhận tiền vào tài khoản đơn vị thụ hưởng hiển thị tại bước thanh toán. Khách hàng không chuyển tiền vào tài khoản cá nhân của bất kỳ ai, kể cả Thành viên giới thiệu hoặc người tự xưng là nhân viên HOMI365.",
            ]},
        ]},
    ],
    "sign": "<strong>HOMI365</strong><br>(Ban hành/Phê duyệt bởi người có thẩm quyền)",
}

MEMBER = {
    "id": "dieu-khoan-thanh-vien",   # giữ id cũ để link đã chia sẻ không gãy
    "title": "Chính sách ưu đãi thành viên",
    "heads": ["CHÍNH SÁCH ƯU ĐÃI THÀNH VIÊN HOMI365"],
    "h1": "Chính sách ưu đãi thành viên HOMI365",
    "intro": "Phiên bản 1.0 · Hiệu lực từ " + EFFECTIVE,
    "sections": [
        {"h": "1. ĐỐI TƯỢNG ÁP DỤNG", "items": [
            "Áp dụng cho khách hàng đủ điều kiện đăng ký và được HOMI365 xác nhận là Thành viên. Mỗi cá nhân chỉ được duy trì 01 tài khoản Thành viên.",
        ]},
        {"h": "2. TÍCH ĐIỂM HOMI", "items": [
            "Mỗi đơn hàng hợp lệ được HOMI365 xác nhận thanh toán sẽ phát sinh ưu đãi theo hạng Thành viên và sản phẩm/dịch vụ áp dụng.",
            "Điểm HOMI là đơn vị quy ước dùng để ghi nhận Khoản ưu đãi; 01 Điểm HOMI tương ứng 01 đồng Khoản ưu đãi theo chương trình hiện hành.",
            "Đơn hàng bị hủy, từ chối hoặc hoàn tiền thì Điểm HOMI/ưu đãi tương ứng bị thu hồi.",
        ]},
        {"h": "3. HẠNG THÀNH VIÊN – ÁP DỤNG GÓI HOMI365-01", "items": [
            "Hạng được xét theo số đơn giao dịch hợp lệ lũy kế:",
            {"list": [
                "Copper: từ 0 đơn;", "Silver: từ 10 đơn;", "Gold: từ 18 đơn;",
                "Diamond: từ 24 đơn;", "Titanium: từ 28 đơn;", "Lithium: từ 30 đơn.",
            ]},
            "HOMI365 tự động xét hạng vào cuối mỗi tháng dương lịch. Số đơn hợp lệ được cộng dồn qua các tháng. Để duy trì hạng, Thành viên cần có ít nhất 01 đơn mới trong mỗi tháng; nếu không phát sinh đơn, Thành viên có thể được điều chỉnh xuống hạng liền kề theo thể lệ.",
        ]},
        {"h": "4. QUY ĐỔI ĐIỂM", "items": [
            "Thành viên được yêu cầu quy đổi số Điểm HOMI khả dụng tối đa 01 lần trong mỗi tháng dương lịch và trước ngày cuối cùng dương lịch hàng tháng.",
            "Số điểm yêu cầu quy đổi không vượt quá số dư khả dụng.",
        ]},
        {"h": "5. QUY ĐỊNH VỀ ĐIỂM VÀ ƯU ĐÃI", "items": [
            "Điểm HOMI không được mua bán, chuyển nhượng hoặc sử dụng ngoài chương trình HOMI365. HOMI365 có quyền điều chỉnh hoặc thu hồi điểm phát sinh từ đơn hàng gian lận, không hợp lệ, hoàn tiền hoặc vi phạm thể lệ.",
        ]},
        {"h": "6. TRÁCH NHIỆM CỦA THÀNH VIÊN", "items": [
            "Thành viên cung cấp thông tin chính xác, bảo mật tài khoản và sử dụng chương trình đúng mục đích. Không tạo đơn hàng khống, mạo danh, sử dụng thông tin của người khác, mua bán tài khoản hoặc đưa ra thông tin sai lệch về sản phẩm/dịch vụ.",
        ]},
        {"h": "7. TẠM KHÓA VÀ CHẤM DỨT", "items": [
            "HOMI365 có quyền tạm khóa tài khoản, dừng ghi nhận hoặc thu hồi điểm chưa quy đổi nếu phát hiện gian lận hoặc vi phạm Chính sách. Thành viên có thể chấm dứt tham gia theo quy trình của HOMI365.",
        ]},
        {"h": "8. ĐIỀU CHỈNH CHƯƠNG TRÌNH", "items": [
            "HOMI365 có thể điều chỉnh mức ưu đãi, tỷ lệ điểm, ngưỡng hạng hoặc điều kiện chương trình. Nội dung thay đổi được công bố trước khi áp dụng và không làm ảnh hưởng trái pháp luật đến quyền đã phát sinh của Thành viên.",
        ]},
        {"h": "9. THÔNG TIN VÀ KHIẾU NẠI", "items": [
            "Mọi yêu cầu tra soát điểm, hạng Thành viên hoặc khiếu nại được tiếp nhận qua:",
            {"list": [_CONTACT[0]] + _CONTACT[2:]},
            "Chính sách này áp dụng cùng Điều kiện giao dịch chung và Chính sách bảo mật, bảo vệ dữ liệu cá nhân của HOMI365.",
        ]},
    ],
}

DOCS = [MEMBER, PURCHASE]


# ---------------------------------------------------------------------------
# Khung đọc trong form (font nhỏ, style inline vì mockup KH không có class).
# ---------------------------------------------------------------------------
_T = '<div style="font-size:13px;font-weight:700;color:var(--c1);text-align:center">'
_SUB = '<div style="font-size:11px;font-style:italic;color:var(--c5);text-align:center;margin:var(--s2) 0 var(--s4)">'
_H = '<div style="font-weight:700;color:var(--c2);margin:var(--s5) 0 var(--s2)">'
_P = '<p style="margin:0 0 var(--s3)">'
_UL = '<ul style="margin:0 0 var(--s3);padding-left:20px">'
_OL = '<ol style="margin:0 0 var(--s3);padding-left:22px">'
_LI = '<li style="margin-bottom:2px">'


def _block(it):
    if isinstance(it, str):
        return _P + it + '</p>'
    if "list" in it:
        return _UL + "".join(_LI + t + '</li>' for t in it["list"]) + '</ul>'
    if "steps" in it:
        return _OL + "".join(_LI + t + '</li>' for t in it["steps"]) + '</ol>'
    raise ValueError(it)


def html(doc):
    out = "".join(_T + h + '</div>' for h in doc["heads"])
    out += _SUB + doc["intro"] + '</div>'
    for sec in doc["sections"]:
        out += _H + sec["h"] + '</div>' + "".join(_block(i) for i in sec["items"])
    if doc.get("sign"):
        out += ('<div style="margin-top:var(--s5);text-align:right;font-size:11px;'
                'color:var(--c5)">' + doc["sign"] + '</div>')
    return out


# ---------------------------------------------------------------------------
# Trang policy.html — nối vào POLICIES, đặt lên đầu danh mục.
# ---------------------------------------------------------------------------
def policy_js():
    objs = []
    for d in DOCS:
        secs = [dict(x) for x in d["sections"]]
        if d.get("sign"):
            secs[-1] = dict(secs[-1], items=secs[-1]["items"] + [d["sign"]])
        o = {"id": d["id"], "title": d["title"], "heading": d["h1"],
             "intro": d["intro"], "official": True, "sections": secs}
        objs.append(o)
    body = ",\n".join(json.dumps(o, ensure_ascii=False, indent=2) for o in objs)
    return ("\n\n/* --- HOMI365 gửi 08/10/2026, hiệu lực từ " + EFFECTIVE + ": Chính sách ưu đãi\n"
            "   thành viên + Chính sách mua hàng & bảo mật dữ liệu (sinh từ\n"
            "   tools/policy_docs.py — đừng sửa tay). Đặt lên đầu danh mục. */\n"
            "POLICIES.unshift(\n" + body + "\n);\n")
