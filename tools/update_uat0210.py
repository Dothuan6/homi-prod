# -*- coding: utf-8 -*-
"""
update_uat0210.py — các thay đổi giao diện sau buổi UAT 02/10/2026.

Hai đợt: 06/10 (mục 1–7, 10, 11, 22 — mục 1–6 ở dưới) và 08/10 theo phản hồi
của KH ở sheet Change Request (mục 7 cuối file — làm hết các mục còn lại, làm
lại mục 1 và 5, đổi luồng duyệt đổi điểm sang 1 lớp, thêm màn B9).

Nguồn yêu cầu: sheet "Plan Update" trong Google Sheet "[Homi] - Change Request".
Đợt 06/10 chỉ làm các mục KHÔNG bị chặn: 1, 2, 3, 4, 5, 6, 7, 10, 11, 22
(mục 16 và 19 không có gì phải sửa trên giao diện). Các mục còn lại chờ khách
hàng trả lời H2–H5 nên chưa đụng tới.

File này được `build-v3.py` nạp vào. Tách riêng để bảng vá cũ trong
`build-v3.py` giữ nguyên, và để gỡ cả đợt chỉ cần bỏ 6 lời gọi `uat.*`.

Khác hai bảng vá cũ ở hai điểm:

  * Neo là chuỗi ở ĐẦU RA CUỐI (đã đổi màu, đã đổi tên vai), không phải chuỗi
    trong mockup gốc — chạy sau cùng nên không sợ bản vá khác sửa mất neo.
  * Neo không khớp là DỪNG build, kể cả với markup. Bảng BG_PATCHES cũ im lặng
    khi trượt neo và đã từng làm thiếu cột mà build vẫn báo "Xong".
"""

# ============================================================================
# 0. TIỆN ÍCH
# ============================================================================

_INFO = ('font-size:12px;color:var(--c4);background:rgba(30,58,102,.07);'
         'border:1px solid rgba(30,58,102,.3);border-radius:var(--r-md);'
         'padding:var(--s4) var(--s5);line-height:1.6')
_INP = ('height:44px;padding:0 var(--s5);border:1px solid rgba(154,163,176,.6);'
        'border-radius:var(--r-md);font-size:14px')
_FOCUS = 'border-color:#1E3A66;box-shadow:0 0 0 3px rgba(30,58,102,.25)'
_BTN_P = ('height:44px;background:var(--c6);color:var(--c12);border:none;'
          'border-radius:var(--r-md);font-size:15px;font-weight:600')
_BTN_G = ('height:44px;background:var(--c12);color:var(--c2);'
          'border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);'
          'font-size:15px;font-weight:600')
_HOVER_P = 'background:#1B3358'
_HOVER_G = 'background:rgba(154,163,176,.08)'
_OVERLAY = ('position:fixed;inset:0;background:rgba(43,48,58,.5);display:flex;'
            'align-items:center;justify-content:center;z-index:250;'
            'padding:var(--s7)')


# ============================================================================
# 1. MARKUP
# ============================================================================

# ---- Mục 1: ô nhập SĐT ở đầu trang, form khoá bên dưới (A1) -------------
# Bản 06/10 dựng thành một màn riêng. KH điều chỉnh: vào trang vẫn thấy form
# mua hàng nhưng bị khoá, ô nhập SĐT đặt ở đầu trang.
_A1_OPEN_OLD = (
    '  <sc-if value="{{isA1}}" hint-placeholder-val="{{true}}">\n'
    '  <div style="display:flex;justify-content:center;padding:var(--s8) var(--s7) var(--s10);background:var(--warm-50)">\n'
    '    <div style="width:100%;max-width:1160px;display:grid;grid-template-columns:1fr 380px;gap:var(--s8);align-items:start">')
# (08/10, lần 2) KH: ô SĐT nằm NGAY TRÊN THANH HEADER, không thêm hàng nào —
# chỉ ô số điện thoại + nút Tiếp tục, đặt sát bên phải logo; nút "Đăng nhập
# thành viên HOMI365" vẫn giữ ở góc phải.
# Lỗi nhập hiện ngay dưới ô; SĐT đã có tài khoản thì bật khung gợi ý thả xuống
# dưới ô (không chiếm hàng). Đã mở form thì ô hiện số đang dùng + nút Đổi số.
# build-v3.py dựng thanh trên riêng cho A1 bằng A1_HEADER_PHONE.
A1_HEADER_PHONE = (
    '<div class="homi-buyphone" style="margin-left:var(--s9);position:relative;display:flex;gap:var(--s3);align-items:center;flex:none">'
    # (10/10) KH: câu hướng dẫn đặt ngay trước ô SĐT.
    '<div class="homi-buyphone-lbl" style="max-width:200px;font-size:13px;line-height:1.4;color:var(--c2);margin-right:var(--s2)">'
    'Vui lòng nhập số điện thoại để kiểm tra tài khoản</div>'
    '<div class="homi-buyphone-in" style="position:relative">'
    '<input type="text" inputmode="numeric" maxlength="10" placeholder="Số điện thoại (090xxxxxxx)" '
    'value="{{buyHeaderPhone}}" disabled="{{buyUnlocked}}" sc-camel-on-change="{{setBuyPhoneInput}}" '
    'style="width:240px;max-width:100%;height:40px;padding:0 var(--s5);border:1px solid {{buyPhoneBorder}};'
    'border-radius:var(--r-md);font-size:15px;background:var(--c12)" style-focus="' + _FOCUS + '">'
    '<sc-if value="{{buyPhoneError}}" hint-placeholder-val="{{false}}">'
    '<div style="position:absolute;top:100%;left:0;margin-top:4px;white-space:nowrap;font-size:12px;color:var(--err)">{{buyPhoneError}}</div>'
    '</sc-if>'
    # (10/10) SĐT chưa có tài khoản -> báo ngay dưới ô, form mở để nhập.
    '<sc-if value="{{buyPhoneNewNote}}" hint-placeholder-val="{{false}}">'
    '<div class="homi-buyphone-ok" style="position:absolute;top:100%;left:0;margin-top:4px;white-space:nowrap;font-size:12px;font-weight:600;color:#2F7A48">'
    'Anh chị chưa có tài khoản, vui lòng nhập thông tin để mua hàng</div>'
    '</sc-if></div>'
    '<sc-if value="{{buyHeaderAsk}}" hint-placeholder-val="{{true}}">'
    '<button sc-camel-on-click="{{submitBuyPhone}}" style="' + _BTN_P + ';height:40px;padding:0 var(--s7)" style-hover="' + _HOVER_P + '">Tiếp tục</button>'
    '</sc-if>'
    '<sc-if value="{{buyUnlocked}}" hint-placeholder-val="{{false}}">'
    '<button sc-camel-on-click="{{buyChangePhone}}" style="' + _BTN_G + ';height:40px;padding:0 var(--s6)" style-hover="' + _HOVER_G + '">Đổi số</button>'
    '</sc-if>'
    '<sc-if value="{{buyPhoneFound}}" hint-placeholder-val="{{false}}">'
    '<div class="homi-buyphone-pop" style="position:absolute;top:calc(100% + 10px);left:0;width:380px;max-width:calc(100vw - 32px);'
    'background:var(--c12);border:1px solid rgba(30,58,102,.3);border-radius:var(--r-md);box-shadow:0 8px 28px rgba(30,58,102,.18);'
    'padding:var(--s5) var(--s6);display:flex;flex-direction:column;gap:var(--s4);z-index:60">'
    # (10/10, lần 2) KH bỏ tiêu đề "Anh chị đã có tài khoản" — chỉ giữ hướng dẫn + nút.
    '<div>'
    '<div style="font-size:13px;color:var(--c2);line-height:1.6">Đăng nhập để form tự điền theo đơn gần nhất, hoặc bỏ qua và tự điền.</div></div>'
    '<div style="display:flex;gap:var(--s3);flex-wrap:wrap;align-items:center">'
    '<button sc-camel-on-click="{{buyGoLogin}}" style="' + _BTN_P + ';height:38px;padding:0 var(--s6)" style-hover="' + _HOVER_P + '">Đăng nhập</button>'
    '<button sc-camel-on-click="{{buySkipLogin}}" style="' + _BTN_G + ';height:38px;padding:0 var(--s5)" style-hover="' + _HOVER_G + '">Bỏ qua và tự điền</button>'
    '<button sc-camel-on-click="{{buyResetPhone}}" style="background:none;border:none;font-size:13px;font-weight:600;color:var(--c6);padding:var(--s2)">Dùng số khác</button>'
    '</div></div></sc-if></div>')
_A1_OPEN_NEW = (
    '  <sc-if value="{{isA1}}" hint-placeholder-val="{{true}}">\n'
    '  <div style="display:flex;flex-direction:column;align-items:center;gap:var(--s7);padding:var(--s8) var(--s7) var(--s10);background:var(--warm-50)">\n'
    '    <div style="width:100%;max-width:1160px;display:grid;grid-template-columns:1fr 380px;gap:var(--s8);align-items:start;{{buyLockCss}}">')

# ---- Mục 2: dòng nhắc tự điền + "Mua cho người khác" (A1) -----------------
A1_AUTOFILL_NOTE = """
          <sc-if value="{{buyIsSelf}}" hint-placeholder-val="{{false}}">
            <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--s4);""" + _INFO + """\"><div style="flex:1;min-width:200px">Đã điền theo đơn ngày <strong>{{buyProfileDate}}</strong> ({{buyProfileOrder}}). Bạn sửa trực tiếp được nếu thông tin đã thay đổi.</div><button sc-camel-on-click="{{buyForOther}}" style="flex:none;height:32px;padding:0 var(--s5);background:var(--c12);border:1px solid #1E3A66;border-radius:var(--r-sm);font-size:12px;font-weight:700;color:#1E3A66;white-space:nowrap">Mua cho người khác</button></div>
          </sc-if>
          <sc-if value="{{buyIsOther}}" hint-placeholder-val="{{false}}">
            <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--s4);""" + _INFO + """\"><div style="flex:1;min-width:200px">Đang nhập thông tin cho <strong>người khác</strong>. Phần tự điền đã được xoá.</div><button sc-camel-on-click="{{buyForSelf}}" style="flex:none;height:32px;padding:0 var(--s5);background:var(--c12);border:1px solid #1E3A66;border-radius:var(--r-sm);font-size:12px;font-weight:700;color:#1E3A66;white-space:nowrap">Dùng lại thông tin của tôi</button></div>
          </sc-if>
"""

_A1_TITLE = ('<div style="font-size:18px;font-weight:700;color:var(--c1)">'
             'Thông tin nhận hàng</div>')

# ---- Mục 3: kiểm tra tuổi 18–100 (A1) --------------------------------------
_A1_DOB_OLD = (
    '<label style="font-size:14px;font-weight:600;color:var(--c2)">Ngày sinh</label>'
    '<input type="text" placeholder="22/01/1991" inputmode="numeric" maxlength="10" '
    'value="{{buyerDob}}" sc-camel-on-change="{{setBuyerDob}}" '
    'style="height:44px;padding:0 var(--s5);border:1px solid rgba(154,163,176,.6);'
    'border-radius:var(--r-md);font-size:14px" '
    'style-focus="border-color:#1E3A66;box-shadow:0 0 0 3px rgba(30,58,102,.25)"></div>')
_A1_DOB_NEW = (
    '<label style="font-size:14px;font-weight:600;color:var(--c2)">Ngày sinh</label>'
    '<input type="text" placeholder="22/01/1991" inputmode="numeric" maxlength="10" '
    'value="{{buyerDob}}" sc-camel-on-change="{{setBuyerDob}}" '
    'style="height:44px;padding:0 var(--s5);border:1px solid {{buyerDobBorder}};'
    'border-radius:var(--r-md);font-size:14px" '
    'style-focus="border-color:#1E3A66;box-shadow:0 0 0 3px rgba(30,58,102,.25)">'
    '<sc-if value="{{buyerDobError}}" hint-placeholder-val="{{false}}">'
    '<div style="font-size:12px;color:var(--err)">{{buyerDobError}}</div>'
    '</sc-if></div>')

# ---- Mục 5: khoá ô đồng ý đến khi bấm link chính sách (A1) ----------------
_A1_TC_OLD = (
    '<input type="checkbox" checked="{{buyTcChecked}}" '
    'sc-camel-on-change="{{toggleBuyTc}}" '
    'style="margin-top:3px;flex:none;width:16px;height:16px;accent-color:#1E3A66">'
    '<span>Bằng cách đăng ký mua hàng và thanh toán, bạn đã đồng ý với '
    '<a href="policy.html?s=quy-che-website" style="color:#1E3A66;font-weight:600">'
    'Điều khoản sử dụng</a> và '
    '<a href="policy.html?s=bao-mat-thong-tin" style="color:#1E3A66;font-weight:600">'
    'Chính sách bảo mật</a> của HOMI365.</span>')
# KH điều chỉnh mục 5: không mở khoá bằng bấm link nữa — hiện luôn khung nội
# dung chính sách ngay trong form, khách KÉO XUỐNG ĐỌC HẾT mới tick được. Hai
# link bỏ class tnc-link để bấm vào không mở khoá; vẫn mở bản đầy đủ ở tab mới.
_P = '<p style="margin:0 0 var(--s3)">'
_H = '<div style="font-weight:700;color:var(--c2);margin:var(--s4) 0 var(--s2)">'
# (08/10) Nội dung = toàn văn "Chính sách mua hàng và Chính sách bảo mật và bảo
# vệ dữ liệu cá nhân" KH gửi (hiệu lực 01/10/2026) — nguồn ở policy_docs.py.
import policy_docs as pdoc
A1_POLICY_BOX = (
    '<div class="tnc-doc" style="height:240px;overflow-y:auto;border:1px solid rgba(154,163,176,.45);'
    'border-radius:var(--r-md);padding:var(--s4) var(--s5);font-size:12px;line-height:1.7;'
    'color:var(--c4);background:rgba(154,163,176,.05)">'
    + pdoc.html(pdoc.PURCHASE) +
    '<div style="margin-top:var(--s4);padding-top:var(--s3);border-top:1px solid rgba(154,163,176,.3);font-size:11px;color:var(--c5)">'
    'Hết nội dung. Xem bản đầy đủ ở trang riêng: '
    '<a href="policy.html?s=chinh-sach-mua-hang" target="_blank" style="color:#1E3A66;font-weight:600">Chính sách mua hàng &amp; bảo mật dữ liệu</a></div>'
    '</div>')
# (08/10) KH bỏ dòng nhắc "Kéo xuống đọc hết…" — ô đồng ý mờ sẵn là đủ.
_A1_TC_NEW = (
    '<input type="checkbox" class="tnc-agree" disabled checked="{{buyTcChecked}}" '
    'sc-camel-on-change="{{toggleBuyTc}}" '
    'style="margin-top:3px;flex:none;width:16px;height:16px;accent-color:#1E3A66;'
    'opacity:.4;cursor:not-allowed">'
    '<span>Tôi đã đọc và đồng ý với '
    '<a href="policy.html?s=chinh-sach-mua-hang" target="_blank" '
    'style="color:#1E3A66;font-weight:600">Chính sách mua hàng và Chính sách bảo mật, '
    'bảo vệ dữ liệu cá nhân</a> của HOMI365.</span>')
# Khung chính sách đặt ngay trên ô đồng ý.
_A1_TC_LABEL = ('<label style="display:flex;gap:var(--s3);align-items:flex-start;cursor:pointer;'
                'font-size:12px;color:var(--c2);line-height:1.6">' + _A1_TC_OLD)

# ---- Mục 1: C1 biết mình được gọi từ form mua hàng -------------------------
_C1_HEAD_OLD = ('<div style="font-size:22px;font-weight:700;color:var(--c1);'
                'line-height:1.4">Đăng nhập để xem điểm thưởng và ưu đãi của bạn'
                '</div></div>')
_C1_HEAD_NEW = (
    '<div style="font-size:22px;font-weight:700;color:var(--c1);line-height:1.4">'
    '{{loginHeading}}</div>'
    '<sc-if value="{{loginFromBuy}}" hint-placeholder-val="{{false}}">'
    '<div style="font-size:13px;color:var(--c5);margin-top:var(--s3);line-height:1.6">'
    'Đăng nhập xong bạn quay lại form mua hàng, thông tin được điền sẵn theo đơn '
    'gần nhất.</div>'
    '<button sc-camel-on-click="{{backToBuy}}" style="background:none;border:none;'
    'font-size:13px;font-weight:600;color:var(--c6);margin-top:var(--s2);'
    'padding:var(--s2)">Bỏ qua, quay lại form mua hàng</button>'
    '</sc-if></div>')

# ---- Mục 6: bỏ trạng thái chờ kích hoạt (A2, A3) ---------------------------
_A2_DONE_OLD = ('Ngay lập tức, bạn có thể giới thiệu khách hàng tham gia sản phẩm.'
                '<br>Điểm thưởng và ưu đãi sẽ tạm giữ cho tới khi Quản trị viên '
                'kích hoạt thành công.')
_A2_DONE_NEW = ('Bạn giới thiệu khách hàng và gửi yêu cầu đổi điểm được ngay.'
                '<br>Điểm HOMI của mỗi đơn được ghi nhận '
                'sau khi đơn đó được Quản trị viên duyệt.')

_TNC_OLD = ('Điểm chỉ được cộng sau khi tài khoản Thành viên đã được kích hoạt; '
            'các đơn phát sinh trước thời điểm kích hoạt vẫn được tính và cộng bù '
            'đầy đủ.')
_TNC_NEW = ('Điểm của mỗi đơn được cộng ngay sau khi đơn đó được HOMI365 duyệt; '
            'Thành viên dùng được link giới thiệu và gửi yêu cầu đổi điểm ngay sau '
            'khi đăng ký.')

# Banner "CHỜ KÍCH HOẠT" ở A3: cắt cả khối theo hai mốc đầu / cuối.
_A3_BANNER_START = '      <sc-if value="{{isNewAgent}}" hint-placeholder-val="{{false}}">'
_A3_BANNER_END = ('Chưa thể rút tiền — chờ kích hoạt</button>\n'
                  '      </div>\n      </sc-if>\n')

_A3_NOTE_OLD = ('Yêu cầu rút tiền đang ở trạng thái <strong>chờ duyệt</strong> hoặc '
                '<strong>đã duyệt</strong> sẽ được tạm giữ và trừ khỏi số dư khả '
                'dụng, cho tới khi chi trả xong hoặc bị từ chối. Bị từ chối thì '
                'tiền hoàn lại số dư khả dụng.')
_A3_NOTE_NEW = ('Yêu cầu đổi điểm đang <strong>chờ duyệt</strong> hoặc '
                '<strong>đã duyệt</strong> được trừ khỏi số dư khả dụng cho tới '
                'khi chi trả xong. Yêu cầu bị từ chối thì điểm được cộng lại vào '
                'số dư khả dụng.')

_A3_PENDING_ORDERS = (
    '        <sc-if value="{{hasPendingOrders}}" hint-placeholder-val="{{false}}">\n'
    '          <div style="' + _INFO + '">Bạn có <strong>{{pendingOrderCount}} đơn'
    '</strong> đang chờ Quản trị viên duyệt. Điểm HOMI của đơn được ghi nhận ngay '
    'sau khi đơn được duyệt.</div>\n'
    '        </sc-if>\n')

# ---- Mục 10: xuất danh sách chi trả (B3) ------------------------------------
_B3_EXPORT_OLD = (
    '<div style="font-size:24px;font-weight:700">Yêu cầu rút tiền</div>\n'
    '            <button style="height:38px;padding:0 var(--s6);background:var(--c12);'
    'border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px;'
    'font-weight:600;color:var(--c2)" style-hover="background:rgba(154,163,176,.08)">'
    'Xuất file Excel</button>')

_PO_COLS = "1.3fr 1.1fr 1fr .8fr .9fr"
B3_EXPORT_NEW = (
    '<div style="font-size:24px;font-weight:700">Yêu cầu rút tiền</div>\n'
    '            <button sc-camel-on-click="{{openPayoutExport}}" style="height:38px;'
    'padding:0 var(--s6);background:var(--c6);border:none;border-radius:var(--r-md);'
    'font-size:13px;font-weight:600;color:var(--c12)" style-hover="' + _HOVER_P + '">'
    'Xuất danh sách chi trả</button>\n'
    """
            <!-- (21) MODAL: xuất danh sách chi trả theo kỳ — bổ sung sau UAT 02/10 -->
            <sc-if value="{{showPayoutExport}}" hint-placeholder-val="{{false}}">
              <div style=\"""" + _OVERLAY + """\">
                <div style="width:100%;max-width:640px;max-height:92vh;overflow:auto;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div><div style="font-size:18px;font-weight:700;color:var(--c1)">Xuất danh sách chi trả</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">Mỗi kỳ xuất một file Excel để gửi ngân hàng chi.</div></div>
                    <button sc-camel-on-click="{{closePayoutExport}}" style="background:none;border:none;font-size:18px;color:var(--c5)">✕</button>
                  </div>
                  <div style="display:flex;flex-direction:column;gap:var(--s3)">
                    <div style="font-size:12px;font-weight:600;color:var(--c5)">Kỳ chi trả</div>
                    <div style="display:flex;gap:var(--s2);flex-wrap:wrap">
                      <sc-for list="{{payoutPeriods}}" as="pp" hint-placeholder-count="3">
                        <button sc-camel-on-click="{{pp.onClick}}" style="{{pp.style}}">{{pp.label}}</button>
                      </sc-for>
                    </div>
                  </div>
                  <div style=\"""" + _INFO + """\">File gồm 5 cột: <strong>Tên chủ tài khoản · Số tài khoản · Ngân hàng · Số điểm · Số tiền</strong>. Chỉ lấy các yêu cầu <strong>đã duyệt đủ 2 bước</strong> và chưa chi của kỳ được chọn.</div>
                  <div style="border:1px solid rgba(154,163,176,.35);border-radius:var(--r-md);overflow:auto">
                    <div style="display:grid;grid-template-columns:""" + _PO_COLS + """;min-width:560px;background:rgba(154,163,176,.08);padding:var(--s4) var(--s5);font-size:11px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em">
                      <div>Tên chủ tài khoản</div><div>Số tài khoản</div><div>Ngân hàng</div><div style="text-align:right">Số điểm</div><div style="text-align:right">Số tiền</div>
                    </div>
                    <sc-for list="{{payoutRows}}" as="pr" hint-placeholder-count="2">
                      <div style="display:grid;grid-template-columns:""" + _PO_COLS + """;min-width:560px;align-items:center;padding:var(--s4) var(--s5);font-size:13px;color:var(--c1);border-top:1px solid rgba(154,163,176,.2)">
                        <div style="font-weight:600">{{pr.accountHolder}}</div><div style="font-family:monospace;color:var(--c4)">{{pr.accountNumber}}</div><div style="color:var(--c4)">{{pr.bankName}}</div><div style="text-align:right">{{pr.points}}</div><div style="text-align:right;font-weight:700">{{pr.amount}}</div>
                      </div>
                    </sc-for>
                    <sc-if value="{{payoutEmpty}}" hint-placeholder-val="{{false}}">
                      <div style="padding:var(--s7);text-align:center;color:var(--c5);font-size:13px">Kỳ này không có yêu cầu nào đã duyệt chờ chi.</div>
                    </sc-if>
                  </div>
                  <div style="display:flex;justify-content:space-between;gap:var(--s5);font-size:13px;color:var(--c2)"><span>Kỳ {{payoutPeriod}} · {{payoutCount}} yêu cầu</span><span>Tổng chi: <strong style="color:var(--c1)">{{payoutTotal}}</strong></span></div>
                  <sc-if value="{{payoutExported}}" hint-placeholder-val="{{false}}">
                    <div style="font-size:13px;color:#2F7A48;background:rgba(47,122,72,.12);border-radius:var(--r-md);padding:var(--s5)">Đã xuất <strong>{{payoutExported}}</strong> · {{payoutCount}} yêu cầu.</div>
                  </sc-if>
                  <div style="display:flex;gap:var(--s3)">
                    <button sc-camel-on-click="{{closePayoutExport}}" style="flex:1;""" + _BTN_G + """;font-size:14px">Đóng</button>
                    <button sc-camel-on-click="{{runPayoutExport}}" disabled="{{payoutEmpty}}" style="{{payoutBtnStyle}}">Xuất file Excel</button>
                  </div>
                </div>
              </div>
            </sc-if>""")

# ---- Mục 11: chi không thành công + hoàn điểm (B3) --------------------------
_B3_PAID_BTN_OLD = (
    '<button sc-camel-on-click="{{openPaidModal}}" style="height:42px;'
    'background:var(--c12);color:var(--c6);border:1px solid var(--c6);'
    'border-radius:var(--r-md);font-size:14px;font-weight:600" '
    'style-hover="background:rgba(30,58,102,.06)">Đánh dấu đã chi trả</button>\n'
    '        </sc-if>\n')
B3_PAID_BTN_NEW = (
    _B3_PAID_BTN_OLD.replace(
        '</button>\n        </sc-if>\n',
        '</button>\n'
        '          <button sc-camel-on-click="{{openPayFailModal}}" style="height:42px;'
        'background:var(--c12);color:var(--err);border:1px solid var(--err);'
        'border-radius:var(--r-md);font-size:14px;font-weight:600" '
        'style-hover="background:rgba(192,57,43,.06)">Ngân hàng chi không thành công'
        '</button>\n        </sc-if>\n')
    + '        <sc-if value="{{selectedWithdrawal.canRefund}}" hint-placeholder-val="{{false}}">\n'
      '          <button sc-camel-on-click="{{openRefundModal}}" style="height:42px;'
      'background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);'
      'font-size:14px;font-weight:600" style-hover="' + _HOVER_P + '">Hoàn điểm</button>\n'
      '        </sc-if>\n'
      '        <sc-if value="{{selectedWithdrawal.hasFailNote}}" hint-placeholder-val="{{false}}">\n'
      '          <div style="font-size:13px;color:var(--err);background:rgba(192,57,43,.08);'
      'border-radius:var(--r-md);padding:var(--s5)"><strong>Ngân hàng trả về:</strong> '
      '{{selectedWithdrawal.failNote}}</div>\n'
      '        </sc-if>\n'
      '        <sc-if value="{{selectedWithdrawal.hasRefundReason}}" hint-placeholder-val="{{false}}">\n'
      '          <div style="font-size:13px;color:var(--c4);background:rgba(30,58,102,.08);'
      'border-radius:var(--r-md);padding:var(--s5)"><strong>Lý do hoàn điểm:</strong> '
      '{{selectedWithdrawal.refundReason}}</div>\n'
      '        </sc-if>\n')

_MODAL_PAID_ANCHOR = '        <sc-if value="{{isPaidModal}}" hint-placeholder-val="{{false}}">'
B3_NEW_MODALS = """        <!-- (22) Chi không thành công + hoàn điểm — bổ sung sau UAT 02/10 -->
        <sc-if value="{{isPayFailModal}}" hint-placeholder-val="{{false}}">
          <div style="font-size:18px;font-weight:700;color:var(--c1)">Ngân hàng chi không thành công</div>
          <div style="font-size:14px;color:var(--c2);line-height:1.6">Ghi nhận khoản chi <strong>{{actionWithdrawal.amount}}</strong> cho <strong>{{actionWithdrawal.seller}}</strong> bị ngân hàng trả về? Yêu cầu chuyển sang <strong>Chi không thành công</strong>; điểm chưa được trả lại cho tới khi bạn bấm Hoàn điểm.</div>
          <div style="display:flex;flex-direction:column;gap:var(--s2)">
            <label style="font-size:12px;font-weight:600;color:var(--c5)">Nội dung ngân hàng trả về (tuỳ chọn)</label>
            <input type="text" placeholder="VD: Số tài khoản không tồn tại" value="{{paidNote}}" sc-camel-on-change="{{setPaidNote}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px" style-focus=\"""" + _FOCUS + """\">
          </div>
          <div style="display:flex;gap:var(--s3)">
            <button sc-camel-on-click="{{closeActionModal}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Hủy</button>
            <button sc-camel-on-click="{{confirmPayFail}}" style="flex:1;height:44px;background:var(--err);color:var(--c12);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600">Xác nhận</button>
          </div>
        </sc-if>

        <sc-if value="{{isRefundModal}}" hint-placeholder-val="{{false}}">
          <div style="font-size:18px;font-weight:700;color:var(--c1)">Hoàn điểm</div>
          <div style="font-size:14px;color:var(--c2);line-height:1.6">Cộng lại <strong>{{actionWithdrawal.amount}}</strong> vào số dư khả dụng của <strong>{{actionWithdrawal.seller}}</strong>. Thành viên tạo được yêu cầu đổi điểm mới sau khi sửa thông tin tài khoản.</div>
          <div style="display:flex;flex-direction:column;gap:var(--s2)">
            <label style="font-size:12px;font-weight:600;color:var(--c5)">Lý do hoàn điểm (*)</label>
            <textarea placeholder="VD: Ngân hàng trả về, sai số tài khoản" value="{{rejectReason}}" sc-camel-on-change="{{setRejectReason}}" style="min-height:90px;padding:var(--s5);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px;resize:vertical"></textarea>
          </div>
          <div style=\"""" + _INFO + """\">Khi xác nhận, hệ thống gửi email báo cho thành viên rằng tài khoản nhận tiền có vấn đề, và ghi thao tác này vào Nhật ký hệ thống.</div>
          <div style="display:flex;gap:var(--s3)">
            <button sc-camel-on-click="{{closeActionModal}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Hủy</button>
            <button sc-camel-on-click="{{confirmRefund}}" disabled="{{rejectDisabled}}" style="{{refundConfirmStyle}}">Hoàn điểm</button>
          </div>
        </sc-if>

"""

