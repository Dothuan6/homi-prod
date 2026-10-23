#!/usr/bin/env python3
"""
Áp PRD Nhóm A — tab "10.23" (23/10/2026) lên screens/*.html.

  1. Tự mua qua link của mình: bản giao diện không có dòng chặn tự mua, chỉ thêm
     đơn tự mua mẫu ở B6 (người mua = người giới thiệu).
  2. Tạo đơn khi bấm Thanh toán ("Đơn vừa đặt"); bấm lại cùng thông tin, đơn
     chưa hết hạn -> dùng lại đơn và mã cũ.
  3. Mã đơn = <Mã thành viên của link>-<4 số> (vd HTMT0083-0001), hiện trên modal
     QR kèm nút sao chép, trùng với mã ở B6 và nội dung chuyển khoản.
  4. "Đơn vừa đặt" quá 1 tiếng chưa tải ảnh -> "Hủy do hết hạn thanh toán";
     tải ảnh lúc đó báo hết hạn, đặt lại thì có mã mới.
  5. 4 câu hỏi sức khỏe tick sẵn "Không", khoá ô "Có".

Chạy lại nhiều lần không sao (có dấu MARK). build-routes.py tự gọi trước khi sinh trang.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "screens"
MARK = "// (23/10) PRD Nhóm A 10.23"

# Mã đơn mẫu cũ (DH + 6 số) -> <mã thành viên của link>-<4 số>.
ID_MAP = {
    "DH923983": "TTB4123-0003", "DH100511": "LVC5456-0003", "DH100234": "VMK7998-0002",
    "DH100088": "LVC5456-0002", "DH100012": "TTB4123-0002", "DH100077": "HTMT0083-0001",
}

NEW_ORDERS = """      // (23/10) Đơn vừa đặt: khách đã bấm Thanh toán, chưa tải ảnh — Admin chỉ xem.
      { id:'TTB4123-0004', buyer:'Trịnh Văn Long', phone:'0906666666', email:'trinhvanlong@gmail.com',
        address:'15 Lý Tự Trọng, Phường Sài Gòn, TP. Hồ Chí Minh',
        pkg:'HOMI365-01 · Gói 1 năm', amountNum:10000000, referrer:'Trần Thị Bích', refCode:'TTB4123',
        date:'03/09/2026 10:05', status:'order_new', proof:null, activationCode:null,
        auditLog:[{label:'Khách bấm Thanh toán — tạo đơn (Đơn vừa đặt)', actor:'Hệ thống', time:'03/09/2026 10:05'}] },
      // (23/10) Đơn tự mua: thành viên mua qua link của chính mình, xử lý như đơn thường.
      { id:'VMK7998-0004', buyer:'Vũ Minh Khang', phone:'0934567998', email:'vuminhkhang@gmail.com',
        address:'27 Bạch Đằng, Phường Hải Châu, TP. Đà Nẵng',
        pkg:'HOMI365-01 · Gói nửa năm', amountNum:6000000, referrer:'Vũ Minh Khang', refCode:'VMK7998',
        date:'03/09/2026 08:40', status:'order_pending', proof:'bill-VMK7998-0004.jpg', activationCode:null,
        auditLog:[{label:'Khách bấm Thanh toán — tạo đơn (Đơn vừa đặt)', actor:'Hệ thống', time:'03/09/2026 08:40'},
                  {label:'Khách tải ảnh chuyển khoản — chuyển Chờ đối soát', actor:'Vũ Minh Khang', time:'03/09/2026 08:52'}] },
      // (23/10) Quá 1 tiếng chưa tải ảnh -> hệ thống tự hủy, Admin không thao tác.
      { id:'VMK7998-0003', buyer:'Lâm Thị Thu', phone:'0907777777', email:'lamthithu@gmail.com',
        address:'9 Nguyễn Văn Linh, Phường Thanh Khê, TP. Đà Nẵng',
        pkg:'HOMI365-01 · Gói 1 năm', amountNum:10000000, referrer:'Vũ Minh Khang', refCode:'VMK7998',
        date:'01/09/2026 20:15', status:'order_expired', proof:null, activationCode:null,
        auditLog:[{label:'Khách bấm Thanh toán — tạo đơn (Đơn vừa đặt)', actor:'Hệ thống', time:'01/09/2026 20:15'},
                  {label:'Hủy do hết hạn thanh toán (quá 1 tiếng chưa tải ảnh chuyển khoản)', actor:'Hệ thống', time:'01/09/2026 21:15'}] },
