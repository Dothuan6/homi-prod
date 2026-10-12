#!/usr/bin/env python3
"""
Sinh các trang theo URL thật của hệ thống HOMI365 từ screens/*.html.

    https://homi365.com.vn/<MÃ>                -> A1 form mua hàng (404.html chuyển về)
    https://homi365.com.vn/policy?s=<slug>     -> Chính sách
    https://homi365.com.vn/agent/dang-nhap     -> C1 Đăng nhập thành viên
    https://homi365.com.vn/agent/dang-ky       -> A2 Đăng ký thành viên
    https://homi365.com.vn/agent               -> A3 Dashboard thành viên
    https://homi365.com.vn/admin/...           -> B1..B9 quản trị

Host trên Netlify (_redirects) hoặc GitHub Pages: file foo.html được phục vụ ở /foo (không đuôi .html).
Đường dẫn còn lại (vd /SA2237) rơi vào 404.html -> chuyển về trang gốc kèm
?__p=SA2237, trang gốc đổi lại thanh địa chỉ thành /SA2237 và điền mã giới thiệu.
Chạy được cả khi site nằm ở domain riêng (gốc /) lẫn <user>.github.io/homi-prod/.

Chạy:  python tools/build-routes.py      (build-v3.py tự gọi ở cuối)
"""
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
SRC = SITE / "screens"
DOMAIN = "https://homi365.com.vn"

# mã màn -> file nguồn trong screens/
FILE = {
    "A1": "a1-buy.html", "A2": "a2-register.html", "A3": "a3-dashboard.html",
    "C1": "c1-login.html", "B1": "b1-admin-login.html", "B2": "b2-members.html",
    "B3": "b3-withdrawals.html", "B4": "b4-warehouse.html", "B5": "b5-products.html",
    "B6": "b6-orders.html", "B7": "b7-admin-users.html", "B8": "b8-audit-log.html",
    "B9": "b9-rank-review.html", "POLICY": "policy.html",
}
# mã màn -> URL tính từ gốc site (không có / đầu)
ROUTE = {
    "A1": "", "A2": "agent/dang-ky", "A3": "agent", "C1": "agent/dang-nhap",
    "POLICY": "policy",
    "B1": "admin/dang-nhap", "B2": "admin/thanh-vien", "B9": "admin/xet-hang",
    "B3": "admin/doi-diem", "B4": "admin/kho-hang", "B5": "admin/san-pham",
    "B6": "admin/don-hang", "B7": "admin/tai-khoan", "B8": "admin/nhat-ky",
}
# file xuất ra: (đường dẫn, mã màn). /agent và /admin có cả x.html lẫn x/index.html
# để GitHub Pages ưu tiên kiểu nào cũng ra đúng màn.
OUT = [
    ("index.html", "A1"), ("policy.html", "POLICY"),
    ("agent.html", "A3"), ("agent/index.html", "A3"),
    ("agent/dang-nhap.html", "C1"), ("agent/dang-ky.html", "A2"),
    ("admin.html", "B2"), ("admin/index.html", "B2"),
] + [(ROUTE[c] + ".html", c) for c in ("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9")]


def fix_links(t):
    """Link hiển thị / copy cho người dùng -> full URL theo hệ thống thật."""
    t = t.replace("'homi365.com.vn/dang-nhap/' + affCode", "'%s/agent/dang-nhap'" % DOMAIN)
    t = t.replace("'.../dang-nhap/' + affCode", "'.../agent/dang-nhap'")
    t = t.replace("'homi365.com.vn/' + affCode", "'%s/' + affCode" % DOMAIN)
    t = t.replace("'homi365.com.vn/htmt0083'", "'%s/HTMT0083'" % DOMAIN)
    return t


def link(code, depth):
    p = "../" * depth
    r = ROUTE[code]
    return (p + r) if r else (p or "./")