# ---- Mục 22: nhắc gửi email khi admin sửa hồ sơ (B2) ------------------------
_B2_PF_BTNS_OLD = ('              <div style="display:flex;gap:var(--s4)">\n'
                   '                <button sc-camel-on-click="{{cancelProfileEdit}}"')
B2_PF_BTNS_NEW = ('              <div style="' + _INFO + '">{{pfMailNote}}</div>\n'
                  + _B2_PF_BTNS_OLD)

_B2_PF_EDIT_BTN_OLD = '              <button sc-camel-on-click="{{startProfileEdit}}"'
B2_PF_EDIT_BTN_NEW = (
    '              <sc-if value="{{profileSavedNote}}" hint-placeholder-val="{{false}}">\n'
    '                <div style="font-size:12px;color:#2F7A48;background:rgba(47,122,72,.12);'
    'border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">{{profileSavedNote}}</div>\n'
    '              </sc-if>\n' + _B2_PF_EDIT_BTN_OLD)

# (neo, thay bằng[, chỉ áp cho các khối này]). Form đăng ký A2 dùng lại đúng
# các ô Tỉnh / Phường / Ngày sinh của A1, nên bản vá riêng cho form mua hàng
# phải khoá vào khối A1 — nếu không dấu (*) ở A2 cũng mất theo.
MARKUP = [
    # --- A1 ---
    (_A1_OPEN_OLD, _A1_OPEN_NEW),
    # (08/10) Bỏ dòng "Đã điền theo đơn…" + nút "Mua cho người khác": không có
    # trong yêu cầu KH (mục 2 chỉ cần tự điền theo đơn trước).
    (_A1_DOB_OLD, _A1_DOB_NEW, ("A1",)),
    ('>Tỉnh/Thành phố (*)</label>\n              <div style="position:relative">\n'
     '                <input type="text" value="{{provinceQuery}}"',
     '>Tỉnh/Thành phố</label>\n              <div style="position:relative">\n'
     '                <input type="text" value="{{provinceQuery}}"', ("A1",)),
    ('>Phường/Xã (*)</label>\n              <div style="position:relative">\n'
     '                <input type="text" value="{{wardQuery}}"',
     '>Phường/Xã</label>\n              <div style="position:relative">\n'
     '                <input type="text" value="{{wardQuery}}"', ("A1",)),
    (_A1_TC_LABEL, A1_POLICY_BOX + '\n          ' + _A1_TC_LABEL.replace(_A1_TC_OLD, _A1_TC_NEW)),
    # (06/10, bổ sung) Ba ô nhận ưu đãi ở form MUA HÀNG không còn bắt buộc:
    # người chỉ mua, không làm thành viên thì chưa cần khai tài khoản. Form
    # đăng ký thành viên (A2) vẫn bắt buộc vì đó là nơi nhận chi trả.
    ('>Ngân hàng (*)</label>', '>Ngân hàng</label>', ("A1",)),
    # (09/10) KH: ô Địa chỉ ở form mua hàng cũng không bắt buộc.
    ('>Địa chỉ (*)</label>', '>Địa chỉ</label>', ("A1",)),
    ('>Số tài khoản (*)</label><input type="text" placeholder="Nhập số tài khoản" '
     'value="{{buyerBankAccount}}"',
     '>Số tài khoản</label><input type="text" placeholder="Nhập số tài khoản" '
     'value="{{buyerBankAccount}}"', ("A1",)),
    ('>Tên chủ tài khoản (*)</label>', '>Tên chủ tài khoản</label>', ("A1",)),
    # --- C1 ---
    (_C1_HEAD_OLD, _C1_HEAD_NEW),
    # --- A2 ---
    (_A2_DONE_OLD, _A2_DONE_NEW),
    ('style="{{regSubmitStyle}}">Xác nhận &amp; kích hoạt</button>',
     'style="{{regSubmitStyle}}">Xác nhận &amp; hoàn tất đăng ký</button>'),
    # (_TNC_OLD, _TNC_NEW) bỏ 08/10: khung A2 thay bằng toàn văn chính sách KH gửi.
    # --- A3 ---
    ('      <sc-if value="{{isActiveAgent}}" hint-placeholder-val="{{true}}">',
     '      <sc-if value="{{isA3}}" hint-placeholder-val="{{true}}">'),
    ('>Đang chờ duyệt · tạm giữ</div>', '>Đang chờ duyệt</div>'),
    ('<div style="font-size:12px;color:var(--c5)">Đã rút</div>',
     '<div style="font-size:12px;color:var(--c5)">Đã đổi</div>'),
    ('<div style="font-size:12px;color:var(--c5)">Đã rút (tổng)</div>',
     '<div style="font-size:12px;color:var(--c5)">Đã đổi (tổng)</div>'),
    (_A3_NOTE_OLD + '</div>\n', _A3_NOTE_NEW + '</div>\n' + _A3_PENDING_ORDERS),
    ('Bạn đã gửi yêu cầu rút tiền trong tháng này. Lượt rút tiếp theo khả dụng từ',
     'Bạn đã gửi yêu cầu đổi điểm trong tháng này. Lượt đổi tiếp theo khả dụng từ'),
    ('>Số tiền muốn rút</label>', '>Số điểm muốn đổi</label>'),
    ('placeholder="Nhập số tiền (đ)" value="{{withdrawAmount}}"',
     'placeholder="Nhập số điểm" value="{{withdrawAmount}}"'),
    ('            <div style="font-size:12px;color:var(--err)">{{withdrawAmountError}}</div>\n'
     '          </sc-if>\n',
     '            <div style="font-size:12px;color:var(--err)">{{withdrawAmountError}}</div>\n'
     '          </sc-if>\n'
     '          <div style="font-size:11px;color:var(--c5)">1 Điểm HOMI = 1 VNĐ</div>\n'),
    # --- B3 ---
    (_B3_EXPORT_OLD, B3_EXPORT_NEW),
    (_B3_PAID_BTN_OLD, B3_PAID_BTN_NEW),
    (_MODAL_PAID_ANCHOR, B3_NEW_MODALS + _MODAL_PAID_ANCHOR),
    ('<option>Khoá / mở khoá</option><option>Tải file lên</option>',
     '<option>Khoá / mở khoá</option><option>Hoàn điểm</option>'
     '<option>Tải file lên</option>'),
    ('Rut khoan thuong tich diem ct uu dai khach hang',
     'Doi diem thuong ct uu dai khach hang'),
    # --- B2 ---
    (_B2_PF_BTNS_OLD, B2_PF_BTNS_NEW),
    (_B2_PF_EDIT_BTN_OLD, B2_PF_EDIT_BTN_NEW),
]


def patch_blocks(blocks, die):
    """Áp MARKUP lên mọi khối. Mỗi bản vá phải khớp ít nhất một khối."""
    out = dict(blocks)
    for i, item in enumerate(MARKUP):
        old, new = item[0], item[1]
        only = item[2] if len(item) > 2 else None
        every = len(item) > 3 and item[3] == "all"
        hit = 0
        for k in out:
            if only and k not in only:
                continue
            n = out[k].count(old)
            if n > 1 and every:
                out[k] = out[k].replace(old, new)
                hit += 1
                continue
            if n > 1:
                die("bản vá UAT #%d khớp %d lần trong khối %s — neo chưa đủ "
                    "chặt:\n%s" % (i, n, k, old[:100]))
            if n == 1:
                out[k] = out[k].replace(old, new)
                hit += 1
        if not hit:
            die("bản vá UAT #%d không khớp khối nào:\n---\n%s\n---" % (i, old[:160]))

    # Mục 6: cắt banner "CHỜ KÍCH HOẠT" ở A3.
    cut = 0
    for k in out:
        a = out[k].find(_A3_BANNER_START)
        if a < 0:
            continue
        b = out[k].find(_A3_BANNER_END, a)
        if b < 0:
            die("thấy đầu banner chờ kích hoạt ở khối %s nhưng không thấy cuối" % k)
        out[k] = out[k][:a] + out[k][b + len(_A3_BANNER_END):]
        cut += 1
    if not cut:
        die("không tìm thấy banner chờ kích hoạt ở A3 để gỡ")

    # (08/10) Cắt thay nguyên khối theo cặp mốc.
    for i, (start, end, repl) in enumerate(CUTS):
        hit = 0
        for k in out:
            a = out[k].find(start)
            if a < 0:
                continue
            b = out[k].find(end, a)
            if b < 0:
                die("CUTS #%d: thấy mốc đầu ở khối %s nhưng không thấy mốc cuối" % (i, k))
            out[k] = out[k][:a] + repl + out[k][b:]
            hit += 1
        if not hit:
            die("CUTS #%d không khớp khối nào:\n%s" % (i, start[:120]))

    return {k: rename(v) for k, v in out.items()}


# ============================================================================
# 2. ĐỔI CHỮ "rút tiền" -> "đổi điểm" (mục 7)
# ============================================================================
# Chạy SAU CÙNG, trên cả markup lẫn script. Thứ tự: cụm dài trước, cụm chung sau.
RENAMES = [
    # (08/10) Mục 24 — đổi tên gói hiển thị thành HOMI365-01. Chỉ đổi TÊN;
    # mã CN02 trong SKU kho / mã gói giữ nguyên (chờ KH xác nhận).
    ("CN02 — Bác sĩ 24/7 hỗ trợ tư vấn sức khỏe", "HOMI365-01"),
    ("Gói 1 năm · CN02", "HOMI365-01 · Gói 1 năm"),
    ("Gói nửa năm · CN02-6M", "HOMI365-01 · Gói nửa năm"),
    ("name: 'Gói Bác sĩ 24/7 · kèm đồng hồ HW01'", "name: 'HOMI365-01'"),
    ('placeholder="Gói Bác sĩ 24/7 · License 12 tháng"', 'placeholder="HOMI365-01"'),
    ("— CN02</span>", "— HOMI365-01</span>"),
    # (08/10) Hotline mới theo thông tin pháp nhân HOMI365 gửi cho footer.
    ("1900 633 570", "1900 9007"),
    ("Xác nhận duyệt yêu cầu rút <strong>", "Xác nhận duyệt yêu cầu đổi <strong>"),
    ("Yêu cầu rút {{actionWithdrawal.amount}}", "Yêu cầu đổi {{actionWithdrawal.amount}}"),
    ("Yêu cầu rút tiền", "Yêu cầu đổi điểm"),
    ("yêu cầu rút tiền", "yêu cầu đổi điểm"),
    ("Rút tiền", "Đổi điểm"),
    ("rút tiền", "đổi điểm"),
]


def rename(s):
    for old, new in RENAMES:
        s = s.replace(old, new)
    return s


# ============================================================================
# 3. SCRIPT
# ============================================================================

_JS_STATE = """    selectedOrderId: null,
    // (20) Sau UAT 02/10 — bước SĐT trước form mua hàng + tự điền.
    // buyStep: 'phone' | 'form'. buyMode: '' chưa đăng nhập | 'self' đã
    // tự điền theo đơn cũ | 'other' đang mua cho người khác.
    buyStep: 'phone', buyPhoneInput: '', buyPhoneError: '', buyPhoneFound: false,
    buyMode: '', buyProfile: null, returnTo: '',
    // (21) Xuất danh sách chi trả theo kỳ.
    showPayoutExport: false, payoutPeriod: '08/2026', payoutExported: '',
    // (23) Dòng xác nhận sau khi admin lưu hồ sơ: { id, text }.
    profileSaved: null,
"""

_JS_CLASS_OLD = "  STATUS_ORDER = { pending: 0, specialist_approved: 1, approved: 2, rejected: 3, paid: 4 };"
_JS_CLASS_NEW = """  STATUS_ORDER = { pending: 0, specialist_approved: 1, approved: 2, rejected: 3, paid: 4, pay_failed: 5, refunded: 6 };
  PAYOUT_PERIODS = ['09/2026', '08/2026', '07/2026'];

  // (20) Đơn gần nhất của người đã có tài khoản — dùng để tự điền form mua
  // hàng. Bản mẫu dùng chung một hồ sơ cho mọi SĐT đã đăng ký; bản thật lấy
  // từ đơn mới nhất của chính tài khoản vừa đăng nhập.
  BUYER_LAST_ORDER = {
    orderId: 'DH100077', orderDate: '12/08/2026',
    buyerName: 'Hoàng Thị Mỹ Trinh', buyerEmail: 'trinh.htm@gmail.com',
    buyerCccd: '079191000083', buyerAddress: 'Số 36 đường 27A',
    buyerDob: '22/01/1991', buyerBankAccount: '0071001234567',
    accountHolder: 'HOANG THI MY TRINH'
  };
  buyCarry(phone) {
    const p = this.BUYER_LAST_ORDER;
    return { buyStep: 'form', buyMode: 'self', buyProfile: { ...p, buyerPhone: phone },
      buyerPhone: phone, buyPhoneInput: phone, buyerName: p.buyerName, buyerEmail: p.buyerEmail,
      buyerCccd: p.buyerCccd, buyerAddress: p.buyerAddress, buyerDob: p.buyerDob,
      buyerBankAccount: p.buyerBankAccount, accountHolder: p.accountHolder };
  }

  // (20) Mục 3 — người mua phải từ 18 đến 100 tuổi. Chỉ xét khi đã gõ đủ
  // dd/mm/yyyy; đang gõ dở thì chưa báo lỗi.
  dobError(v) {
    const m = /^(\\d{2})\\/(\\d{2})\\/(\\d{4})$/.exec(v || '');
    if (!m) return '';
    const d = +m[1], mo = +m[2], y = +m[3];
    const dt = new Date(y, mo - 1, d);
    if (dt.getFullYear() !== y || dt.getMonth() !== mo - 1 || dt.getDate() !== d)
      return 'Ngày sinh không hợp lệ.';
    const now = new Date();
    let age = now.getFullYear() - y;
    if (now.getMonth() < mo - 1 || (now.getMonth() === mo - 1 && now.getDate() < d)) age--;
    return (age < 18 || age > 100) ? 'Người mua phải từ 18 đến 100 tuổi.' : '';
  }"""

_JS_BADGE_OLD = "      paid: ['rgba(47,122,72,.14)', '#2F7A48', 'Đã chi trả'],"
_JS_BADGE_NEW = (_JS_BADGE_OLD + "\n"
    "      pay_failed: ['rgba(192,57,43,.12)', '#C0392B', 'Chi không thành công'],\n"
    "      refunded: ['rgba(154,163,176,.18)', '#5B6472', 'Đã hoàn điểm'],")

_JS_FILTER_OLD = ("WITHDRAWAL_FILTERS = [['all','Tất cả'],['pending','Chờ duyệt'],"
                  "['specialist_approved','Chờ Head'],['approved','Đã duyệt'],"
                  "['rejected','Từ chối'],['paid','Đã chi trả']];")
# (08/10) Duyệt 1 lớp: bỏ "Chờ Head", thêm các trạng thái sau thanh toán.
_JS_FILTER_NEW = ("WITHDRAWAL_FILTERS = [['all','Tất cả'],['pending','Chờ duyệt'],"
                  "['approved','Đã duyệt'],['paid','Thanh toán thành công'],"
                  "['pay_failed','Chi không thành công'],['refunded','Đã hoàn điểm'],"
                  "['rejected','Từ chối'],['cancelled','Thành viên đã huỷ']];")

_JS_WD_SEED_OLD = "    return raw.map(w => ({ ...w, amount: w.amountNum.toLocaleString('vi-VN') + 'đ' }));\n  }\n\n  makeStock() {"
_JS_WD_SEED_NEW = """    // (26) KH chốt duyệt 1 lớp: dữ liệu mẫu cũ bỏ bước "chờ Head".
    raw.forEach(w => {
      if (w.status === 'specialist_approved') w.status = 'pending';
      w.auditLog = w.auditLog.filter(l => !/chờ Head/.test(l.label))
        .map(l => /Head xác nhận duyệt/.test(l.label) ? { ...l, label: 'Admin duyệt', actor: 'Admin' } : l);
    });
    raw.push(
      { id:8, seller:'Trương Thanh Bình', amountNum:700000, date:'29/08/2026', accountNumber:'0123456789012', bankName:'VietinBank', branch:'CN TP.HCM', accountHolder:'TRUONG THANH BINH', status:'approved',
        auditLog:[{label:'Tạo yêu cầu', actor:'Trương Thanh Bình', time:'29/08/2026 20:05'},{label:'Admin duyệt (duyệt hàng loạt)', actor:'Admin', time:'01/09/2026 10:15'}] },
      { id:9, seller:'Ngô Thị Em', amountNum:500000, date:'02/09/2026', accountNumber:'0221234567', bankName:'MB Bank', branch:'CN TP.HCM', accountHolder:'NGO THI EM', status:'cancelled',
        auditLog:[{label:'Tạo yêu cầu', actor:'Ngô Thị Em', time:'02/09/2026 08:40'},{label:'Thành viên tự huỷ yêu cầu', actor:'Ngô Thị Em', time:'03/09/2026 21:12'}] }
    );
    // (22) Hai dòng mẫu cho luồng ngân hàng chi không thành công.
    raw.push(
      { id:6, seller:'Đỗ Anh Tuấn', amountNum:1500000, date:'22/08/2026', accountNumber:'0451000987654', bankName:'Vietcombank', branch:'CN Bình Dương', accountHolder:'DO ANH TUAN', status:'pay_failed', failNote:'Số tài khoản không tồn tại.',
        auditLog:[{label:'Tạo yêu cầu', actor:'Đỗ Anh Tuấn', time:'22/08/2026 09:14'},{label:'Admin duyệt', actor:'Admin', time:'23/08/2026 10:02'},{label:'Chi không thành công (không có trong file kết quả thanh toán)', actor:'Admin', time:'03/09/2026 09:30'}] },
      { id:7, seller:'Trần Thị Bích', amountNum:1000000, date:'18/07/2026', accountNumber:'0071001234567', bankName:'Vietcombank', branch:'CN TP.HCM', accountHolder:'TRAN THI BICH', status:'refunded', failNote:'Tên chủ tài khoản không khớp.', refundReason:'Ngân hàng trả về do sai tên chủ tài khoản; thành viên đã được báo cập nhật lại.',
        auditLog:[{label:'Tạo yêu cầu', actor:'Trần Thị Bích', time:'18/07/2026 14:20'},{label:'Admin duyệt', actor:'Admin', time:'20/07/2026 09:00'},{label:'Chi không thành công (không có trong file kết quả thanh toán)', actor:'Admin', time:'04/08/2026 10:10'},{label:'Hoàn điểm: sai tên chủ tài khoản', actor:'Admin', time:'04/08/2026 10:25'},{label:'Gửi email báo tài khoản nhận tiền có vấn đề', actor:'Hệ thống', time:'04/08/2026 10:25'}] }
    );
""" + _JS_WD_SEED_OLD

_JS_AUDIT_OLD = "  AUDIT = [\n"
_JS_AUDIT_NEW = """  AUDIT = [
    // (22)(23) Dòng mẫu cho hoàn điểm và admin sửa hồ sơ — sau UAT 02/10.
    { time:'17/09/2026 10:05', actor:'Nguyễn Thị Hạnh', role:'Admin',
      module:'Rút tiền', target:'YC-2026-0091 · Đỗ Anh Tuấn',
      action:'Hoàn điểm', before:'Chi không thành công', after:'Đã hoàn điểm · +1.500.000',
      evidence:'Lý do: sai số tài khoản', ip:'113.161.46.118' },
    { time:'17/09/2026 09:40', actor:'Nguyễn Thị Hạnh', role:'Admin',
      module:'Thành viên', target:'Ngô Thị Em · NTE3112',
      action:'Cập nhật', before:'Email: em3112@gmail.com', after:'Email: ngothiem.hcm@gmail.com',
      evidence:'Đã gửi email báo (địa chỉ cũ + mới)', ip:'113.161.46.118' },
"""

_JS_AUDIT_BADGE_OLD = "    'Tải file lên': ['rgba(30,58,102,.12)', '#1E3A66']"
_JS_AUDIT_BADGE_NEW = ("    'Hoàn điểm': ['rgba(150,92,10,.15)', '#965C0A'],\n"
                       + _JS_AUDIT_BADGE_OLD)

# Hằng tính trước `return {` của renderVals.
_JS_CONSTS_OLD = "    // A2\n    const regStepBg"
_JS_CONSTS_NEW = """    // (20) A1 sau UAT 02/10 — tuổi người mua + điều kiện bật nút Thanh toán.
    const buyerDobError = this.dobError(s.buyerDob);
    const payOk = s.buyTcChecked && s.payStage !== 'sending' && !buyerDobError;

    // A2
    const regStepBg"""

_JS_BAL_OLD = "    const availableBalance = 4000000;"
_JS_BAL_NEW = ("    // (20) Mục 6 — thành viên mới dùng được ngay; số dư là số thật,\n"
               "    // chưa có đơn nào được duyệt thì bằng 0.\n"
               "    // (09/10) Yêu cầu đổi điểm đang mở giữ điểm lại: trừ khỏi số dư khả dụng,\n"
               "    // hiện ở ô Đang chờ duyệt — hai ô luôn khớp số tiền của yêu cầu.\n"
               "    const pendingWdNum = myWdOpen ? +String(myWd.amount).replace(/\\D/g, '') : 0;\n"
               "    const availableBalance = s.agentStage === 'active' ? 4000000 - pendingWdNum : 0;")

_JS_BAL_LBL_OLD = ("      availableBalanceLabel: '4.000.000đ', pendingBalanceLabel: '800.000đ', "
                   "earnedBalanceLabel: '6.000.000đ',")
_JS_BAL_LBL_NEW = (
    "      availableBalanceLabel: availableBalance.toLocaleString('vi-VN') + 'đ',\n"
    "      pendingBalanceLabel: pendingWdNum.toLocaleString('vi-VN') + 'đ',\n"
    "      earnedBalanceLabel: s.agentStage === 'active' ? '6.000.000đ' : '0đ',\n"
    "      // H1 đã chốt: điểm ghi nhận SAU KHI admin duyệt đơn. Thành viên mới\n"
    "      // có 1 đơn đang chờ duyệt nên điểm chưa vào số dư.\n"
    "      hasPendingOrders: s.agentStage !== 'active', pendingOrderCount: 1,")

_JS_WD_ERR_OLD = ("'Vui lòng nhập số tiền hợp lệ.' : (withdrawAmountNum > availableBalance "
                  "? 'Số tiền vượt quá số dư khả dụng.' : '')")
_JS_WD_ERR_NEW = ("'Vui lòng nhập số điểm hợp lệ.' : (withdrawAmountNum > availableBalance "
                  "? 'Số điểm vượt quá số dư khả dụng.' : '')")

_JS_ISA1_OLD = "      isA1: s.screen === 'A1', isA2: s.screen === 'A2',"
_JS_ISA1_NEW = """      isA1: s.screen === 'A1',
      // (20) KH điều chỉnh: form luôn hiện nhưng khoá tới khi xác định xong SĐT
      // ở ô đầu trang.
      buyLocked: s.buyStep !== 'form', buyUnlocked: s.buyStep === 'form',
      buyLockCss: s.buyStep === 'form' ? ''
        : 'opacity:.45;pointer-events:none;user-select:none;filter:grayscale(.25)',
      buyBarBorder: s.buyStep === 'form' ? 'rgba(154,163,176,.35)' : '#1E3A66',
      buyBarShadow: s.buyStep === 'form' ? 'none' : '0 4px 18px rgba(30,58,102,.12)',
      buyBarPhone: s.buyerPhone || s.buyPhoneInput || '—',
      // Ô SĐT trên header: đã mở form thì hiện số đang dùng (khoá), nút Đổi số.
      buyHeaderPhone: s.buyStep === 'form' ? (s.buyerPhone || s.buyPhoneInput || '') : (s.buyPhoneInput || ''),
      buyHeaderAsk: s.buyStep !== 'form' && !s.buyPhoneFound,
      buyChangePhone: () => this.setState({ buyStep: 'phone', buyPhoneInput: '',
        buyPhoneFound: false, buyPhoneError: '', buyMode: '', buyPhoneNew: false }),
      buyPhoneNewNote: s.buyStep === 'form' && !!s.buyPhoneNew,
      buyPhoneInput: s.buyPhoneInput,
      setBuyPhoneInput: (e) => this.setState({
        buyPhoneInput: (e.target.value || '').replace(/\\D/g, '').slice(0, 10),
        buyPhoneError: '', buyPhoneFound: false }),
      buyPhoneError: s.buyPhoneError,
      buyPhoneBorder: s.buyPhoneError ? '#C0392B' : 'rgba(154,163,176,.6)',
      buyPhoneFound: s.buyPhoneFound, buyPhoneAsk: !s.buyPhoneFound,
      // Chỉ trả lời CÓ / CHƯA có tài khoản — không lộ tên hay đơn hàng của
      // người khác cho ai gõ đúng số.
      submitBuyPhone: () => {
        const ph = (s.buyPhoneInput || '').trim();
        if (!ph) { this.setState({ buyPhoneError: 'Vui lòng nhập số điện thoại.' }); return; }
        if (!/^0\\d{9}$/.test(ph)) { this.setState({ buyPhoneError: 'Số điện thoại gồm 10 chữ số, bắt đầu bằng 0.' }); return; }
        if (this.REGISTERED_PHONES.includes(ph)) { this.setState({ buyPhoneFound: true, buyPhoneError: '' }); return; }
        this.setState({ buyStep: 'form', buyerPhone: ph, buyMode: '', buyPhoneNew: true });
      },
      buyGoLogin: () => GO('C1', { agentLoginStep: 'login', agentPhone: s.buyPhoneInput,
        loginPhoneChecked: true, returnTo: 'A1' }),
      buySkipLogin: () => this.setState({ buyStep: 'form', buyerPhone: s.buyPhoneInput, buyMode: '' }),
      buyResetPhone: () => this.setState({ buyPhoneInput: '', buyPhoneFound: false, buyPhoneError: '' }),
      // (20) Mục 2 — tự điền theo đơn gần nhất, cho đổi sang mua cho người khác.
      buyIsSelf: s.buyMode === 'self', buyIsOther: s.buyMode === 'other',
      buyProfileDate: (s.buyProfile || {}).orderDate || '',
      buyProfileOrder: (s.buyProfile || {}).orderId || '',
      buyForOther: () => this.setState({ buyMode: 'other', buyerName: '', buyerPhone: '',
        buyerEmail: '', buyerCccd: '', buyerAddress: '', buyerDob: '',
        buyerBankAccount: '', accountHolder: '' }),
      buyForSelf: () => { const p = s.buyProfile || {}; this.setState({ buyMode: 'self',
        buyerName: p.buyerName || '', buyerPhone: p.buyerPhone || '',
        buyerEmail: p.buyerEmail || '', buyerCccd: p.buyerCccd || '',
        buyerAddress: p.buyerAddress || '', buyerDob: p.buyerDob || '',
        buyerBankAccount: p.buyerBankAccount || '', accountHolder: p.accountHolder || '' }); },
      buyerDobError,
      buyerDobBorder: buyerDobError ? '#C0392B' : 'rgba(154,163,176,.6)',
      // (20) C1 được gọi từ form mua hàng.
      loginFromBuy: s.returnTo === 'A1',
      loginHeading: s.returnTo === 'A1' ? 'Đăng nhập để tiếp tục mua hàng'
        : 'Đăng nhập để xem điểm thưởng và ưu đãi của bạn',
      backToBuy: () => GO('A1', { buyStep: 'form', buyerPhone: s.agentPhone.trim(), buyMode: '' }),
      isA2: s.screen === 'A2',"""