"""

NEXT_ID = """  """ + MARK + """: mã đơn = <Mã thành viên của link>-<4 số>,
  // đếm riêng từng link, bắt đầu 0001, không dùng lại. Bản mẫu đếm trong
  // localStorage của trình duyệt; bản thật sinh ở BE, khoá chống trùng khi tạo đồng thời.
  ORDER_SEQ_BASE = { TTB4123: 4, LVC5456: 3, VMK7998: 4 };
  nextOrderId() {
    const ref = (window.__REF_CODE || 'HTMT0083').toUpperCase();
    let n = this.ORDER_SEQ_BASE[ref] || 0;
    try { n = Math.max(n, parseInt(localStorage.getItem('__homi_seq_' + ref) || '0', 10) || 0); } catch (e) {}
    n += 1;
    try { localStorage.setItem('__homi_seq_' + ref, String(n)); } catch (e) {}
    return ref + '-' + String(n).padStart(4, '0');
  }

"""

QR_CODE_BLOCK = """        <div style="display:flex;align-items:center;justify-content:space-between;gap:var(--s4);border:1px solid rgba(30,58,102,.25);background:rgba(30,58,102,.05);border-radius:var(--r-md);padding:var(--s4) var(--s5);text-align:left">
          <div><div style="font-size:12px;color:var(--c5)">Mã đơn hàng</div><div style="font-size:17px;font-weight:700;color:var(--c1);font-family:monospace;letter-spacing:.02em">{{orderId}}</div></div>
          <button sc-camel-on-click="{{copyOrderId}}" style="flex:none;height:34px;padding:0 var(--s5);background:var(--c12);color:var(--c6);border:1px solid var(--c6);border-radius:var(--r-md);font-size:13px;font-weight:600" style-hover="background:rgba(30,58,102,.08)">{{copyOrderIdLabel}}</button>
        </div>