# Mã giới thiệu hợp lệ (site tĩnh, không có database) -> tên hiện ở ô "Mã giới thiệu".
# Mã ngoài danh sách, hoặc vào trang gốc không có mã -> màn thông báo
# "Vui lòng dùng liên kết giới thiệu của người bán…". Thêm mã: sửa ở đây rồi chạy lại.
# Không có PTD4789 (Phạm Thị Dung — tài khoản đang khoá).
VALID_REF = {
    "SA2237": "",
    "HTMT0083": "HOÀNG THỊ MỸ TRINH",
    "TTB4123": "TRẦN THỊ BÍCH",
    "LVC5456": "LÊ VĂN CƯỜNG",
    "NTE3112": "NGÔ THỊ EM",
    "VMK7998": "VŨ MINH KHANG",
    "DVP8221": "ĐẶNG VĂN PHÚC",
    "TTB4123-2": "TRƯƠNG THANH BÌNH",
}

# Trang gốc: nhận /<MÃ> (từ 404.html, _redirects hoặc gõ thẳng).
BOOT_A1 = """<script>
(function () {
  var VALID = __VALID__;
  var q = new URLSearchParams(location.search), p = q.get('__p');
  if (p) {
    q.delete('__p'); var qs = q.toString();
    history.replaceState(null, '', location.pathname.replace(/[^\\/]*$/, '') + p + (qs ? '?' + qs : '') + location.hash);
  }
  var seg = decodeURIComponent(location.pathname.split('/').pop() || '');
  if (/\\.html?$/i.test(seg)) seg = '';
  var code = seg.toUpperCase();
  if (code && Object.prototype.hasOwnProperty.call(VALID, code)) {
    window.__REF_CODE = code;
    window.__REF_LABEL = VALID[code] ? code + ' — ' + VALID[code] : code;
    try { sessionStorage.setItem('__homi_ref', code); } catch (e) {}
  } else {
    document.documentElement.classList.add('homi-noref');
  }
})();
</script>
<style>
  .homi-noref-msg{display:none}
  .homi-noref .homi-noref-msg{display:flex}
  .homi-noref .homi-a1-main,.homi-noref .homi-buyphone{display:none!important}
</style>"""

NOREF_MSG = """  <div class="homi-noref-msg" style="justify-content:center;padding:var(--s8) var(--s7) var(--s10)">
    <div style="width:100%;max-width:1160px;background:var(--c12);border:1px solid rgba(154,163,176,.25);border-radius:var(--r-lg);box-shadow:var(--sh);padding:var(--s9) var(--s8);text-align:center;font-size:15px;line-height:1.6;color:var(--c4)">Vui lòng dùng liên kết giới thiệu của người bán (dạng homi365.com.vn/&lt;mã giới thiệu&gt;) để tiếp tục mua hàng.</div>
  </div>
"""
A1_MAIN = """  <sc-if value="{{isA1}}" hint-placeholder-val="{{true}}">
  <div style="display:flex;flex-direction:column;align-items:center;gap:var(--s7);padding:var(--s8) var(--s7) var(--s10);background:var(--warm-50)">"""