_JS_PAY_OLD = """      payDisabled: !s.buyTcChecked || s.payStage === 'sending',
      payStyle: 'height:48px;color:var(--c12);border:none;border-radius:var(--r-md);'
        + 'font-size:16px;font-weight:700;box-shadow:var(--sh);background:'
        + ((s.buyTcChecked && s.payStage !== 'sending')
             ? 'var(--c6)' : 'rgba(154,163,176,.5)')
        + ';cursor:' + ((s.buyTcChecked && s.payStage !== 'sending')
             ? 'pointer' : 'not-allowed'),"""
_JS_PAY_NEW = """      payDisabled: !payOk,
      payStyle: 'height:48px;color:var(--c12);border:none;border-radius:var(--r-md);'
        + 'font-size:16px;font-weight:700;box-shadow:var(--sh);background:'
        + (payOk ? 'var(--c6)' : 'rgba(154,163,176,.5)')
        + ';cursor:' + (payOk ? 'pointer' : 'not-allowed'),"""

_JS_LOGIN_OLD = """        if (ph && s.agentPassword === '123456') {
          GO('A3',"""
_JS_LOGIN_NEW = """        if (ph && s.agentPassword === '123456') {
          // (20) Gọi từ form mua hàng: (11/10) đúng mật khẩu vẫn phải qua bước
          // OTP, xác thực xong mới quay lại form A1 (điền sẵn) — agentOtpConfirm.
          if (s.returnTo === 'A1') { this.setState({ agentLoginStep: 'otp', agentLoginError: false }); return; }
          GO('A3',"""

_JS_OTP_OLD = "      agentOtpConfirm: () => GO('A3', { agentStage: 'active' }),"
_JS_OTP_NEW = ("      agentOtpConfirm: () => (s.returnTo === 'A1'\n"
               "        ? GO('A1', this.buyCarry(s.agentPhone.trim()))\n"
               "        : GO('A3', { agentStage: 'active' })),")

_JS_CMT1_OLD = """        // Agent đã được Head duyệt -> dashboard hoạt động (rút tiền được).
        // Agent chưa duyệt -> dashboard chờ kích hoạt (ưu đãi tạm giữ)."""
_JS_CMT1_NEW = """        // Sau UAT 02/10 không còn trạng thái chờ kích hoạt: thành viên nào
        // cũng vào dashboard dùng được ngay. 'new' chỉ còn nghĩa là chưa có
        // đơn nào được duyệt nên số dư bằng 0."""

_JS_CMT2_OLD = "      // Chưa kích hoạt thì hoa hồng bị giữ, chưa được tính điểm.\n      heldCommissionLabel: '1.200.000đ',\n"
_JS_CMT2_NEW = ""

# B3 — trạng thái mới + xuất danh sách chi trả.
_JS_ACTION_OLD = "    // Action modal\n    const actionWithdrawalRaw"
_JS_ACTION_NEW = """    // (22) Ngân hàng chi không thành công -> hoàn điểm thủ công.
    if (selectedWithdrawal) {
      const st = selectedWithdrawal.status;
      Object.assign(selectedWithdrawal, {
        canRefund: st === 'pay_failed',
        hasFailNote: !!selectedWithdrawal.failNote,
        hasRefundReason: !!selectedWithdrawal.refundReason
      });
      if (st === 'pay_failed') selectedWithdrawal.approvalStageNote =
        'Ngân hàng chi không thành công. Điểm của yêu cầu này chưa được trả lại — bấm Hoàn điểm để cộng lại vào số dư của thành viên.';
      if (st === 'refunded') selectedWithdrawal.approvalStageNote =
        'Đã hoàn điểm cho thành viên. Yêu cầu này đóng lại, thành viên tạo yêu cầu mới sau khi sửa thông tin tài khoản.';
    }

    // (21) Danh sách chi trả theo kỳ: yêu cầu đã duyệt đủ 2 bước, chưa chi.
    const payoutRows = withdrawalsData
      .filter(w => w.status === 'approved' && (w.date || '').slice(3) === s.payoutPeriod)
      .map(w => ({ ...w, points: w.amountNum.toLocaleString('vi-VN') }));
    const payoutEmpty = payoutRows.length === 0;

    // Action modal
    const actionWithdrawalRaw"""

_JS_WD_RET_OLD = "      openPaidModal: () => this.setState({ actionModal: { type: 'paid', kind: 'withdrawal', id: s.selectedWithdrawalId }, paidNote: '' }),"
_JS_WD_RET_NEW = _JS_WD_RET_OLD + """
      // (22) Chi không thành công + hoàn điểm.
      openPayFailModal: () => this.setState({ actionModal: { type: 'payfail', kind: 'withdrawal', id: s.selectedWithdrawalId }, paidNote: '' }),
      openRefundModal: () => this.setState({ actionModal: { type: 'refund', kind: 'withdrawal', id: s.selectedWithdrawalId }, rejectReason: '' }),
      isPayFailModal: !!(s.actionModal && s.actionModal.type === 'payfail'),
      isRefundModal: !!(s.actionModal && s.actionModal.type === 'refund'),
      refundConfirmStyle: 'flex:1;height:44px;border:none;border-radius:5px;font-size:14px;font-weight:600;color:#FFFFFF;background:'
        + (rejectDisabled ? 'rgba(154,163,176,.5)' : 'var(--c6)') + ';cursor:' + (rejectDisabled ? 'not-allowed' : 'pointer'),
      confirmPayFail: () => {
        const id = s.actionModal.id, now = '03/09/2026 10:15';
        const actor = s.adminRole === 'specialist' ? 'Admin' : 'Head';
        this.setState({ withdrawalsData: withdrawalsData.map(w => w.id === id
          ? { ...w, status: 'pay_failed', failNote: (s.paidNote || '').trim(),
              auditLog: [...w.auditLog, { label: 'Ngân hàng chi không thành công', actor, time: now }] }
          : w), actionModal: null, paidNote: '' });
      },
      confirmRefund: () => {
        if (!s.rejectReason.trim()) return;
        const id = s.actionModal.id, now = '03/09/2026 10:20';
        const actor = s.adminRole === 'specialist' ? 'Admin' : 'Head';
        this.setState({ withdrawalsData: withdrawalsData.map(w => w.id === id
          ? { ...w, status: 'refunded', refundReason: s.rejectReason.trim(),
              auditLog: [...w.auditLog,
                { label: 'Hoàn điểm: ' + s.rejectReason.trim(), actor, time: now },
                { label: 'Gửi email báo tài khoản nhận tiền có vấn đề', actor: 'Hệ thống', time: now }] }
          : w), actionModal: null, rejectReason: '' });
      },
      // (21) Xuất danh sách chi trả.
      showPayoutExport: s.showPayoutExport,
      openPayoutExport: () => this.setState({ showPayoutExport: true, payoutExported: '' }),
      closePayoutExport: () => this.setState({ showPayoutExport: false, payoutExported: '' }),
      payoutPeriod: s.payoutPeriod,
      payoutPeriods: this.PAYOUT_PERIODS.map(p => ({
        label: 'Tháng ' + p, onClick: () => this.setState({ payoutPeriod: p, payoutExported: '' }),
        style: 'height:34px;padding:0 14px;border-radius:30px;font-size:12px;font-weight:600;border:1px solid '
          + (s.payoutPeriod === p ? '#1E3A66;background:rgba(30,58,102,.08);color:#1E3A66'
                                  : 'rgba(154,163,176,.4);background:transparent;color:var(--c5)')
      })),
      payoutRows, payoutEmpty, payoutCount: payoutRows.length,
      payoutTotal: payoutRows.reduce((t, w) => t + w.amountNum, 0).toLocaleString('vi-VN') + 'đ',
      payoutExported: s.payoutExported,
      payoutBtnStyle: 'flex:1;height:44px;border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:#FFFFFF;background:'
        + (payoutEmpty ? 'rgba(154,163,176,.5)' : 'var(--c6)') + ';cursor:' + (payoutEmpty ? 'not-allowed' : 'pointer'),
      runPayoutExport: () => { if (payoutEmpty) return; this.setState({
        payoutExported: 'chi-tra-HOMI365-' + s.payoutPeriod.slice(3) + '-' + s.payoutPeriod.slice(0, 2) + '.xlsx' }); },"""

# B2 — sửa hồ sơ: nhắc gửi email (mục 22).
_JS_PF_OLD = """      saveProfileEdit: () => this.setState({
        memberEdits: { ...s.memberEdits, [s.selectedMemberId]: { ...s.profileDraft } },
        profileEdit: false, profileDraft: {} }),"""
_JS_PF_NEW = """      // (23) Mục 22 — admin sửa hồ sơ thì hệ thống gửi email cho người đó,
      // nêu giá trị mới. Đổi email thì gửi cả địa chỉ cũ lẫn địa chỉ mới.
      saveProfileEdit: () => {
        const cur = selectedMember || {}, d = s.profileDraft || {};
        const keys = ['name', 'phone', 'email', 'cccd', 'dobGender', 'address', 'bankAccount', 'bankHolder'];
        const changed = keys.filter(k => d[k] !== undefined && d[k] !== cur[k]);
        const mailChanged = changed.includes('email');
        const text = !changed.length ? ''
          : mailChanged
            ? 'Đã lưu hồ sơ · đã gửi email báo thay đổi tới ' + cur.email + ' (địa chỉ cũ) và ' + d.email + ' (địa chỉ mới).'
            : 'Đã lưu hồ sơ · đã gửi email báo thay đổi tới ' + cur.email + '.';
        this.setState({
          memberEdits: { ...s.memberEdits, [s.selectedMemberId]: { ...(s.memberEdits[s.selectedMemberId] || {}), ...d } },
          profileEdit: false, profileDraft: {},
          profileSaved: text ? { id: s.selectedMemberId, text } : null });
      },
      profileSavedNote: (s.profileSaved && s.profileSaved.id === s.selectedMemberId
        && s.profileOpen && !s.profileEdit) ? s.profileSaved.text : '',
      pfMailNote: (() => {
        const cur = (selectedMember || {}).email || '', nw = pfv('email');
        return (nw && nw !== cur)
          ? 'Email đã đổi. Khi lưu, hệ thống gửi email báo thay đổi tới cả địa chỉ cũ (' + cur + ') và địa chỉ mới (' + nw + '), nêu rõ các giá trị mới.'
          : 'Khi lưu, hệ thống sẽ gửi email báo thay đổi tới ' + cur + ', nêu rõ các giá trị mới.';
      })(),"""


JS = [
    ("    selectedOrderId: null,\n", _JS_STATE),
    (_JS_CLASS_OLD, _JS_CLASS_NEW),
    (_JS_BADGE_OLD, _JS_BADGE_NEW),
    (_JS_FILTER_OLD, _JS_FILTER_NEW),
    (_JS_WD_SEED_OLD, _JS_WD_SEED_NEW),
    (_JS_AUDIT_OLD, _JS_AUDIT_NEW),
    (_JS_AUDIT_BADGE_OLD, _JS_AUDIT_BADGE_NEW),
    (_JS_CONSTS_OLD, _JS_CONSTS_NEW),
    (_JS_BAL_OLD, _JS_BAL_NEW),
    (_JS_BAL_LBL_OLD, _JS_BAL_LBL_NEW),
    (_JS_WD_ERR_OLD, _JS_WD_ERR_NEW),
    (_JS_ISA1_OLD, _JS_ISA1_NEW),
    (_JS_PAY_OLD, _JS_PAY_NEW),
    (_JS_LOGIN_OLD, _JS_LOGIN_NEW),
    (_JS_OTP_OLD, _JS_OTP_NEW),
    (_JS_CMT1_OLD, _JS_CMT1_NEW),
    (_JS_CMT2_OLD, _JS_CMT2_NEW),
    (_JS_ACTION_OLD, _JS_ACTION_NEW + ""),
    (_JS_WD_RET_OLD, _JS_WD_RET_NEW),
    (_JS_PF_OLD, _JS_PF_NEW),
    # pfv(): ô sửa hồ sơ lấy giá trị nháp, chưa có thì lấy giá trị đang lưu —
    # để mở thẳng trạng thái "#sua-ho-so" bằng hash vẫn thấy form điền sẵn.
    ("    // (21) Danh sách chi trả theo kỳ:",
     "    const pfv = (k) => { const d = s.profileDraft || {};\n"
     "      return d[k] !== undefined ? d[k] : ((selectedMember || {})[k] || ''); };\n\n"
     "    // (21) Danh sách chi trả theo kỳ:"),
] + [
    ("      pf%s: (s.profileDraft || {}).%s || ''," % (a, b),
     "      pf%s: pfv('%s')," % (a, b))
    for a, b in [("Name", "name"), ("Phone", "phone"), ("Email", "email"),
                 ("Cccd", "cccd"), ("Dob", "dobGender"), ("Address", "address"),
                 ("BankAccount", "bankAccount"), ("BankHolder", "bankHolder")]
]


def patch_script(script, die):
    for i, (old, new) in enumerate(JS):
        n = script.count(old)
        if n != 1:
            die("bản vá JS UAT #%d khớp %d lần (cần đúng 1):\n---\n%s\n---"
                % (i, n, old[:160]))
        script = script.replace(old, new)
    return rename(script)


# ============================================================================
# 4. TRẠNG THÁI XEM THỬ (index.html + #hash)
# ============================================================================

MY_WD = {"amount": "1.000.000đ", "date": "05/09/2026", "status": "pending"}


def patch_screens(screens):
    by = {sc["code"]: sc for sc in screens}

    # A1 — mặc định giờ là bước nhập SĐT; các trạng thái cũ đều ở bước form.
    a1 = by["A1"]
    old = [(h, lb, dict(st, buyStep="form")) for h, lb, st in a1["states"][1:]]
    prof = {"orderId": "DH100077", "orderDate": "12/08/2026",
            "buyerName": "Hoàng Thị Mỹ Trinh", "buyerPhone": "0901234567",
            "buyerEmail": "trinh.htm@gmail.com", "buyerCccd": "079191000083",
            "buyerAddress": "Số 36 đường 27A", "buyerDob": "22/01/1991",
            "buyerBankAccount": "0071001234567",
            "accountHolder": "HOANG THI MY TRINH"}
    filled = {k: v for k, v in prof.items() if k not in ("orderId", "orderDate")}
    a1["states"] = [
        ("", "Bước 0 — nhập số điện thoại", {"buyStep": "phone"}),
        ("sdt-da-co", "SĐT đã có tài khoản — gợi ý đăng nhập",
         {"buyStep": "phone", "buyPhoneInput": "0901234567", "buyPhoneFound": True}),
        ("form", "Form mua hàng — SĐT chưa có tài khoản, nhập thông tin",
         {"buyStep": "form", "buyerPhone": "0900000000", "buyPhoneInput": "0900000000",
          "buyPhoneNew": True}),
        ("form-tu-dien", "Form tự điền theo đơn gần nhất (sau đăng nhập)",
         dict(filled, buyStep="form", buyMode="self", buyProfile=prof)),
        ("loi-tuoi", "Form — ngày sinh ngoài 18–100 tuổi",
         {"buyStep": "form", "buyerPhone": "0900000000", "buyerDob": "15/03/2015",
          "buyTcChecked": True}),
    ] + old

    # C1 — đăng nhập được gọi từ form mua hàng.
    by["C1"]["states"].insert(2, (
        "tu-mua-hang", "Đăng nhập từ form mua hàng — xong quay lại A1",
        {"agentLoginStep": "login", "agentPhone": "0901234567",
         "loginPhoneChecked": True, "returnTo": "A1"}))

    # A3 — đổi nhãn + hash theo mục 6 và 7.
    a3 = by["A3"]
    a3["states"] = [
        ("", "Thành viên mới — dùng được ngay, chưa có đơn được duyệt",
         {"agentStage": "new"}),
        ("da-tinh-hh", "Thành viên đã có điểm", {"agentStage": "active"}),
        ("doi-diem", "Form yêu cầu đổi điểm",
         {"agentStage": "active", "showWithdrawForm": True}),
        ("doi-diem-ok", "Đổi điểm — gửi thành công",
         {"agentStage": "active", "showWithdrawSuccess": True}),
        # (26) Mục 8 — huỷ yêu cầu trước ngày khoá sổ.
        ("co-yeu-cau", "Đang có yêu cầu đổi điểm — huỷ được",
         {"agentStage": "active", "myWd": MY_WD}),
        ("huy-yeu-cau", "Modal huỷ yêu cầu đổi điểm",
         {"agentStage": "active", "myWd": MY_WD, "showCancelWd": True}),
        ("da-khoa-so", "Đã khoá sổ (ngày cuối tháng) — không huỷ được",
         {"agentStage": "active", "myWd": MY_WD, "wdPeriodLocked": True}),
        # (08/10) Theo Chính sách ưu đãi thành viên mục 4: qua hạn thì không gửi mới.
        ("het-han-gui", "Đã qua hạn gửi yêu cầu kỳ này — chờ kỳ sau",
         {"agentStage": "active", "wdPeriodLocked": True}),
    ]

    # B2 — sửa hồ sơ có dòng nhắc gửi email.
    by["B2"]["states"] += [
        ("sua-ho-so", "Sửa hồ sơ — nhắc gửi email báo thay đổi",
         {"selectedMemberId": 2, "profileOpen": True, "profileEdit": True}),
        ("sua-ho-so-doi-email", "Sửa hồ sơ — đổi email, gửi cả địa chỉ cũ và mới",
         {"selectedMemberId": 2, "profileOpen": True, "profileEdit": True,
          "profileDraft": {"email": "cuong.levan@gmail.com"}}),
    ]

    # B3 — (08/10) viết lại theo luồng duyệt 1 lớp: bỏ modal "đánh dấu đã chi
    # trả" bằng tay và modal "ngân hàng chi không thành công" bằng tay — cả hai
    # giờ cập nhật từ file kết quả thanh toán.
    by["B3"]["states"] = [
        ("", "Danh sách yêu cầu · chọn để duyệt hàng loạt", {}),
        ("chi-tiet", "Chi tiết yêu cầu Chờ duyệt", {"selectedWithdrawalId": 1}),
        ("duyet", "Modal duyệt một yêu cầu", {"selectedWithdrawalId": 1,
            "actionModal": {"type": "approve", "kind": "withdrawal", "id": 1}}),
        ("tu-choi", "Modal từ chối yêu cầu", {"selectedWithdrawalId": 1,
            "actionModal": {"type": "reject", "kind": "withdrawal", "id": 1}}),
        ("duyet-hang-loat", "Modal duyệt hàng loạt",
         {"actionModal": {"type": "bulk", "kind": "withdrawal", "ids": [1, 2]}}),
        ("xuat-chi-tra", "Modal xuất danh sách chi trả theo kỳ", {"showPayoutExport": True}),
        ("tai-ket-qua", "Modal tải lên kết quả thanh toán — đối chiếu",
         {"showPayResult": True, "payResultFile": "sao-ke-chi-tra-HOMI365-2026-08.xlsx"}),
        ("chi-khong-thanh-cong", "Chi tiết yêu cầu chi không thành công",
         {"selectedWithdrawalId": 6}),
        ("hoan-diem", "Modal hoàn điểm — lý do bắt buộc",
         {"selectedWithdrawalId": 6,
          "actionModal": {"type": "refund", "kind": "withdrawal", "id": 6}}),
        ("da-hoan-diem", "Chi tiết yêu cầu đã hoàn điểm", {"selectedWithdrawalId": 7}),
        ("thanh-vien-huy", "Chi tiết yêu cầu thành viên đã huỷ", {"selectedWithdrawalId": 9}),
    ]

    # (27) B2 — bổ nhiệm đặc biệt làm lại (mục 15) + tuyến trên hiệu lực (20).
    b2 = by["B2"]
    st2 = []
    for h, lb, st in b2["states"]:
        if h == "cap-nhat-cap":
            st2.append(("cap-nhat-cap", "Modal bổ nhiệm đặc biệt — admin xác nhận, gửi email anh Phương",
                        {"selectedMemberId": 5, "rankEditId": 5, "rankEditChoice": "Diamond",
                         "rankReason": "Đạt doanh số đặc biệt quý 3",
                         "rankRequester": "Hoàng Thị Mỹ Trinh"}))
        elif h == "da-cap-nhat-cap":
            # (08/10) KH: anh Phương duyệt NGOÀI hệ thống; admin vào xác nhận là
            # cấp có hiệu lực ngay, hệ thống chỉ cần gửi email cho anh Phương.
            st2.append(("da-bo-nhiem", "Đã bổ nhiệm đặc biệt — có hiệu lực ngay, đã gửi email anh Phương",
                        {"selectedMemberId": 5, "rankOverrides": {"5": "Diamond"},
                         "rankSaved": "Đã bổ nhiệm Gold → Diamond, có hiệu lực ngay. Đã gửi email cho anh Phương và email báo thành viên.",
                         "rankLogs": {"5": [{"label": "Bổ nhiệm đặc biệt Gold → Diamond · lý do: Đạt doanh số đặc biệt quý 3 · người yêu cầu: Hoàng Thị Mỹ Trinh · admin xác nhận (đã duyệt ngoài hệ thống) · đã gửi email anh Phương",
                                             "time": "08/10/2026 10:20"}]}}))
        else:
            st2.append((h, lb, st))
    st2.append(("tuyen-tren-hieu-luc", "Tuyến trên hiệu lực khác tuyến trên trực tiếp (đồng cấp)",
                {"selectedMemberId": 4}))
    b2["states"] = st2

    # (27) B9 — màn mới Xét thăng / hạ cấp, đặt ngay sau B2.
    b9 = {"code": "B9", "title": "B9 · Xét thăng / hạ cấp", "group": "Quản trị",
          "blocks": b2["blocks"],
          "states": [
              ("", "Danh sách đề xuất kỳ 09/2026", {}),
              ("tu-choi", "Modal từ chối — bắt nhập lý do", {"rrModal": {"type": "deny", "id": 1}}),
              ("duyet-tat-ca", "Modal duyệt tất cả", {"rrModal": {"type": "bulk", "ids": [2, 1, 5]}}),
              ("da-xu-ly", "Đã duyệt 1 đề xuất, từ chối 1 đề xuất",
               {"rrStatus": {"2": "approved", "1": "denied"},
                "rrReason": {"1": "Thành viên nghỉ phép cả tháng 9, giữ hạng."}}),
          ]}
    screens.insert(screens.index(b2) + 1, b9)

    # (28) B5 — cấu hình hoa hồng theo %; một trạng thái nhập sai để thấy cảnh báo.
    by["B5"]["states"].append(
        ("hoa-hong-loi", "Hoa hồng % — nhập sai, cảnh báo và khoá nút lưu",
         {"commCfg": {"y": {"pct": {"Copper": 20, "Silver": 30, "Gold": 35, "Diamond": 34,
                                    "Titanium": 38, "Lithium": 38.5}}}}))

    # Mục 7 — đổi chữ ở tên màn và nhãn trạng thái.
    for sc in screens:
        sc["title"] = rename(sc["title"])
        sc["states"] = [(h, rename(lb), st) for h, lb, st in sc["states"]]
    return screens


# ============================================================================
# 5. otp.js + policies.js
# ============================================================================

def patch_otp(js, die):
    old = "    var hint = document.querySelector('.tnc-hint');\n"
    if js.count(old) != 1:
        die("không tìm thấy neo trong OTP_JS để mở khoá ô đã tích sẵn")
    # Trạng thái mở bằng #hash có thể đã tích sẵn ô đồng ý (ví dụ
    # a1-buy.html#loi-duong-truyen). Ô đã tích mà vẫn khoá thì vô lý.
    # KHÔNG đọc box.checked: trước khi runtime dựng xong, thẻ input thô còn
    # mang thuộc tính checked="{{…}}" nên trình duyệt coi là đã tích.
    return js.replace(old, "    var st0 = window.__STATE__ || {};\n"
                           "    if (st0.buyTcChecked || st0.tncChecked) read = true;\n"
                      + old).replace(
        "// cuộn hết văn bản, hoặc mở một link chính sách.",
        "// cuộn hết văn bản, hoặc mở một link chính sách. Từ 06/10 form mua hàng\n"
        "// (A1) dùng chung cơ chế này: ô đồng ý khoá tới khi bấm link chính sách.")


_POL = [
    ("'Điểm chỉ được cộng vào tài khoản sau khi Thành viên đã được kích hoạt.',\n"
     "        'Các đơn hàng phát sinh trước thời điểm kích hoạt vẫn được ghi nhận và "
     "cộng bù đầy đủ, tính từ đơn đầu tiên.',",
     "'Điểm của mỗi đơn được cộng ngay sau khi đơn đó được HOMI365 duyệt.',\n"
     "        'Thành viên dùng được link giới thiệu và gửi yêu cầu đổi điểm ngay sau "
     "khi đăng ký.',"),
    ("trước khi tài khoản được kích hoạt.'", "khi hoàn tất đăng ký.'"),
]


def patch_policy(js, die):
    for old, new in _POL:
        if js.count(old) != 1:
            die("không khớp neo trong TNC_POLICY_JS:\n%s" % old[:100])
        js = js.replace(old, new)
    # (08/10) Bỏ bản Điều khoản thành viên cũ, thay bằng 2 văn bản KH gửi
    # (cùng id dieu-khoan-thanh-vien để link cũ vẫn mở đúng trang). Neo ở
    # trên vẫn kiểm tra để biết TNC_POLICY_JS gốc không bị đổi ngầm.
    return pdoc.policy_js()


# ============================================================================
# 6. DIFF-vs-mockup-KH.md — mục 19
# ============================================================================

