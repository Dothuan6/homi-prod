#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract-bundle.py — giải nén mockup của khách hàng.

`Prototypev-v3/Homi365_Mockup-0409.html` là một bundle tự giải nén: markup thật
nằm trong <script type="__bundler/template"> ở dạng chuỗi JSON, còn font/ảnh nằm
base64 (có thể gzip) trong <script type="__bundler/manifest">. Script này làm
đúng những gì trình duyệt làm khi mở file đó, nhưng ghi kết quả ra đĩa:

    prototype-v3/tools/_raw/
      template.html      markup đầy đủ, đọc được bằng mắt
      res/<uuid>.<ext>   ảnh / font đã giải nén
      pages/<uuid>.html  trang lồng (nếu bundle có iframe)
      REPORT.txt         thống kê: số asset, mime, kích thước, số màn tìm thấy

Chạy:
    cd D:\\BA\\ProjectBA\\Medigo
    python prototype-v3\\tools\\extract-bundle.py

Cần Python 3.7+. Không cần cài thư viện ngoài.
"""

import base64
import gzip
import json
import re
import sys
from pathlib import Path

# --- Đường dẫn ---------------------------------------------------------------

HERE = Path(__file__).resolve().parent          # prototype-v3/tools
ROOT = HERE.parent.parent                        # Medigo/
SRC = ROOT / "Prototypev-v3" / "Homi365_Mockup-0409.html"
OUT = HERE / "_raw"

# --- Bảng đuôi file theo mime ------------------------------------------------

EXT = {
    "font/woff2": "woff2", "font/woff": "woff", "font/ttf": "ttf",
    "font/otf": "otf", "application/font-woff": "woff",
    "application/x-font-ttf": "ttf", "application/vnd.ms-fontobject": "eot",
    "image/png": "png", "image/jpeg": "jpg", "image/jpg": "jpg",
    "image/gif": "gif", "image/webp": "webp", "image/svg+xml": "svg",
    "image/x-icon": "ico", "text/html": "html", "text/css": "css",
    "text/plain": "txt", "application/javascript": "js",
    "text/javascript": "js", "application/json": "json",
}
FONT_MIME = re.compile(r"^(font/|application/(x-)?font-|application/vnd\.ms-fontobject)", re.I)


def ext_for(mime):
    return EXT.get((mime or "").split(";")[0].strip().lower(), "bin")


def island(html, kind):
    """Lấy nội dung <script type="__bundler/<kind>">…</script>."""
    m = re.search(
        r'<script[^>]*type="__bundler/%s"[^>]*>(.*?)</script>' % re.escape(kind),
        html, re.S | re.I)
    return m.group(1) if m else None


def human(n):
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return "%.1f %s" % (n, unit)
        n /= 1024.0


def main():
    if not SRC.exists():
        sys.exit("Không tìm thấy file nguồn:\n  %s" % SRC)

    print("Đọc  %s  (%s)" % (SRC.name, human(SRC.stat().st_size)))
    html = SRC.read_text(encoding="utf-8", errors="replace")

    raw_manifest = island(html, "manifest")
    raw_template = island(html, "template")
    if raw_manifest is None or raw_template is None:
        sys.exit("File này không phải bundle — thiếu island manifest hoặc template.")

    manifest = json.loads(raw_manifest)
    template = json.loads(raw_template)          # island template là MỘT chuỗi JSON
    raw_pages = island(html, "page_order")
    page_order = json.loads(raw_pages) if raw_pages else []
    page_set = set(page_order)

    (OUT / "res").mkdir(parents=True, exist_ok=True)
    if page_set:
        (OUT / "pages").mkdir(parents=True, exist_ok=True)

    report = []
    report.append("Nguồn      : %s" % SRC)
    report.append("Số asset   : %d" % len(manifest))
    report.append("Trang lồng : %d" % len(page_order))
    report.append("")
    report.append("%-38s %-28s %10s" % ("uuid", "mime", "kích thước"))
    report.append("-" * 80)

    n_font = n_img = n_page = 0

    for uuid, entry in manifest.items():
        data = base64.b64decode(entry["data"])
        if entry.get("compressed"):
            try:
                data = gzip.decompress(data)
            except OSError as err:
                print("  ! giải nén hỏng %s: %s" % (uuid, err))

        mime = entry.get("mime", "")
        report.append("%-38s %-28s %10s" % (uuid, mime, human(len(data))))

        # Trang lồng: ghi thành .html riêng, KHÔNG thay uuid trong template
        # (loader dùng marker about:blank#<uuid> chứ không phải blob url).
        if uuid in page_set:
            (OUT / "pages" / (uuid + ".html")).write_bytes(data)
            n_page += 1
            continue

        ext = ext_for(mime)
        (OUT / "res" / ("%s.%s" % (uuid, ext))).write_bytes(data)

        # Trình duyệt nhúng font bằng data: URI vì CSP của artifact host chặn
        # blob:. Trên đĩa thì không cần — trỏ thẳng ra file cho template.html
        # nhẹ và đọc được (14 font dạng base64 làm file phình gấp ~4 lần).
        if FONT_MIME.match(mime or ""):
            n_font += 1
        else:
            n_img += 1

        template = template.replace(uuid, "res/%s.%s" % (uuid, ext))

    # Loader gỡ 2 thuộc tính này vì blob url từ file:// bị SRI chặn.
    template = re.sub(r'\s+integrity="[^"]*"', "", template, flags=re.I)
    template = re.sub(r'\s+crossorigin="[^"]*"', "", template, flags=re.I)

    out_html = OUT / "template.html"
    out_html.write_text(template, encoding="utf-8")

    # Đếm nhanh các màn hình để đối chiếu với plan.
    screens = sorted(set(re.findall(r"\{\{(is[A-Za-z0-9]+)\}\}", template)))
    cyan = len(re.findall(r"#00ADEE|#0099d1", template, re.I))

    report.append("")
    report.append("Cờ màn hình tìm thấy (%d): %s" % (len(screens), ", ".join(screens)))
    report.append("Số chỗ hardcode #00ADEE / #0099d1: %d" % cyan)
    (OUT / "REPORT.txt").write_text("\n".join(report), encoding="utf-8")

    print("")
    print("Xong. Mở %s bằng Chrome để xem mockup gốc đã giải nén." % out_html.name)
    print("  template.html : %s" % human(len(template.encode("utf-8"))))
    print("  font          : %d" % n_font)
    print("  ảnh/khác      : %d" % n_img)
    print("  trang lồng    : %d" % n_page)
    print("  cờ màn hình   : %d  ->  %s" % (len(screens), ", ".join(screens)))
    print("  hardcode cyan : %d chỗ" % cyan)
    print("")
    print("Kết quả nằm ở: %s" % OUT)


if __name__ == "__main__":
    main()