"""

QR_EXPIRED_BLOCK = """
        <sc-if value="{{orderExpired}}" hint-placeholder-val="{{false}}">
          <div style="display:flex;flex-direction:column;gap:var(--s4);border:1px solid rgba(192,57,43,.35);background:rgba(192,57,43,.08);border-radius:var(--r-md);padding:var(--s5)">
            <div style="font-size:13px;font-weight:600;color:#C0392B;line-height:1.5">Đơn hàng đã hết hạn thanh toán, vui lòng đặt lại.</div>
            <button sc-camel-on-click="{{reorderExpired}}" style="height:40px;background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600" style-hover="background:#1B3358">Đặt lại</button>
          </div>
        </sc-if>"""


def rep(t, old, new, name, count=1):
    n = t.count(old)
    if n != count:
        raise SystemExit("update_prd1023 [%s]: tìm thấy %d chỗ, cần %d" % (name, n, count))
    return t.replace(old, new)


def patch_script(t):
    # Sức khỏe mẫu theo đơn: mọi đơn 4 mục "Không" (khách không chọn được "Có").
    t = rep(t, """ORDER_HEALTH = { DH923983: ['no','no','no','no'], DH100511: ['no','yes','no','no'],
                   DH100234: ['no','no','no','no'], DH100088: ['no','no','no','no'] };""",
            """ORDER_HEALTH = { 'TTB4123-0003': ['no','no','no','no'], 'LVC5456-0003': ['no','no','no','no'],
                   'VMK7998-0002': ['no','no','no','no'], 'LVC5456-0002': ['no','no','no','no'],
                   'TTB4123-0004': ['no','no','no','no'], 'VMK7998-0004': ['no','no','no','no'],
                   'VMK7998-0003': ['no','no','no','no'] };""", "ORDER_HEALTH")
    for old, new in ID_MAP.items():
        t = t.replace(old, new)
    t = rep(t, "'DH' + (100000 + i * 13)",
            "['TTB4123', 'LVC5456', 'VMK7998', 'NTE3112'][i % 4] + '-' + String(11 + i).padStart(4, '0')",
            "mã đơn kho")
    t = rep(t, "  makeOrders() {\n    const raw = [\n", "  makeOrders() {\n    const raw = [\n" + NEW_ORDERS, "đơn mẫu")
    t = rep(t, "order_rejected: ['rgba(192,57,43,.12)', '#C0392B', 'Từ chối']\n    };",
            "order_rejected: ['rgba(192,57,43,.12)', '#C0392B', 'Từ chối'],\n"
            "      order_new: ['rgba(30,58,102,.1)', '#1E3A66', 'Đơn vừa đặt'],\n"
            "      order_expired: ['rgba(154,163,176,.2)', '#5B6472', 'Hủy do hết hạn thanh toán']\n    };", "badge")
    t = rep(t, "ORDER_FILTERS = [['all','Tất cả'],['order_pending','Chờ đối soát'],['order_paid','Đã thanh toán'],['order_rejected','Từ chối']];",
            "ORDER_FILTERS = [['all','Tất cả'],['order_new','Đơn vừa đặt'],['order_pending','Chờ đối soát'],['order_paid','Đã thanh toán'],['order_rejected','Từ chối'],['order_expired','Hủy do hết hạn thanh toán']];",
            "bộ lọc")
    t = rep(t, "          : (selOrderRaw.status === 'order_rejected' ? 'Đơn đã bị từ chối.' : null),",
            "          : selOrderRaw.status === 'order_new'\n"
            "          ? 'Đơn vừa đặt: khách đã bấm Thanh toán nhưng chưa tải ảnh chuyển khoản. Chỉ xem, chưa thao tác được. Quá 1 tiếng chưa tải ảnh, hệ thống tự hủy đơn.'\n"
            "          : selOrderRaw.status === 'order_expired'\n"
            "          ? 'Đơn đã hủy do hết hạn thanh toán (quá 1 tiếng chưa tải ảnh chuyển khoản). Không nhận ảnh, không tính ưu đãi, không gửi email, không thao tác.'\n"
            "          : (selOrderRaw.status === 'order_rejected' ? 'Đơn đã bị từ chối.' : null),", "ghi chú B6")
    # Sức khỏe: tick sẵn "Không", khoá "Có".
    t = rep(t, "buyHealth: {},", "buyHealth: { 0: 'no', 1: 'no', 2: 'no', 3: 'no' },", "buyHealth mặc định")
    t = rep(t, "const healthDoneCount = [0, 1, 2, 3].filter(i => ['no', 'yes'].includes((s.buyHealth || {})[i])).length;",
            "const healthDoneCount = 4; " + MARK + ": 4 mục luôn \"Không\"", "healthDoneCount")
    t = rep(t, "const set = (x) => this.setState({ buyHealth: { ...(s.buyHealth || {}), [i]: v === x ? undefined : x } });",
            "const set = () => {}; " + MARK + ": tick sẵn \"Không\", ô \"Có\" khoá", "health set")
    t = rep(t, "const [nb, nbg, nm] = box(v === 'no'), [yb, ybg, ym] = box(v === 'yes');",
            "const [nb, nbg, nm] = box(true), yb = 'rgba(154,163,176,.35)', ybg = 'rgba(154,163,176,.15)', ym = '';",
            "health box")
    # Mã đơn + tạo / dùng lại đơn khi bấm Thanh toán.
    t = rep(t, "  aliasOf(name, phone) {", NEXT_ID + "  aliasOf(name, phone) {", "nextOrderId")
    t = rep(t, "if (s.orderCreated) { this.setState({ showQRPayment: true }); return; }",
            MARK + ": cùng phiên, cùng thông tin, đơn chưa hết hạn -> dùng lại đơn và mã cũ.\n"
            "        const sig = [s.buyerName, s.buyerPhone, s.buyerEmail, s.buyerCccd, s.cn02Package].join('|');\n"
            "        if (s.orderCreated && !s.orderExpired && s.orderSig === sig) { this.setState({ showQRPayment: true }); return; }",
            "submitPayment")
    t = rep(t, "payStage: 'idle', orderCreated: true, showQRPayment: true\n",
            "payStage: 'idle', orderCreated: true, showQRPayment: true,\n"
            "          orderId: this.nextOrderId(), orderSig: sig, orderCreatedAt: Date.now(),\n"
            "          orderExpired: false, orderIdCopied: false\n", "tạo đơn")
    t = rep(t, "confirmQRPayment: () => this.setState({ showQRPayment: false, showPaymentSuccess: true }),",
            MARK + ": \"Đơn vừa đặt\" quá 1 tiếng chưa tải ảnh -> đã hủy, không nhận ảnh.\n"
            "      confirmQRPayment: () => (s.orderExpired || (s.orderCreatedAt && Date.now() - s.orderCreatedAt > 3600000))\n"
            "        ? this.setState({ orderExpired: true })\n"
            "        : this.setState({ showQRPayment: false, showPaymentSuccess: true }),\n"
            "      orderExpired: !!s.orderExpired, qrUploadOpen: !s.orderExpired,\n"
            "      reorderExpired: () => this.setState({ orderCreated: false, orderExpired: false, showQRPayment: false, orderSig: '' }),\n"
            "      copyOrderId: () => { try { navigator.clipboard.writeText(s.orderId); } catch (e) {}\n"
            "        this.setState({ orderIdCopied: true }); clearTimeout(this.__copyTimer);\n"
            "        this.__copyTimer = setTimeout(() => this.setState({ orderIdCopied: false }), 1500); },\n"
            "      copyOrderIdLabel: s.orderIdCopied ? 'Đã sao chép' : 'Sao chép',", "confirmQRPayment")
    return t


def patch_a1_markup(t):
    t = rep(t, """<button sc-camel-on-click="{{closeQRPayment}}" style="background:none;border:none;font-size:18px;color:var(--c5)">✕</button>
        </div>