DIFF = [
    "## 19. Cập nhật sau UAT 02/10 — đợt 06/10", "",
    "Nguồn: sheet `Plan Update` trong Google Sheet `[Homi] - Change Request`. "
    "Đợt này chỉ làm các mục **không bị chặn** bởi câu hỏi H2–H5. Toàn bộ bản vá "
    "nằm ở `tools/update_uat0210.py`, neo không khớp là dừng build.", "",
    "| Mục | Màn | Thay đổi | Xem thử |", "|---|---|---|---|",
    "| 1 | A1, C1 | Thêm **bước nhập số điện thoại** trước form mua hàng. Số đã có "
    "tài khoản thì hiện khối gợi ý với hai nút Đăng nhập / Bỏ qua và tự điền; số "
    "mới vào thẳng form, điền sẵn số vừa nhập. Hệ thống chỉ trả lời có hay chưa có "
    "tài khoản. Đăng nhập đi qua C1 rồi **quay lại form mua hàng** (đã chốt). | "
    "`a1-buy.html`, `#sdt-da-co`, `#form`, `c1-login.html#tu-mua-hang` |",
    "| 2 | A1 | Sau đăng nhập form **tự điền theo đơn gần nhất**, sửa trực tiếp được. "
    "(08/10: bỏ dòng nhắc \"Đã điền theo đơn…\" và nút Mua cho người khác — không có "
    "trong yêu cầu KH.) | `#form-tu-dien` |",
    "| 3 | A1 | Ô Ngày sinh kiểm tra tuổi **18–100**, báo lỗi ngay dưới ô và khoá "
    "nút Thanh toán. Chỉ xét khi đã gõ đủ `dd/mm/yyyy`. | `#loi-tuoi` |",
    "| 4 | A1 | Bỏ dấu (*) ở Tỉnh/Thành phố và Phường/Xã. Nút Thanh toán vốn "
    "không phụ thuộc hai ô này nên không có điều kiện nào phải gỡ. Bổ sung cùng "
    "ngày: ba ô **Ngân hàng, Số tài khoản, Tên chủ tài khoản** ở form mua hàng "
    "cũng bỏ dấu (*) — vẫn giữ ô, chỉ không bắt buộc nhập. Form đăng ký thành "
    "viên A2 giữ nguyên bắt buộc. | `#form` |",
    "| 5 | A1 | Ô đồng ý chính sách **mờ và khoá**, bấm một trong hai link chính "
    "sách thì mở. Hai link đổi sang mở tab mới — trước đây mở cùng tab, bấm là "
    "mất dữ liệu đang nhập. Dùng lại cơ chế của A2 bước 4 trong `js/otp.js`. | "
    "`#form` |",
    "| 6 | A2, A3 | **Bỏ trạng thái chờ kích hoạt.** A2 bước 5 và nút bước 4 "
    "không còn chữ \"kích hoạt\", \"tạm giữ\". A3 gỡ banner CHỜ KÍCH HOẠT; khối "
    "số dư và nút đổi điểm hiện cho cả thành viên mới, số dư là số thật. Đơn chưa "
    "duyệt hiện dòng \"điểm được ghi nhận sau khi đơn được duyệt\" (H1 đã chốt). "
    "Sửa câu tương ứng ở Điều khoản mục 2. | `a2-register.html#buoc-5`, "
    "`a3-dashboard.html` |",
    "| 7 | mọi màn | Đổi toàn bộ **\"rút tiền\" → \"đổi điểm\"**: tiêu đề, nút, "
    "cột bảng, bộ lọc, sidebar, phân hệ trong nhật ký, tên trạng thái ở "
    "`index.html`. Hash `#rut-tien` đổi thành `#doi-diem`. | — |",
    "| 10 | B3 | Nút **Xuất danh sách chi trả** mở hộp thoại chọn kỳ, liệt kê 5 "
    "cột của file, xem trước các dòng và tổng chi của kỳ. | "
    "`b3-withdrawals.html#xuat-chi-tra` |",
    "| 11 | B3, B8 | Hai trạng thái mới **Chi không thành công** và **Đã hoàn "
    "điểm**, có bộ lọc riêng. Yêu cầu đã duyệt có thêm nút ghi nhận ngân hàng "
    "trả về; sau đó nút **Hoàn điểm** với lý do bắt buộc và dòng nhắc hệ thống "
    "gửi email. B8 thêm hành động Hoàn điểm. | `#bao-chi-loi`, "
    "`#chi-khong-thanh-cong`, `#hoan-diem`, `#da-hoan-diem` |",
    "| 22 | B2, B8 | Form sửa hồ sơ có dòng nhắc **hệ thống sẽ gửi email báo "
    "thay đổi**; đổi email thì nêu cả địa chỉ cũ và mới. Lưu xong hiện dòng xác "
    "nhận. B8 thêm dòng mẫu. | `b2-members.html#sua-ho-so`, "
    "`#sua-ho-so-doi-email` |", "",
    "**Hai mục không có gì phải sửa trên giao diện:**", "",
    "- **Mục 19** (bỏ từ \"tách nhánh\"): prototype không dùng từ này ở màn nào.",
    "- **Mục 16** (email khi thăng/hạ cấp): không có giao diện, xem danh sách "
    "email dưới đây.", "",
    "**Email hệ thống phát sinh từ đợt này** — nội dung do team HOMI365 biên "
    "soạn:", "",
    "| Email | Gửi cho | Khi nào | Mục |", "|---|---|---|---|",
    "| Báo thăng / hạ cấp | Thành viên | Mỗi khi cấp thay đổi | 16 |",
    "| Báo tài khoản nhận tiền có vấn đề | Thành viên | Admin bấm Hoàn điểm | 11 |",
    "| Báo hồ sơ được sửa, nêu giá trị mới | Thành viên (đổi email thì cả địa "
    "chỉ cũ lẫn mới) | Admin lưu hồ sơ | 22 |", "",
    "**Giả định của bản mẫu — cần xác nhận khi làm thật:**", "",
    "1. **Thế nào là \"đã có tài khoản\" (mục 1).** Bản mẫu coi là số đã đăng ký "
    "thành viên, vì chỉ thành viên mới đăng nhập được. Khách từng mua nhưng chưa "
    "đăng ký thành viên được coi như khách mới.",
    "2. **Mua cho người khác (mục 2)** xoá hết phần tự điền, kể cả số điện thoại "
    "và tài khoản ngân hàng. Ai là người giới thiệu của đơn mua lần 2 trở đi "
    "đang chờ trả lời câu hỏi H5 ở sheet Change Request.",
    "3. **Chi không thành công (mục 11)** được ghi nhận từ trạng thái Đã duyệt, "
    "trước khi đánh dấu đã chi trả. Nếu ngân hàng trả về sau khi đã đánh dấu thì "
    "cần thêm nhánh từ Đã chi trả.",
    "4. **Cột của file chi trả (mục 10)** là 5 cột theo sheet; danh sách cuối "
    "cùng còn chờ phía HOMI365 xác nhận.",
    "5. **Nội dung chuyển khoản** ở chi tiết yêu cầu đổi từ `Rut khoan thuong…` "
    "sang `Doi diem thuong…` cho khớp mục 7.",
    "6. **Điều khoản mục 2** (bước 4 đăng ký và trang chính sách) đã sửa một câu "
    "cho khớp mục 6 — cần Pháp lý đọc lại.", "",
    "**Chưa làm, chờ khách hàng:** mục 8, 9 (H2, H3) · 12, 13, 14 (màn đề xuất "
    "thăng/hạ cấp) · 15, 20, 21 (H4) · 17, 18 (H5) · 23 (xác nhận đảo quyết định "
    "về B5).", "",
    "**Còn lệch, nằm ngoài phạm vi đợt này:** ngăn chi tiết thành viên ở B2 và "
    "hộp thoại Head duyệt hồ sơ vẫn ghi \"ưu đãi đang tạm giữ\", \"kích hoạt\". "
    "Sau mục 6 các câu này không còn đúng, nhưng ý nghĩa mới của bước Head duyệt "
    "hồ sơ chưa được chốt nên chưa sửa.", "",
]


def patch_diff(diff):
    """Chèn mục 19 vào trước phần 'Ghi chú'."""
    i = diff.index("## Ghi chú")
    return diff[:i] + DIFF + diff[i:]


# ============================================================================
# 7. ĐỢT 08/10 — THEO PHẢN HỒI KH Ở SHEET CHANGE REQUEST
# ============================================================================
# Chạy SAU các bản vá đợt 06/10 ở trên (nối thêm vào MARKUP / JS), nên neo có
# thể là chuỗi do chính đợt 06/10 sinh ra.

MARKUP_0810 = []
JS_0810 = []
CUTS = []          # (mốc đầu, mốc cuối KHÔNG gồm, thay bằng) — cắt cả khối

# ---------------------------------------------------------------------------
# 7.1 Đổi điểm — A3: thành viên tự huỷ yêu cầu trước ngày khoá sổ (mục 8)
# ---------------------------------------------------------------------------
_BADGE = ('font-size:11px;font-weight:700;padding:var(--s1) var(--s5);'
          'border-radius:var(--r-xl);white-space:nowrap')

A3_MY_WD = """
        <!-- (26) Yêu cầu đổi điểm của bạn trong kỳ — huỷ được tới ngày khoá sổ -->
        <sc-if value="{{hasMyWd}}" hint-placeholder-val="{{false}}">
          <div style="background:var(--c12);border:1px solid rgba(154,163,176,.35);border-radius:var(--r-md);padding:var(--s6);display:flex;flex-direction:column;gap:var(--s4)">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:var(--s4)"><div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Yêu cầu đổi điểm kỳ {{wdPeriod}}</div><span style=\"""" + _BADGE + """;background:{{myWdBadgeBg}};color:{{myWdBadgeColor}}">{{myWdStatusLabel}}</span></div>
            <div style="display:flex;justify-content:space-between;align-items:baseline;gap:var(--s4)"><div style="font-size:22px;font-weight:800;color:var(--c1)">{{myWdAmount}}</div><div style="font-size:12px;color:var(--c5)">Gửi ngày {{myWdDate}}</div></div>
            <sc-if value="{{canCancelWd}}" hint-placeholder-val="{{false}}">
              <button sc-camel-on-click="{{openCancelWd}}" style="height:40px;background:var(--c12);color:var(--err);border:1px solid var(--err);border-radius:var(--r-md);font-size:14px;font-weight:600" style-hover="background:rgba(192,57,43,.06)">Huỷ yêu cầu</button>
              <div style="font-size:11px;color:var(--c5);line-height:1.6">Huỷ được tới <strong>{{wdLockLabel}}</strong> (hạn chót trước ngày cuối tháng). Huỷ xong điểm được cộng lại vào số dư và bạn tạo được yêu cầu mới.</div>
            </sc-if>
            <sc-if value="{{wdLockedNote}}" hint-placeholder-val="{{false}}">
              <button disabled="{{true}}" style="height:40px;background:rgba(154,163,176,.15);color:var(--c5);border:1px solid rgba(154,163,176,.4);border-radius:var(--r-md);font-size:14px;font-weight:600;cursor:not-allowed">Huỷ yêu cầu</button>
              <div style="font-size:12px;color:var(--c4);background:rgba(154,163,176,.12);border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">Đã khoá sổ kỳ {{wdPeriod}} lúc {{wdLockLabel}}. Yêu cầu không huỷ hay sửa được nữa, đang chờ duyệt và chi trả.</div>
            </sc-if>
            <sc-if value="{{myWdCancelled}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:var(--c5);line-height:1.6">Bạn đã huỷ yêu cầu này. Có thể tạo yêu cầu mới trước khi khoá sổ lúc {{wdLockLabel}}.</div>
            </sc-if>
          </div>
        </sc-if>
        <sc-if value="{{showCancelWd}}" hint-placeholder-val="{{false}}">
          <div style=\"""" + _OVERLAY + """\">
            <div style="width:100%;max-width:360px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
              <div style="font-size:18px;font-weight:700;color:var(--c1)">Huỷ yêu cầu đổi điểm?</div>
              <div style="font-size:14px;color:var(--c2);line-height:1.6">Yêu cầu đổi <strong>{{myWdAmount}}</strong> kỳ {{wdPeriod}} sẽ bị huỷ, điểm được cộng lại vào số dư khả dụng. Bạn có thể tạo yêu cầu mới trước khi khoá sổ.</div>
              <div style="display:flex;gap:var(--s3)">
                <button sc-camel-on-click="{{closeCancelWd}}" style="flex:1;""" + _BTN_G + """;font-size:14px">Giữ lại</button>
                <button sc-camel-on-click="{{confirmCancelWd}}" style="flex:1;height:44px;background:var(--err);color:var(--c12);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600">Huỷ yêu cầu</button>
              </div>
            </div>
          </div>
        </sc-if>
"""

MARKUP_0810 += [
    ('Bạn đã gửi yêu cầu đổi điểm trong tháng này. Lượt đổi tiếp theo khả dụng từ '
     '<strong>{{nextWithdrawDate}}</strong>.',
     'Bạn đang có yêu cầu đổi điểm trong kỳ {{wdPeriod}}. Muốn đổi số điểm khác thì '
     'huỷ yêu cầu bên dưới rồi tạo lại, trước khi khoá sổ lúc <strong>{{wdLockLabel}}</strong>.'),
    ('style="{{withdrawButtonStyle}}">Tạo yêu cầu rút tiền</button>\n',
     'style="{{withdrawButtonStyle}}">Tạo yêu cầu rút tiền</button>\n' + A3_MY_WD),
]

# ---------------------------------------------------------------------------
# 7.2 Đổi điểm — B3: duyệt 1 lớp, duyệt hàng loạt, tải kết quả thanh toán (8–11)
# ---------------------------------------------------------------------------
_CHK = ('width:16px;height:16px;border:1.5px solid {{%s}};border-radius:3px;'
        'display:inline-flex;align-items:center;justify-content:center;font-size:11px;'
        'font-weight:700;color:#FFFFFF;background:{{%s}}')

B3_BULK_BAR = """
          <!-- (26) Duyệt hàng loạt — chỉ yêu cầu Chờ duyệt -->
          <sc-if value="{{wdHasPending}}" hint-placeholder-val="{{true}}">
            <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--s4);""" + _INFO + """\">
              <div>Đã chọn <strong>{{wdSelCount}}</strong> / {{wdPendingCount}} yêu cầu Chờ duyệt. Duyệt xong điểm bị trừ khỏi số dư thành viên và yêu cầu vào danh sách xuất file chi trả.</div>
              <div style="display:flex;gap:var(--s3);flex-wrap:wrap">
                <button sc-camel-on-click="{{openBulkSelected}}" disabled="{{wdSelDisabled}}" style="{{wdSelBtnStyle}}">Duyệt đã chọn ({{wdSelCount}})</button>
                <button sc-camel-on-click="{{openBulkAll}}" style="height:34px;padding:0 var(--s5);background:var(--c8);color:var(--c12);border:none;border-radius:var(--r-md);font-size:12px;font-weight:600">Duyệt tất cả Chờ duyệt ({{wdPendingCount}})</button>
              </div>
            </div>
          </sc-if>"""

_B3_TABLE_OPEN = (
    '\n          </div>\n'
    '          <div style="background:var(--c12);border:1px solid rgba(154,163,176,.35);'
    'border-radius:var(--r-lg);overflow:auto">\n'
    '            <div style="display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr .9fr')

B3_UPLOAD_MODAL = """            <!-- (26) MODAL: tải lên kết quả thanh toán từ ngân hàng -->
            <sc-if value="{{showPayResult}}" hint-placeholder-val="{{false}}">
              <div style=\"""" + _OVERLAY + """;align-items:flex-start;overflow-y:auto">
                <div style="width:100%;max-width:680px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25);margin:var(--s8) 0">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div><div style="font-size:18px;font-weight:700;color:var(--c1)">Tải lên kết quả thanh toán</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1);line-height:1.6">File danh sách lệnh ngân hàng đã chi thành công (Excel / CSV). Hệ thống đối chiếu theo số tài khoản và số tiền với các yêu cầu Đã duyệt.</div></div>
                    <button sc-camel-on-click="{{closePayResult}}" style="background:none;border:none;font-size:18px;color:var(--c5)">✕</button>
                  </div>
                  <label style="border:1px dashed rgba(154,163,176,.6);border-radius:var(--r-md);padding:var(--s6);display:flex;align-items:center;justify-content:center;gap:var(--s3);cursor:pointer;color:var(--c5);font-size:13px;font-weight:600" style-hover="border-color:#1E3A66;color:#1E3A66">
                    <span style="font-size:18px">⬆</span> Chọn file kết quả thanh toán
                    <input type="file" accept=".xlsx,.xls,.csv" sc-camel-on-change="{{setPayResultFile}}" style="display:none">
                  </label>
                  <button sc-camel-on-click="{{usePayResultSample}}" style="align-self:flex-start;background:none;border:none;font-size:12px;font-weight:600;color:var(--c6);padding:0">Dùng file mẫu (bản demo)</button>
                  <sc-if value="{{hasPayResult}}" hint-placeholder-val="{{false}}">
                    <div style="font-size:13px;color:var(--c2)">File: <strong style="font-family:monospace">{{payResultFile}}</strong></div>
                    <div style="border:1px solid rgba(154,163,176,.35);border-radius:var(--r-md);overflow:auto">
                      <div style="display:grid;grid-template-columns:1.2fr 1fr .9fr 1.6fr;min-width:560px;background:rgba(154,163,176,.08);padding:var(--s4) var(--s5);font-size:11px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em">
                        <div>Thành viên</div><div>Số tài khoản</div><div style="text-align:right">Số tiền</div><div style="text-align:right">Kết quả đối chiếu</div>
                      </div>
                      <sc-for list="{{payResultRows}}" as="pr" hint-placeholder-count="2">
                        <div style="display:grid;grid-template-columns:1.2fr 1fr .9fr 1.6fr;min-width:560px;align-items:center;padding:var(--s4) var(--s5);font-size:13px;color:var(--c1);border-top:1px solid rgba(154,163,176,.2)">
                          <div style="font-weight:600">{{pr.seller}}</div><div style="font-family:monospace;color:var(--c4)">{{pr.accountNumber}}</div><div style="text-align:right;font-weight:700">{{pr.amount}}</div><div style="text-align:right"><span style=\"""" + _BADGE + """;background:{{pr.resultBg}};color:{{pr.resultColor}}">{{pr.resultLabel}}</span></div>
                        </div>
                      </sc-for>
                    </div>
                    <div style="font-size:12px;color:#965C0A;background:rgba(150,92,10,.12);border-radius:var(--r-md);padding:var(--s4) var(--s5);line-height:1.6">1 dòng trong file không khớp yêu cầu nào nên bị bỏ qua: NGUYEN VAN AN · 0123456789 · 300.000đ.</div>
                    <div style="font-size:13px;color:var(--c2)"><strong>{{payOkCount}}</strong> thanh toán thành công · <strong>{{payFailCount}}</strong> chi không thành công (không có trong file — sau khi cập nhật, bấm Hoàn điểm cho từng yêu cầu).</div>
                  </sc-if>
                  <sc-if value="{{payResultEmpty}}" hint-placeholder-val="{{false}}">
                    <div style="font-size:13px;color:var(--c5)">Không còn yêu cầu nào ở trạng thái Đã duyệt để đối chiếu.</div>
                  </sc-if>
                  <sc-if value="{{payResultApplied}}" hint-placeholder-val="{{false}}">
                    <div style="font-size:13px;color:#2F7A48;background:rgba(47,122,72,.12);border-radius:var(--r-md);padding:var(--s5)">{{payResultApplied}}</div>
                  </sc-if>
                  <div style="display:flex;gap:var(--s3)">
                    <button sc-camel-on-click="{{closePayResult}}" style="flex:1;""" + _BTN_G + """;font-size:14px">Đóng</button>
                    <button sc-camel-on-click="{{applyPayResult}}" disabled="{{payApplyDisabled}}" style="{{payApplyStyle}}">Cập nhật trạng thái</button>
                  </div>
                </div>
              </div>
            </sc-if>
"""

B3_BULK_MODAL = """        <!-- (26) Duyệt hàng loạt -->
        <sc-if value="{{isBulkModal}}" hint-placeholder-val="{{false}}">
          <div style="font-size:18px;font-weight:700;color:var(--c1)">Duyệt {{bulkCount}} yêu cầu đổi điểm</div>
          <div style="display:flex;flex-direction:column;gap:var(--s2);max-height:200px;overflow:auto;border:1px solid rgba(154,163,176,.35);border-radius:var(--r-md);padding:var(--s4) var(--s5)">
            <sc-for list="{{bulkRows}}" as="br" hint-placeholder-count="2">
              <div style="display:flex;justify-content:space-between;gap:var(--s4);font-size:13px;color:var(--c2)"><span>{{br.seller}}</span><span style="font-weight:600">{{br.amount}}</span></div>
            </sc-for>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:14px;font-weight:700;color:var(--c1)"><span>Tổng</span><span>{{bulkTotal}}</span></div>
          <div style=\"""" + _INFO + """\">Sau khi duyệt, các yêu cầu chuyển sang Đã duyệt, điểm bị trừ khỏi số dư của thành viên và sẵn sàng xuất file chi trả.</div>
          <div style="display:flex;gap:var(--s3)">
            <button sc-camel-on-click="{{closeActionModal}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Đóng</button>
            <button sc-camel-on-click="{{confirmBulkApprove}}" style="flex:1;height:44px;background:var(--c8);color:var(--c12);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600">Duyệt {{bulkCount}} yêu cầu</button>
          </div>
        </sc-if>

"""

MARKUP_0810 += [
    (_B3_TABLE_OPEN, B3_BULK_BAR + _B3_TABLE_OPEN),
    ('<div>Thành viên</div><div>Khoản thưởng hiện tại</div>',
     '<div sc-camel-on-click="{{wdToggleAll}}" style="display:flex;align-items:center;cursor:pointer">'
     '<span style="' + (_CHK % ('wdAllBorder', 'wdAllBg')) + '">{{wdAllMark}}</span></div>'
     '<div>Thành viên</div><div>Số dư khả dụng</div>'),
    ('"><div>TỔNG</div><div>{{sumRewardLabel}}</div>',
     '"><div></div><div>TỔNG</div><div>{{sumRewardLabel}}</div>'),
    ('\n                <div style="font-weight:600">{{w.seller}}</div>',
     '\n                <div sc-camel-on-click="{{w.onToggle}}" style="display:flex;align-items:center;cursor:{{w.boxCursor}}">'
     '<sc-if value="{{w.selectable}}" hint-placeholder-val="{{false}}">'
     '<span style="' + (_CHK % ('w.boxBorder', 'w.boxBg')) + '">{{w.boxMark}}</span></sc-if></div>'
     '\n                <div style="font-weight:600">{{w.seller}}</div>'),
    ('grid-template-columns:1.2fr 1fr 1fr 1fr .9fr 1.1fr 1fr .9fr .9fr .6fr;min-width:1320px',
     'grid-template-columns:36px 1.2fr 1fr 1fr 1fr .9fr 1.1fr 1fr .9fr .9fr .6fr;min-width:1360px',
     None, 'all'),
    # Bỏ nhãn "Bước 1/2 · Admin duyệt" ở modal duyệt đổi điểm (giữ ở modal duyệt hồ sơ).
    ('          <div style="font-size:11px;font-weight:700;color:#1E3A66;text-transform:uppercase;'
     'letter-spacing:.04em">{{actionStageLabel}}</div>\n'
     '          <div style="font-size:18px;font-weight:700;color:var(--c1)">Xác nhận duyệt yêu cầu</div>',
     '          <div style="font-size:18px;font-weight:700;color:var(--c1)">Xác nhận duyệt yêu cầu</div>'),
    ('        <!-- (22) Chi không thành công + hoàn điểm', B3_BULK_MODAL + '        <!-- (22) Chi không thành công + hoàn điểm'),
    ('            <!-- (21) MODAL: xuất danh sách chi trả', B3_UPLOAD_MODAL + '            <!-- (21) MODAL: xuất danh sách chi trả'),
]

# --- JS đổi điểm --------------------------------------------------------------
JS_0810 += [
    ("    profileSaved: null,\n",
     "    profileSaved: null,\n"
     "    // (26) Đổi điểm sau phản hồi KH: yêu cầu của chính thành viên (A3),\n"
     "    // duyệt hàng loạt và tải kết quả thanh toán (B3).\n"
     "    myWd: null, wdPeriodLocked: false, showCancelWd: false,\n"
     "    wdSel: {}, showPayResult: false, payResultFile: '', payResultApplied: '',\n"),
    ("      pending: ['rgba(150,92,10,.15)', '#965C0A', 'Chờ duyệt (0/2)'],",
     "      pending: ['rgba(150,92,10,.15)', '#965C0A', 'Chờ duyệt'],"),
    ("      approved: ['rgba(15,127,150,.14)', '#0F7F96', 'Đã duyệt (2/2)'],",
     "      approved: ['rgba(15,127,150,.14)', '#0F7F96', 'Đã duyệt'],\n"
     "      cancelled: ['rgba(154,163,176,.18)', '#5B6472', 'Thành viên đã huỷ'],"),
    ("      paid: ['rgba(47,122,72,.14)', '#2F7A48', 'Đã chi trả'],",
     "      paid: ['rgba(47,122,72,.14)', '#2F7A48', 'Thanh toán thành công'],"),
    ("        const nextStatus = isSpecialist ? 'specialist_approved' : 'approved';\n"
     "        const label = isSpecialist ? 'Admin duyệt (chờ Head)' : 'Head xác nhận duyệt';",
     "        // (26) KH chốt: duyệt đổi điểm còn 1 lớp — duyệt là xong.\n"
     "        const nextStatus = 'approved';\n"
     "        const label = isSpecialist ? 'Admin duyệt' : 'Head duyệt';"),
    ("      module:'Rút tiền', target:'YC-2026-0088 · Trần Thị Bích',\n"
     "      action:'Duyệt', before:'Chờ Head duyệt', after:'Đã duyệt',",
     "      module:'Rút tiền', target:'YC-2026-0088 · Trần Thị Bích',\n"
     "      action:'Duyệt', before:'Chờ duyệt', after:'Đã duyệt',"),
    ("      action:'Từ chối', before:'Chờ Head duyệt', after:'Từ chối',",
     "      action:'Từ chối', before:'Chờ duyệt', after:'Từ chối',"),
    ("    // (22)(23) Dòng mẫu cho hoàn điểm và admin sửa hồ sơ — sau UAT 02/10.\n",
     "    // (26) Duyệt hàng loạt + tải file kết quả thanh toán — sau phản hồi KH.\n"
     "    { time:'03/09/2026 09:30', actor:'Nguyễn Thị Hạnh', role:'Admin',\n"
     "      module:'Rút tiền', target:'Kết quả thanh toán kỳ 08/2026',\n"
     "      action:'Tải file lên', before:'2 Đã duyệt', after:'1 thanh toán thành công / 1 chi không thành công',\n"
     "      evidence:'sao-ke-chi-tra-HOMI365-2026-08.xlsx', ip:'113.161.46.118' },\n"
     "    { time:'01/09/2026 10:15', actor:'Nguyễn Thị Hạnh', role:'Admin',\n"
     "      module:'Rút tiền', target:'Kỳ 08/2026 · 12 yêu cầu',\n"
     "      action:'Duyệt', before:'Chờ duyệt', after:'Đã duyệt',\n"
     "      evidence:'Duyệt hàng loạt', ip:'113.161.46.118' },\n"
     "    // (22)(23) Dòng mẫu cho hoàn điểm và admin sửa hồ sơ — sau UAT 02/10.\n"),
    # A3 — yêu cầu của chính thành viên.
    ("    const hasActiveThisMonth = false;",
     "    // (26) Mục 8 — mỗi kỳ 1 yêu cầu; đang có yêu cầu Chờ duyệt / Đã duyệt thì\n"
     "    // khoá nút tạo mới, muốn đổi số điểm thì huỷ rồi tạo lại trước khoá sổ.\n"
     "    const myWd = s.myWd;\n"
     "    const myWdOpen = !!(myWd && ['pending', 'approved'].includes(myWd.status));\n"
     "    const hasActiveThisMonth = myWdOpen;"),
    ("      submitWithdrawForm: () => this.setState({ showWithdrawForm: false, showWithdrawSuccess: true }),",
     "      submitWithdrawForm: () => this.setState({ showWithdrawForm: false, showWithdrawSuccess: true,\n"
     "        myWd: { amount: withdrawAmountNum.toLocaleString('vi-VN') + 'đ',\n"
     "                date: this.nowStamp().slice(0, 10), status: 'pending' } }),"),
    ("      hasActiveThisMonth, nextWithdrawDate: '01/10/2026',",
     "      hasActiveThisMonth, nextWithdrawDate: '01/10/2026',\n"
     "      // (26) Kỳ hiện tại và hạn gửi / huỷ yêu cầu. Chính sách ưu đãi thành viên\n"
     "      // mục 4 (HOMI365 chốt 08/10): gửi TRƯỚC ngày cuối cùng của tháng → hạn là\n"
     "      // 23:59 ngày liền trước ngày cuối tháng; ngày cuối tháng đã khoá sổ.\n"
     "      wdPeriod: '09/2026', wdLockLabel: '23:59 ngày 29/09/2026',\n"
     "      hasMyWd: !!myWd, myWdAmount: myWd ? myWd.amount : '', myWdDate: myWd ? myWd.date : '',\n"
     "      myWdStatusLabel: !myWd ? '' : myWd.status === 'cancelled' ? 'Đã huỷ'\n"
     "        : myWd.status === 'approved' ? 'Đã duyệt'\n"
     "        : s.wdPeriodLocked ? 'Đã khoá sổ · chờ duyệt' : 'Chờ duyệt',\n"
     "      myWdBadgeBg: !myWd || myWd.status === 'cancelled' ? 'rgba(154,163,176,.18)'\n"
     "        : myWd.status === 'approved' ? 'rgba(15,127,150,.14)' : 'rgba(150,92,10,.15)',\n"
     "      myWdBadgeColor: !myWd || myWd.status === 'cancelled' ? '#5B6472'\n"
     "        : myWd.status === 'approved' ? '#0F7F96' : '#965C0A',\n"
     "      canCancelWd: !!(myWd && myWd.status === 'pending' && !s.wdPeriodLocked),\n"
     "      wdLockedNote: !!(myWdOpen && s.wdPeriodLocked),\n"
     "      myWdCancelled: !!(myWd && myWd.status === 'cancelled'),\n"
     "      showCancelWd: s.showCancelWd,\n"
     "      openCancelWd: () => this.setState({ showCancelWd: true }),\n"
     "      closeCancelWd: () => this.setState({ showCancelWd: false }),\n"
     "      confirmCancelWd: () => this.setState({ showCancelWd: false,\n"
     "        myWd: { ...s.myWd, status: 'cancelled' } }),"),
    # B3 — ô chọn từng dòng + duyệt hàng loạt + đối chiếu kết quả thanh toán.
    ("    const withdrawalsEmpty = withdrawals.length === 0;",
     """    const withdrawalsEmpty = withdrawals.length === 0;

    // (26) Duyệt hàng loạt — chỉ yêu cầu Chờ duyệt mới chọn được.
    const wdSel = s.wdSel || {};
    const wdPendingAll = withdrawalsData.filter(w => w.status === 'pending');
    withdrawals.forEach(w => {
      const on = !!wdSel[w.id], can = w.status === 'pending';
      Object.assign(w, { selectable: can, boxMark: on ? '✓' : '',
        boxBg: on ? '#1E3A66' : '#FFFFFF', boxBorder: on ? '#1E3A66' : 'rgba(154,163,176,.8)',
        boxCursor: can ? 'pointer' : 'default',
        onToggle: (e) => { if (e) e.stopPropagation(); if (!can) return;
          this.setState({ wdSel: { ...wdSel, [w.id]: !on } }); } });
    });
    const wdSelIds = wdPendingAll.filter(w => wdSel[w.id]).map(w => w.id);
    const wdAllOn = wdPendingAll.length > 0 && wdSelIds.length === wdPendingAll.length;
    const bulkIds = (s.actionModal && s.actionModal.type === 'bulk') ? (s.actionModal.ids || []) : [];
    const bulkRows = withdrawalsData.filter(w => bulkIds.includes(w.id));

    // (26) Đối chiếu file kết quả thanh toán với các yêu cầu Đã duyệt. Bản mẫu:
    // mọi yêu cầu đều khớp file, trừ yêu cầu của Trương Thanh Bình (id 8) — để
    // thấy được nhánh chi không thành công.
    const payResultRows = withdrawalsData.filter(w => w.status === 'approved').map(w => {
      const ok = w.id !== 8;
      return { ...w, ok,
        resultLabel: ok ? 'Khớp · Thanh toán thành công' : 'Không có trong file · Chi không thành công',
        resultBg: ok ? 'rgba(47,122,72,.14)' : 'rgba(192,57,43,.12)',
        resultColor: ok ? '#2F7A48' : '#C0392B' };
    });
    const payApplyDisabled = !s.payResultFile || !!s.payResultApplied || !payResultRows.length;"""),
]