PAGE_404 = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>HOMI365</title>
<script>
// /<MÃ GIỚI THIỆU> không có file thật -> về trang gốc kèm ?__p=<MÃ>.
// Trên <user>.github.io/<repo>/ thì giữ lại đoạn /<repo>/ đầu đường dẫn.
(function () {
  var keep = /\\.github\\.io$/i.test(location.hostname) ? 1 : 0;
  var parts = location.pathname.split('/');
  var root = parts.slice(0, 1 + keep).join('/') + '/';
  var rest = parts.slice(1 + keep).filter(Boolean);
  if (rest.length === 1 && /^[A-Za-z0-9_-]{2,32}$/.test(rest[0]))
    location.replace(root + '?__p=' + encodeURIComponent(rest[0]) + location.hash);
  else
    location.replace(root);
})();
</script>
</head>
<body></body>
</html>
"""

HREF_RE = re.compile(r'href="(%s)' % "|".join(re.escape(f) for f in FILE.values()))
FILES_RE = re.compile(r"window\.__FILES = \{[^}]*\};")


def render(src_text, code, depth):
    t = fix_links(src_text)
    p = "../" * depth
    for d in ("css", "js", "assets"):
        t = t.replace('"../%s/' % d, '"%s%s/' % (p, d))
    by_file = {f: c for c, f in FILE.items()}
    t = HREF_RE.sub(lambda m: 'href="' + link(by_file[m.group(1)], depth), t)
    files = {c: link(c, depth) for c in FILE if c != "POLICY"}
    # Quay lại form (vd đăng nhập từ form mua hàng xong) -> về đúng /<MÃ> đã vào.
    t, n = FILES_RE.subn(lambda m: "window.__FILES = %s;\n"
                         "try { var __r = sessionStorage.getItem('__homi_ref'); "
                         "if (__r) window.__FILES.A1 += __r; } catch (e) {}" % json.dumps(files), t)
    if code != "POLICY" and n != 1:
        raise SystemExit("%s: không tìm thấy window.__FILES" % FILE[code])
    # Ô "Mã giới thiệu" ở form A1 lấy theo URL /<MÃ>.
    t = t.replace('value="HTMT0083 — HOÀNG THỊ MỸ TRINH"', 'value="{{buyRefLabel}}"')
    t = t.replace("showUplineBlockedModal: s.showUplineBlockedModal,",
                  "buyRefLabel: window.__REF_LABEL || 'HTMT0083 — HOÀNG THỊ MỸ TRINH',\n"
                  "      showUplineBlockedModal: s.showUplineBlockedModal,", 1)
    if code == "A1":
        boot = BOOT_A1.replace("__VALID__", json.dumps(VALID_REF, ensure_ascii=False))
        t = t.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + boot, 1)
        if A1_MAIN not in t:
            raise SystemExit("a1-buy.html: không tìm thấy khối A1 để chèn màn thông báo")
        t = t.replace(A1_MAIN, NOREF_MSG + A1_MAIN.replace(
            '<div style="display:flex', '<div class="homi-a1-main" style="display:flex', 1), 1)
    if "../index.html" in t or ".html?s=" in t:
        raise SystemExit("%s: còn link kiểu cũ" % FILE[code])
    return t


def main():
    # Nguồn screens/ cũng dùng full URL cho link hiển thị.
    for f in SRC.glob("*.html"):
        s = f.read_text(encoding="utf-8")
        s2 = fix_links(s)
        if s2 != s:
            f.write_text(s2, encoding="utf-8")
    cache = {c: (SRC / f).read_text(encoding="utf-8") for c, f in FILE.items()}
    for path, code in OUT:
        out = SITE / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(cache[code], code, path.count("/")), encoding="utf-8")
        print("  %-26s <- %s" % (path, FILE[code]))
    (SITE / "404.html").write_text(PAGE_404, encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    # Netlify: rewrite 200 (không đổi URL, không qua 404). File có thật luôn
    # được ưu tiên hơn rule, nên /css/..., /agent/dang-nhap... không bị ảnh hưởng.
    rules = ["# Sinh bởi tools/build-routes.py — không sửa tay."]
    for path, code in OUT:
        if path in ("index.html",) or path.endswith("/index.html"):
            continue
        rules.append("/%-22s /%-26s 200" % (path[:-5], path))
    rules.append("# /<MÃ GIỚI THIỆU>, vd /SA2237 -> form mua hàng A1")
    rules.append("/%-22s /%-26s 200" % (":code", "index.html"))
    (SITE / "_redirects").write_text("\n".join(rules) + "\n", encoding="utf-8")
    print("  404.html, .nojekyll, _redirects (Netlify)")


if __name__ == "__main__":
    main()