""", """<button sc-camel-on-click="{{closeQRPayment}}" style="background:none;border:none;font-size:18px;color:var(--c5)">✕</button>
        </div>
""" + QR_CODE_BLOCK, "modal mã đơn")
    lab = '        <label style="border:1px dashed rgba(154,163,176,.6);border-radius:var(--r-md);padding:var(--s6);display:flex;flex-direction:column;align-items:center;gap:var(--s2);cursor:pointer;color:var(--c5)"'
    i = t.find(lab)
    if i < 0 or t.count(lab) != 1:
        raise SystemExit("update_prd1023 [ô tải ảnh]: không tìm thấy")
    j = t.index("</label>", i) + len("</label>")
    t = t[:i] + '        <sc-if value="{{qrUploadOpen}}" hint-placeholder-val="{{true}}">\n' + t[i:j] + "\n        </sc-if>" + QR_EXPIRED_BLOCK + t[j:]
    # Ô "Có" khoá, ô "Không" không bấm bỏ được.
    k = t.find('class="health-yes"')
    e = t.index("</span>", k)
    t = t[:k] + t[k:e].replace("cursor:pointer", "cursor:not-allowed;opacity:.55") + t[e:]
    k = t.find('class="health-no"')
    e = t.index("</span>", k)
    t = t[:k] + t[k:e].replace("cursor:pointer", "cursor:default") + t[e:]
    t = rep(t, "var H = {", 'var H = {"qr-het-han": {"buyStep": "form", "showQRPayment": true, "orderCreated": true, '
            '"orderId": "HTMT0083-0002", "orderExpired": true}, ', "hash A1")
    return t


def patch_b6_markup(t):
    return rep(t, "var H = {", 'var H = {"vua-dat": {"selectedOrderId": "TTB4123-0004"}, '
               '"huy-het-han": {"selectedOrderId": "VMK7998-0003"}, "tu-mua": {"selectedOrderId": "VMK7998-0004"}, ',
               "hash B6")


def main():
    n = 0
    for f in sorted(SRC.glob("*.html")):
        if f.name == "policy.html":
            continue
        t = f.read_text(encoding="utf-8")
        if MARK in t:
            continue
        t = patch_script(t)
        if f.name == "a1-buy.html":
            t = patch_a1_markup(t)
        if f.name == "b6-orders.html":
            t = patch_b6_markup(t)
        f.write_text(t, encoding="utf-8")
        n += 1
    print("  update_prd1023: đã áp %d file" % n)


if __name__ == "__main__":
    main()