# Duyệt 1 lớp: ghi đè quyền và câu chữ của ngăn chi tiết yêu cầu.
_JS_WD_1LAYER = """    // (26) KH chốt: duyệt đổi điểm còn 1 lớp (Admin). Không còn "Chờ Head",
    // không đánh dấu đã chi trả bằng tay — trạng thái thanh toán cập nhật từ
    // file kết quả ngân hàng.
    if (selectedWithdrawal) {
      const st0 = selectedWithdrawal.status;
      Object.assign(selectedWithdrawal, {
        canApprove: st0 === 'pending', canReject: st0 === 'pending', canMarkPaid: false,
        approveButtonLabel: 'Duyệt',
        approvalStageNote: ({
          pending: 'Đang chờ Admin duyệt. Duyệt xong điểm bị trừ khỏi số dư và yêu cầu vào danh sách xuất file chi trả.',
          approved: 'Đã duyệt — chờ xuất file chi trả và tải lên kết quả thanh toán từ ngân hàng.',
          paid: 'Thanh toán thành công (cập nhật từ file kết quả ngân hàng).',
          cancelled: 'Thành viên đã tự huỷ yêu cầu trước ngày khoá sổ.'
        })[st0] || selectedWithdrawal.approvalStageNote
      });
    }

"""

_JS_WD_RET_0810 = """
      // (26) Duyệt hàng loạt.
      wdHasPending: wdPendingAll.length > 0, wdPendingCount: wdPendingAll.length,
      wdSelCount: wdSelIds.length, wdSelDisabled: wdSelIds.length === 0,
      wdSelBtnStyle: 'height:34px;padding:0 var(--s5);border-radius:var(--r-md);font-size:12px;font-weight:600;'
        + (wdSelIds.length ? 'background:var(--c12);color:var(--c8);border:1px solid var(--c8);cursor:pointer'
                           : 'background:transparent;color:rgba(154,163,176,.9);border:1px dashed rgba(154,163,176,.6);cursor:not-allowed'),
      wdAllMark: wdAllOn ? '✓' : '', wdAllBg: wdAllOn ? '#1E3A66' : '#FFFFFF',
      wdAllBorder: wdAllOn ? '#1E3A66' : 'rgba(154,163,176,.8)',
      wdToggleAll: () => this.setState({ wdSel: wdAllOn ? {}
        : Object.fromEntries(wdPendingAll.map(w => [w.id, true])) }),
      openBulkSelected: () => wdSelIds.length && this.setState({
        actionModal: { type: 'bulk', kind: 'withdrawal', ids: wdSelIds } }),
      openBulkAll: () => this.setState({
        actionModal: { type: 'bulk', kind: 'withdrawal', ids: wdPendingAll.map(w => w.id) } }),
      isBulkModal: !!(s.actionModal && s.actionModal.type === 'bulk'),
      bulkRows, bulkCount: bulkRows.length,
      bulkTotal: bulkRows.reduce((t, w) => t + w.amountNum, 0).toLocaleString('vi-VN') + 'đ',
      confirmBulkApprove: () => {
        const now = '01/09/2026 10:15';
        const actor = s.adminRole === 'specialist' ? 'Admin' : 'Head';
        this.setState({ withdrawalsData: withdrawalsData.map(w => bulkIds.includes(w.id) && w.status === 'pending'
          ? { ...w, status: 'approved', auditLog: [...w.auditLog, { label: actor + ' duyệt (duyệt hàng loạt)', actor, time: now }] }
          : w), actionModal: null, wdSel: {} });
      },
      // (26) Tải lên kết quả thanh toán.
      showPayResult: s.showPayResult,
      openPayResult: () => this.setState({ showPayResult: true, payResultFile: '', payResultApplied: '' }),
      closePayResult: () => this.setState({ showPayResult: false, payResultFile: '', payResultApplied: '' }),
      setPayResultFile: (e) => this.setState({ payResultApplied: '',
        payResultFile: (e.target.files && e.target.files[0]) ? e.target.files[0].name : '' }),
      usePayResultSample: () => this.setState({ payResultFile: 'sao-ke-chi-tra-HOMI365-2026-08.xlsx', payResultApplied: '' }),
      payResultFile: s.payResultFile,
      hasPayResult: !!s.payResultFile && payResultRows.length > 0 && !s.payResultApplied,
      payResultEmpty: !!s.payResultFile && !payResultRows.length && !s.payResultApplied,
      payResultRows,
      payOkCount: payResultRows.filter(r => r.ok).length,
      payFailCount: payResultRows.filter(r => !r.ok).length,
      payResultApplied: s.payResultApplied,
      payApplyDisabled,
      payApplyStyle: 'flex:1;height:44px;border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:#FFFFFF;background:'
        + (payApplyDisabled ? 'rgba(154,163,176,.5)' : 'var(--c6)') + ';cursor:' + (payApplyDisabled ? 'not-allowed' : 'pointer'),
      applyPayResult: () => {
        if (payApplyDisabled) return;
        const now = '03/09/2026 09:30', file = s.payResultFile;
        const okIds = payResultRows.filter(r => r.ok).map(r => r.id);
        const failIds = payResultRows.filter(r => !r.ok).map(r => r.id);
        this.setState({
          withdrawalsData: withdrawalsData.map(w => okIds.includes(w.id)
            ? { ...w, status: 'paid', paidNote: 'Theo file ' + file,
                auditLog: [...w.auditLog, { label: 'Thanh toán thành công (file ' + file + ')', actor: 'Admin', time: now }] }
            : failIds.includes(w.id)
              ? { ...w, status: 'pay_failed', failNote: 'Không có trong file kết quả thanh toán ' + file + '.',
                  auditLog: [...w.auditLog, { label: 'Chi không thành công (không có trong file ' + file + ')', actor: 'Admin', time: now }] }
              : w),
          payResultApplied: 'Đã cập nhật: ' + okIds.length + ' thanh toán thành công, ' + failIds.length
            + ' chi không thành công. Vào từng yêu cầu Chi không thành công để Hoàn điểm.'
        });
      },"""


JS_0810 += [
    ("    // (22) Ngân hàng chi không thành công -> hoàn điểm thủ công.\n",
     _JS_WD_1LAYER + "    // (22) Ngân hàng chi không thành công -> hoàn điểm thủ công.\n"),
    ("      // (21) Xuất danh sách chi trả.\n",
     _JS_WD_RET_0810.lstrip("\n") + "\n      // (21) Xuất danh sách chi trả.\n"),
]

MARKUP_0810 += [
    # Nút tải kết quả thanh toán đặt cạnh nút xuất file.
    ('            <button sc-camel-on-click="{{openPayoutExport}}"',
     '            <div style="display:flex;gap:var(--s3);flex-wrap:wrap"><button sc-camel-on-click="{{openPayResult}}" '
     'style="height:38px;padding:0 var(--s6);background:var(--c12);border:1px solid rgba(154,163,176,.6);'
     'border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c2)" style-hover="background:rgba(154,163,176,.08)">'
     'Tải lên kết quả thanh toán</button><button sc-camel-on-click="{{openPayoutExport}}"'),
    ('Xuất danh sách chi trả</button>\n', 'Xuất danh sách chi trả</button></div>\n'),
    ('Chỉ lấy các yêu cầu <strong>đã duyệt đủ 2 bước</strong> và chưa chi của kỳ được chọn.',
     'Chỉ lấy các yêu cầu <strong>Đã duyệt</strong>, chưa thanh toán, của kỳ được chọn. Ngân hàng chi xong thì tải file kết quả lên bằng nút <strong>Tải lên kết quả thanh toán</strong>.'),
]


# ---------------------------------------------------------------------------
# 7.3 Thăng / hạ cấp — màn B9, gói quy đổi, tuyến trên hiệu lực, bổ nhiệm
#     đặc biệt, Super Lithium (mục 12–15, 17, 18, 20, 21)
# ---------------------------------------------------------------------------
_OFF_STYLE = ("'display:flex;justify-content:space-between;align-items:center;gap:var(--s4);"
              "width:100%;min-height:42px;padding:var(--s3) var(--s5);border-radius:var(--r-md);"
              "font-size:13px;text-align:left;border:1px dashed rgba(154,163,176,.5);"
              "background:transparent;color:rgba(154,163,176,.9);cursor:not-allowed'")

B2_RANK_ROWS = """          <!-- (27) Gói xét cấp + tuyến trên hiệu lực -->
          <div style="display:flex;flex-direction:column;gap:var(--s3);font-size:13px;margin-bottom:var(--s5);border:1px solid rgba(154,163,176,.3);border-radius:var(--r-md);padding:var(--s5)">
            <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Gói xét cấp (từ lần đổi cấp gần nhất)</span><span style="font-weight:700;color:var(--c1)">{{mRankCount}}</span></div>
            <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Gói tháng này (quy đổi)</span><span style="font-weight:600;color:var(--c2)">{{mRankMonth}}</span></div>
            <div style="font-size:11px;color:var(--c5);line-height:1.6">Gói 1 năm = 1 · gói 6 tháng = 0,5. Mỗi tháng lên hoặc xuống tối đa 1 cấp; dưới 1 gói quy đổi trong tháng thì bị hạ 1 cấp.</div>
            <div style="height:1px;background:rgba(154,163,176,.25)"></div>
            <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Tuyến trên trực tiếp</span><span style="color:var(--c2);text-align:right">{{mUplineDirect}}</span></div>
            <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Tuyến trên hiệu lực</span><span style="font-weight:700;color:var(--c1);text-align:right">{{mUplineEff}}</span></div>
            <sc-if value="{{hasUplineNote}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:#965C0A;background:rgba(150,92,10,.12);border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">{{mUplineNote}}</div>
            </sc-if>
          </div>
          <sc-if value="{{hasRankSaved}}" hint-placeholder-val="{{false}}">
            <div style="font-size:12px;color:#2F7A48;background:rgba(47,122,72,.12);border-radius:var(--r-md);padding:var(--s4) var(--s5);margin-bottom:var(--s5);line-height:1.6">{{rankSavedText}}</div>
          </sc-if>
"""

RANK_MODAL_NEW = """  <!-- MODAL: bổ nhiệm đặc biệt (17/09, làm lại theo phản hồi KH 08/10) -->
  <sc-if value="{{showRankEdit}}" hint-placeholder-val="{{false}}">
    <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:flex-start;justify-content:center;z-index:260;padding:var(--s7);overflow-y:auto">
      <div style="width:100%;max-width:460px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25);margin:var(--s8) 0">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:var(--s5)">
          <div>
            <div style="font-size:18px;font-weight:700;color:var(--c1)">Bổ nhiệm đặc biệt</div>
            <div style="font-size:12px;color:var(--c5);margin-top:var(--s1);line-height:1.6">{{rankEditName}} · đang ở cấp <strong>{{rankEditCurrent}}</strong></div>
          </div>
          <button sc-camel-on-click="{{closeRankEdit}}" style="background:none;border:none;font-size:18px;color:var(--c5);flex:none">&#10005;</button>
        </div>
        <div style=\"""" + _INFO + """\">Việc duyệt làm <strong>ngoài hệ thống</strong>. Admin chỉ xác nhận bổ nhiệm sau khi đã được duyệt — cấp mới <strong>có hiệu lực ngay khi lưu</strong>. Hệ thống gửi email cho <strong>anh Phương</strong> và lưu email làm bằng chứng.</div>
        <div style="display:flex;flex-direction:column;gap:var(--s2)">
          <div style="font-size:13px;font-weight:600;color:var(--c2)">Cấp đề nghị</div>
          <sc-for list="{{rankOptions}}" as="ro" hint-placeholder-count="7">
            <button sc-camel-on-click="{{ro.onClick}}" disabled="{{ro.disabled}}" style="{{ro.style}}"><span>{{ro.name}}</span><span style="font-size:11px;text-align:right;line-height:1.5">{{ro.note}}</span></button>
          </sc-for>
          <div style="font-size:11px;color:var(--c5);line-height:1.6">Không chọn được cấp <strong>bằng hoặc cao hơn</strong> tuyến trên hiệu lực ({{rankEditUpLabel}}), cũng không thấp hơn tuyến dưới trực tiếp. Super Lithium là tài khoản công ty.</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:13px;font-weight:600;color:var(--c2)">Lý do (*)</label><textarea placeholder="VD: Đạt doanh số đặc biệt quý 3" value="{{rankReason}}" sc-camel-on-change="{{setRankReason}}" style="min-height:80px;padding:var(--s4) var(--s5);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px;resize:vertical"></textarea></div>
        <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:13px;font-weight:600;color:var(--c2)">Người yêu cầu (*)</label><input type="text" placeholder="Họ tên người đề nghị bổ nhiệm" value="{{rankRequester}}" sc-camel-on-change="{{setRankRequester}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px" style-focus=\"""" + _FOCUS + """\"></div>
        <div style="display:flex;gap:var(--s3)">
          <button sc-camel-on-click="{{closeRankEdit}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Huỷ</button>
          <button sc-camel-on-click="{{submitRankEdit}}" disabled="{{rankSubmitDisabled}}" style="{{rankSubmitStyle}}">Xác nhận bổ nhiệm &amp; gửi email</button>
        </div>
      </div>
    </div>
  </sc-if>

"""

CUTS.append(("  <!-- MODAL: cập nhật cấp thành viên (bổ sung 17/09) -->",
             "  <!-- MODAL: approve/reject/paid confirm -->", RANK_MODAL_NEW))

_RR_COLS = "30px 1.25fr .7fr .9fr .95fr .8fr 1.9fr 1fr 1.25fr"
B9_SCREEN = """      <!-- B9 XÉT THĂNG / HẠ CẤP (bổ sung sau UAT 02/10 — mục 12, 13, 14, 17, 18) -->
      <sc-if value="{{isB9}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;flex-direction:column;gap:var(--s7)">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
            <div><div style="font-size:24px;font-weight:700">Xét thăng / hạ cấp</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">Kỳ 09/2026 · danh sách đề xuất lập lúc 00:00 ngày 01/10/2026 · cấp mới chỉ có hiệu lực khi được duyệt</div></div>
            <button sc-camel-on-click="{{rrRunSel}}" disabled="{{rrSelDisabled}}" style="{{rrRunStyle}}">Chạy lại xét cấp cho nhóm đã chọn ({{rrSelCount}})</button>
          </div>
          <div style=\"""" + _INFO + """\">Mỗi tháng lên/xuống tối đa <strong>1 cấp</strong> · lên cấp thì gói xét cấp <strong>về 0</strong> · gói 1 năm = 1, gói 6 tháng = 0,5 · cần lên cấp: Silver <strong>10</strong> · Gold <strong>8</strong> · Diamond <strong>6</strong> · Titanium <strong>4</strong> · Lithium <strong>2</strong> gói · tháng dưới 1 gói thì hạ 1 cấp.</div>
          <sc-if value="{{rrRunNote}}" hint-placeholder-val="{{false}}">
            <div style="font-size:13px;color:#2F7A48;background:rgba(47,122,72,.12);border-radius:var(--r-md);padding:var(--s4) var(--s5)">{{rrRunNote}}</div>
          </sc-if>
          <div style="display:flex;gap:var(--s5);flex-wrap:wrap;align-items:center;justify-content:space-between">
            <div style="display:flex;gap:var(--s2);flex-wrap:wrap">
              <sc-for list="{{rrFilters}}" as="f" hint-placeholder-count="4">
                <button sc-camel-on-click="{{f.onClick}}" style="{{f.style}}">{{f.label}}</button>
              </sc-for>
            </div>
            <div style="display:flex;gap:var(--s3);flex-wrap:wrap">
              <button sc-camel-on-click="{{rrApproveSel}}" disabled="{{rrSelDisabled}}" style="{{rrSelBtnStyle}}">Duyệt đã chọn ({{rrSelCount}})</button>
              <button sc-camel-on-click="{{rrApproveAll}}" disabled="{{rrNoPending}}" style="{{rrAllBtnStyle}}">Duyệt tất cả ({{rrPendingCount}})</button>
            </div>
          </div>
          <div style="background:var(--c12);border:1px solid rgba(154,163,176,.35);border-radius:var(--r-lg);overflow:auto">
            <div style="display:grid;grid-template-columns:""" + _RR_COLS + """;min-width:1060px;background:rgba(154,163,176,.08);padding:var(--s5) var(--s6);font-size:11px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;align-items:center">
              <div sc-camel-on-click="{{rrToggleAll}}" style="display:flex;align-items:center;cursor:pointer"><span style=\"""" + (_CHK % ('rrAllBorder', 'rrAllBg')) + """\">{{rrAllMark}}</span></div><div>Thành viên</div><div>Cấp hiện tại</div><div>Gói xét cấp</div><div>Tháng này (quy đổi)</div><div>Đề xuất</div><div>Lý do hệ thống đề xuất</div><div>Trạng thái</div><div></div>
            </div>
            <sc-for list="{{rrRows}}" as="r" hint-placeholder-count="3">
              <div style="display:grid;grid-template-columns:""" + _RR_COLS + """;min-width:1060px;align-items:start;padding:var(--s5) var(--s6);font-size:13px;color:var(--c1);border-top:1px solid rgba(154,163,176,.2)">
                <div sc-camel-on-click="{{r.onToggle}}" style="display:flex;align-items:center;cursor:{{r.boxCursor}};padding-top:2px"><sc-if value="{{r.canAct}}" hint-placeholder-val="{{true}}"><span style=\"""" + (_CHK % ('r.boxBorder', 'r.boxBg')) + """\">{{r.boxMark}}</span></sc-if></div>
                <div><div style="font-weight:600">{{r.name}}</div><div style="font-size:11px;color:var(--c5);font-family:monospace">{{r.code}}</div></div>
                <div style="font-weight:600">{{r.from}}</div>
                <div><div style="font-weight:700">{{r.cum}}</div><div style="font-size:11px;color:var(--c5)">{{r.cumSub}}</div></div>
                <div><div style="font-weight:600">{{r.month}}</div><div style="font-size:11px;color:var(--c5)">{{r.monthSub}}</div></div>
                <div><span style=\"""" + _BADGE + """;background:{{r.propBg}};color:{{r.propColor}}">{{r.propLabel}}</span></div>
                <div style="color:var(--c2);line-height:1.55;font-size:12px">{{r.reason}}<sc-if value="{{r.hasNote}}" hint-placeholder-val="{{false}}"><div style="font-size:11px;color:#965C0A;margin-top:var(--s1)">{{r.note}}</div></sc-if></div>
                <div><span style=\"""" + _BADGE + """;background:{{r.stBg}};color:{{r.stColor}}">{{r.stLabel}}</span><div style="font-size:11px;color:var(--c5);margin-top:var(--s1)">{{r.stSub}}</div><sc-if value="{{r.hasDenyReason}}" hint-placeholder-val="{{false}}"><div style="font-size:11px;color:var(--c5);margin-top:var(--s2);line-height:1.5">Lý do: {{r.denyReason}}</div></sc-if></div>
                <div style="display:flex;gap:var(--s2);justify-content:flex-end;flex-wrap:wrap">
                  <sc-if value="{{r.canAct}}" hint-placeholder-val="{{true}}">
                    <button sc-camel-on-click="{{r.onApprove}}" style="height:32px;padding:0 var(--s5);background:var(--c8);color:var(--c12);border:none;border-radius:var(--r-md);font-size:12px;font-weight:600">Duyệt</button>
                    <button sc-camel-on-click="{{r.onDeny}}" style="height:32px;padding:0 var(--s5);background:var(--c12);color:var(--err);border:1px solid var(--err);border-radius:var(--r-md);font-size:12px;font-weight:600">Từ chối</button>
                  </sc-if>
                </div>
              </div>
            </sc-for>
            <sc-if value="{{rrEmpty}}" hint-placeholder-val="{{false}}">
              <div style="padding:var(--s9);text-align:center;color:var(--c5);font-size:13px">Không có đề xuất nào khớp bộ lọc.</div>
            </sc-if>
          </div>
        </div>

        <sc-if value="{{isRrDeny}}" hint-placeholder-val="{{false}}">
          <div style=\"""" + _OVERLAY + """\">
            <div style="width:100%;max-width:400px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
              <div style="font-size:18px;font-weight:700;color:var(--c1)">Từ chối đề xuất</div>
              <div style="font-size:13px;color:var(--c5)">{{rrModalName}} · {{rrModalProp}}. Nhập lý do không duyệt (bắt buộc):</div>
              <textarea placeholder="Nhập lý do…" value="{{rrDenyText}}" sc-camel-on-change="{{setRrDenyText}}" style="min-height:90px;padding:var(--s5);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px;resize:vertical"></textarea>
              <div style="display:flex;gap:var(--s3)">
                <button sc-camel-on-click="{{closeRrModal}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Huỷ</button>
                <button sc-camel-on-click="{{confirmRrDeny}}" disabled="{{rrDenyDisabled}}" style="{{rrDenyStyle}}">Từ chối</button>
              </div>
            </div>
          </div>
        </sc-if>
        <sc-if value="{{isRrBulk}}" hint-placeholder-val="{{false}}">
          <div style=\"""" + _OVERLAY + """\">
            <div style="width:100%;max-width:420px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
              <div style="font-size:18px;font-weight:700;color:var(--c1)">Duyệt {{rrBulkCount}} đề xuất</div>
              <div style="display:flex;flex-direction:column;gap:var(--s2);border:1px solid rgba(154,163,176,.35);border-radius:var(--r-md);padding:var(--s4) var(--s5)">
                <sc-for list="{{rrBulkRows}}" as="b" hint-placeholder-count="3">
                  <div style="display:flex;justify-content:space-between;gap:var(--s4);font-size:13px;color:var(--c2)"><span>{{b.name}}</span><span style="font-weight:600">{{b.from}} → {{b.to}}</span></div>
                </sc-for>
              </div>
              <div style=\"""" + _INFO + """\">Cấp mới có hiệu lực từ 01/10/2026. Hệ thống gửi email báo thăng / hạ cấp cho từng thành viên và ghi lịch sử thay đổi hạng.</div>
              <div style="display:flex;gap:var(--s3)">
                <button sc-camel-on-click="{{closeRrModal}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Đóng</button>
                <button sc-camel-on-click="{{confirmRrBulk}}" style="flex:1;height:44px;background:var(--c8);color:var(--c12);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600">Duyệt {{rrBulkCount}} đề xuất</button>
              </div>
            </div>
          </div>
        </sc-if>
      </sc-if>

"""

MARKUP_0810 += [
    ('            <span style="font-weight:700;color:var(--c1)">{{effRank}} · {{selectedMember.tierLabel}}</span>\n'
     '          </div>\n',
     '            <span style="font-weight:700;color:var(--c1)">{{effRank}} · {{selectedMember.tierLabel}}</span>\n'
     '          </div>\n' + B2_RANK_ROWS),
    ('>Cập nhật cấp</button>', '>Bổ nhiệm đặc biệt</button>'),
    ('Việc trình và duyệt làm ngoài hệ thống. Ở đây chỉ ghi nhận cấp đã được duyệt, kèm số phiếu để đối chiếu.',
     'Duyệt làm ngoài hệ thống. Admin nhập lý do và người yêu cầu rồi xác nhận — cấp mới có hiệu lực ngay, hệ thống gửi email cho anh Phương.'),
    ('      <!-- B4 WAREHOUSE -->', B9_SCREEN + '      <!-- B4 WAREHOUSE -->'),
    # (09/10) KH: A3 chỉ 1 dòng "Gói xét cấp x / y · còn z gói để lên …", bỏ dòng tháng này.
]

_JS_RR_CLASS = """  // (27) Xét cấp sau phản hồi KH — mục 12–14, 17, 18. Ngưỡng theo Chính sách ưu đãi
  // thành viên mục 3 (HOMI365 chốt 08/10), đơn vị là gói quy đổi (CR mục 17).
  // Gói xét cấp đếm từ lần đổi cấp gần nhất; y = gói 1 năm, h = gói 6 tháng,
  // my / mh = riêng tháng này. Trọng số: 1 năm = 1 gói, 6 tháng = 0,5 gói.
  RANK_THRESHOLD = { Silver: 10, Gold: 18, Diamond: 24, Titanium: 28, Lithium: 30 };
  // (09/10) Lên cấp thì đếm lại từ 0 → số gói cần cho MỖI BẬC = ngưỡng cấp đích
  // trừ ngưỡng cấp hiện tại: Copper→Silver 10 · Silver→Gold 8 · Gold→Diamond 6 ·
  // Diamond→Titanium 4 · Titanium→Lithium 2 (KH xác nhận: Silver lên Gold cần 8 gói).
  rankStep(to) { const i = this.RANKS.indexOf(to); if (i <= 0) return null;
    const prev = this.RANKS[i - 1]; return this.RANK_THRESHOLD[to] - (this.RANK_THRESHOLD[prev] || 0); }
  RANK_COUNT = { 1:{y:3,h:2,my:0,mh:1}, 2:{y:8,h:5,my:2,mh:1}, 3:{y:0,h:0,my:0,mh:0},
                 4:{y:1,h:1,my:0,mh:1}, 5:{y:7,h:4,my:3,mh:2}, 6:{y:0,h:0,my:0,mh:0},
                 7:{y:2,h:2,my:1,mh:0} };
  RANK_REVIEW = [
    { id:2, to:'Silver', dir:'up', reason:'Đủ ngưỡng Copper → Silver: 10,5 / 10 gói quy đổi.',
      note:'Lên Silver là ngang tuyến trên Trần Thị Bích — tuyến trên hiệu lực chuyển lên người kế tiếp có cấp cao hơn.' },
    { id:1, to:'Copper', dir:'down', reason:'Tháng này chỉ 0,5 gói quy đổi (1 gói 6 tháng) — dưới 1 gói. Nửa gói lẻ không cộng dồn sang tháng sau.', note:'' },
    { id:5, to:'Diamond', dir:'up', reason:'Đủ ngưỡng Gold → Diamond: 9 / 6 gói quy đổi. Không nhảy bậc — bán bao nhiêu trong tháng cũng chỉ lên 1 cấp.',
      note:'Lên Diamond thì gói xét cấp về 0, 3 gói dư không chuyển sang. Muốn lên Titanium phải bán thêm đủ 4 gói.' }
  ];
  pkgCount(c) { return c.y + c.h * 0.5; }
  nfmt(x) { return Number(x).toLocaleString('vi-VN'); }
  nextRank(r) { const i = this.RANKS.indexOf(r); return i >= 0 && i < this.RANKS.length - 1 ? this.RANKS[i + 1] : null; }

  // 7.3.3 AC (làm lại sau phản hồi KH): hiển thị gói xét cấp đã quy đổi.
  RANK_PROGRESS = { new: 'Gói xét cấp 1 / 10 · còn 9 gói để lên Silver',
                    active: 'Gói xét cấp 1,5 / 8 · còn 6,5 gói để lên Gold' };
  RANK_MONTH_NOTE = { new: 'Tháng này 1 gói · gói 6 tháng tính 0,5 · lên cấp mới đếm lại từ 0',
                      active: 'Tháng này 1,5 gói (1 gói 1 năm + 1 gói 6 tháng) · đủ giữ hạng' };"""

_JS_RR_CONSTS = """    // (27) Màn Xét thăng / hạ cấp (B9).
    const rrStatus = s.rrStatus || {}, rrSel = s.rrSel || {}, rrReasons = s.rrReason || {};
    const rrAllRows = this.RANK_REVIEW.map(r => {
      const m = this.MEMBERS.find(x => x.id === r.id);
      const from = this.RANK_LABEL[m.rank] || m.rank;
      const c = this.RANK_COUNT[r.id], nr = this.nextRank(from);
      const st = rrStatus[r.id] || 'pending', can = st === 'pending', on = can && !!rrSel[r.id];
      return { ...r, name: m.name, code: ALIAS[m.id], from,
        cum: this.nfmt(this.pkgCount(c)) + (nr ? ' / ' + this.rankStep(nr) : ''),
        cumSub: c.y + ' gói 1 năm + ' + c.h + ' gói 6 tháng',
        month: this.nfmt(c.my + c.mh * 0.5) + ' gói', monthSub: c.my + ' × 1 năm + ' + c.mh + ' × 6 tháng',
        propLabel: (r.dir === 'up' ? '↑ ' : '↓ ') + r.to,
        propBg: r.dir === 'up' ? 'rgba(47,122,72,.14)' : 'rgba(192,57,43,.12)',
        propColor: r.dir === 'up' ? '#2F7A48' : '#C0392B',
        hasNote: !!r.note, st, canAct: can,
        stLabel: st === 'approved' ? 'Đã duyệt' : st === 'denied' ? 'Từ chối' : 'Chờ duyệt',
        stSub: st === 'approved' ? 'Hiệu lực 01/10/2026 · đã gửi email' : '',
        stBg: st === 'approved' ? 'rgba(47,122,72,.14)' : st === 'denied' ? 'rgba(192,57,43,.12)' : 'rgba(150,92,10,.15)',
        stColor: st === 'approved' ? '#2F7A48' : st === 'denied' ? '#C0392B' : '#965C0A',
        hasDenyReason: st === 'denied' && !!rrReasons[r.id], denyReason: rrReasons[r.id] || '',
        boxMark: on ? '✓' : '', boxBg: on ? '#1E3A66' : '#FFFFFF',
        boxBorder: on ? '#1E3A66' : 'rgba(154,163,176,.8)', boxCursor: can ? 'pointer' : 'default',
        onToggle: (e) => { if (e) e.stopPropagation(); if (!can) return;
          this.setState({ rrSel: { ...rrSel, [r.id]: !on } }); },
        onApprove: () => this.setState({ rrStatus: { ...rrStatus, [r.id]: 'approved' },
          rrSel: { ...rrSel, [r.id]: false } }),
        onDeny: () => this.setState({ rrModal: { type: 'deny', id: r.id }, rrDenyText: '' }) };
    });
    const rrRows = rrAllRows.filter(r => (s.rrFilter || 'all') === 'all' || r.st === s.rrFilter);
    const rrPending = rrAllRows.filter(r => r.st === 'pending');
    const rrSelIds = rrPending.filter(r => rrSel[r.id]).map(r => r.id);
    const rrAllOn = rrPending.length > 0 && rrSelIds.length === rrPending.length;
    const rrModal = s.rrModal || null;
    const rrDenyRow = rrModal && rrModal.type === 'deny' ? rrAllRows.find(r => r.id === rrModal.id) : null;
    const rrBulkRows = rrModal && rrModal.type === 'bulk' ? rrAllRows.filter(r => (rrModal.ids || []).includes(r.id)) : [];
    const rrDenyDisabled = !(s.rrDenyText || '').trim();
    const rrBtn = (on, solid) => 'height:34px;padding:0 var(--s5);border-radius:var(--r-md);font-size:12px;font-weight:600;'
      + (!on ? 'background:transparent;color:rgba(154,163,176,.9);border:1px dashed rgba(154,163,176,.6);cursor:not-allowed'
         : solid ? 'background:var(--c8);color:var(--c12);border:none;cursor:pointer'
         : 'background:var(--c12);color:var(--c8);border:1px solid var(--c8);cursor:pointer');

    // (27) Thông tin xét cấp + tuyến trên hiệu lực của thành viên đang mở.
    const mRc0 = selectedMember ? this.RANK_COUNT[selectedMember.id] : null;
    // (09/10) Vừa bổ nhiệm đặc biệt = đã đổi cấp -> gói xét cấp đếm lại từ 0.
    const mRc = mRc0 && (s.rankOverrides || {})[selectedMember.id] ? { ...mRc0, y: 0, h: 0 } : mRc0;
    const mRank = selectedMember ? rankOf(selectedMember) : '';
    // (09/10) Lịch sử đơn hàng & ưu đãi: % ưu đãi theo cấp và theo từng gói (B5).
    const mPct = (k) => ((((s.commCfg || {})[k] || {}).pct || this.COMM_DEFAULT)[mRank] || 0);
    const mNext = this.nextRank(mRank);
    const mUpDirect = selectedMember ? this.MEMBERS.find(x => x.name === selectedMember.upline) : null;
    const mUpEff = selectedMember ? effUp(selectedMember) : null;

"""

_JS_RR_RETURN = """      // (27) Xét thăng / hạ cấp (B9).
      rrRows, rrEmpty: rrRows.length === 0,
      rrFilters: [['all','Tất cả'],['pending','Chờ duyệt'],['approved','Đã duyệt'],['denied','Từ chối']].map(([id, label]) => ({
        label, onClick: () => this.setState({ rrFilter: id }),
        style: 'height:34px;padding:0 14px;border-radius:30px;font-size:12px;font-weight:600;border:1px solid '
          + ((s.rrFilter || 'all') === id ? '#1E3A66;background:rgba(30,58,102,.08);color:#1E3A66'
                                          : 'rgba(154,163,176,.4);background:transparent;color:var(--c5)') })),
      rrPendingCount: rrPending.length, rrNoPending: rrPending.length === 0,
      rrSelCount: rrSelIds.length, rrSelDisabled: rrSelIds.length === 0,
      rrSelBtnStyle: rrBtn(rrSelIds.length > 0, false), rrAllBtnStyle: rrBtn(rrPending.length > 0, true),
      rrRunStyle: 'height:38px;padding:0 var(--s6);border-radius:var(--r-md);font-size:13px;font-weight:600;'
        + (rrSelIds.length ? 'background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);cursor:pointer'
                           : 'background:transparent;color:rgba(154,163,176,.9);border:1px dashed rgba(154,163,176,.6);cursor:not-allowed'),
      rrAllMark: rrAllOn ? '✓' : '', rrAllBg: rrAllOn ? '#1E3A66' : '#FFFFFF',
      rrAllBorder: rrAllOn ? '#1E3A66' : 'rgba(154,163,176,.8)',
      rrToggleAll: () => this.setState({ rrSel: rrAllOn ? {} : Object.fromEntries(rrPending.map(r => [r.id, true])) }),
      rrApproveSel: () => rrSelIds.length && this.setState({ rrModal: { type: 'bulk', ids: rrSelIds } }),
      rrApproveAll: () => rrPending.length && this.setState({ rrModal: { type: 'bulk', ids: rrPending.map(r => r.id) } }),
      rrRunSel: () => rrSelIds.length && this.setState({ rrRunNote: 'Đã chạy lại xét cấp cho '
        + rrSelIds.length + ' thành viên đã chọn lúc ' + this.nowStamp() + ' — đề xuất không thay đổi.' }),
      rrRunNote: s.rrRunNote || '',
      isRrDeny: !!rrDenyRow, isRrBulk: rrBulkRows.length > 0,
      rrModalName: rrDenyRow ? rrDenyRow.name : '', rrModalProp: rrDenyRow ? rrDenyRow.from + ' → ' + rrDenyRow.to : '',
      rrBulkRows, rrBulkCount: rrBulkRows.length,
      rrDenyText: s.rrDenyText || '', setRrDenyText: (e) => this.setState({ rrDenyText: e.target.value }),
      rrDenyDisabled,
      rrDenyStyle: 'flex:1;height:44px;border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:#FFFFFF;background:'
        + (rrDenyDisabled ? 'rgba(154,163,176,.5)' : 'var(--err)') + ';cursor:' + (rrDenyDisabled ? 'not-allowed' : 'pointer'),
      closeRrModal: () => this.setState({ rrModal: null, rrDenyText: '' }),
      confirmRrDeny: () => { if (rrDenyDisabled || !rrDenyRow) return;
        this.setState({ rrStatus: { ...rrStatus, [rrDenyRow.id]: 'denied' },
          rrReason: { ...rrReasons, [rrDenyRow.id]: s.rrDenyText.trim() },
          rrSel: { ...rrSel, [rrDenyRow.id]: false }, rrModal: null, rrDenyText: '' }); },
      confirmRrBulk: () => { const st = { ...rrStatus };
        rrBulkRows.forEach(r => { st[r.id] = 'approved'; });
        this.setState({ rrStatus: st, rrSel: {}, rrModal: null }); },

      // (27) Ngăn chi tiết thành viên: gói xét cấp + tuyến trên hiệu lực.
      mRankCount: mRc ? this.nfmt(this.pkgCount(mRc)) + (mNext ? ' / ' + this.rankStep(mNext) + ' (lên ' + mNext + ')' : '') : '—',
      mHistY: '+' + this.nfmt(this.COMM_PKGS.y.price * mPct('y') / 100) + 'đ',
      mHistH: '+' + this.nfmt(this.COMM_PKGS.h.price * mPct('h') / 100) + 'đ',
      mHistPctY: this.nfmt(mPct('y')) + '%', mHistPctH: this.nfmt(mPct('h')) + '%',
      mRankMonth: mRc ? this.nfmt(mRc.my + mRc.mh * 0.5) + ' gói (' + mRc.my + ' × 1 năm + ' + mRc.mh + ' × 6 tháng)' : '—',
      mUplineDirect: mUpDirect ? mUpDirect.name + ' · ' + rankOf(mUpDirect) : 'Không có (thành viên gốc)',
      mUplineEff: mUpEff ? mUpEff.name + ' · ' + rankOf(mUpEff) : 'Công ty · Super Lithium',
      hasUplineNote: !!(selectedMember && (mUpDirect ? mUpDirect !== mUpEff : false)),
      mUplineNote: (selectedMember && mUpDirect && mUpDirect !== mUpEff)
        ? 'Đồng cấp với tuyến trên trực tiếp ' + mUpDirect.name + ' (' + rankOf(mUpDirect) + ') nên bám lên '
          + (mUpEff ? mUpEff.name + ' (' + rankOf(mUpEff) + ')' : 'Công ty (Super Lithium)') + ' — người kế tiếp có cấp cao hơn.'
        : '',

      // (27) Bổ nhiệm đặc biệt (mục 15) — ghi đè các hàm cùng tên ở trên.
      rankEditUpLabel: rankEditUp ? rankEditUp.name + ' · ' + rankOf(rankEditUp) : 'Công ty',
      rankReason: s.rankReason || '', setRankReason: (e) => this.setState({ rankReason: e.target.value }),
      rankRequester: s.rankRequester || '', setRankRequester: (e) => this.setState({ rankRequester: e.target.value }),
      openRankEdit: () => selectedMember && this.setState({ rankEditId: selectedMember.id,
        rankEditChoice: rankOf(selectedMember), rankReason: '', rankRequester: '' }),
      closeRankEdit: () => this.setState({ rankEditId: null, rankEditChoice: null, rankReason: '', rankRequester: '' }),
      submitRankEdit: () => {
        if (!rankReady || !rankTarget) return;
        const id = rankTarget.id, now = this.nowStamp();
        const log = (s.rankLogs[id] || []).slice();
        // (08/10) Duyệt ngoài hệ thống — admin xác nhận là có hiệu lực ngay.
        log.unshift({ label: 'Bổ nhiệm đặc biệt ' + rankEditCurrent + ' → ' + s.rankEditChoice
          + ' · lý do: ' + s.rankReason.trim() + ' · người yêu cầu: ' + s.rankRequester.trim()
          + ' · admin xác nhận (đã duyệt ngoài hệ thống) · đã gửi email anh Phương', time: now });
        this.setState({ rankOverrides: { ...s.rankOverrides, [id]: s.rankEditChoice },
          rankSaved: 'Đã bổ nhiệm ' + rankEditCurrent + ' → ' + s.rankEditChoice
            + ', có hiệu lực ngay. Đã gửi email cho anh Phương và email báo thành viên.',
          rankLogs: { ...s.rankLogs, [id]: log },
          rankEditId: null, rankEditChoice: null, rankReason: '', rankRequester: '' });
      },
      hasRankSaved: !!(selectedMember && s.rankSaved), rankSavedText: s.rankSaved || '',

"""

JS_0810 += [
    ("  ADMIN_NAV = [['B2','Thành viên'],['B3','Yêu cầu rút tiền'],",
     "  ADMIN_NAV = [['B2','Thành viên'],['B9','Xét thăng / hạ cấp'],['B3','Yêu cầu rút tiền'],"),
    ("['B2','B3','B4','B5','B6','B7','B8'].includes(s.screen)",
     "['B2','B3','B4','B5','B6','B7','B8','B9'].includes(s.screen)"),
    ("      isB8: s.screen === 'B8',", "      isB8: s.screen === 'B8',\n      isB9: s.screen === 'B9',"),
    ("    profileSaved: null,\n",
     "    profileSaved: null,\n"
     "    // (27) Xét cấp (B9) + bổ nhiệm đặc biệt (duyệt ngoài, admin xác nhận).\n"
     "    rrStatus: {}, rrSel: {}, rrReason: {}, rrFilter: 'all', rrModal: null, rrDenyText: '', rrRunNote: '',\n"
     "    rankReason: '', rankRequester: '', rankSaved: '',\n"),
    ("  RANK_PROGRESS = { new: 'Còn 9 đơn để lên hạng Silver',\n"
     "                    active: 'Còn 8 đơn để lên hạng Gold' };",
     _JS_RR_CLASS),
    ("      rankProgress: this.RANK_PROGRESS[s.agentStage === 'active' ? 'active' : 'new'],",
     "      rankProgress: this.RANK_PROGRESS[s.agentStage === 'active' ? 'active' : 'new'],\n"
     "      rankMonthNote: this.RANK_MONTH_NOTE[s.agentStage === 'active' ? 'active' : 'new'],"),
    ("    const rankIdx = (r) => this.RANKS.indexOf(r);",
     "    const rankIdx = (r) => this.RANKS.indexOf(r);\n"
     "    // (27) Tuyến trên HIỆU LỰC: đi ngược lên tới người đầu tiên có cấp cao\n"
     "    // hơn mình; không có ai thì là công ty (Super Lithium) — trả về null.\n"
     "    const effUp = (m) => { const me = rankIdx(rankOf(m)); let cur = m;\n"
     "      for (let k = 0; k < 12; k++) {\n"
     "        const u = this.MEMBERS.find(x => x.name === cur.upline);\n"
     "        if (!u) return null;\n"
     "        if (rankIdx(rankOf(u)) > me) return u;\n"
     "        cur = u;\n"
     "      }\n"
     "      return null; };"),
    ("    let rankEditName = '', rankEditCurrent = '', rankOptions = [];",
     "    let rankEditName = '', rankEditCurrent = '', rankOptions = [];\n    let rankEditUp = null;"),
    ("      // Trần: không được cao hơn người giới thiệu trực tiếp.\n"
     "      const up = this.MEMBERS.find(x => x.name === rankTarget.upline);\n"
     "      const ceil = up ? rankIdx(rankOf(up)) : this.RANKS.length - 1;",
     "      // (27) Trần theo tuyến trên HIỆU LỰC và KHÔNG được bằng tuyến trên (H3).\n"
     "      const up = effUp(rankTarget);\n"
     "      rankEditUp = up;\n"
     "      const ceil = up ? rankIdx(rankOf(up)) - 1 : this.RANKS.length - 1;"),
    ("          note: tooHigh ? 'Cao hơn tuyến trên (' + rankOf(up) + ')'",
     "          note: tooHigh ? (i === ceil + 1 ? 'Bằng' : 'Cao hơn') + ' tuyến trên ' + up.name + ' (' + rankOf(up) + ')'"),
    ("    const rankReady = !!s.rankEditChoice\n"
     "      && s.rankEditChoice !== rankEditCurrent\n"
     "      && s.rankDocNo.trim().length > 0\n"
     "      && s.rankDocDate.trim().length > 0\n"
     "      && s.rankApprover.trim().length > 0;",
     "    // (27) Mục 21 — Super Lithium là tài khoản công ty: hiện cho admin thấy\n"
     "    // nhưng không gán được cho thành viên.\n"
     "    if (rankTarget) rankOptions.push({ name: 'Super Lithium', disabled: true,\n"
     "      note: 'Tài khoản công ty — không gán cho thành viên', style: " + _OFF_STYLE + ",\n"
     "      onClick: () => {} });\n"
     "    // (27) Mục 15 — bỏ minh chứng phiếu; bắt buộc Lý do + Người yêu cầu.\n"
     "    const rankReady = !!s.rankEditChoice\n"
     "      && s.rankEditChoice !== rankEditCurrent\n"
     "      && (s.rankReason || '').trim().length > 0\n"
     "      && (s.rankRequester || '').trim().length > 0;"),
    ("    const selectedStockRaw = s.selectedStockId",
     _JS_RR_CONSTS + "    const selectedStockRaw = s.selectedStockId"),
    ("      openApproveMemberModal:", _JS_RR_RETURN + "      openApproveMemberModal:"),
]


# ---------------------------------------------------------------------------
# 7.4 Sản phẩm — hoa hồng theo % giá trị gói (mục 23) + Super Lithium (21)
# ---------------------------------------------------------------------------
_CM_COLS = "1.1fr .9fr .9fr 1.1fr 1.1fr"
B5_COMMISSION = """
          <!-- (28) Hoa hồng theo cấp — tính % trên giá trị gói (mục 23, 21) -->
          <div style="background:var(--c12);border:1px solid rgba(154,163,176,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s5)">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
              <div><div style="font-size:18px;font-weight:700;color:var(--c1)">Hoa hồng theo cấp</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1);line-height:1.6">Tính theo <strong>phần trăm giá trị gói</strong>, <strong>cấu hình riêng cho từng gói</strong> (gói 1 năm và gói nửa năm tách nhau). Cột Trực tiếp là phần người bán ở cấp đó nhận khi tự bán.</div></div>
              <button sc-camel-on-click="{{saveCommission}}" disabled="{{commSaveDisabled}}" style="{{commSaveStyle}}">Lưu cấu hình</button>
            </div>
            <!-- (09/10) KH: % của gói 6tr tách riêng với gói 10tr — chọn gói để cấu hình -->
            <div style="display:flex;gap:var(--s3);flex-wrap:wrap">
              <sc-for list="{{commPkgTabs}}" as="t" hint-placeholder-count="2">
                <button sc-camel-on-click="{{t.onClick}}" style="{{t.style}}">{{t.label}}<span style="display:block;font-size:11px;font-weight:500;opacity:.85">{{t.sub}}</span></button>
              </sc-for>
            </div>
            <div style="border:1px solid rgba(154,163,176,.35);border-radius:var(--r-md);overflow:auto">
              <div style="display:grid;grid-template-columns:""" + _CM_COLS + """;min-width:720px;background:rgba(154,163,176,.08);padding:var(--s4) var(--s5);font-size:11px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em">
                <div>Cấp · {{commPkgName}}</div><div>Trực tiếp (%)</div><div>Chênh lệch (%)</div><div style="text-align:right">Trực tiếp (đ)</div><div style="text-align:right">Chênh lệch (đ)</div>
              </div>
              <sc-for list="{{commRows}}" as="c" hint-placeholder-count="6">
                <div style="display:grid;grid-template-columns:""" + _CM_COLS + """;min-width:720px;align-items:center;padding:var(--s3) var(--s5);font-size:13px;color:var(--c1);border-top:1px solid rgba(154,163,176,.2)">
                  <div style="font-weight:600">{{c.rank}}</div>
                  <div style="display:flex;align-items:center;gap:var(--s2)"><input type="text" inputmode="decimal" value="{{c.pct}}" sc-camel-on-change="{{c.onChange}}" style="width:76px;height:34px;padding:0 var(--s4);border:1px solid {{c.border}};border-radius:var(--r-md);font-size:13px;text-align:right"><span style="color:var(--c5)">%</span></div>
                  <div>
                    <sc-if value="{{c.hasDiff}}" hint-placeholder-val="{{true}}">
                      <div style="display:flex;align-items:center;gap:var(--s2)"><input type="text" inputmode="decimal" value="{{c.diffPct}}" sc-camel-on-change="{{c.onDiffChange}}" style="width:76px;height:34px;padding:0 var(--s4);border:1px solid {{c.diffBorder}};border-radius:var(--r-md);font-size:13px;text-align:right"><span style="color:var(--c5)">%</span></div>
                    </sc-if>
                    <sc-if value="{{c.noDiff}}" hint-placeholder-val="{{false}}"><span style="color:var(--c5)">—</span></sc-if>
                  </div>
                  <div style="text-align:right">{{c.amt}}</div>
                  <div style="text-align:right;color:var(--c4)">{{c.diffAmt}}</div>
                </div>
              </sc-for>
              <div style="display:grid;grid-template-columns:""" + _CM_COLS + """;min-width:720px;align-items:center;padding:var(--s3) var(--s5);font-size:13px;color:var(--c5);border-top:1px solid rgba(154,163,176,.2);background:rgba(30,58,102,.04)">
                <div><div style="font-weight:600;color:var(--c2)">Super Lithium</div><div style="font-size:11px">Tài khoản công ty · không hiển thị với thành viên</div></div>
                <div>Nhận phần còn lại</div><div>—</div><div style="text-align:right">—</div><div style="text-align:right">—</div>
              </div>
              <div style="display:grid;grid-template-columns:""" + _CM_COLS + """;min-width:720px;align-items:center;padding:var(--s4) var(--s5);font-size:13px;font-weight:700;color:var(--c1);border-top:1px solid rgba(154,163,176,.35);background:rgba(154,163,176,.06)">
                <div>Tổng phân bổ tối đa / đơn</div><div>{{commMaxPct}}</div><div></div><div style="text-align:right">{{commMaxAmt}}</div><div></div>
              </div>
            </div>
            <sc-if value="{{commWarn}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:var(--err);background:rgba(192,57,43,.08);border-radius:var(--r-md);padding:var(--s4) var(--s5);line-height:1.6">{{commWarn}}</div>
            </sc-if>
            <div style="font-size:11px;color:var(--c5);line-height:1.6">Phần chênh lệch giữa các cấp cũng tính theo <strong>% giá trị gói</strong> (HOMI365 trả lời H6). Mỗi gói có bộ % riêng; số tiền quy đổi theo giá của gói đang chọn. Super Lithium đứng trên cùng, Lithium không thăng lên được.</div>
            <sc-if value="{{commSaved}}" hint-placeholder-val="{{false}}">
              <div style="font-size:13px;color:#2F7A48;background:rgba(47,122,72,.12);border-radius:var(--r-md);padding:var(--s4) var(--s5)">{{commSaved}}</div>
            </sc-if>
          </div>
"""

MARKUP_0810 += [
    ('            </table>\n          </div>\n        </div>\n      </sc-if>\n\n      <sc-if value="{{showProductForm}}"',
     '            </table>\n          </div>\n' + B5_COMMISSION
     + '        </div>\n      </sc-if>\n\n      <sc-if value="{{showProductForm}}"'),
]

_JS_COMM_CONSTS = """    // (28) Hoa hồng theo % giá trị gói (mục 23, H6). (09/10) KH: mỗi gói một bộ %
    // riêng — gói 1 năm (y, 10tr) và gói nửa năm (h, 6tr) không tính chung.
    const pctNum = (v) => { const n = parseFloat(String(v).replace(',', '.')); return isNaN(n) ? NaN : n; };
    const commCfgAll = s.commCfg || {};
    const commCfgOf = (k) => ({ pct: (commCfgAll[k] || {}).pct || this.COMM_DEFAULT,
                                diff: (commCfgAll[k] || {}).diff || this.COMM_DIFF_DEFAULT });
    const commPkg = s.commPkg || 'y';
    const commPkgPrice = this.COMM_PKGS[commPkg].price;
    let commWarn = '';
    const commBadAll = {};
    Object.keys(this.COMM_PKGS).forEach(k => {
      const { pct, diff } = commCfgOf(k), nm = this.COMM_PKGS[k].name, bad = commBadAll[k] = { pct: {}, diff: {} };
      this.RANKS.forEach((r, i) => {
        const v = pctNum(pct[r]);
        if (isNaN(v) || v < 0 || v > 100) { bad.pct[r] = true; commWarn = commWarn || (nm + ': tỷ lệ của ' + r + ' phải là số từ 0 đến 100.'); }
        else if (i > 0 && v < pctNum(pct[this.RANKS[i - 1]])) { bad.pct[r] = true;
          commWarn = commWarn || (nm + ': tỷ lệ của ' + r + ' không được thấp hơn cấp dưới (' + this.RANKS[i - 1] + ').'); }
        if (i > 0) { const d = pctNum(diff[r]);
          if (isNaN(d) || d < 0 || d > 100) { bad.diff[r] = true; commWarn = commWarn || (nm + ': chênh lệch của ' + r + ' phải là số từ 0 đến 100.'); } }
      });
    });
    const { pct: commPct, diff: commDiff } = commCfgOf(commPkg);
    const commBad = commBadAll[commPkg].pct, diffBad = commBadAll[commPkg].diff;
    const commMax = pctNum(commPct.Lithium);
    const vnd = (x) => isNaN(x) ? '—' : Math.round(x).toLocaleString('vi-VN') + 'đ';
    const commSet = (field, r, val) => this.setState({ commSaved: '', commCfg: { ...commCfgAll,
      [commPkg]: { ...commCfgOf(commPkg), [field]: { ...commCfgOf(commPkg)[field], [r]: val } } } });

"""

_JS_COMM_RETURN = """      // (28) Hoa hồng theo % — theo gói đang chọn.
      commPkgTabs: Object.keys(this.COMM_PKGS).map(k => { const on = k === commPkg, bad = Object.keys(commBadAll[k].pct).length + Object.keys(commBadAll[k].diff).length > 0; return {
        label: this.COMM_PKGS[k].name, sub: this.COMM_PKGS[k].price.toLocaleString('vi-VN') + 'đ' + (bad ? ' · có lỗi' : ''),
        style: 'height:auto;padding:var(--s3) var(--s6);border-radius:var(--r-md);font-size:13px;font-weight:700;text-align:left;cursor:pointer;'
          + (on ? 'background:#1E3A66;color:#FFFFFF;border:1px solid #1E3A66' : 'background:var(--c12);color:' + (bad ? '#C0392B' : 'var(--c2)') + ';border:1px solid ' + (bad ? '#C0392B' : 'rgba(154,163,176,.6)')),
        onClick: () => this.setState({ commPkg: k }) }; }),
      commPkgName: this.COMM_PKGS[commPkg].name,
      commRows: this.RANKS.map(r => { const v = pctNum(commPct[r]), first = r === this.RANKS[0]; return {
        rank: r, pct: String(commPct[r]), border: commBad[r] ? '#C0392B' : 'rgba(154,163,176,.6)',
        amt: vnd(commPkgPrice * v / 100),
        hasDiff: !first, noDiff: first,
        diffPct: first ? '' : String(commDiff[r]),
        diffBorder: diffBad[r] ? '#C0392B' : 'rgba(154,163,176,.6)',
        diffAmt: first ? '—' : vnd(commPkgPrice * pctNum(commDiff[r]) / 100),
        onDiffChange: (e) => commSet('diff', r, e.target.value),
        onChange: (e) => commSet('pct', r, e.target.value) }; }),
      commMaxPct: isNaN(commMax) ? '—' : commMax.toLocaleString('vi-VN') + '%',
      commMaxAmt: vnd(commPkgPrice * commMax / 100),
      commWarn,
      commSaved: s.commSaved || '',
      commSaveDisabled: !!commWarn,
      commSaveStyle: 'height:38px;padding:0 var(--s6);border:none;border-radius:var(--r-md);font-size:13px;font-weight:600;color:#FFFFFF;background:'
        + (commWarn ? 'rgba(154,163,176,.5)' : 'var(--c6)') + ';cursor:' + (commWarn ? 'not-allowed' : 'pointer'),
      saveCommission: () => !commWarn && this.setState({ commSaved: 'Đã lưu cấu hình lúc ' + this.nowStamp()
        + ' · áp dụng cho đơn được duyệt từ thời điểm này, đơn cũ giữ cách tính cũ.' }),

"""

JS_0810 += [
    ("    profileSaved: null,\n",
     "    profileSaved: null,\n"
     "    // (28) Cấu hình hoa hồng theo % (B5).\n"
     "    commCfg: null, commPkg: 'y', commSaved: '',\n"),
    ("  pkgCount(c) { return c.y + c.h * 0.5; }",
     "  // (28) Hoa hồng % theo cấp (trực tiếp) + chênh lệch % (H6, 08/10) — mặc định\n"
     "  // quy từ số tiền cũ trên gói 1 năm 10tr: Silver 1tr = 10% … Lithium 50k = 0,5%.\n"
     "  COMM_DEFAULT = { Copper: 20, Silver: 30, Gold: 35, Diamond: 37, Titanium: 38, Lithium: 38.5 };\n"
     "  COMM_DIFF_DEFAULT = { Silver: 10, Gold: 5, Diamond: 2, Titanium: 1, Lithium: 0.5 };\n"
     "  // (09/10) Mỗi gói một bộ % riêng. Mặc định gói nửa năm lấy cùng số với gói 1 năm\n"
     "  // để admin chỉnh; bản thật đọc từ cấu hình đã lưu của từng gói.\n"
     "  COMM_PKGS = { y: { name: 'Gói 1 năm', price: 10000000 }, h: { name: 'Gói nửa năm', price: 6000000 } };\n"
     "  pkgCount(c) { return c.y + c.h * 0.5; }"),
    ("    const selectedStockRaw = s.selectedStockId",
     _JS_COMM_CONSTS + "    const selectedStockRaw = s.selectedStockId"),
    ("      openApproveMemberModal:", _JS_COMM_RETURN + "      openApproveMemberModal:"),
]


# ---------------------------------------------------------------------------
# 7.5 DIFF-vs-mockup-KH.md — mục 20
# ---------------------------------------------------------------------------
DIFF_0810 = [
    "## 20. Cập nhật theo phản hồi KH ở sheet Change Request — đợt 08/10", "",
    "KH đã trả lời các câu hỏi H1–H5 và chốt từng mục; đợt này làm hết, kể cả "
    "các thay đổi lớn. Bản vá vẫn nằm trong `tools/update_uat0210.py` (mục 7), "
    "neo không khớp là dừng build.", "",
    "| Mục | Màn | Thay đổi | Xem thử |", "|---|---|---|---|",
    "| 1 (làm lại) | A1 | Bỏ màn nhập SĐT riêng của đợt 06/10. Vào trang thấy **form mua "
    "hàng nhưng bị khoá** (mờ, không bấm được); ô nhập SĐT nằm ở **đầu trang**. Xác "
    "định xong SĐT thì form mở khoá, đầu trang thu lại thành một dòng có nút Đổi số. "
    "| `a1-buy.html`, `#sdt-da-co`, `#form` |",
    "| 5 (làm lại) | A1 | Không mở khoá bằng bấm link nữa. Form hiện **khung nội dung "
    "chính sách** cuộn được; khách **kéo xuống đọc hết** mới tick được ô đồng ý. Link "
    "bản đầy đủ vẫn mở tab mới nhưng không mở khoá. | `#form` |",
    "| 8 | A3 | Thẻ **Yêu cầu đổi điểm kỳ 09/2026** dưới nút tạo yêu cầu: trạng thái, "
    "nút **Huỷ yêu cầu** + hộp xác nhận. Gửi / huỷ được tới 23:59 ngày liền trước ngày "
    "cuối tháng (Chính sách ưu đãi thành viên mục 4, chốt 08/10); ngày cuối tháng khoá sổ, nút mờ kèm giải thích. Đang có yêu cầu thì khoá nút tạo mới. | "
    "`a3-dashboard.html#co-yeu-cau`, `#huy-yeu-cau`, `#da-khoa-so` |",
    "| 9 | B3 | **Đảo ngược mô hình duyệt 2 lớp**: bỏ bước Head, bỏ trạng thái Chờ Head. "
    "Luồng mới: Chờ duyệt → Admin duyệt → Đã duyệt → xuất file → ngân hàng chi → "
    "**tải lên file kết quả thanh toán** → Thanh toán thành công / Chi không thành công. "
    "Có ô chọn từng dòng, **Duyệt đã chọn** và **Duyệt tất cả Chờ duyệt** (H2). Không "
    "còn nhập mã giao dịch từng lệnh, không còn nút đánh dấu đã chi trả bằng tay. | "
    "`b3-withdrawals.html`, `#duyet-hang-loat`, `#tai-ket-qua` |",
    "| 10 | B3 | Hộp thoại xuất danh sách chi trả lấy các yêu cầu **Đã duyệt** (bỏ điều "
    "kiện duyệt đủ 2 bước). | `#xuat-chi-tra` |",
    "| 11 | B3 | Chi không thành công giờ sinh ra từ file kết quả (yêu cầu Đã duyệt "
    "không có trong file). Hoàn điểm giữ nguyên: lý do bắt buộc, gửi email, ghi nhật "
    "ký. Thêm trạng thái **Thành viên đã huỷ** cho mục 8. | `#chi-khong-thanh-cong`, "
    "`#hoan-diem`, `#thanh-vien-huy` |",
    "| 12, 13, 14, 17, 18 | **B9 (màn mới)** | Màn **Xét thăng / hạ cấp**: danh sách đề "
    "xuất cuối kỳ (cấp hiện tại, gói xét cấp, gói tháng này đã quy đổi, cấp đề xuất "
    "chỉ ±1 bậc, lý do hệ thống), ô chọn, **Duyệt đã chọn / Duyệt tất cả**, **Từ "
    "chối bắt nhập lý do**, nút **Chạy lại xét cấp cho nhóm đã chọn**. Gói 6 tháng "
    "tính 0,5; dưới 1 gói / tháng thì đề xuất hạ; nửa gói lẻ không cộng dồn (H4). | "
    "`b9-rank-review.html`, `#tu-choi`, `#duyet-tat-ca`, `#da-xu-ly` |",
    "| 14, 17 | A3, B2 | A3: dòng tiến độ đổi sang **gói xét cấp đã quy đổi** + dòng "
    "tháng này. B2: thêm khối Gói xét cấp / Gói tháng này. | `a3-dashboard.html`, "
    "`b2-members.html#chi-tiet` |",
    "| 15 | B2 | **Bổ nhiệm đặc biệt** thay cho Cập nhật cấp: bỏ số phiếu, ngày duyệt, "
    "người duyệt, file minh chứng; thêm **Lý do** và **Người yêu cầu** (bắt buộc). "
    "Duyệt làm **ngoài hệ thống** (chốt 08/10): admin bấm **Xác nhận bổ nhiệm & gửi "
    "email** là cấp mới có hiệu lực ngay, hệ thống gửi email cho anh Phương (lưu làm bằng "
    "chứng) và email báo thành viên. **Không cho chọn cấp bằng tuyến trên** (H3). | "
    "`#cap-nhat-cap`, `#da-bo-nhiem` |",
    "| 20 | B2 | Hiện **tuyến trên trực tiếp** và **tuyến trên hiệu lực** (đi ngược lên "
    "tới người đầu tiên có cấp cao hơn, không có thì là công ty) kèm ghi chú khi khác "
    "nhau. Trần của bổ nhiệm đặc biệt tính theo tuyến trên hiệu lực. | "
    "`#tuyen-tren-hieu-luc` |",
    "| 21 | B2, B5 | **Super Lithium** hiện trong danh sách cấp nhưng không chọn được "
    "(tài khoản công ty), có dòng riêng trong bảng hoa hồng; A3 không bao giờ hiện. "
    "Giới hạn số tầng tuyến trên khi chia ưu đãi KHÔNG làm thành cấu hình trên giao diện "
    "(bỏ 09/10) — dev tự xử lý trong logic tính. | `b5-products.html` |",
    "| 23 | B5 | Khối **Hoa hồng theo cấp**: mỗi cấp nhập **% trên giá trị gói**, tự quy "
    "ra tiền cho gói 1 năm và nửa năm, dòng tổng phân bổ tối đa, cảnh báo khi ngoài "
    "0–100% hoặc cấp trên thấp hơn cấp dưới. Cột **chênh lệch cũng nhập %** (H6 trả lời "
    "08/10), mặc định quy từ số tiền cũ trên gói 1 năm (Silver 10% … Lithium 0,5%). "
    "**09/10: mỗi gói một bộ % riêng** — chọn tab Gói 1 năm (10tr) / Gói nửa năm (6tr) để "
    "cấu hình, số tiền quy theo giá gói đang chọn; mặc định gói nửa năm lấy cùng số với gói "
    "1 năm để admin chỉnh. | `b5-products.html`, `#hoa-hong-loi` |",
    "| 24 | A1, B5, B6 | Đổi **tên hiển thị** gói thành **HOMI365-01**. Mã CN02 trong "
    "SKU kho và mã gói giữ nguyên. | — |", "",
    "**Giả định của bản mẫu — cần xác nhận:**", "",
    "1. **Bổ nhiệm đặc biệt (15)** — đã chốt 08/10: anh Phương duyệt ngoài hệ thống, "
    "admin vào xác nhận là có hiệu lực ngay; hệ thống chỉ cần gửi email cho anh Phương.",
    "2. **Ngưỡng số gói từng cấp** — đã chốt 08/10 theo Chính sách ưu đãi thành viên: "
    "Silver 10, Gold 18, Diamond 24, Titanium 28, Lithium 30 (xem mục 21).",
    "3. **Hoa hồng % mặc định** quy từ bảng tiền cũ của gói 1 năm (Copper 20% … "
    "Lithium 38,5%). Tính % trên gói nửa năm 6tr cho ra 1.200.000đ … 2.310.000đ, "
    "khác bản chốt 01/10 (ưu đãi gói nửa năm = 1/2 gói 1 năm). Cần KH xác nhận lại.",
    "4. **Đối chiếu file kết quả thanh toán** theo số tài khoản + số tiền. Bản mẫu "
    "giả lập 1 yêu cầu không có trong file và 1 dòng file không khớp yêu cầu nào.",
    "5. **Duyệt đổi điểm** cho cả Admin và Head bấm (Head có đủ quyền Admin).",
    "6. **Mốc chi trả 5 ngày sau khoá sổ** (H1) KH chưa trả lời — chưa thể hiện "
    "trên giao diện.", "",
    "**Còn lệch, chưa sửa:** ngăn chi tiết thành viên ở B2 và hộp thoại Head duyệt "
    "hồ sơ vẫn ghi \"ưu đãi đang tạm giữ\", \"kích hoạt\" (xem mục 19).", "",
]


DIFF_POLICY = [
    "## 21. Văn bản chính sách chính thức (HOMI365 gửi 08/10, hiệu lực 01/10/2026)", "",
    "Nguồn dữ liệu duy nhất: `tools/policy_docs.py` — sinh ra cả khung đọc trong form "
    "lẫn trang `policy.html`, nên hai nơi không lệch chữ.", "",
    "| Văn bản | Hiện ở | Ghi chú |",
    "|---|---|---|",
    "| Chính sách mua hàng + Chính sách bảo mật và bảo vệ dữ liệu cá nhân (kèm Điều "
    "kiện giao dịch chung, Vận chuyển và giao nhận, Phương thức thanh toán) | A1 khung "
    "đọc trên ô đồng ý · `policy.html?s=chinh-sach-mua-hang` | Thay bản tóm tắt tự "
    "viết. \"Ngày cập nhật 10/10/2026\" đổi thành \"Hiệu lực từ 01/10/2026\". |",
    "| Chính sách ưu đãi thành viên HOMI365, phiên bản 1.0 | A2 bước 4 · "
    "`policy.html?s=dieu-khoan-thanh-vien` (giữ id cũ) | Thay bản Điều khoản & Điều "
    "kiện cũ (còn chỗ trống ………). Sửa lỗi gõ \"ngày cuối cũng\" → \"ngày cuối cùng\". |",
    "",
    "Cả A1 và A2: ô đồng ý chỉ mở khi **kéo đọc hết** khung; bấm link mở bản đầy đủ "
    "không còn mở khoá. Footer: thêm link Chính sách mua hàng & bảo mật dữ liệu, đổi "
    "tên \"Điều khoản thành viên\" → \"Chính sách ưu đãi thành viên\". Hai văn bản "
    "chính thức không còn dòng \"Nội dung mẫu dựng giao diện\" ở cuối trang.", "",
    "**Bỏ 7 trang chính sách mẫu (HOMI365 chốt 08/10):** Quy chế hoạt động, Bảo mật thông "
    "tin, Thanh toán, Vận chuyển & giao nhận, Đổi trả & hoàn tiền, Bảo hành, Kiểm hàng — "
    "nội dung chép từ gocare.vn, mâu thuẫn với văn bản KH (thẻ/ví/cổng thanh toán, phí "
    "giao hàng). Trang chính sách và footer chỉ còn 2 văn bản; link cũ `?s=<id cũ>` tự "
    "chuyển về Chính sách mua hàng & bảo mật dữ liệu. Câu \"Chính sách đổi trả và hoàn tiền\" ở mục "
    "Phí giao hàng: HOMI365 xác nhận nội dung này nằm chung trang Chính sách mua hàng, "
    "không tách trang riêng.", "",
    "**Văn bản lệch với prototype — kết quả chốt 08/10:**", "",
    "1. **Ngưỡng hạng — ĐÃ CHỐT 08/10.** Ngưỡng theo văn bản: Silver 10, Gold 18, "
    "Diamond 24, Titanium 28, Lithium 30 — đã thay số minh hoạ ở B9/A3/B2. Đơn vị vẫn là "
    "*gói quy đổi* (gói 1 năm = 1, gói 6 tháng = 0,5 — Change Request mục 17) và lên cấp "
    "thì đếm lại từ 0, không nhảy bậc (mục 14) — HOMI365 xác nhận lại 08/10: Copper bán 12 "
    "gói thì tháng sau lên Silver, từ Silver đếm lại từ 0; bán bao nhiêu trong tháng cũng "
    "chỉ lên 1 cấp, phần dư bỏ. **Chốt 09/10:** số gói cần cho mỗi bậc = ngưỡng cấp đích "
    "trừ ngưỡng cấp hiện tại — Copper→Silver 10, Silver→Gold 8, Gold→Diamond 6, "
    "Diamond→Titanium 4, Titanium→Lithium 2 (ví dụ KH: Silver bán 1 gói 1 năm + 1 gói 6 "
    "tháng → \"Gói xét cấp 1,5 / 8 · còn 6,5 gói để lên Gold\"). A3 chỉ hiện đúng 1 dòng này. Văn bản ghi \"số đơn giao dịch hợp lệ "
    "lũy kế\", chưa nêu trọng số gói 6 tháng và việc đếm lại — nên đề nghị HOMI365 bổ "
    "sung câu chữ cho khớp.",
    "2. **Hạ hạng — ĐÃ CHỐT 08/10: giữ logic prototype.** Trong tháng phải đạt "
    "tối thiểu 1 gói quy đổi mới giữ hạng: gói 1 năm = 1 gói, gói 6 tháng = 0,5 gói, "
    "nên cần 2 gói 6 tháng (hoặc 1 gói 1 năm). Tháng chỉ có 1 đơn gói 6 tháng vẫn bị "
    "đề xuất hạ 1 cấp. Văn bản mục 3 (\"ít nhất 01 đơn mới trong mỗi tháng\") đang "
    "lệch với quy tắc này — cần HOMI365 sửa câu chữ trong văn bản.",
    "3. **Hạn gửi yêu cầu đổi điểm — ĐÃ CHỐT 08/10: theo văn bản.** Gửi và huỷ được "
    "tới 23:59 ngày liền trước ngày cuối tháng (kỳ 09/2026: 23:59 ngày 29/09); ngày cuối "
    "tháng khoá sổ. A3 đã sửa mốc, thêm trạng thái `#het-han-gui` (chưa có yêu cầu, "
    "qua hạn → nút tạo mờ, hẹn kỳ sau).",
    "4. Văn bản không nhắc tới Super Lithium, bổ nhiệm đặc biệt, tỷ lệ hoa hồng % "
    "theo gói — giữ nguyên trên prototype.", "",
]


def patch_diff(diff):  # noqa: F811 — thay bản đợt 06/10, chèn cả mục 19, 20, 21
    i = diff.index("## Ghi chú")
    return diff[:i] + DIFF + DIFF_0810 + DIFF_POLICY + diff[i:]


# ---------------------------------------------------------------------------
# 7.x (08/10) Hạn gửi yêu cầu đổi điểm theo Chính sách ưu đãi thành viên mục 4:
# gửi trước ngày cuối cùng của tháng. Từ ngày cuối tháng (khoá sổ) nút tạo yêu
# cầu mờ, kể cả khi chưa có yêu cầu nào trong kỳ.
# ---------------------------------------------------------------------------
MARKUP_0810 += [
    ('<sc-if value="{{hasActiveThisMonth}}" hint-placeholder-val="{{false}}">\n'
     '          <div style="font-size:12px;color:var(--c2);background:rgba(150,92,10,.14);'
     'border-radius:var(--r-sm);padding:var(--s4)">Bạn đang có yêu cầu',
     '<sc-if value="{{wdClosedNote}}" hint-placeholder-val="{{false}}">\n'
     '          <div style="font-size:12px;color:var(--c4);background:rgba(154,163,176,.14);'
     'border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">Đã qua hạn gửi yêu cầu đổi '
     'điểm kỳ {{wdPeriod}} (hạn chót <strong>{{wdLockLabel}}</strong> — trước ngày cuối tháng). '
     'Bạn gửi được yêu cầu cho kỳ sau từ <strong>{{nextWithdrawDate}}</strong>.</div>\n'
     '        </sc-if>\n'
     '        <sc-if value="{{wdOpenNote}}" hint-placeholder-val="{{false}}">\n'
     '          <div style="font-size:12px;color:var(--c2);background:rgba(150,92,10,.14);'
     'border-radius:var(--r-sm);padding:var(--s4)">Bạn đang có yêu cầu'),
]
JS_0810 += [
    ("    const withdrawButtonDisabled = hasActiveThisMonth;",
     "    // (08/10) Qua hạn gửi (ngày cuối tháng đã khoá sổ) thì cũng khoá nút tạo mới.\n"
     "    const withdrawButtonDisabled = hasActiveThisMonth || !!s.wdPeriodLocked;"),
    ("      hasActiveThisMonth, nextWithdrawDate: '01/10/2026',",
     "      hasActiveThisMonth, nextWithdrawDate: '01/10/2026',\n"
     "      wdOpenNote: hasActiveThisMonth && !s.wdPeriodLocked,\n"
     "      wdClosedNote: !!s.wdPeriodLocked && !hasActiveThisMonth,"),
]

# (09/10) Điểm tích lũy = 1 điểm / 1đ ưu đãi ĐÃ GHI NHẬN (DoD US-17, Chính sách
# ưu đãi thành viên mục 2). Số 1.240 cũ là số mẫu gõ cứng từ mockup KH.
MARKUP_0810 += [
    ('>{{metricPoints}}</div></div>',
     '>{{metricPoints}}</div><div style="font-size:11px;color:var(--c5);line-height:1.5">'
     '1 điểm = 1đ ưu đãi đã ghi nhận</div></div>'),
]
JS_0810 += [
    ("      metricPoints: s.agentStage === 'active' ? '1.240' : '0',",
     "      metricPoints: s.agentStage === 'active' ? '6.000.000' : '0',"),
]

MARKUP.extend(MARKUP_0810)
JS.extend(JS_0810)


# ===========================================================================
# (09/10) Rà soát bản deploy — các mục HOMI365 duyệt sau báo cáo QA.
# ===========================================================================
MARKUP_0910 = [
    # B2 — duyệt hồ sơ thành viên: 1 bước Head, KHÔNG chặn thành viên dùng link.
    ('Đủ 2 lượt duyệt là tài khoản được kích hoạt: toàn bộ <strong>hoa hồng đang tạm giữ'
     '</strong> và <strong>điểm tích luỹ</strong> của thành viên được <strong>cộng dồn về '
     'quá khứ</strong> — tính từ đơn đầu tiên, không phải từ thời điểm kích hoạt — và mở '
     'khoá cho rút tiền.',
     'Head xác nhận thông tin hồ sơ (CCCD, tài khoản nhận ưu đãi) là đúng. Duyệt hay chưa '
     'duyệt <strong>không ảnh hưởng</strong> link bán hàng, điểm tích luỹ và quyền đổi điểm '
     'của thành viên — các chức năng này dùng được ngay từ khi đăng ký.'),
    # B7 — mô tả vai trò theo luồng duyệt hiện tại.
    ('làm bước 1 của mọi quy trình duyệt 2 lớp: xác nhận tiền về của đơn hàng, duyệt hồ sơ '
     'thành viên, duyệt yêu cầu ',
     'xác nhận tiền về của đơn hàng (bước 1) và duyệt yêu cầu '),
    ('làm bước 2 và là người duy nhất được kích hoạt tài khoản, cấp mã kích hoạt, đánh dấu '
     'đã chi trả, và quản lý chính màn này.',
     'xác nhận đơn và cấp mã kích hoạt, duyệt hồ sơ thành viên (không chặn thành viên dùng '
     'link bán hàng), và quản lý chính màn này.'),
    # B2 chi tiết — lịch sử đơn: đổi chữ + số theo % ưu đãi của cấp, từng gói.
    ('Lịch sử đơn hàng &amp; hoa hồng', 'Lịch sử đơn hàng &amp; ưu đãi'),
    ('<span>Đơn #10234 — CN02</span><span style="font-weight:600">+120.000đ</span>',
     '<span>Đơn #10234 — HOMI365-01 · Gói 1 năm · {{mHistPctY}}</span>'
     '<span style="font-weight:600">{{mHistY}}</span>'),
    ('<span>Đơn #10198 — CN02</span><span style="font-weight:600">+120.000đ</span>',
     '<span>Đơn #10198 — HOMI365-01 · Gói nửa năm · {{mHistPctH}}</span>'
     '<span style="font-weight:600">{{mHistH}}</span>'),
    # A2 bước 1.
    ('Số tài khoản nhận hoa hồng (*)', 'Số tài khoản nhận ưu đãi (*)'),
    # A1 + A2 — không chọn sẵn, placeholder dạng mẫu.
    ('placeholder="Gõ để tìm tỉnh/thành…"', 'placeholder="Chọn tỉnh/thành phố"', None, 'all'),
    ('placeholder="Gõ để tìm phường/xã…"', 'placeholder="Chọn phường/xã"', None, 'all'),
    ('placeholder="Gõ để tìm ngân hàng…"', 'placeholder="Chọn ngân hàng"', None, 'all'),
    ('<option>Nam</option><option>Nữ</option><option>Khác</option>',
     '<option value="">Chọn giới tính</option><option>Nam</option><option>Nữ</option>'
     '<option>Khác</option>', None, 'all'),
    ('placeholder="22/01/1991"', 'placeholder="dd/mm/yyyy"', None, 'all'),
    ('placeholder="22/01/2021"', 'placeholder="dd/mm/yyyy"', None, 'all'),
    ('placeholder="NGUYEN VAN AN"', 'placeholder="VD: NGUYEN VAN AN"', None, 'all'),
    ('placeholder="Cục Cảnh sát QLHC về TTXH"', 'placeholder="VD: Cục Cảnh sát QLHC về TTXH"'),
    ('placeholder="Nguyễn Văn A"', 'placeholder="VD: Nguyễn Văn A"'),
    # A2 — hàng Ngày cấp / Nơi cấp tràn khỏi khung (lỗi cũ): cột co được.
    ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s7)"><div style="display:flex;'
     'flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">'
     'Ngày cấp (*)',
     '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:var(--s7)"><div style="display:flex;'
     'flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">'
     'Ngày cấp (*)'),
    # B6 — cột Nội dung: 1 dòng, cắt chữ, rê chuột xem đủ.
    ('<td style="padding:var(--s5);color:var(--c2);font-family:monospace;font-size:12px">'
     '{{o.transferNote}}</td>',
     '<td style="padding:var(--s5);color:var(--c2);font-family:monospace;font-size:12px">'
     '<div title="{{o.transferNote}}" style="max-width:200px;white-space:nowrap;overflow:hidden;'
     'text-overflow:ellipsis">{{o.transferNote}}</div></td>'),
]

JS_0910 = [
    ("    pending: 'Chờ xác nhận thanh toán',\n    specialist_approved: 'Chờ Head duyệt',",
     "    // (09/10) Duyệt hồ sơ còn 1 bước Head; không chặn thành viên dùng link.\n"
     "    pending: 'Chờ Head duyệt',\n    specialist_approved: 'Chờ Head duyệt',"),
    ("        canApproveMember: !isSpecialist && effStatus === 'specialist_approved',\n"
     "        canRejectMember: !isSpecialist && effStatus === 'specialist_approved',\n"
     "        approveMemberButtonLabel: 'Xác nhận, kích hoạt Thành viên hoạt động (Head)',",
     "        canApproveMember: !isSpecialist && ['pending', 'specialist_approved'].includes(effStatus),\n"
     "        canRejectMember: !isSpecialist && ['pending', 'specialist_approved'].includes(effStatus),\n"
     "        approveMemberButtonLabel: 'Duyệt hồ sơ (Head)',"),
    ("        approvalStageNote: effStatus === 'pending'\n"
     "          ? 'Chưa xác nhận thanh toán. Vào màn Đơn hàng xác nhận tiền về trước, hồ sơ này mới duyệt được.'\n"
     "          : effStatus === 'specialist_approved'\n"
     "            ? 'Đơn hàng đã được xác nhận thanh toán. Manager duyệt để thành viên nhận điểm và ưu đãi đang tạm giữ.'\n"
     "            : (effStatus === 'rejected' ? 'Hồ sơ đã bị từ chối.' : null)",
     "        approvalStageNote: ['pending', 'specialist_approved'].includes(effStatus)\n"
     "          ? 'Chờ Head duyệt hồ sơ. Thành viên vẫn dùng link bán hàng, nhận điểm và đổi điểm bình thường — duyệt chỉ để xác nhận thông tin hồ sơ là đúng.'\n"
     "          : (effStatus === 'rejected' ? 'Hồ sơ đã bị từ chối.' : null)"),
    ("'Head duyệt thành viên — mở khoá điểm và ưu đãi đang tạm giữ'", "'Head duyệt hồ sơ thành viên'"),
    ("    const actionStageLabel = s.adminRole === 'specialist' ? 'Bước 1/2 · Admin duyệt' : 'Bước 2/2 · Head xác nhận';",
     "    const actionStageLabel = 'Head duyệt hồ sơ';"),
    # Tên màn A2.
    ("['A2','A2 · Đăng ký Agent']", "['A2','A2 · Đăng ký thành viên']"),
    # A1 + A2 — Tỉnh / Phường / Ngân hàng để trống, người dùng tự chọn.
    ("    bankQuery: 'Vietcombank', bankOpen: false,\n"
     "    provinceQuery: 'Thành phố Hồ Chí Minh', provinceOpen: false,\n"
     "    wardQuery: 'Phường Bến Thành', wardOpen: false,",
     "    bankQuery: '', bankOpen: false,\n"
     "    provinceQuery: '', provinceOpen: false,\n"
     "    wardQuery: '', wardOpen: false,"),
    ("            wardQuery: (p.wards && p.wards[0]) || '' }) })),",
     "            wardQuery: '' }) })),"),
    # Tự điền theo đơn gần nhất thì điền luôn tỉnh / phường / ngân hàng.
    ("      buyerBankAccount: p.buyerBankAccount, accountHolder: p.accountHolder };",
     "      buyerBankAccount: p.buyerBankAccount, accountHolder: p.accountHolder,\n"
     "      provinceQuery: 'Thành phố Hồ Chí Minh', wardQuery: 'Phường Bình Trưng', bankQuery: 'Vietcombank' };"),
    # B8 tab File.
    ("linkedTo:'Cập nhật cấp · Lê Văn Cường'", "linkedTo:'Bổ nhiệm đặc biệt · Lê Văn Cường'"),
]

# A3 — yêu cầu đang mở 800.000đ, khớp ô "Đang chờ duyệt".
MY_WD = {"amount": "800.000đ", "date": "05/09/2026", "status": "pending"}

_patch_screens_0810 = patch_screens


def patch_screens(screens):  # noqa: F811
    screens = _patch_screens_0810(screens)
    by = {sc["code"]: sc for sc in screens}
    # A2 — đổi tên màn; SĐT + email tự điền từ đơn mua (US-22), chỉ đọc.
    a2 = by["A2"]
    a2["title"] = "A2 · Đăng ký thành viên"
    a2["states"] = [(h, lb, dict({"buyerPhone": "0977000111", "buyerEmail": "an.nv@gmail.com"}, **st))
                    for h, lb, st in a2["states"]]
    # A1 tự điền theo đơn gần nhất: có cả tỉnh / phường / ngân hàng.
    by["A1"]["states"] = [
        (h, lb, dict(st, provinceQuery="Thành phố Hồ Chí Minh", wardQuery="Phường Bình Trưng",
                     bankQuery="Vietcombank") if h == "form-tu-dien" else st)
        for h, lb, st in by["A1"]["states"]]
    # B2 — duyệt / từ chối hồ sơ là việc của Head.
    by["B2"]["states"] = [
        (h, lb, dict(st, adminRole="head") if h in ("duyet", "tu-choi") else st)
        for h, lb, st in by["B2"]["states"]]
    # B7 — mặc định vai Head để thấy danh sách; vai Admin xem trạng thái riêng.
    by["B7"]["states"] = [(h, lb, dict(st, adminRole="head")) for h, lb, st in by["B7"]["states"]] + [
        ("vai-admin", "Vai Admin — không có quyền vào màn này", {"adminRole": "specialist"})]
    return screens


DIFF_0910 = [
    "## 22. Rà soát bản deploy — đợt 09/10", "",
    "| Màn | Thay đổi |",
    "|---|---|",
    "| B2 duyệt hồ sơ | Còn **1 bước Head duyệt**; hồ sơ mới ở trạng thái \"Chờ Head duyệt\". "
    "Duyệt hay chưa **không chặn** thành viên dùng link bán hàng, nhận điểm, đổi điểm. Bỏ chữ "
    "\"kích hoạt / tạm giữ / 2 lượt duyệt\" trong modal. Vai Admin chỉ xem, không có nút duyệt. |",
    "| B2 bổ nhiệm | Bổ nhiệm xong thì gói xét cấp về 0 (VD: 0 / 4 lên Titanium). |",
    "| B2 chi tiết | \"Lịch sử đơn hàng & ưu đãi\"; số tiền = giá gói × % ưu đãi của cấp, tính "
    "riêng từng gói (Copper: gói 1 năm 2.000.000đ, gói nửa năm 1.200.000đ). |",
    "| A2 | Tên màn \"Đăng ký thành viên\"; \"Số tài khoản nhận ưu đãi\"; SĐT + email tự điền "
    "từ đơn mua (chỉ đọc). |",
    "| A1, A2 | Tỉnh/Phường/Ngân hàng/Giới tính để trống, không chọn sẵn; placeholder mẫu: "
    "dd/mm/yyyy, VD: NGUYEN VAN AN, VD: Nguyễn Văn A, VD: Cục Cảnh sát QLHC về TTXH. |",
    "| A3 | Có yêu cầu đổi điểm đang mở thì số đó hiện ở \"Đang chờ duyệt\" và trừ khỏi "
    "\"Số dư khả dụng\"; không có yêu cầu thì \"Đang chờ duyệt\" = 0đ. |",
    "| A1 header | Trước ô SĐT có câu \"Vui lòng nhập số điện thoại để kiểm tra tài khoản\". "
    "SĐT mới → dưới ô "
    "báo \"Anh chị chưa có tài khoản, vui lòng nhập thông tin để mua hàng\" và mở form (10/10). |",
    "| B3 | Cột \"Khoản thưởng hiện tại\" → \"Số dư khả dụng\". |",
    "| B6 | Cột Nội dung 1 dòng, cắt chữ, rê chuột xem đủ. |",
    "| B7 | Mở mặc định với vai Head; thêm trạng thái vai Admin (không có quyền). Sửa mô tả vai trò. |",
    "| B8 | Tab File: \"Bổ nhiệm đặc biệt · Lê Văn Cường\". |",
    "",
]


def patch_diff(diff):  # noqa: F811 — thêm mục 22
    i = diff.index("## Ghi chú")
    return diff[:i] + DIFF + DIFF_0810 + DIFF_POLICY + DIFF_0910 + diff[i:]


MARKUP.extend(MARKUP_0910)
JS.extend(JS_0910)


# ===========================================================================
# (10/10) Danh sách ngân hàng theo file Techcombank KH gửi + ô nhập tay.
# ===========================================================================
import json as _json
import re as _re
import banks_tcb as _banks

_BANK_STATE = ("    bankQuery: '', bankOpen: false,",
               "    bankQuery: '', bankOpen: false, bankManual: false, bankManualText: '',")
_BANK_INPUT = ('height:44px;padding:0 var(--s5);border:1px solid rgba(154,163,176,.6);'
               'border-radius:var(--r-md);font-size:14px;width:100%')
# (12/10) KH bỏ ô nhập tay ngân hàng — chỉ chọn từ danh sách.
MARKUP_1010 = []
JS_1010 = [
    (_BANK_STATE[0], _BANK_STATE[1]),
    # 111 ngân hàng — hiện đủ, không cắt 60 như trước.
    (".slice(0, 60).map(b => ({ label: b,", ".slice(0, 200).map(b => ({ label: b,"),
    ("      bankQuery: s.bankQuery, bankOpen: s.bankOpen,",
     "      bankQuery: s.bankQuery, bankOpen: s.bankOpen,\n"
     "      // (10/10) Không có trong danh sách -> nhập tay tên ngân hàng + chi nhánh.\n"
     "      bankPick: !s.bankManual, bankManual: !!s.bankManual, bankManualText: s.bankManualText || '',\n"
     "      setBankManualText: (e) => this.setState({ bankManualText: e.target.value }),\n"
     "      toggleBankManual: () => this.setState({ bankManual: !s.bankManual, bankOpen: false }),\n"
     "      bankModeHint: s.bankManual ? 'Nhập đúng tên ngân hàng và chi nhánh.' : 'Không tìm thấy ngân hàng?',\n"
     "      bankModeLink: s.bankManual ? 'Chọn từ danh sách' : 'Nhập tay',"),
    # Bỏ nạp danh sách từ API VietQR — dùng danh sách theo file Techcombank.
    ("      fetch('https://api.vietqr.io/v2/banks')\n"
     "        .then(r => r.json())\n"
     "        .then(j => { const b = (j && j.data || []).map(x => x.shortName + ' — ' + x.name);\n"
     "                     if (b.length) this.setState({ banks: b }); })\n"
     "        .catch(() => {});\n",
     "      // (10/10) Ngân hàng lấy theo file Techcombank (BANKS_FALLBACK), không gọi API.\n"),
    ("provinceQuery: 'Thành phố Hồ Chí Minh', wardQuery: 'Phường Bình Trưng', bankQuery: 'Vietcombank' };",
     "provinceQuery: 'Thành phố Hồ Chí Minh', wardQuery: 'Phường Bình Trưng', bankQuery: 'NGOAI THUONG VN (VCB)' };"),
]
_patch_script_0910 = patch_script


def patch_script(script, die):  # noqa: F811
    script = _patch_script_0910(script, die)
    pat = _re.compile(r"^  BANKS_FALLBACK = \[.*\];$", _re.M)
    if len(pat.findall(script)) != 1:
        die("không tìm thấy đúng 1 dòng BANKS_FALLBACK")
    return pat.sub(lambda m: "  // (10/10) Theo DomesticBeneficiaryBank.xlsx (Techcombank) — xem tools/banks_tcb.py\n"
                   "  BANKS_FALLBACK = " + _json.dumps(_banks.BANKS, ensure_ascii=False) + ";", script)


_patch_screens_0910 = patch_screens


def patch_screens(screens):  # noqa: F811
    screens = _patch_screens_0910(screens)
    for sc in screens:
        if sc["code"] == "A1":
            sc["states"] = [(h, lb, dict(st, bankQuery="NGOAI THUONG VN (VCB)") if st.get("bankQuery") else st)
                            for h, lb, st in sc["states"]]
    return screens



# (10/10) Thông tin sức khỏe cá nhân — bảng dưới khung Thanh toán (A1);
# khách tick Không / Có từng mục, đơn hàng lưu lại, admin xem ở chi tiết đơn (B6).
HEALTH_Q = [
    "Người bị bệnh tâm thần, bệnh phong, bệnh ung thư;",
    "Người bị tàn tật hoặc thương tật vĩnh viễn từ 50% trở lên;",
    "Người đang trong thời gian điều trị nội trú ốm đau, bệnh tật, tai nạn;",
    "Người mất năng lực hoặc bị hạn chế năng lực hành vi dân sự.",
]
_HBOX = ('width:18px;height:18px;border:1.5px solid {{h.%sBorder}};border-radius:3px;display:inline-flex;'
         'align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#FFFFFF;'
         'background:{{h.%sBg}};cursor:pointer')
_HGRID = 'display:grid;grid-template-columns:22px 1fr 46px 30px;gap:var(--s3);align-items:center'
A1_HEALTH = (
    '\n        <div style="background:var(--c12);border:1px solid rgba(154,163,176,.35);border-radius:var(--r-lg);'
    'padding:var(--s7);display:flex;flex-direction:column;gap:var(--s4)">\n'
    '          <div style="font-size:16px;font-weight:700;color:var(--c1)">Thông tin sức khỏe cá nhân</div>\n'
    '          <div style="' + _HGRID + ';font-size:12px;font-weight:700;color:var(--c5);padding-bottom:var(--s2);'
    'border-bottom:1px solid rgba(154,163,176,.3)"><div>TT</div><div>Nội dung</div>'
    '<div style="text-align:center">Không</div><div style="text-align:center">Có</div></div>\n'
    '          <sc-for list="{{healthRows}}" as="h" hint-placeholder-count="4">\n'
    '            <div style="' + _HGRID + ';font-size:13px;color:var(--c2);line-height:1.5;padding-bottom:var(--s3);'
    'border-bottom:1px solid rgba(154,163,176,.15)"><div style="font-weight:700;color:var(--c1)">{{h.no}}</div>'
    '<div>{{h.q}}</div>'
    '<div style="text-align:center"><span class="health-no" sc-camel-on-click="{{h.onNo}}" style="' + (_HBOX % ('no', 'no')) + '">{{h.noMark}}</span></div>'
    '<div style="text-align:center"><span class="health-yes" sc-camel-on-click="{{h.onYes}}" style="' + (_HBOX % ('yes', 'yes')) + '">{{h.yesMark}}</span></div>'
    '</div>\n'
    '          </sc-for>\n'
    # (12/10) Chưa đủ 4 mục thì nhắc + khoá nút Thanh toán.
    '          <sc-if value="{{healthMissing}}" hint-placeholder-val="{{false}}">'
    '<div class="health-hint" style="font-size:12px;color:#965C0A;background:rgba(150,92,10,.1);'
    'border-radius:var(--r-sm);padding:var(--s3) var(--s4);line-height:1.5">'
    'Vui lòng đánh dấu Không / Có cho đủ 4 mục để tiếp tục thanh toán ({{healthDoneCount}}/4).</div></sc-if>\n'
    '        </div>')
_B6_HEALTH = (
    '\n            <div style="height:1px;background:rgba(154,163,176,.25)"></div>\n\n'
    '            <div style="display:flex;flex-direction:column;gap:var(--s3);font-size:13px">\n'
    '              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Thông tin sức khỏe cá nhân (khách khai)</div>\n'
    '              <sc-for list="{{selectedOrder.healthRows}}" as="h" hint-placeholder-count="4">\n'
    '                <div style="display:grid;grid-template-columns:18px 1fr auto;gap:var(--s3);align-items:start;line-height:1.5">'
    '<span style="color:var(--c5)">{{h.no}}</span><span style="color:var(--c2)">{{h.q}}</span>'
    '<span style="font-weight:700;color:{{h.color}};white-space:nowrap">{{h.label}}</span></div>\n'
    '              </sc-for>\n'
    '            </div>\n'
    # Chấp thuận điều khoản của ĐƠN HÀNG — giống khung ở hồ sơ thành viên.
    '\n            <div style="height:1px;background:rgba(154,163,176,.25)"></div>\n\n'
    '            <div style="display:flex;flex-direction:column;gap:var(--s3);font-size:13px">\n'
    '              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Chấp thuận điều khoản</div>\n'
    '              <div style="border:1px solid rgba(47,122,72,.35);background:rgba(47,122,72,.08);border-radius:var(--r-md);'
    'padding:var(--s5);display:flex;flex-direction:column;gap:var(--s3)">\n'
    + ''.join('                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">%s</span>'
              '<span style="%s">{{selectedOrder.%s}}</span></div>\n' % row for row in [
                  ("Văn bản", "color:var(--c2);text-align:right", "tncDoc"),
                  ("Phiên bản HOMI365", "font-weight:600;font-family:monospace", "tncVersion"),
                  ("Thời điểm đồng ý", "font-weight:600;font-family:monospace", "tncAt"),
                  ("Địa chỉ IP", "font-weight:600;font-family:monospace", "tncIp"),
                  ("Định danh", "color:var(--c2);text-align:right;font-family:monospace", "tncUser")]) +
    '                <div style="font-size:11px;color:var(--c5);line-height:1.6">Bằng chứng khách chấp thuận khi mua gói '
    '(gồm cả quyền lợi bảo hiểm kèm gói), phục vụ đối chiếu khi khách khiếu nại hoặc cơ quan chức năng kiểm tra.</div>\n'
    '              </div>\n'
    '            </div>\n')
MARKUP_1010 += [
    ('>Phiên bản T&amp;C</span>', '>Phiên bản HOMI365</span>', None, 'all'),
    ('TECHCOMBANK - 0009383764899', 'TECHCOMBANK - 79365'),
    # KH (10/10, lần 2): đặt ngay dưới khung gói HOMI365-01, trên khung Thanh toán.
    ('{{pkg.price}}</span>\n            </label>\n          </sc-for>\n        </div>',
     '{{pkg.price}}</span>\n            </label>\n          </sc-for>\n        </div>' + A1_HEALTH),
    ('{{selectedOrder.address}}</span></div>\n            </div>\n',
     '{{selectedOrder.address}}</span></div>\n            </div>\n' + _B6_HEALTH),
]
_HQ_JS = _json.dumps(HEALTH_Q, ensure_ascii=False)
JS_1010 += [
    ("    bankQuery: '', bankOpen: false, bankManual: false, bankManualText: '',",
     "    bankQuery: '', bankOpen: false, bankManual: false, bankManualText: '', buyHealth: {},"),
    ("      bankModeLink: s.bankManual ? 'Chọn từ danh sách' : 'Nhập tay',",
     "      bankModeLink: s.bankManual ? 'Chọn từ danh sách' : 'Nhập tay',\n"
     "      // (10/10) Thông tin sức khỏe: mỗi mục chọn Không hoặc Có (bấm lại để bỏ chọn).\n"
     "      healthRows: this.HEALTH_Q.map((q, i) => { const v = (s.buyHealth || {})[i];\n"
     "        const set = (x) => this.setState({ buyHealth: { ...(s.buyHealth || {}), [i]: v === x ? undefined : x } });\n"
     "        const box = (on) => on ? ['#1E3A66', '#1E3A66', '✓'] : ['rgba(154,163,176,.8)', 'transparent', ''];\n"
     "        const [nb, nbg, nm] = box(v === 'no'), [yb, ybg, ym] = box(v === 'yes');\n"
     "        return { no: i + 1, q, onNo: () => set('no'), onYes: () => set('yes'),\n"
     "          noBorder: nb, noBg: nbg, noMark: nm, yesBorder: yb, yesBg: ybg, yesMark: ym }; }),"),
    ("  makeOrders() {",
     "  // (10/10) Thông tin sức khỏe cá nhân khách khai lúc mua (A1), lưu theo đơn.\n"
     "  HEALTH_Q = " + _HQ_JS + ";\n"
     "  ORDER_HEALTH = { DH923983: ['no','no','no','no'], DH100511: ['no','yes','no','no'],\n"
     "                   DH100234: ['no','no','no','no'], DH100088: ['no','no','no','no'] };\n"
     "  makeOrders() {"),
    ("        activationCodeLabel: selOrderRaw.activationCode || '— chưa cấp —',",
     "        activationCodeLabel: selOrderRaw.activationCode || '— chưa cấp —',\n"
     "        healthRows: this.HEALTH_Q.map((q, i) => { const v = (this.ORDER_HEALTH[selOrderRaw.id] || [])[i];\n"
     "          return { no: i + 1, q, label: v === 'yes' ? 'Có' : v === 'no' ? 'Không' : 'Chưa đánh dấu',\n"
     "            color: v === 'yes' ? '#C0392B' : v === 'no' ? 'var(--c1)' : 'var(--c5)' }; }),\n"
     "        // (10/10) Lưu vết chấp thuận Chính sách mua hàng khi khách đặt đơn.\n"
     "        tncDoc: 'Chính sách mua hàng & bảo mật dữ liệu', tncVersion: 'v1.0',\n"
     "        tncAt: selOrderRaw.date + ':04', tncIp: '113.161.' + (40 + selOrderRaw.id.length) + '.' + (+selOrderRaw.id.slice(-3) % 250),\n"
     "        tncUser: selOrderRaw.id + ' · ' + selOrderRaw.phone,"),
]
_patch_screens_1010a = patch_screens


def patch_screens(screens):  # noqa: F811
    screens = _patch_screens_1010a(screens)
    for sc in screens:
        if sc["code"] == "A1":
            sc["states"].append(("suc-khoe", "Thông tin sức khỏe — khách đã đánh dấu",
                                 {"buyStep": "form", "buyerPhone": "0900000000",
                                  "buyHealth": {"0": "no", "1": "yes", "2": "no", "3": "no"}}))
    return screens



# Ghi chú DIFF cho đợt 10/10 (chèn trước dòng trống cuối bảng mục 22).
DIFF_0910[-1:-1] = [
    "| A1 header (10/10) | Bỏ tiêu đề \"Anh chị đã có tài khoản\" ở khung gợi ý (giữ hướng dẫn + nút "
    "Đăng nhập / Bỏ qua / Dùng số khác). Chỉ còn 2 câu: \"Vui lòng nhập số điện thoại để kiểm tra tài khoản\" "
    "trước ô SĐT và \"Anh chị chưa có tài khoản, vui lòng nhập thông tin để mua hàng\" khi SĐT mới. |",
    "| A1, A2 · Ngân hàng (10/10) | Danh sách theo file Techcombank `DomesticBeneficiaryBank.xlsx` "
    "(sheet External batch payment, 111 ngân hàng, giữ nguyên tên để khớp file chi trả; bỏ Kho bạc, NHNN, "
    "Quỹ TDCS) — `tools/banks_tcb.py`; bỏ gọi API VietQR. Không có ô nhập tay (KH bỏ 12/10). |",
    "| A1 · Sức khỏe (10/10) | Khung \"Thông tin sức khỏe cá nhân\" ngay dưới khung gói HOMI365-01: 4 mục, "
    "mỗi mục tick Không / Có (`#suc-khoe`). Đơn hàng lưu lại; B6 chi tiết đơn hiện từng mục, \"Có\" tô đỏ. |",
    "| B6 · Chấp thuận điều khoản (10/10) | Chi tiết đơn có khung Chấp thuận điều khoản như hồ sơ thành viên: "
    "văn bản, Phiên bản HOMI365, thời điểm đồng ý, IP, định danh (mã đơn · SĐT). Đổi nhãn \"Phiên bản T&C\" "
    "→ \"Phiên bản HOMI365\" ở cả B2. |",
    "| A1 · QR (10/10) | Số tài khoản nhận: TECHCOMBANK - 79365 (CONG TY CO PHAN GIAI PHAP VA DICH VU HOMI365). |",
]


# (11/10) C1 từ form mua hàng: SĐT → mật khẩu → OTP → về A1. Đăng nhập thường giữ flow cũ.
MARKUP_1010 += [
    ('Đăng nhập không thành công. Nhập mã OTP đã gửi tới {{agentMaskedPhone}} để tiếp tục.',
     '{{agentOtpNote}}'),
]
JS_1010 += [
    ("      agentBackToLogin: () => this.setState({ agentLoginStep: 'login' }),",
     "      agentBackToLogin: () => this.setState({ agentLoginStep: 'login' }),\n"
     "      agentOtpNote: (s.returnTo === 'A1' && !s.agentLoginError)\n"
     "        ? 'Nhập mã OTP đã gửi tới ' + (s.agentPhone ? s.agentPhone.slice(0, 3) + '•••' + s.agentPhone.slice(-3) : '090•••123') + ' để hoàn tất đăng nhập và quay lại form mua hàng.'\n"
     "        : 'Đăng nhập không thành công. Nhập mã OTP đã gửi tới ' + (s.agentPhone ? s.agentPhone.slice(0, 3) + '•••' + s.agentPhone.slice(-3) : '090•••123') + ' để tiếp tục.',"),
]
_patch_screens_1110 = patch_screens


def patch_screens(screens):  # noqa: F811
    screens = _patch_screens_1110(screens)
    for sc in screens:
        if sc["code"] == "C1":
            i = [h for h, _, _ in sc["states"]].index("tu-mua-hang") + 1
            sc["states"].insert(i, ("tu-mua-hang-otp", "Từ form mua hàng — nhập OTP sau mật khẩu, xong quay lại A1",
                                    {"agentLoginStep": "otp", "agentPhone": "0901234567",
                                     "loginPhoneChecked": True, "returnTo": "A1"}))
    return screens


DIFF_0910[-1:-1] = [
    "| C1 (11/10) | Vào từ form mua hàng: nhập SĐT → mật khẩu → **màn OTP** → xác thực xong mới quay lại "
    "form A1 (tự điền) — `c1-login.html#tu-mua-hang-otp`. Bấm \"Đăng nhập thành viên HOMI365\" giữ flow cũ: "
    "đúng mật khẩu vào thẳng dashboard. |",
]


# (12/10) Modal thanh toán thành công: SĐT đã có tài khoản thì mời ĐĂNG NHẬP
# (không mời đăng ký thành viên nữa); SĐT mới giữ nội dung mời đăng ký.
_PAYOK_LOGIN_BTN = ('<button sc-camel-on-click="{{payOkLogin}}" style="height:46px;background:var(--c6);'
                    'color:var(--c12);border:none;border-radius:var(--r-md);font-size:15px;font-weight:700;'
                    'box-shadow:var(--sh)">Đăng nhập thành viên</button>')
MARKUP_1010 += [
    ('Đơn hàng đã được ghi nhận, mời gia nhập HOMI365</div>', '{{payOkTitle}}</div>'),
    ('Bạn có muốn đăng ký làm Thành viên HOMI365 để nhận các ưu đãi không?', '{{payOkAsk}}'),
    ('<button sc-camel-on-click="{{choosRegisterSeller}}"',
     '<sc-if value="{{payOkNew}}" hint-placeholder-val="{{true}}"><button sc-camel-on-click="{{choosRegisterSeller}}"',
     ),
    ('>Đăng ký thành viên</button>',
     '>Đăng ký thành viên</button></sc-if>'
     '<sc-if value="{{payOkMember}}" hint-placeholder-val="{{false}}">' + _PAYOK_LOGIN_BTN + '</sc-if>',
     ),
    ('>Không, thoát ra</button>', '>{{payOkSkipLabel}}</button>'),
]
JS_1010 += [
    ("      loginFromBuy: s.returnTo === 'A1',",
     "      // (12/10) Modal thanh toán thành công — người đã có tài khoản thì mời đăng nhập.\n"
     "      ...(() => { const ph = (s.buyerPhone || s.buyPhoneInput || '').trim();\n"
     "        const member = s.buyMode === 'self' || this.REGISTERED_PHONES.includes(ph);\n"
     "        const masked = ph ? ph.slice(0, 3) + '•••' + ph.slice(-3) : '';\n"
     "        return { payOkMember: member, payOkNew: !member,\n"
     "          payOkTitle: member ? 'Đơn hàng đã được ghi nhận' : 'Đơn hàng đã được ghi nhận, mời gia nhập HOMI365',\n"
     "          payOkAsk: member\n"
     "            ? 'Số điện thoại ' + masked + ' đã có tài khoản thành viên HOMI365. Đăng nhập để theo dõi đơn hàng và điểm ưu đãi.'\n"
     "            : 'Bạn có muốn đăng ký làm Thành viên HOMI365 để nhận các ưu đãi không?',\n"
     "          payOkSkipLabel: member ? 'Để sau' : 'Không, thoát ra',\n"
     "          payOkLogin: () => GO('C1', { agentLoginStep: 'login', agentPhone: ph, loginPhoneChecked: true, returnTo: '' }) }; })(),\n"
     "      loginFromBuy: s.returnTo === 'A1',"),
]
_patch_screens_1210 = patch_screens


def patch_screens(screens):  # noqa: F811
    screens = _patch_screens_1210(screens)
    for sc in screens:
        if sc["code"] == "A1":
            i = [h for h, _, _ in sc["states"]].index("thanh-toan-ok") + 1
            sc["states"].insert(i, ("thanh-toan-ok-thanh-vien", "Thanh toán xong — SĐT đã có tài khoản, mời đăng nhập",
                                    {"showPaymentSuccess": True, "buyStep": "form", "buyMode": "self",
                                     "buyerPhone": "0901234567", "buyPhoneInput": "0901234567"}))
    return screens


DIFF_0910[-1:-1] = [
    "| A1 · Thanh toán thành công (12/10) | SĐT đã có tài khoản: tiêu đề \"Đơn hàng đã được ghi nhận\", "
    "báo SĐT đã có tài khoản, nút **Đăng nhập thành viên** (sang C1, vào dashboard) + \"Để sau\" — "
    "`a1-buy.html#thanh-toan-ok-thanh-vien`. SĐT mới giữ lời mời đăng ký thành viên. |",
]


# (12/10) Phải trả lời đủ 4 mục sức khỏe (Không hoặc Có) mới bấm được Thanh toán.
JS_1010 += [
    ("    const payOk = s.buyTcChecked && s.payStage !== 'sending' && !buyerDobError;",
     "    // (12/10) Đủ 4 mục Thông tin sức khỏe mới cho thanh toán.\n"
     "    const healthDoneCount = [0, 1, 2, 3].filter(i => ['no', 'yes'].includes((s.buyHealth || {})[i])).length;\n"
     "    const payOk = s.buyTcChecked && s.payStage !== 'sending' && !buyerDobError && healthDoneCount === 4;"),
    ("      bankModeLink: s.bankManual ? 'Chọn từ danh sách' : 'Nhập tay',",
     "      bankModeLink: s.bankManual ? 'Chọn từ danh sách' : 'Nhập tay',\n"
     "      healthDoneCount, healthMissing: healthDoneCount < 4,"),
]

MARKUP.extend(MARKUP_1010)
JS.extend(JS_1010)
