#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-v3.py — dựng prototype-v3 từ mockup đã giải nén của khách hàng.

Nguyên tắc: KHÔNG chép tay một dòng markup nào. Script cắt nguyên xi từng khối
màn hình ra khỏi `_raw/template.html` (theo số dòng + khớp thẻ <sc-if>), giữ
nguyên runtime của KH, rồi chỉ làm 3 việc:

  1. Đổi GIÁ TRỊ màu (bảng COLORS bên dưới) — không đụng layout, font, spacing.
  2. Thay chữ "Homi365 ●" ở thanh trên bằng logo chính thức.
  3. Cắt thành mỗi màn một file .html, nối với nhau bằng link thật.

Chạy:
    cd D:\\BA\\ProjectBA\\Medigo
    python prototype-v3\\tools\\build-v3.py

Cần chạy `extract-bundle.py` trước. Không cần thư viện ngoài.
"""

import json
import re
import shutil
import sys
from pathlib import Path

# Cập nhật sau UAT 02/10 — xem tools/update_uat0210.py
import update_uat0210 as uat
# Toàn văn 2 chính sách HOMI365 gửi 08/10 (hiệu lực 01/10/2026).
import policy_docs as pdoc

HERE = Path(__file__).resolve().parent          # prototype-v3/tools
V3 = HERE.parent                                 # prototype-v3
ROOT = V3.parent                                 # Medigo/ — để lấy lại nội dung v2
RAW = HERE / "_raw"
SRC = RAW / "template.html"

# ============================================================================
# 1. BẢNG MÀU — chỗ duy nhất cần sửa khi KH đổi ý về màu
# ============================================================================
# Thứ tự QUAN TRỌNG: chuỗi cụ thể phải đứng trước chuỗi tổng quát.

COLORS = [
    # --- Thương hiệu: cyan #00ADEE -> navy #1E3A66 -----------------------
    ("#00ADEE", "#1E3A66"),
    ("#00adee", "#1E3A66"),
    ("#0099d1", "#1B3358"),                       # hover
    ("#0088ba", "#122544"),                       # active
    ("#00728f", "#0F7F96"),                       # chữ badge "Đã duyệt"
    ("rgba(0,173,238,.14)", "rgba(15,127,150,.14)"),   # nền badge -> teal
    ("rgba(0,173,238,", "rgba(30,58,102,"),            # còn lại -> navy
    # --- Nút "Thanh toán" trong mockup KH đang là đỏ #EE0000 nhưng hover
    #     lại là cyan — gần như chắc chắn là lỗi. Đưa về màu chính. -------
    ("#EE0000", "#1E3A66"),
    # --- Xanh lá: thành công --------------------------------------------
    ("#84BE52", "#2F7A48"),
    ("#4c7a2e", "#2F7A48"),
    ("#73aa45", "#2F7A48"),
    ("rgba(132,190,82,", "rgba(47,122,72,"),
    # --- Cam: cảnh báo ---------------------------------------------------
    ("#FFA500", "#965C0A"),
    ("#FBAE40", "#965C0A"),
    ("#FFBC40", "#E0B15F"),
    ("#a36400", "#965C0A"),
    ("rgba(255,165,0,", "rgba(150,92,10,"),
    # --- Đỏ: lỗi ---------------------------------------------------------
    ("#D9342B", "#C0392B"),
    ("#E20707", "#C0392B"),
    ("rgba(217,52,43,", "rgba(192,57,43,"),
    ("rgba(226,7,7,", "rgba(192,57,43,"),
    # --- Xám -------------------------------------------------------------
    ("#1F1F1F", "#2B303A"),
    ("#424242", "#5B6472"),
    ("#414445", "#5B6472"),
    ("#939393", "#8A93A3"),
    ("#AAAAAA", "#C9CED4"),
    ("#5c5c5c", "#5B6472"),
    ("rgba(31,31,31,", "rgba(43,48,58,"),
    ("rgba(170,170,170,", "rgba(154,163,176,"),
    ("rgba(204,204,204,.9)", "rgba(18,37,68,.16)"),     # đổ bóng
    # --- Navy sẵn có trong mockup (sidebar admin) ------------------------
    ("#344557", "#1B3358"),
    ("#2a3745", "#122544"),
    ("rgba(52,69,87,", "rgba(27,51,88,"),
]

# Màu KHÔNG được đổi — logo bên thứ ba trong màn thanh toán.
# Nền trang đổi sang warm-50 của HOMI365, thẻ/card giữ trắng -> section xen kẽ
# ấm / trắng như prototype-v2. Áp TRƯỚC bảng COLORS để giá trị var() không bị
# bảng màu đụng vào.
WARM = "#FAF8F3"
CHART = "#1BA3BE"     # teal-500 — màu cột biểu đồ, tách khỏi navy của nút/link

BG_PATCHES = [
    # (2 mục chèn màn B5/B6 được nối thêm ở cuối file, sau khi markup của
    #  chúng đã được khai báo — xem "BG_PATCHES += [...]" bên dưới.)
    # 7.5.2 — cây tuyến 3 cấp (mockup chỉ vẽ F0 → F1) + khối lịch sử hạng.
    # Lưu ý: dữ liệu `tree` nằm trong JS nên phải vá ở JS_PATCHES, không phải ở
    # đây — BG_PATCHES chỉ chạy trên markup.
    ("Sơ đồ tuyến dưới (2 cấp)", "Sơ đồ tuyến dưới (3 cấp)"),
    ("""              <div style="font-size:13px;padding:var(--s3) var(--s5);margin-left:var(--s8);border-left:2px solid rgba(170,170,170,.35);color:var(--c2)">{{t.name}} — F1 · {{t.orders}} đơn</div>""",
     """              <div style="font-size:13px;padding:var(--s3) var(--s5);margin-left:var(--s8);border-left:2px solid rgba(170,170,170,.35);color:var(--c2)">{{t.name}} — F1 · {{t.orders}} đơn</div>
              <sc-for list="{{t.children}}" as="g" hint-placeholder-count="2">
                <div style="font-size:13px;padding:var(--s3) var(--s5);margin-left:var(--s10);border-left:2px solid rgba(170,170,170,.25);color:var(--c5)">{{g.name}} — F2 · {{g.orders}} đơn</div>
              </sc-for>"""),
    ("""          <div style="font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s5)">Lịch sử đơn hàng &amp; hoa hồng</div>""",
     """          <div style="display:flex;justify-content:space-between;gap:var(--s5);font-size:13px;margin-bottom:var(--s5)">
            <span style="color:var(--c5)">Hạng · Cấp tuyến</span>
            <span style="font-weight:700;color:var(--c1)">{{effRank}} · {{selectedMember.tierLabel}}</span>
          </div>

          <!-- (18) Cập nhật cấp theo phiếu đã duyệt ngoài hệ thống -->
          <button sc-camel-on-click="{{openRankEdit}}" style="width:100%;height:40px;margin-bottom:var(--s3);background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c6)" style-hover="background:rgba(170,170,170,.08)">Cập nhật cấp</button>
          <div style="font-size:11px;color:var(--c5);line-height:1.6;margin-bottom:var(--s6)">Việc trình và duyệt làm ngoài hệ thống. Ở đây chỉ ghi nhận cấp đã được duyệt, kèm số phiếu để đối chiếu.</div>

          <sc-if value="{{hasRankLog}}" hint-placeholder-val="{{false}}">
            <div style="font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s4)">Lịch sử điều chỉnh cấp</div>
            <div style="display:flex;flex-direction:column;gap:var(--s3);font-size:13px;margin-bottom:var(--s7)">
              <sc-for list="{{rankLog}}" as="rl" hint-placeholder-count="2">
                <div style="display:flex;justify-content:space-between;gap:var(--s5);color:var(--c2)"><span>{{rl.label}}</span><span style="color:var(--c5);flex:none">{{rl.time}}</span></div>
              </sc-for>
            </div>
          </sc-if>

          <div style="font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s4)">Chấp thuận điều khoản</div>
          <div style="border:1px solid rgba(47,122,72,.35);background:rgba(132,190,82,.08);border-radius:var(--r-md);padding:var(--s5);display:flex;flex-direction:column;gap:var(--s3);font-size:13px;margin-bottom:var(--s7)">
            <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Phiên bản T&amp;C</span><span style="font-weight:600;font-family:monospace">{{selectedMember.tncVersion}}</span></div>
            <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Thời điểm đồng ý</span><span style="font-weight:600;font-family:monospace">{{selectedMember.tncAt}}</span></div>
            <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Địa chỉ IP</span><span style="font-weight:600;font-family:monospace">{{selectedMember.tncIp}}</span></div>
            <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Định danh</span><span style="color:var(--c2);text-align:right;font-family:monospace">{{selectedMember.tncUser}}</span></div>
            <div style="font-size:11px;color:var(--c5);line-height:1.6">Bằng chứng chấp thuận, phục vụ đối chiếu khi cơ quan thuế kiểm tra hoặc thành viên khiếu nại.</div>
          </div>

          <button sc-camel-on-click="{{toggleProfile}}" style="width:100%;display:flex;align-items:center;justify-content:space-between;gap:var(--s5);background:rgba(170,170,170,.08);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);padding:var(--s5) var(--s6);cursor:pointer;font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s5)" style-hover="background:rgba(170,170,170,.15)"><span>Thông tin hồ sơ</span><span style="font-size:14px;color:var(--c6)">{{profileCaret}}</span></button>

          <sc-if value="{{profileOpen}}" hint-placeholder-val="{{true}}">
          <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);padding:var(--s6);margin-bottom:var(--s7);display:flex;flex-direction:column;gap:var(--s4)">
            <sc-if value="{{profileRead}}" hint-placeholder-val="{{true}}">
              <div style="display:flex;flex-direction:column;gap:var(--s3);font-size:13px">
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Họ và tên</span><span style="font-weight:600;text-align:right">{{selectedMember.name}}</span></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Số điện thoại</span><span style="font-weight:600;font-family:monospace">{{selectedMember.phone}}</span></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Email</span><span style="color:var(--c2);text-align:right">{{selectedMember.email}}</span></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Số CCCD</span><span style="color:var(--c2);font-family:monospace">{{selectedMember.cccd}}</span></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Ngày cấp · Nơi cấp</span><span style="color:var(--c2);text-align:right">{{selectedMember.cccdIssue}}</span></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Ngày sinh · Giới tính</span><span style="color:var(--c2);text-align:right">{{selectedMember.dobGender}}</span></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Địa chỉ</span><span style="color:var(--c2);text-align:right;max-width:60%">{{selectedMember.address}}</span></div>
                <div style="height:1px;background:rgba(170,170,170,.25);margin:var(--s2) 0"></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Ngân hàng</span><span style="color:var(--c2);text-align:right">{{selectedMember.bank}}</span></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Số tài khoản</span><span style="font-weight:600;font-family:monospace">{{selectedMember.bankAccount}}</span></div>
                <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5);flex:none">Tên chủ tài khoản</span><span style="font-weight:600;text-align:right">{{selectedMember.bankHolder}}</span></div>
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s5)">
                <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);padding:var(--s6);text-align:center;background:rgba(170,170,170,.05)"><div style="font-size:22px;color:var(--c5)">&#128196;</div><div style="font-size:11px;color:var(--c2);font-family:monospace;margin-top:var(--s2)">{{selectedMember.cccdFront}}</div><div style="font-size:10px;color:var(--c5)">Mặt trước</div></div>
                <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);padding:var(--s6);text-align:center;background:rgba(170,170,170,.05)"><div style="font-size:22px;color:var(--c5)">&#128196;</div><div style="font-size:11px;color:var(--c2);font-family:monospace;margin-top:var(--s2)">{{selectedMember.cccdBack}}</div><div style="font-size:10px;color:var(--c5)">Mặt sau</div></div>
              </div>
              <button sc-camel-on-click="{{startProfileEdit}}" style="height:38px;background:var(--c12);border:1px solid var(--c6);border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c6)" style-hover="background:rgba(0,173,238,.06)">Sửa hồ sơ</button>
            </sc-if>

            <sc-if value="{{profileEdit}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:var(--c2);background:rgba(255,165,0,.12);border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">Admin sửa hộ khi thành viên khai sai — ví dụ sai số tài khoản. Mọi thay đổi được ghi vào lịch sử hồ sơ.</div>
              <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;font-weight:600;color:var(--c2)">Họ và tên</label><input type="text" value="{{pfName}}" sc-camel-on-change="{{setPfName}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px"></div>
              <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;font-weight:600;color:var(--c2)">Số điện thoại</label><input type="text" value="{{pfPhone}}" sc-camel-on-change="{{setPfPhone}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-family:monospace"></div>
              <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;font-weight:600;color:var(--c2)">Email</label><input type="text" value="{{pfEmail}}" sc-camel-on-change="{{setPfEmail}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px"></div>
              <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;font-weight:600;color:var(--c2)">Số CCCD</label><input type="text" value="{{pfCccd}}" sc-camel-on-change="{{setPfCccd}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-family:monospace"></div>
              <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;font-weight:600;color:var(--c2)">Ngày sinh</label><input type="text" value="{{pfDob}}" sc-camel-on-change="{{setPfDob}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px"></div>
              <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;font-weight:600;color:var(--c2)">Địa chỉ</label><input type="text" value="{{pfAddress}}" sc-camel-on-change="{{setPfAddress}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px"></div>
              <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;font-weight:600;color:var(--c2)">Số tài khoản</label><input type="text" value="{{pfBankAccount}}" sc-camel-on-change="{{setPfBankAccount}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-family:monospace"></div>
              <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;font-weight:600;color:var(--c2)">Tên chủ tài khoản</label><input type="text" value="{{pfBankHolder}}" sc-camel-on-change="{{setPfBankHolder}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;text-transform:uppercase"></div>
              <div style="display:flex;gap:var(--s4)">
                <button sc-camel-on-click="{{cancelProfileEdit}}" style="flex:1;height:40px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c2)">Huỷ</button>
                <button sc-camel-on-click="{{saveProfileEdit}}" style="flex:1;height:40px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Lưu hồ sơ</button>
              </div>
            </sc-if>
          </div>
          </sc-if>

          <div style="font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s5)">Lịch sử thăng/giáng hạng</div>
          <div style="display:flex;flex-direction:column;gap:var(--s3);font-size:13px;margin-bottom:var(--s7)">
            <sc-for list="{{selectedMember.rankHistory}}" as="rh" hint-placeholder-count="2">
              <div style="display:flex;justify-content:space-between;gap:var(--s5);color:var(--c2)"><span>{{rh.label}}</span><span style="color:var(--c5);flex:none">{{rh.time}}</span></div>
            </sc-for>
          </div>
          <div style="font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s5)">Lịch sử đơn hàng &amp; hoa hồng</div>"""),

    # C1 — tiêu đề nói thẳng mục đích, bỏ dòng phụ trùng ý.
    ('<div style="font-size:22px;font-weight:700;color:var(--c1)">Đăng nhập thành viên'
     '</div><div style="font-size:13px;color:var(--c5);margin-top:var(--s2)">'
     'Đăng nhập để quản lý hoa hồng &amp; đơn hàng của bạn</div>',
     '<div style="font-size:22px;font-weight:700;color:var(--c1);line-height:1.4">'
     'Đăng nhập để quản lý hoa hồng &amp; đơn hàng của bạn</div>'),

    # C1 — luồng 2 bước: nhập SĐT trước, hệ thống kiểm tra rồi mới hiện ô mật
    # khẩu; SĐT chưa đăng ký thì chuyển thẳng sang màn đăng ký Agent.
    # Ô mật khẩu chỉ hiện sau khi SĐT được xác nhận là đã có tài khoản.
    ("""            <div style="display:flex;flex-direction:column;gap:var(--s2)">
              <div style="display:flex;justify-content:space-between;align-items:center"><label style="font-size:14px;font-weight:600;color:var(--c2)">Mật khẩu</label><a href="#" sc-camel-on-click="{{openForgotPassword}}" style="font-size:12px;font-weight:600;color:var(--c6);text-decoration:none">Quên mật khẩu?</a></div>""",
     """            <sc-if value="{{loginPhoneChecked}}" hint-placeholder-val="{{true}}">
            <div style="display:flex;flex-direction:column;gap:var(--s2)">
              <div style="display:flex;justify-content:space-between;align-items:center"><label style="font-size:14px;font-weight:600;color:var(--c2)">Mật khẩu</label><a href="#" sc-camel-on-click="{{openForgotPassword}}" style="font-size:12px;font-weight:600;color:var(--c6);text-decoration:none">Quên mật khẩu?</a></div>"""),

    # Đóng sc-if của khối mật khẩu + đổi nút theo bước, bỏ dòng mô tả và nút
    # "Đăng ký giới thiệu thành viên mới".
    ("""            </div>
            <sc-if value="{{agentLoginError}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:var(--err);background:rgba(217,52,43,.08);border-radius:var(--r-sm);padding:var(--s4)">Số điện thoại hoặc mật khẩu không đúng. Vui lòng xác thực lại số điện thoại của bạn.</div>
            </sc-if>
            <button sc-camel-on-click="{{agentLoginSubmit}}" style="height:46px;background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);font-size:16px;font-weight:600;box-shadow:var(--sh)" style-hover="background:#0099d1">Đăng nhập</button>
            <div style="font-size:13px;color:var(--c5);text-align:center;line-height:1.6">Chưa có tài khoản? <br><a href="#" sc-camel-on-click="{{openOrderLookup}}" style="color: var(--c6); font-weight: 600; text-decoration: none;">Đăng ký giới thiệu thành viên mới</a></div>""",
     """            </div>
            </sc-if>
            <sc-if value="{{agentLoginError}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:var(--err);background:rgba(217,52,43,.08);border-radius:var(--r-sm);padding:var(--s4)">Số điện thoại hoặc mật khẩu không đúng. Vui lòng xác thực lại số điện thoại của bạn.</div>
            </sc-if>
            <sc-if value="{{loginPhoneEmpty}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:var(--err);background:rgba(217,52,43,.08);border-radius:var(--r-sm);padding:var(--s4)">Vui lòng nhập số điện thoại.</div>
            </sc-if>
            <sc-if value="{{loginNotEligible}}" hint-placeholder-val="{{false}}">
              <div style="display:flex;gap:var(--s3);align-items:flex-start;font-size:13px;color:var(--err);background:rgba(217,52,43,.08);border-radius:var(--r-sm);padding:var(--s5);line-height:1.6"><span style="flex:none;font-weight:700">&#10005;</span><span>Bạn chưa đạt điều kiện đăng nhập thành viên. Số điện thoại này chưa gắn với đơn hàng nào — vui lòng mua sản phẩm qua link giới thiệu trước.</span></div>
            </sc-if>
            <sc-if value="{{loginPhoneUnchecked}}" hint-placeholder-val="{{false}}">
              <button sc-camel-on-click="{{checkLoginPhone}}" style="height:46px;background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);font-size:16px;font-weight:600;box-shadow:var(--sh)" style-hover="background:#0099d1">Tiếp tục</button>
            </sc-if>
            <sc-if value="{{loginPhoneChecked}}" hint-placeholder-val="{{true}}">
              <button sc-camel-on-click="{{agentLoginSubmit}}" style="height:46px;background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);font-size:16px;font-weight:600;box-shadow:var(--sh)" style-hover="background:#0099d1">Đăng nhập</button>
            </sc-if>"""),

    # A2 bước 5 — chốt 09/09: CHỈ MỘT link. Mã giới thiệu chính là alias
    # (viết tắt họ tên + 4 số cuối SĐT), link là homi365.com.vn/<alias>.
    ('<div style="font-size:12px;color:var(--c5);text-transform:uppercase;'
     'letter-spacing:.04em">Mã giới thiệu (aff_id)</div>',
     '<div style="font-size:12px;color:var(--c5);text-transform:uppercase;'
     'letter-spacing:.04em">Mã thành viên của bạn</div>'),
    ('<div style="font-size:30px;font-weight:900;color:var(--c1);'
     'letter-spacing:.02em">923983</div>',
     '<div style="font-size:30px;font-weight:900;color:var(--c1);'
     'letter-spacing:.02em">{{refCode}}</div>'),
    ('<div style="font-size:13px;color:var(--c4);word-break:break-all;'
     'background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s4)">'
     'homi365.vn/san-pham/CN02?aff_id=923983</div>',
     '<div style="font-size:13px;color:var(--c4);word-break:break-all;'
     'background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s4)">'
     '{{refLink}}</div>'),
    # A3 thiếu hẳn link bán hàng — agent rời màn "kích hoạt thành công" là mất
    # đường lấy link. Chèn một thẻ link + nút copy ngay dưới phần chào.
    # copyLink / copyLabel đã có sẵn trong renderVals nên dùng lại được.
    ("""{{agentStageToggleLabel}}</button>
      </div>
""",
     """{{agentStageToggleLabel}}</button>
      </div>

      <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s6)">
        <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Link bán hàng của bạn</div>

        <div style="display:flex;flex-direction:column;gap:var(--s3)">
          <div style="display:flex;gap:var(--s3);align-items:center">
            <div style="flex:1;min-width:0;font-size:13px;color:var(--c4);word-break:break-all;background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s4)">{{refLink}}</div>
            <button sc-camel-on-click="{{copyLink}}" style="flex:none;height:40px;padding:0 var(--s6);background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600" style-hover="background:#0099d1">{{copyLabel}}</button>
          </div>
        </div>
      </div>

      <div style="display:flex;flex-direction:column;gap:var(--s4)">
        <div style="display:flex;gap:var(--s2);flex-wrap:wrap;align-items:center">
          <span style="font-size:12px;color:var(--c5);margin-right:var(--s2)">Số đơn theo</span>
          <sc-for list="{{orderRanges}}" as="r" hint-placeholder-count="5">
            <button sc-camel-on-click="{{r.onClick}}" style="{{r.style}}">{{r.label}}</button>
          </sc-for>
        </div>
        <sc-if value="{{isCustomRange}}" hint-placeholder-val="{{false}}">
          <div style="display:flex;gap:var(--s3);align-items:center;flex-wrap:wrap">
            <input type="date" style="height:38px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:13px;color:var(--c2);background:var(--c12)">
            <span style="font-size:13px;color:var(--c5)">đến</span>
            <input type="date" style="height:38px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:13px;color:var(--c2);background:var(--c12)">
            <button style="height:38px;padding:0 var(--s6);background:var(--c6);border:none;border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Áp dụng</button>
          </div>
        </sc-if>
      </div>
"""),
    # A3: tách hoa hồng thành 4 trạng thái (đã ghi nhận / chờ duyệt · tạm giữ /
    # đã rút / khả dụng) thay vì chỉ 2 con số, và nói rõ cơ chế hold.
    ("""        <div style="display:flex;justify-content:space-between;gap:var(--s5)">
          <div><div style="font-size:12px;color:var(--c6);font-weight:600">Số dư khả dụng</div><div style="font-size:26px;font-weight:900;color:var(--c6)">{{availableBalanceLabel}}</div></div>
          <div style="text-align:right"><div style="font-size:12px;color:var(--c5)">Đang chờ duyệt (đã khóa)</div><div style="font-size:15px;font-weight:700;color:var(--c2)">{{pendingBalanceLabel}}</div></div>
        </div>
        <div style="font-size:11px;color:var(--c5)">Đã ghi nhận: {{earnedBalanceLabel}} · số tiền đang chờ/đã duyệt sẽ tạm khóa khỏi số dư khả dụng.</div>""",
     """        <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s5)">
          <div><div style="font-size:12px;color:var(--c5)">Đã ghi nhận</div><div style="font-size:18px;font-weight:700;color:var(--c2)">{{earnedBalanceLabel}}</div></div>
          <div style="text-align:right"><div style="font-size:12px;color:var(--c5)">Đang chờ duyệt · tạm giữ</div><div style="font-size:18px;font-weight:700;color:var(--c9)">{{pendingBalanceLabel}}</div></div>
          <div><div style="font-size:12px;color:var(--c5)">Đã rút</div><div style="font-size:18px;font-weight:700;color:var(--c2)">{{metricWithdrawn}}</div></div>
          <div style="text-align:right"><div style="font-size:12px;color:var(--c6);font-weight:600">Số dư khả dụng</div><div style="font-size:26px;font-weight:900;color:var(--c6)">{{availableBalanceLabel}}</div></div>
        </div>
        <div style="font-size:11px;color:var(--c5);border-top:1px solid rgba(170,170,170,.35);padding-top:var(--s4);line-height:1.6">Yêu cầu rút tiền đang ở trạng thái <strong>chờ duyệt</strong> hoặc <strong>đã duyệt</strong> sẽ được tạm giữ và trừ khỏi số dư khả dụng, cho tới khi chi trả xong hoặc bị từ chối. Bị từ chối thì tiền hoàn lại số dư khả dụng.</div>"""),
    # Cột biểu đồ hoa hồng (A3): dùng teal thay màu chính.
    ("border-radius:var(--r-sm) var(--r-sm) 0 0;background:var(--c6)",
     "border-radius:var(--r-sm) var(--r-sm) 0 0;background:var(--c-chart)"),
    # Chốt 09/09 — agent đăng ký xong ACTIVE ngay, bán được qua link, nhưng
    # hoa hồng bị tạm giữ và chưa tính điểm cho tới khi admin kích hoạt.
    # (2 mục này phải đứng TRƯỚC bản vá "Medigo" bên dưới vì neo còn chữ cũ.)
    ('<div style="font-size:24px;font-weight:700">Kích hoạt thành công</div>'
     '<div style="font-size:13px;color:var(--c5);margin-top:var(--s2)">'
     'Bạn đã chính thức là seller Medigo</div>',
     '<div style="font-size:24px;font-weight:700">Đăng ký thành công</div>'
     '<div style="font-size:13px;color:var(--c5);margin-top:var(--s2);line-height:1.8">'
     'HOMI365 đã nhận được đăng ký từ bạn.<br>'
     'Ngay lập tức, bạn có thể giới thiệu khách hàng tham gia sản phẩm.<br>'
     'Điểm thưởng và ưu đãi sẽ tạm giữ cho tới khi Quản trị viên kích hoạt '
     'thành công.</div>'),

    ('<div style="font-size:13px;color:var(--c2);background:rgba(255,165,0,.14);'
     'border-radius:var(--r-md);padding:var(--s5)">Chào mừng bạn đến với Medigo! '
     'Hoa hồng của bạn sẽ được tính toán sau khi đơn hàng hoàn tất. '
     'Theo dõi số liệu tại đây.</div>',
     '<div style="border:1px solid rgba(255,165,0,.35);background:rgba(255,165,0,.1);'
     'border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;'
     'gap:var(--s5)">\n'
     '        <div style="display:flex;align-items:center;gap:var(--s3);flex-wrap:wrap">'
     '<span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);'
     'font-size:11px;font-weight:700;background:rgba(255,165,0,.2);color:#a36400">'
     'CHỜ KÍCH HOẠT</span>'
     '<span style="font-size:13px;font-weight:600;color:var(--c1)">'
     'Tài khoản đang chờ quản trị viên kích hoạt</span></div>\n'
     '        <div style="font-size:13px;color:var(--c2);line-height:1.7">'
     'Bạn <strong>giới thiệu khách hàng được ngay</strong> qua link trên, tuy nhiên '
     '<strong>Điểm thưởng và ưu đãi sẽ tạm giữ</strong> cho tới khi Quản trị viên '
     'kích hoạt thành công.</div>\n'
     '        <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s5);'
     'border-top:1px solid rgba(255,165,0,.3);padding-top:var(--s5)">'
     '<div><div style="font-size:12px;color:var(--c5)">Hoa hồng đang tạm giữ</div>'
     '<div style="font-size:22px;font-weight:800;color:#a36400">'
     '{{heldCommissionLabel}}</div></div>'
     '<div style="text-align:right"><div style="font-size:12px;color:var(--c5)">'
     'Số dư khả dụng</div>'
     '<div style="font-size:22px;font-weight:800;color:var(--c5)">0đ</div></div></div>\n'
     '        <button disabled="{{true}}" style="height:44px;border:none;'
     'border-radius:var(--r-md);font-size:14px;font-weight:600;color:#FFFFFF;'
     'background:rgba(170,170,170,.5);cursor:not-allowed">'
     'Chưa thể rút tiền — chờ kích hoạt</button>\n'
     '      </div>'),

    # Kích hoạt = mở khoá tiền. Nói rõ trong hộp xác nhận là sẽ giải phóng
    # toàn bộ hoa hồng và điểm đã tạm giữ, cộng dồn về quá khứ (chốt 09/09).
    ('<div style="font-size:14px;color:var(--c2);line-height:1.6">Xác nhận duyệt '
     'hồ sơ đăng ký của <strong>{{actionMember.name}}</strong> '
     '({{actionMember.affId}})?</div>',
     '<div style="font-size:14px;color:var(--c2);line-height:1.6">Xác nhận duyệt '
     'hồ sơ đăng ký của <strong>{{actionMember.name}}</strong> '
     '({{actionMember.affId}})?</div>\n'
     '          <div style="font-size:12px;color:var(--c2);background:'
     'rgba(132,190,82,.12);border-radius:var(--r-md);padding:var(--s5);'
     'line-height:1.7">Đủ 2 lượt duyệt là tài khoản được kích hoạt: toàn bộ '
     '<strong>hoa hồng đang tạm giữ</strong> và <strong>điểm tích luỹ</strong> '
     'của thành viên được <strong>cộng dồn về quá khứ</strong> — tính từ đơn '
     'đầu tiên, không phải từ thời điểm kích hoạt — và mở khoá cho rút tiền.</div>'),

    # Còn sót tên "Medigo" trong sản phẩm đã re-skin sang HOMI365 (T&C, câu
    # chúc mừng ở A2, lời chào ở A3, tiêu đề đăng nhập quản trị).
    ("Medigo", "HOMI365"),

    # Nhãn bước sai: luồng đăng ký có 5 bước chứ không phải 3.
    ("Bước 1/3 · Thông tin cá nhân", "Bước 1/5 · Thông tin cá nhân"),

    # 7.3.3 AC — thêm dòng "còn thiếu N đơn để lên hạng" dưới ô Hạng hiện tại.
    ('<div style="font-size:12px;color:var(--c5)">Hạng hiện tại</div>'
     '<div style="font-size:24px;font-weight:700;color:var(--c1)">{{metricRank}}</div>',
     '<div style="font-size:12px;color:var(--c5)">Hạng hiện tại</div>'
     '<div style="font-size:24px;font-weight:700;color:var(--c1)">{{metricRank}}</div>'
     '<div style="font-size:11px;font-weight:600;color:var(--c6);line-height:1.5">'
     '{{rankProgress}}</div>'),

    # A1 + C1: nền xám nhạt -> nền ấm
    ("background:rgba(170,170,170,.05)", "background:var(--warm-50)"),
    # Thẻ chỉ có viền, không khai báo nền: trên nền trắng của mockup thì không
    # thấy, nhưng trên nền ấm mới sẽ bị chìm -> cho về trắng để nổi khối.
    ('style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg)',
     'style="background:var(--c12);border:1px solid rgba(170,170,170,.35);'
     'border-radius:var(--r-lg)'),
    # A3: đang để trắng -> nền ấm cho các thẻ nổi lên
    ("padding:0 var(--s7) var(--s11);background:var(--c12)",
     "padding:0 var(--s7) var(--s11);background:var(--warm-50)"),
]

# ---------------------------------------------------------------------------
# Bổ sung ngoài mockup KH (yêu cầu 08/09): màn Quản lý sản phẩm và chức năng
# Thêm hàng vào kho. Viết bằng đúng style inline của mockup để không lệch tông.
# Dùng màu gốc (#00ADEE, rgba(170,...)) để bảng COLORS xử lý như mọi chỗ khác.
# ---------------------------------------------------------------------------

_INP = ('height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
        'border-radius:var(--r-md);font-size:14px')
_FOCUS = 'border-color:#00ADEE;box-shadow:0 0 0 3px rgba(0,173,238,.25)'
_BTN_PRIMARY = ('height:38px;padding:0 var(--s6);background:var(--c6);border:none;'
                'border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c12)')
_BTN_GHOST = ('height:38px;padding:0 var(--s6);background:var(--c12);'
              'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);'
              'font-size:13px;font-weight:600;color:var(--c2)')


# Điều khoản & Điều kiện chương trình thành viên — dựng thành một trang chính
# sách độc lập, có địa chỉ cố định và số hiệu phiên bản, để còn trích dẫn được
# khi thành viên khiếu nại hoặc cơ quan thuế kiểm tra. Nội dung trùng với văn
# bản hiển thị ở bước 4 của form đăng ký.
TNC_POLICY_JS = """

/* --- Bổ sung 10/09: Điều khoản & Điều kiện chương trình thành viên --------
   Đặt lên đầu danh mục vì đây là văn bản thành viên phải đồng ý khi đăng ký.
   Các con số bỏ trống chờ bộ phận Pháp lý và khách hàng chốt.            */
POLICIES.unshift({
  id: 'dieu-khoan-thanh-vien',
  title: 'Điều khoản & Điều kiện chương trình thành viên',
  intro: 'Phiên bản 1.0 · hiệu lực từ …/…/2026. Văn bản này điều chỉnh quan hệ giữa Công ty Cổ phần Giải pháp và Dịch vụ HOMI365 và Thành viên tham gia chương trình giới thiệu khách hàng. Thành viên xác nhận đồng ý với toàn bộ nội dung dưới đây trước khi tài khoản được kích hoạt.',
  sections: [
    { h: '1. Điểm thưởng là gì', items: [
      'Điểm thưởng (sau đây gọi là Điểm HOMI) là đơn vị quy ước nội bộ do HOMI365 phát hành, ghi nhận đóng góp của Thành viên trong việc giới thiệu khách hàng.',
      { list: [
        'Điểm HOMI không phải là tiền tệ và không có giá trị thanh toán ngoài hệ thống HOMI365.',
        'Điểm HOMI không được mua bán, tặng cho hay chuyển nhượng giữa các Thành viên.',
        'Điểm HOMI không được quy đổi thành tiền mặt ngoài cơ chế đổi thưởng quy định tại Mục 3.'
      ] }
    ] },
    { h: '2. Quy chế tích điểm', items: [
      'Điểm được ghi nhận khi đơn hàng phát sinh qua link giới thiệu của Thành viên và được HOMI365 xác nhận thanh toán thành công.',
      { list: [
        'Tỷ lệ quy đổi: ………… VNĐ giá trị đơn hàng tương ứng 1 Điểm HOMI.',
        'Điểm chỉ được cộng vào tài khoản sau khi Thành viên đã được kích hoạt.',
        'Các đơn hàng phát sinh trước thời điểm kích hoạt vẫn được ghi nhận và cộng bù đầy đủ, tính từ đơn đầu tiên.',
        'Đơn hàng bị huỷ hoặc hoàn tiền sẽ bị thu hồi số điểm tương ứng.'
      ] }
    ] },
    { h: '3. Quy chế tiêu điểm và đổi thưởng', items: [
      { list: [
        'Tỷ lệ quy đổi: 1 Điểm HOMI tương ứng ………… VNĐ.',
        'Yêu cầu quy đổi được xử lý theo quy trình duyệt nội bộ và chi trả vào tài khoản ngân hàng Thành viên đã đăng ký.',
        'Mỗi Thành viên được gửi tối đa 01 yêu cầu quy đổi trong một tháng.',
        'Điểm có thời hạn ………… tháng kể từ ngày ghi nhận. Quá thời hạn mà không quy đổi thì điểm tự động hết hiệu lực và không được khôi phục.'
      ] },
      'Thông tin tài khoản nhận tiền do Thành viên khai báo. Trường hợp khai sai dẫn tới chuyển nhầm, Thành viên chịu trách nhiệm phối hợp xử lý với ngân hàng.'
    ] },
    { h: '4. Quyền thay đổi thể lệ', items: [
      'HOMI365 có quyền điều chỉnh, tạm ngừng hoặc chấm dứt chương trình, bao gồm tỷ lệ tích điểm, tỷ lệ quy đổi và điều kiện xếp hạng.',
      { list: [
        'Mọi thay đổi được thông báo qua email và trên hệ thống trước tối thiểu ………… ngày so với ngày có hiệu lực.',
        'Điểm đã tích trước thời điểm thay đổi được bảo lưu theo thể lệ cũ.',
        'Mỗi lần thay đổi sẽ phát hành một phiên bản Điều khoản mới; phiên bản cũ được lưu trữ để đối chiếu.'
      ] }
    ] },
    { h: '5. Bảo mật và xử lý dữ liệu cá nhân', items: [
      'Thành viên đồng ý để HOMI365 thu thập và xử lý dữ liệu cá nhân gồm họ tên, số điện thoại, email, số CCCD, ngày cấp và nơi cấp, địa chỉ, ảnh chụp CCCD và thông tin tài khoản ngân hàng.',
      { list: [
        'Mục đích: vận hành chương trình, chi trả ưu đãi và thực hiện nghĩa vụ thuế theo pháp luật Việt Nam.',
        'Dữ liệu được lưu trữ có mã hoá; chỉ nhân sự được phân quyền mới có quyền truy cập.',
        'Không chuyển giao cho bên thứ ba, trừ trường hợp pháp luật yêu cầu.',
        'Thành viên có quyền yêu cầu tra cứu, chỉnh sửa hoặc xoá dữ liệu bằng cách liên hệ hotline 1900 633 570.'
      ] }
    ] },
    { h: '6. Chấm dứt tư cách Thành viên', items: [
      'HOMI365 có quyền khoá tài khoản và thu hồi điểm chưa quy đổi nếu phát hiện hành vi gian lận, tạo đơn khống, mạo danh hoặc vi phạm pháp luật.',
      'Thành viên có thể chủ động chấm dứt tham gia bằng văn bản. Điểm chưa quy đổi tại thời điểm chấm dứt sẽ hết hiệu lực.'
    ] },
    { h: '7. Ghi nhận việc chấp thuận', items: [
      'Khi Thành viên xác nhận đồng ý, hệ thống lưu lại: định danh Thành viên, thời điểm chấp thuận chính xác tới giây, số hiệu phiên bản Điều khoản và địa chỉ IP của thiết bị.',
      'Bản ghi này chỉ được thêm mới, không sửa và không xoá, dùng làm căn cứ đối chiếu khi có khiếu nại hoặc khi cơ quan quản lý kiểm tra.'
    ] }
  ]
});
"""


# ---------------------------------------------------------------------------
# Lớp responsive.
#
# Mockup KH viết toàn bộ style inline, không có class nào để bám. Muốn ghi đè
# thì chỉ còn hai đường: sửa từng chuỗi style (hàng trăm chỗ, dễ vỡ neo của các
# bảng vá khác), hoặc nhắm bằng selector thuộc tính [style*="…"] kèm !important.
# Chọn cách thứ hai — không đụng một ký tự nào vào markup KH.
#
# Nguyên tắc: KHÔNG đổi bố cục ở màn rộng. Mọi quy tắc dưới đây đều nằm trong
# media query, nên bản desktop mà KH đã duyệt giữ nguyên từng pixel.
#
# Điểm gãy: 900 khung quản trị & 2 cột · 720 thanh trên · 640 điện thoại.
#
# BẪY đã kiểm chứng trên bản deploy: runtime DC ghi lại style bằng
# el.style.cssText nên trình duyệt chuẩn hoá chuỗi — "grid-template-columns:1fr
# 1fr;gap:var(--s7)" trong file nguồn trở thành "grid-template-columns: 1fr 1fr;
# gap: var(--s7);" trong DOM, và ".8fr" thành "0.8fr". Selector phải viết theo
# dạng ĐÃ CHUẨN HOÁ. Vẫn giữ thêm dạng gốc (không khoảng trắng) cho những phần
# nằm ngoài <x-dc> mà runtime không đụng tới.
def _dual(*pats):
    """Selector [style*=…] cho cả dạng gốc lẫn dạng runtime đã chuẩn hoá."""
    return ",\n".join('[style*="%s"]' % p for p in pats)


SEL_A1_GRID = _dual("grid-template-columns:1fr 380px",
                    "grid-template-columns: 1fr 380px")
SEL_FORM_PAIR = _dual("grid-template-columns:1fr 1fr;gap:var(--s7)",
                      "grid-template-columns: 1fr 1fr; gap: var(--s7)")
SEL_ADMIN = _dual("grid-template-columns:220px 1fr",
                  "grid-template-columns: 220px 1fr")
SEL_CARDS4 = _dual("grid-template-columns:repeat(4,1fr)",
                   "grid-template-columns: repeat(4, 1fr)")
SEL_CARDS3 = _dual("grid-template-columns:repeat(3,1fr)",
                   "grid-template-columns: repeat(3, 1fr)")
SEL_DRAWER = _dual("width:420px;max-width:92vw", "width: 420px; max-width: 92vw",
                   "width:470px;max-width:92vw", "width: 470px; max-width: 92vw",
                   "width:460px;max-width:92vw", "width: 460px; max-width: 92vw")


def _admin_child(child, decls):
    """Quy tắc cho con trực tiếp của khung quản trị, nhân cho cả 2 dạng selector."""
    return ",\n".join("%s %s" % (s, child) for s in SEL_ADMIN.split(",\n")) \
        + " {\n" + decls + "\n}"


RESPONSIVE_CSS = ("""/* ============================================================
   HOMI365 · prototype-v3 — lớp responsive
   Sinh tự động bởi tools/build-v3.py — đừng sửa tay,
   sửa RESPONSIVE_CSS trong script rồi chạy lại.

   Toàn bộ quy tắc nằm trong media query: màn >=1025px giữ nguyên
   bố cục desktop KH đã duyệt. Dùng [style*="…"] + !important vì
   markup gốc không có class để bám.
   ============================================================ */

img { max-width: 100%; }

/* --- Thanh trên -------------------------------------------------------- */
/* Logo 71px cao = 174px ngang, cộng nút đăng nhập ~230px là 404px — tràn mọi
   điện thoại. Dưới 720px cho nút xuống hàng riêng và chiếm trọn bề ngang. */
@media (max-width: 720px) {
  .homi-topbar { padding-left: var(--s5) !important; padding-right: var(--s5) !important; }
  .homi-topbar-in { flex-wrap: wrap; gap: var(--s4); }
  .homi-logo img { height: 40px !important; }
  .homi-login {
    margin-left: 0 !important;
    width: 100%;
    justify-content: center;
    white-space: normal !important;
    height: auto !important;
    min-height: 40px;
    padding: var(--s3) var(--s5) !important;
    text-align: center;
  }
  /* (08/10) A1: ô SĐT trên header xuống hàng, chiếm trọn bề ngang. */
  .homi-buyphone { margin-left: 0 !important; width: 100%; flex-wrap: wrap; }
  .homi-buyphone-lbl { max-width: none !important; width: 100%; margin-right: 0 !important; }
  .homi-buyphone-ok { white-space: normal !important; position: static !important; }
  .homi-buyphone > .homi-buyphone-in { flex: 1; }
  .homi-buyphone input { width: 100% !important; }
}
@media (max-width: 420px) {
  .homi-logo img { height: 34px !important; }
}

/* --- Bố cục hai cột của màn công khai ---------------------------------- */
@media (max-width: 900px) {
  /* A1: form nhận hàng | tóm tắt đơn 380px */
""" + SEL_A1_GRID + """ { grid-template-columns: 1fr !important; }
  /* Footer: khối pháp nhân | cột chính sách */
  .footer-grid { grid-template-columns: 1fr !important; gap: var(--s7) !important; }
}

/* --- Cặp ô nhập trong form (A1, A2) ------------------------------------ */
/* Chỉ nhắm cặp dùng gap:var(--s7) — đó là các hàng ô nhập. Cặp dùng
   gap:var(--s5) là thẻ số liệu trong cột hẹp 430px của A3 và trong ngăn
   chi tiết quản trị; hai cột ở đó vẫn đọc tốt trên điện thoại nên để yên. */
@media (max-width: 640px) {
""" + SEL_FORM_PAIR + """ { grid-template-columns: 1fr !important; }
}

/* --- Khung quản trị B2…B7 ---------------------------------------------- */
/* Cột điều hướng dọc 220px -> dải nút ngang cuộn được, đặt ngay dưới thanh
   trên. Hai nhãn nhóm ("Vận hành", "Vai trò (demo)") bị ẩn vì nằm ngang thì
   chúng chỉ chiếm chỗ mà không thêm nghĩa. */
@media (max-width: 900px) {
""" + SEL_ADMIN + """ {
  grid-template-columns: 1fr !important;
  min-height: 0 !important;
}
""" + _admin_child("> div:first-child",
                   "  flex-direction: row !important;\n"
                   "  align-items: center;\n"
                   "  gap: var(--s2) !important;\n"
                   "  padding: var(--s3) var(--s5) !important;\n"
                   "  overflow-x: auto;\n"
                   "  -webkit-overflow-scrolling: touch;") + """
""" + _admin_child("> div:first-child sc-for", "  display: contents;") + """
""" + _admin_child("> div:first-child button",
                   "  flex: none;\n  white-space: nowrap;") + """
""" + _admin_child("> div:first-child > div:first-child",
                   "  display: none !important;") + """
""" + _admin_child("> div:first-child > div:last-child",
                   "  margin-top: 0 !important;\n"
                   "  padding-top: 0 !important;\n"
                   "  border-top: 0 !important;\n"
                   "  flex-direction: row !important;\n"
                   "  align-items: center;\n"
                   "  flex: none;") + """
""" + _admin_child("> div:first-child > div:last-child > div",
                   "  display: none !important;") + """
""" + _admin_child("> div:last-child",
                   "  padding: var(--s7) var(--s5) !important;") + """

  /* Thẻ tổng hợp trên đầu bảng */
""" + SEL_CARDS4 + """ { grid-template-columns: repeat(2, 1fr) !important; }
}
@media (max-width: 640px) {
""" + SEL_CARDS4 + """,
""" + SEL_CARDS3 + """ { grid-template-columns: 1fr !important; }
}

/* Bảng lưới của B2/B3/B4/B6 vẫn cuộn ngang trong khung overflow:auto của nó —
   cố ép về một cột thì các con số dính vào nhau, đọc còn khó hơn vuốt ngang. */

/* B5 (sản phẩm) và B7 (tài khoản admin) dựng bằng <table> thật, khung bọc để
   overflow:hidden. Ở màn hẹp trình duyệt bóp cột đến mức cột "Mô tả" xuống
   dòng mỗi chữ một hàng. Cho khung cuộn ngang và đặt bề ngang tối thiểu, xử
   lý giống các bảng còn lại. */
@media (max-width: 900px) {
""" + _admin_child("table", "  min-width: 620px !important;") + """
""" + _admin_child("div:has(> table)", "  overflow-x: auto !important;") + """
}

/* --- Ô nhập OTP (A2 bước 2, C1 xác thực & quên mật khẩu) --------------- */
/* 6 ô cố định 44px + 5 khe 8px = 304px, rộng hơn lòng thẻ trên điện thoại nên
   ô cuối tràn ra ngoài viền. Cho các ô co giãn đều theo bề ngang còn lại. */
@media (max-width: 640px) {
  .otp-box {
    flex: 1 1 0 !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: 52px;
  }
  div:has(> .otp-box) { gap: var(--s2) !important; }
}

/* --- Ngăn chi tiết trượt từ phải --------------------------------------- */
@media (max-width: 640px) {
""" + SEL_DRAWER + """ {
  width: 100% !important;
  max-width: 100% !important;
}
}

/* --- Trang mục lục index.html ------------------------------------------ */
/* File này có <style> riêng đặt sau link nên phải !important mới thắng. */
@media (max-width: 640px) {
  body > header { padding: var(--s5) !important; }
  body > main, body > footer { padding-left: var(--s5) !important; padding-right: var(--s5) !important; }
  body > main .grid { grid-template-columns: 1fr !important; }
}
""")


# (6) (7) Footer công ty + link sang trang chính sách.
# Chỗ nào KH chưa cung cấp thì để dấu chấm lửng đúng như bản gốc, không bịa.
POLICY_LINKS = [
    # (08/10) Chỉ còn 2 văn bản HOMI365 ban hành; 7 trang mẫu cũ đã bỏ.
    ("dieu-khoan-thanh-vien", "Chính sách ưu đãi thành viên"),
    ("chinh-sach-mua-hang", "Chính sách mua hàng &amp; bảo mật dữ liệu"),
]


def footer_html(prefix="", pol_prefix=""):
    """prefix: đường tới thư mục gốc (cho ảnh logo).
    pol_prefix: đường tới policy.html — file này nằm trong screens/ nên khi
    footer được nhúng vào chính screens/*.html thì để rỗng."""
    links = "".join(
        '<a href="%spolicy.html?s=%s" style="color:var(--c2);text-decoration:none;'
        'font-size:13px" style-hover="color:#00ADEE">%s</a>' % (pol_prefix, pid, label)
        for pid, label in POLICY_LINKS)
    return (
        '\n  <footer style="background:var(--c12);border-top:1px solid rgba(170,170,170,.35);'
        'padding:var(--s10) var(--s7) var(--s8);margin-top:auto">\n'
        '    <div style="max-width:1160px;margin:0 auto;display:flex;flex-direction:column;'
        'gap:var(--s7)">\n'
        '      <div style="display:grid;grid-template-columns:1.4fr 1fr;gap:var(--s9)" '
        'class="footer-grid">\n'
        '        <div style="display:flex;flex-direction:column;gap:var(--s3)">\n'
        '          <img src="%sassets/logo homi-01.png" alt="HOMI365" '
        'style="max-width:30%%;height:auto;align-self:flex-start;margin-bottom:var(--s2)">\n'
        '          <div style="font-size:13px;font-weight:700;color:var(--c1);'
        'text-transform:uppercase;line-height:1.6">Công ty Cổ phần Giải pháp và '
        'Dịch vụ HOMI365</div>\n'
        # Thông tin pháp nhân — HOMI365 gửi 08/10/2026.
        '          <div style="font-size:13px;color:var(--c2);line-height:1.8">'
        'Giấy chứng nhận đăng ký doanh nghiệp số 0319717698 cấp ngày 21 tháng 09 năm 2026<br>'
        'Trụ sở chính tại: Số 36 đường 27A, Phường Bình Trưng, Thành Phố Hồ Chí Minh, Việt Nam<br>'
        'Mã số thuế: 0319717698<br>'
        'Hotline: <a href="tel:19009007" style="color:#00ADEE;font-weight:600;'
        'text-decoration:none">1900 9007</a><br>'
        'Email: <a href="mailto:info@homi365.com.vn" style="color:#00ADEE;font-weight:600;'
        'text-decoration:none">info@homi365.com.vn</a></div>\n'
        '        </div>\n'
        '        <div style="display:flex;flex-direction:column;gap:var(--s3)">\n'
        '          <div style="font-size:12px;font-weight:700;color:var(--c5);'
        'text-transform:uppercase;letter-spacing:.05em">Chính sách</div>\n'
        '          %s\n'
        '        </div>\n'
        '      </div>\n'
        '      <div style="border-top:1px solid rgba(170,170,170,.25);padding-top:var(--s6);'
        'font-size:12px;color:var(--c5);line-height:1.8;text-align:center">'
        'Người chịu trách nhiệm nội dung: Bà Phùng Thị Thúy Linh. '
        'Chức vụ: Giám đốc</div>\n'
        '    </div>\n'
        '  </footer>\n' % (prefix, links)
    )


# Toàn văn Điều khoản & Điều kiện, có đủ 5 nội dung bắt buộc theo rà soát
# pháp lý 10/09. Số liệu để trống bằng dấu chấm lửng — chờ Pháp lý điền.
# (08/10) Thay bằng toàn văn "Chính sách ưu đãi thành viên HOMI365" do KH gửi,
# hiệu lực 01/10/2026 — nguồn ở tools/policy_docs.py.
TNC_BODY = (pdoc.html(pdoc.MEMBER)
    + '<div style="margin-top:var(--s6);padding-top:var(--s4);border-top:1px solid rgba(170,170,170,.3);'
      'font-size:12px;color:var(--c5)">Chính sách này áp dụng cùng '
      '<a href="policy.html?s=chinh-sach-mua-hang" target="_blank" style="color:#00ADEE;font-weight:600">'
      'Điều kiện giao dịch chung và Chính sách bảo mật, bảo vệ dữ liệu cá nhân</a>.</div>')

# Không hiện dòng nhắc — ô đồng ý mờ sẵn đã đủ nói lên là chưa bấm được.
TNC_HINT = ""

# Dải dẫn đầu khung điều khoản. Hai việc: cho người đọc lối mở bản đầy đủ ở
# một địa chỉ cố định (để còn lưu, in, trích dẫn khi khiếu nại), và làm nhánh
# "bấm vào link điều khoản" mở khoá ô đồng ý dùng được thật — trước đây link
# chỉ nằm ở đáy khung nên phải cuộn hết mới thấy, thành ra thừa.
TNC_TOP = (
    '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:var(--s4);'
    'justify-content:space-between;background:rgba(0,173,238,.07);'
    'border:1px solid rgba(0,173,238,.3);border-radius:var(--r-md);'
    'padding:var(--s4) var(--s5);margin-bottom:var(--s5)">'
    '<div style="font-size:12px;color:var(--c4);line-height:1.6">'
    'Bản đầy đủ: <strong>Chính sách ưu đãi thành viên HOMI365 — phiên bản 1.0, '
    'hiệu lực từ 01/10/2026</strong></div>'
    '<a href="policy.html?s=dieu-khoan-thanh-vien" target="_blank" '
    'style="flex:none;font-size:12px;font-weight:700;'
    'color:#00ADEE;text-decoration:none;border:1px solid #00ADEE;'
    'border-radius:var(--r-sm);padding:6px 12px;white-space:nowrap">'
    'Mở văn bản đầy đủ ↗</a></div>'
)


OTP_JS = """// Ô nhập OTP: gõ một số là nhảy sang ô kế, Backspace ở ô trống thì lùi lại,
// dán cả mã 6 số thì tự rải ra các ô. Gắn bằng event uỷ quyền trên document
// nên không phụ thuộc thời điểm runtime dựng xong DOM.
(function () {
  function boxes(el) {
    return Array.prototype.slice.call(
      el.parentNode.querySelectorAll('input.otp-box'));
  }

  document.addEventListener('input', function (e) {
    var el = e.target;
    if (!el.classList || !el.classList.contains('otp-box')) return;
    el.value = (el.value || '').replace(/\\D/g, '').slice(0, 1);
    if (!el.value) return;
    var list = boxes(el), i = list.indexOf(el);
    if (i > -1 && i < list.length - 1) list[i + 1].focus();
  });

  document.addEventListener('keydown', function (e) {
    var el = e.target;
    if (!el.classList || !el.classList.contains('otp-box')) return;
    var list = boxes(el), i = list.indexOf(el);
    if (e.key === 'Backspace' && !el.value && i > 0) {
      e.preventDefault();
      list[i - 1].focus();
      list[i - 1].value = '';
    }
    if (e.key === 'ArrowLeft' && i > 0) { e.preventDefault(); list[i - 1].focus(); }
    if (e.key === 'ArrowRight' && i < list.length - 1) { e.preventDefault(); list[i + 1].focus(); }
  });

  document.addEventListener('paste', function (e) {
    var el = e.target;
    if (!el.classList || !el.classList.contains('otp-box')) return;
    var txt = (e.clipboardData || window.clipboardData).getData('text') || '';
    var digits = txt.replace(/\\D/g, '');
    if (!digits) return;
    e.preventDefault();
    var list = boxes(el), i = list.indexOf(el);
    for (var k = 0; k < digits.length && i + k < list.length; k++) {
      list[i + k].value = digits[k];
    }
    list[Math.min(i + digits.length, list.length - 1)].focus();
  });
})();

// Điều khoản & Điều kiện: ô "Tôi đồng ý" chỉ bấm được sau khi người dùng đã
// cuộn hết văn bản, hoặc mở một link chính sách. Runtime dựng lại DOM mỗi lần
// đổi state nên phải áp lại trạng thái sau mỗi lần DOM thay đổi.
(function () {
  var read = false;

  function apply() {
    var box = document.querySelector('.tnc-agree');
    if (!box) return;
    var hint = document.querySelector('.tnc-hint');
    box.disabled = !read;
    box.style.opacity = read ? '1' : '.4';
    box.style.cursor = read ? 'pointer' : 'not-allowed';
    if (hint) hint.style.display = read ? 'none' : '';
  }

  function markRead() { if (!read) { read = true; apply(); } }

  // scroll không nổi bọt -> bắt ở pha capture.
  document.addEventListener('scroll', function (e) {
    var d = e.target;
    if (!d.classList || !d.classList.contains('tnc-doc')) return;
    if (d.scrollTop + d.clientHeight >= d.scrollHeight - 8) markRead();
  }, true);

  document.addEventListener('click', function (e) {
    if (e.target.classList && e.target.classList.contains('tnc-link')) markRead();
  });

  if (window.MutationObserver) {
    new MutationObserver(apply).observe(document.documentElement,
      { childList: true, subtree: true });
  }
  document.addEventListener('DOMContentLoaded', apply);
  apply();
})();
"""

POLICY_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chính sách · HOMI365</title>
<link rel="icon" href="../assets/Icon_viewweb_final.jpg">
<meta name="theme-color" content="#1E3A66">
<link rel="stylesheet" href="../css/fonts.css">
<link rel="stylesheet" href="../css/base.css">
<link rel="stylesheet" href="../css/tokens.css">
<link rel="stylesheet" href="../css/responsive.css">
<style>
  body{font-family:var(--ff);background:var(--warm-50);color:var(--c1);margin:0;
       min-height:100vh;display:flex;flex-direction:column}
  body>footer{margin-top:auto}
  main{flex:1}
  a{color:var(--c6)}
  .bar{position:sticky;top:0;z-index:50;background:var(--c12);
       border-bottom:1px solid rgba(154,163,176,.35);padding:16px var(--s7)}
  .bar .in{max-width:1160px;margin:0 auto;display:flex;align-items:center}
  .bar img{height:40px;display:block}
  main{max-width:1160px;margin:0 auto;padding:var(--s9) var(--s7) var(--s11);
       display:grid;grid-template-columns:1fr 300px;gap:var(--s9);align-items:start}
  article{background:var(--c12);border:1px solid rgba(154,163,176,.35);
          border-radius:var(--r-lg);padding:var(--s9)}
  article h1{font-size:26px;margin:0 0 var(--s6)}
  article h2{font-size:17px;margin:var(--s8) 0 var(--s4);color:var(--c3)}
  article p{font-size:14px;line-height:1.85;color:var(--c2);margin:0 0 var(--s4)}
  article ul,article ol{margin:0 0 var(--s5);padding-left:var(--s8)}
  article li{font-size:14px;line-height:1.85;color:var(--c2);margin-bottom:var(--s2)}
  .intro{font-size:15px;color:var(--c2);background:rgba(30,58,102,.05);
         border-radius:var(--r-md);padding:var(--s6);line-height:1.8}
  .side{background:var(--c12);border:1px solid rgba(154,163,176,.35);
        border-radius:var(--r-lg);padding:var(--s6);position:sticky;top:96px}
  .side .t{font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;
           letter-spacing:.05em;margin-bottom:var(--s4)}
  .side a{display:block;font-size:13px;color:var(--c2);text-decoration:none;
          padding:var(--s3) var(--s4);border-radius:var(--r-sm);line-height:1.5}
  .side a:hover{background:rgba(30,58,102,.06)}
  .side a.on{background:rgba(30,58,102,.1);color:var(--c6);font-weight:700}
  .crumb{font-size:13px;color:var(--c5);margin-bottom:var(--s5)}
  .crumb a{text-decoration:none}
  @media(max-width:860px){main{grid-template-columns:1fr}.side{position:static}}
</style>
</head>
<body>
<div class="bar"><div class="in">
  <a href="../index.html"><img src="../assets/logo homi-01.png" alt="HOMI365"></a>
</div></div>
<main>
  <article id="doc"></article>
  <aside class="side"><div class="t">Danh mục chính sách</div><nav id="menu"></nav></aside>
</main>
<div id="foot"></div>
<script src="../js/policies.js"></script>
<script>
(function () {
  var id = new URLSearchParams(location.search).get('s') || POLICIES[0].id;
  // Link cũ tới 7 trang mẫu đã bỏ (08/10) → về văn bản chính thức tương ứng.
  var MOVED = { 'quy-che-website': 'chinh-sach-mua-hang', 'bao-mat-thong-tin': 'chinh-sach-mua-hang',
    'thanh-toan': 'chinh-sach-mua-hang', 'van-chuyen-giao-nhan': 'chinh-sach-mua-hang',
    'doi-tra-hoan-tien': 'chinh-sach-mua-hang', 'bao-hanh': 'chinh-sach-mua-hang',
    'kiem-hang': 'chinh-sach-mua-hang' };
  id = MOVED[id] || id;
  var p = POLICIES.find(function (x) { return x.id === id; }) || POLICIES[0];

  document.getElementById('menu').innerHTML = POLICIES.map(function (x) {
    return '<a class="' + (x.id === p.id ? 'on' : '') + '" href="?s=' + x.id + '">'
      + x.title + '</a>';
  }).join('');

  function block(it) {
    if (typeof it === 'string') return '<p>' + it + '</p>';
    if (it.list) return '<ul>' + it.list.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>';
    if (it.steps) return '<ol>' + it.steps.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ol>';
    return '';
  }

  document.getElementById('doc').innerHTML =
    '<div class="crumb"><a href="../index.html">Trang chủ</a> / ' + p.title + '</div>'
    + '<h1>' + (p.heading || p.title) + '</h1>'
    + (p.intro ? '<p class="intro">' + p.intro + '</p>' : '')
    + p.sections.map(function (sec) {
        return '<h2>' + sec.h + '</h2>' + sec.items.map(block).join('');
      }).join('')
    + (p.official ? '' : '<p style="font-size:12px;color:var(--c5);margin-top:var(--s8)">'
    + 'Nội dung mẫu dựng giao diện — bản chính thức cần bộ phận Pháp lý rà soát '
    + 'và cập nhật pháp nhân, hotline, email theo thông tin HOMI365.</p>');

  document.title = p.title.replace('&amp;', '&') + ' · HOMI365';
})();
</script>
</body>
</html>
"""


def combo(key, placeholder):
    """Ô chọn có tìm kiếm: gõ để lọc, bấm để mở/đóng danh sách.

    Dùng chung cho Ngân hàng / Tỉnh thành / Phường xã. Viết bằng đúng cú pháp
    runtime của mockup (sc-if / sc-for / sc-camel-on-*) nên không cần thư viện.
    """
    return (
        '<div style="position:relative">\n'
        '                <input type="text" value="{{%sQuery}}" '
        'sc-camel-on-change="{{set%sQuery}}" sc-camel-on-click="{{toggle%s}}" '
        'placeholder="%s" style="width:100%%;%s" style-focus="%s">\n'
        '                <sc-if value="{{%sOpen}}" hint-placeholder-val="{{false}}">\n'
        '                  <div style="position:absolute;left:0;right:0;top:48px;z-index:60;'
        'background:var(--c12);border:1px solid rgba(170,170,170,.6);'
        'border-radius:var(--r-md);box-shadow:0 8px 24px rgba(0,0,0,.12);'
        'max-height:260px;overflow-y:auto">\n'
        '                    <sc-for list="{{%sOptions}}" as="o" hint-placeholder-count="6">\n'
        '                      <div sc-camel-on-click="{{o.onPick}}" '
        'style="padding:var(--s4) var(--s5);cursor:pointer;font-size:14px;color:var(--c2);'
        'border-bottom:1px solid rgba(170,170,170,.15)" '
        'style-hover="background:rgba(0,173,238,.06)">{{o.label}}</div>\n'
        '                    </sc-for>\n'
        '                    <sc-if value="{{%sEmpty}}" hint-placeholder-val="{{false}}">\n'
        '                      <div style="padding:var(--s5);font-size:13px;color:var(--c5)">'
        'Không tìm thấy kết quả phù hợp</div>\n'
        '                    </sc-if>\n'
        '                  </div>\n'
        '                </sc-if>\n'
        '              </div>'
        % (key, key[0].upper() + key[1:], key[0].upper() + key[1:], placeholder,
           _INP, _FOCUS, key, key, key)
    )

# (19) B8 — Nhật ký hệ thống. Phạm vi toàn hệ thống, không riêng phân hệ nào.
# Hai tab: thay đổi dữ liệu và file đã tải lên. Dùng lưới CSS (không phải
# <table>) để khung cuộn ngang giống các bảng quản trị còn lại.
_AU_COLS = ("1.1fr 1.2fr .9fr 1.3fr 1.2fr 1fr 1fr 1.2fr .8fr")
_AU_MINW = "1560px"
_AF_COLS = "1.7fr .9fr 1.3fr 1.1fr 1fr .7fr .6fr"
_AF_MINW = "1120px"

B8_AUDIT = """      <!-- B8 NHẬT KÝ HỆ THỐNG (bổ sung, không có trong mockup KH) -->
      <sc-if value="{{isB8}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;flex-direction:column;gap:var(--s7)">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
            <div><div style="font-size:24px;font-weight:700">Nhật ký hệ thống</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">Ghi lại mọi thay đổi dữ liệu và file tải lên, trên toàn bộ phân hệ</div></div>
            <button style="height:38px;padding:0 var(--s6);background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c2)" style-hover="background:rgba(170,170,170,.08)">Xuất file Excel</button>
          </div>

          <div style="display:flex;gap:var(--s3);flex-wrap:wrap">
            <sc-for list="{{auditTabs}}" as="tb" hint-placeholder-count="2">
              <button sc-camel-on-click="{{tb.onClick}}" style="{{tb.style}}">{{tb.label}}</button>
            </sc-for>
          </div>

          <div style="font-size:12px;color:var(--c4);background:rgba(0,173,238,.07);border:1px solid rgba(0,173,238,.3);border-radius:var(--r-md);padding:var(--s4) var(--s5);line-height:1.6">Nhật ký chỉ ghi thêm — không sửa, không xoá được, kể cả với Head. Đây là căn cứ đối chiếu khi có khiếu nại hoặc khi cơ quan quản lý kiểm tra.</div>

          <!-- TAB 1: thay đổi dữ liệu -->
          <sc-if value="{{isAuditChanges}}" hint-placeholder-val="{{true}}">
            <div style="display:flex;gap:var(--s5);flex-wrap:wrap">
              <input type="text" value="{{auditSearch}}" sc-camel-on-change="{{setAuditSearch}}" placeholder="Tìm theo người thực hiện, đối tượng, mã phiếu…" style="flex:1;min-width:240px;height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px" style-focus="border-color:#00ADEE;box-shadow:0 0 0 3px rgba(0,173,238,.25)">
              <sc-raw-select style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;color:var(--c2);background:var(--c12)"><option>Tất cả phân hệ</option><option>Thành viên</option><option>Đơn hàng</option><option>Kho hàng</option><option>Sản phẩm</option><option>Rút tiền</option><option>Tài khoản admin</option></sc-raw-select>
              <sc-raw-select style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;color:var(--c2);background:var(--c12)"><option>Tất cả hành động</option><option>Tạo mới</option><option>Cập nhật</option><option>Duyệt</option><option>Từ chối</option><option>Khoá / mở khoá</option><option>Tải file lên</option></sc-raw-select>
              <sc-raw-select style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;color:var(--c2);background:var(--c12)"><option>30 ngày gần nhất</option><option>7 ngày gần nhất</option><option>Tháng này</option><option>Khoảng ngày…</option></sc-raw-select>
            </div>

            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);overflow:auto">
              <div style="display:grid;grid-template-columns:AUCOLS;min-width:AUMINW;background:rgba(170,170,170,.08);padding:var(--s5) var(--s6);font-size:11px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;white-space:nowrap">
                <div>Thời điểm</div><div>Người thực hiện</div><div>Phân hệ</div><div>Đối tượng</div><div>Hành động</div><div>Giá trị trước</div><div>Giá trị sau</div><div>Minh chứng</div><div>Địa chỉ IP</div>
              </div>
              <sc-for list="{{auditRows}}" as="a" hint-placeholder-count="8">
                <div style="display:grid;grid-template-columns:AUCOLS;min-width:AUMINW;align-items:center;padding:var(--s5) var(--s6);font-size:13px;color:var(--c1);border-top:1px solid rgba(170,170,170,.2)">
                  <div style="color:var(--c5);font-family:monospace;font-size:12px">{{a.time}}</div>
                  <div><div style="font-weight:600">{{a.actor}}</div><div style="font-size:11px;color:var(--c5)">{{a.role}}</div></div>
                  <div style="color:var(--c4)">{{a.module}}</div>
                  <div style="color:var(--c4);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{a.target}}</div>
                  <div><span style="font-size:11px;font-weight:700;padding:var(--s1) var(--s5);border-radius:var(--r-xl);background:{{a.badgeBg}};color:{{a.badgeColor}}">{{a.action}}</span></div>
                  <div style="color:var(--c5)">{{a.before}}</div>
                  <div style="font-weight:600">{{a.after}}</div>
                  <div style="color:var(--c6);font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{a.evidence}}</div>
                  <div style="color:var(--c5);font-family:monospace;font-size:12px">{{a.ip}}</div>
                </div>
              </sc-for>
            </div>
          </sc-if>

          <!-- TAB 2: file đã tải lên -->
          <sc-if value="{{isAuditFiles}}" hint-placeholder-val="{{false}}">
            <div style="display:flex;gap:var(--s5);flex-wrap:wrap">
              <input type="text" value="{{auditSearch}}" sc-camel-on-change="{{setAuditSearch}}" placeholder="Tìm theo tên file, người tải, đối tượng gắn kèm…" style="flex:1;min-width:240px;height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px" style-focus="border-color:#00ADEE;box-shadow:0 0 0 3px rgba(0,173,238,.25)">
              <sc-raw-select style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;color:var(--c2);background:var(--c12)"><option>Tất cả loại file</option><option>Ảnh</option><option>PDF</option><option>Email</option><option>Excel / CSV</option></sc-raw-select>
              <sc-raw-select style="height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;color:var(--c2);background:var(--c12)"><option>Tất cả phân hệ</option><option>Thành viên</option><option>Đơn hàng</option><option>Kho hàng</option><option>Sản phẩm</option></sc-raw-select>
            </div>

            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);overflow:auto">
              <div style="display:grid;grid-template-columns:AFCOLS;min-width:AFMINW;background:rgba(170,170,170,.08);padding:var(--s5) var(--s6);font-size:11px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;white-space:nowrap">
                <div>Tên file</div><div>Loại</div><div>Gắn với</div><div>Người tải lên</div><div>Thời điểm</div><div>Dung lượng</div><div></div>
              </div>
              <sc-for list="{{auditFiles}}" as="f" hint-placeholder-count="6">
                <div style="display:grid;grid-template-columns:AFCOLS;min-width:AFMINW;align-items:center;padding:var(--s5) var(--s6);font-size:13px;color:var(--c1);border-top:1px solid rgba(170,170,170,.2)">
                  <div style="font-family:monospace;font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{f.name}}</div>
                  <div style="color:var(--c4)">{{f.kind}}</div>
                  <div style="color:var(--c4);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{f.linkedTo}}</div>
                  <div style="color:var(--c4)">{{f.by}}</div>
                  <div style="color:var(--c5);font-family:monospace;font-size:12px">{{f.time}}</div>
                  <div style="color:var(--c5)">{{f.size}}</div>
                  <div style="text-align:right"><button style="height:30px;padding:0 var(--s5);background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:12px;font-weight:600;color:var(--c2)" style-hover="background:rgba(170,170,170,.08)">Tải về</button></div>
                </div>
              </sc-for>
            </div>
            <div style="font-size:11px;color:var(--c5);line-height:1.6">File đã tải lên không xoá được. Nếu nộp nhầm, tải bản đúng lên rồi ghi chú trong nhật ký — bản cũ vẫn phải giữ nguyên.</div>
          </sc-if>
        </div>
      </sc-if>

""".replace("AUCOLS", _AU_COLS).replace("AUMINW", _AU_MINW) \
   .replace("AFCOLS", _AF_COLS).replace("AFMINW", _AF_MINW)


B5_PRODUCTS = """      <!-- B5 PRODUCTS (bổ sung, không có trong mockup KH) -->
      <sc-if value="{{isB5}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;flex-direction:column;gap:var(--s7)">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
            <div><div style="font-size:24px;font-weight:700">Quản lý sản phẩm</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">{{productCount}} sản phẩm đang bán</div></div>
            <button sc-camel-on-click="{{openProductForm}}" style="%(btn)s" style-hover="background:#0099d1">+ Thêm sản phẩm</button>
          </div>

          <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);overflow:hidden">
            <table style="width:100%%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="background:rgba(170,170,170,.08);text-align:left">
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5);width:104px">Hình ảnh</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5);width:32%%">Tên sản phẩm</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Mô tả</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5);width:88px"></th>
                </tr>
              </thead>
              <tbody>
                <sc-for list="{{products}}" as="p" hint-placeholder-count="2">
                  <tr style="border-top:1px solid rgba(170,170,170,.2)">
                    <td style="padding:var(--s5);vertical-align:top"><div style="width:72px;height:72px;border-radius:var(--r-md);background:rgba(170,170,170,.15);display:flex;align-items:center;justify-content:center;font-size:10px;color:var(--c5);text-align:center;padding:var(--s2)">{{p.imageLabel}}</div></td>
                    <td style="padding:var(--s5);vertical-align:top"><div style="font-weight:600;color:var(--c1)">{{p.name}}</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1);font-family:monospace">{{p.sku}}</div></td>
                    <td style="padding:var(--s5);vertical-align:top;color:var(--c2);line-height:1.6">{{p.desc}}</td>
                    <td style="padding:var(--s5);vertical-align:top"><button sc-camel-on-click="{{p.onEdit}}" style="height:32px;padding:0 var(--s5);background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:12px;font-weight:600;color:var(--c2)" style-hover="background:rgba(170,170,170,.08)">Sửa</button></td>
                  </tr>
                </sc-for>
              </tbody>
            </table>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{showProductForm}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:flex-start;justify-content:center;z-index:220;padding:var(--s7);overflow-y:auto">
          <div style="width:100%%;max-width:460px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25);margin:var(--s10) 0">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
              <div style="font-size:18px;font-weight:700;color:var(--c1)">{{productFormTitle}}</div>
              <button sc-camel-on-click="{{closeProductForm}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Tên sản phẩm (*)</label>
              <input type="text" value="{{productFormName}}" placeholder="Gói Bác sĩ 24/7 · License 12 tháng" style="%(inp)s" style-focus="%(focus)s">
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Hình ảnh</label>
              <label style="border:1px dashed rgba(170,170,170,.6);border-radius:var(--r-md);padding:var(--s7);display:flex;flex-direction:column;align-items:center;gap:var(--s2);cursor:pointer;color:var(--c5)" style-hover="border-color:#00ADEE;color:#00ADEE">
                <span style="font-size:22px">&#11014;</span>
                <span style="font-size:13px;font-weight:600">Tải ảnh sản phẩm</span>
                <span style="font-size:11px">PNG hoặc JPG, tối đa 2MB</span>
                <input type="file" accept="image/*" style="display:none">
              </label>
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Mô tả</label>
              <textarea rows="4" placeholder="Mô tả ngắn hiển thị ở trang mua hàng…" style="padding:var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-family:inherit;resize:vertical" style-focus="%(focus)s">{{productFormDesc}}</textarea>
            </div>
            <div style="display:flex;gap:var(--s5)">
              <button sc-camel-on-click="{{closeProductForm}}" style="flex:1;height:44px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c2)">Huỷ</button>
              <button sc-camel-on-click="{{closeProductForm}}" style="flex:1;height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Lưu sản phẩm</button>
            </div>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{showAddStock}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:center;justify-content:center;z-index:220;padding:var(--s7)">
          <div style="width:100%%;max-width:420px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
              <div><div style="font-size:18px;font-weight:700;color:var(--c1)">Thêm hàng vào kho</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">Mỗi mã kích hoạt gắn với đúng một sản phẩm</div></div>
              <button sc-camel-on-click="{{closeAddStock}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Mã sản phẩm (*)</label>
              <input type="text" value="{{addStockSku}}" sc-camel-on-change="{{setAddStockSku}}" placeholder="CN02-0025" style="%(inp)s;font-family:monospace" style-focus="%(focus)s">
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Mã kích hoạt (*)</label>
              <input type="text" value="{{addStockCode}}" sc-camel-on-change="{{setAddStockCode}}" placeholder="ACT-100925" style="%(inp)s;font-family:monospace" style-focus="%(focus)s">
            </div>
            <sc-if value="{{addStockError}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:#D9342B;background:rgba(217,52,43,.08);border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">{{addStockError}}</div>
            </sc-if>
            <div style="font-size:11px;color:var(--c5);line-height:1.6">Hàng thêm vào sẽ ở trạng thái <strong>Sẵn hàng</strong> cho tới khi được gán vào đơn. Mã kích hoạt và mã sản phẩm không được trùng với mã đã có trong kho.</div>
            <div style="display:flex;gap:var(--s5)">
              <button sc-camel-on-click="{{closeAddStock}}" style="flex:1;height:44px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c2)">Huỷ</button>
              <button sc-camel-on-click="{{submitAddStock}}" style="flex:1;height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Thêm vào kho</button>
            </div>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{showImportStock}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:flex-start;justify-content:center;z-index:220;padding:var(--s7);overflow-y:auto">
          <div style="width:100%%;max-width:560px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25);margin:var(--s10) 0">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
              <div><div style="font-size:18px;font-weight:700;color:var(--c1)">Import hàng loạt</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">Mã nào hợp lệ thì nhận, mã trùng thì bỏ qua và báo lại</div></div>
              <button sc-camel-on-click="{{closeImportStock}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>

            <label style="border:1px dashed rgba(170,170,170,.6);border-radius:var(--r-md);padding:var(--s6);display:flex;align-items:center;justify-content:center;gap:var(--s3);cursor:pointer;color:var(--c5);font-size:13px;font-weight:600" style-hover="border-color:#00ADEE;color:#00ADEE">
              <span style="font-size:18px">&#11014;</span> Chọn file Excel / CSV
              <input type="file" accept=".xlsx,.xls,.csv" style="display:none">
            </label>

            <div style="display:flex;flex-direction:column;gap:var(--s2)">
              <label style="font-size:14px;font-weight:600;color:var(--c2)">Hoặc dán danh sách</label>
              <div style="font-size:11px;color:var(--c5);line-height:1.6">Mỗi dòng một thiết bị, theo thứ tự <strong>mã sản phẩm, mã kích hoạt</strong>. Ví dụ: <span style="font-family:monospace">CN02-1301, ACT-130145</span></div>
              <textarea rows="7" value="{{importText}}" sc-camel-on-change="{{setImportText}}" placeholder="CN02-1301, ACT-130145&#10;CN02-1302, ACT-130146&#10;CN02-1303, ACT-130147" style="padding:var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:13px;font-family:monospace;resize:vertical" style-focus="%(focus)s"></textarea>
            </div>

            <sc-if value="{{hasImportResult}}" hint-placeholder-val="{{false}}">
              <div style="display:flex;flex-direction:column;gap:var(--s4);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);padding:var(--s6)">
                <div style="display:flex;gap:var(--s7);flex-wrap:wrap;font-size:13px">
                  <div><span style="color:var(--c5)">Tổng dòng: </span><strong>{{importResult.total}}</strong></div>
                  <div><span style="color:var(--c5)">Đã nhập: </span><strong style="color:#4c7a2e">{{importResult.ok}}</strong></div>
                  <div><span style="color:var(--c5)">Bỏ qua: </span><strong style="color:#D9342B">{{importResult.skip}}</strong></div>
                </div>
                <sc-if value="{{importResult.hasSkipped}}" hint-placeholder-val="{{false}}">
                  <div style="display:flex;flex-direction:column;gap:var(--s2);max-height:180px;overflow-y:auto">
                    <sc-for list="{{importResult.skipped}}" as="k" hint-placeholder-count="3">
                      <div style="font-size:12px;display:flex;gap:var(--s4);align-items:baseline">
                        <span style="font-family:monospace;color:var(--c2);flex:1;min-width:0;word-break:break-all">{{k.line}}</span>
                        <span style="flex:none;color:#D9342B">{{k.reason}}</span>
                      </div>
                    </sc-for>
                  </div>
                </sc-if>
              </div>
            </sc-if>

            <div style="display:flex;gap:var(--s5)">
              <button sc-camel-on-click="{{closeImportStock}}" style="flex:1;height:44px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c2)">Đóng</button>
              <button sc-camel-on-click="{{runImportStock}}" style="flex:1;height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Import</button>
            </div>
          </div>
        </div>
      </sc-if>

""" % {"btn": _BTN_PRIMARY, "inp": _INP, "focus": _FOCUS}

B6_ORDERS = """      <!-- B6 ORDERS (bổ sung, không có trong mockup KH) -->
      <sc-if value="{{isB6}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;flex-direction:column;gap:var(--s7)">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
            <div><div style="font-size:24px;font-weight:700">Quản lý đơn hàng</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">{{orderTotal}} đơn · đối soát chuyển khoản và cấp mã kích hoạt</div></div>
            <button style="%(ghost)s" style-hover="background:rgba(170,170,170,.08)">Xuất file Excel</button>
          </div>

          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s5)">
            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Chờ đối soát</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{orderPendingCount}}</div></div>
            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Từ chối</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{orderRejectedCount}}</div></div>
            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Đã thanh toán</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{orderPaidCount}}</div></div>
            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Doanh thu đã đối soát</div><div style="font-size:22px;font-weight:700;color:var(--c1)">{{orderRevenue}}</div></div>
          </div>

          <div style="display:flex;gap:var(--s5);flex-wrap:wrap;align-items:center">
            <div style="display:flex;gap:var(--s2);flex-wrap:wrap">
              <sc-for list="{{orderFilters}}" as="f" hint-placeholder-count="5">
                <button sc-camel-on-click="{{f.onClick}}" style="{{f.style}}">{{f.label}}</button>
              </sc-for>
            </div>
            <input type="text" value="{{orderSearch}}" sc-camel-on-change="{{setOrderSearch}}" placeholder="Tìm theo mã đơn, tên hoặc SĐT khách…" style="flex:1;min-width:220px;height:38px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px" style-focus="%(focus)s">
          </div>

          <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);overflow-x:auto">
            <table style="width:100%%;border-collapse:collapse;font-size:13px;min-width:1180px">
              <thead>
                <tr style="background:rgba(170,170,170,.08);text-align:left">
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Mã đơn</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Khách hàng</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Gói</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Số tiền</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Nội dung</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Minh chứng</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Người giới thiệu</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Ngày đặt</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Ngày kích hoạt</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Ngày hết hiệu lực</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                <sc-for list="{{orders}}" as="o" hint-placeholder-count="8">
                  <tr sc-camel-on-click="{{o.onClick}}" style="border-top:1px solid rgba(170,170,170,.2);cursor:pointer" style-hover="background:rgba(0,173,238,.05)">
                    <td style="padding:var(--s5);font-family:monospace;font-weight:600;color:var(--c1);white-space:nowrap">{{o.id}}</td>
                    <td style="padding:var(--s5)"><div style="font-weight:600;color:var(--c1);white-space:nowrap">{{o.buyer}}</div><div style="font-size:12px;color:var(--c5)">{{o.phone}}</div></td>
                    <td style="padding:var(--s5);color:var(--c2);white-space:nowrap">{{o.pkg}}</td>
                    <td style="padding:var(--s5);font-weight:600;color:var(--c1);white-space:nowrap">{{o.amount}}</td>
                    <td style="padding:var(--s5);color:var(--c2);font-family:monospace;font-size:12px">{{o.transferNote}}</td>
                    <td style="padding:var(--s5)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{o.proofBg}};color:{{o.proofColor}};white-space:nowrap">{{o.proofLabel}}</span></td>
                    <td style="padding:var(--s5);color:var(--c2);white-space:nowrap"><div>{{o.referrer}}</div><div style="font-size:11px;color:var(--c5);font-family:monospace">{{o.refCode}}</div></td>
                    <td style="padding:var(--s5);color:var(--c5);white-space:nowrap">{{o.date}}</td>
                    <td style="padding:var(--s5);color:var(--c4);white-space:nowrap">{{o.activatedLabel}}</td>
                    <td style="padding:var(--s5);color:var(--c4);white-space:nowrap">{{o.expiresLabel}}</td>
                    <td style="padding:var(--s5)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{o.badgeBg}};color:{{o.badgeColor}};white-space:nowrap">{{o.statusLabel}}</span></td>
                  </tr>
                </sc-for>
              </tbody>
            </table>
            <sc-if value="{{ordersEmpty}}" hint-placeholder-val="{{false}}">
              <div style="padding:var(--s10);text-align:center;font-size:13px;color:var(--c5)">Không có đơn hàng nào khớp bộ lọc.</div>
            </sc-if>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{hasSelectedOrder}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.4);display:flex;justify-content:flex-end;z-index:210">
          <div style="width:100%%;max-width:470px;background:var(--c12);height:100%%;overflow-y:auto;padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:-8px 0 30px rgba(0,0,0,.15)">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:var(--s5)">
              <div><div style="font-size:20px;font-weight:700;color:var(--c1);font-family:monospace">{{selectedOrder.id}}</div><div style="margin-top:var(--s2)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{selectedOrder.badgeBg}};color:{{selectedOrder.badgeColor}}">{{selectedOrder.statusLabel}}</span></div></div>
              <button sc-camel-on-click="{{closeOrder}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>

            <sc-if value="{{selectedOrder.stageNote}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:#a36400;background:rgba(255,165,0,.12);border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">{{selectedOrder.stageNote}}</div>
            </sc-if>

            <div style="display:flex;flex-direction:column;gap:var(--s4);font-size:13px">
              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Khách hàng</div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Họ tên</span><span style="font-weight:600;color:var(--c1);text-align:right">{{selectedOrder.buyer}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Số điện thoại</span><span style="font-weight:600;color:var(--c1)">{{selectedOrder.phone}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Email</span><span style="color:var(--c2);text-align:right">{{selectedOrder.email}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Địa chỉ nhận hàng</span><span style="color:var(--c2);text-align:right;max-width:62%%">{{selectedOrder.address}}</span></div>
            </div>

            <div style="height:1px;background:rgba(170,170,170,.25)"></div>

            <div style="display:flex;flex-direction:column;gap:var(--s4);font-size:13px">
              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Đơn hàng</div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Gói</span><span style="font-weight:600;color:var(--c1);text-align:right">{{selectedOrder.pkg}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Số tiền</span><span style="font-weight:700;color:var(--c6);font-size:16px">{{selectedOrder.amount}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Người giới thiệu</span><span style="color:var(--c2)">{{selectedOrder.referrer}} · {{selectedOrder.refCode}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Ngày đặt</span><span style="color:var(--c2)">{{selectedOrder.date}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Mã kích hoạt</span><span style="font-family:monospace;font-weight:600;color:var(--c1)">{{selectedOrder.activationCodeLabel}}</span></div>
            </div>

            <div style="height:1px;background:rgba(170,170,170,.25)"></div>

            <div style="display:flex;flex-direction:column;gap:var(--s4)">
              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Ảnh chuyển khoản</div>
              <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);padding:var(--s7);display:flex;flex-direction:column;align-items:center;gap:var(--s3);background:rgba(170,170,170,.05)">
                <span style="font-size:26px;color:var(--c5)">&#128196;</span>
                <span style="font-size:12px;color:var(--c2);font-family:monospace">{{selectedOrder.proof}}</span>
                <span style="font-size:11px;color:var(--c5)">Bấm để xem ảnh gốc</span>
              </div>
            </div>

            <div style="display:flex;flex-direction:column;gap:var(--s4)">
              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Lịch sử xử lý</div>
              <sc-for list="{{selectedOrder.auditLog}}" as="a" hint-placeholder-count="3">
                <div style="display:flex;gap:var(--s4);font-size:12px">
                  <div style="flex:none;width:6px;height:6px;border-radius:var(--r-full);background:var(--c6);margin-top:6px"></div>
                  <div><div style="color:var(--c1);font-weight:600">{{a.label}}</div><div style="color:var(--c5)">{{a.actor}} · {{a.time}}</div></div>
                </div>
              </sc-for>
            </div>

            <sc-if value="{{selectedOrder.isRejected}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:var(--c2);background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s5);line-height:1.6">Đơn đã bị từ chối. Phase 1 <strong>không mở lại đơn cũ</strong> — khách cần đặt đơn mới qua link giới thiệu.</div>
            </sc-if>

            <sc-if value="{{selectedOrder.canAct}}" hint-placeholder-val="{{true}}">
              <div style="display:flex;flex-direction:column;gap:var(--s4);border-top:1px solid rgba(170,170,170,.25);padding-top:var(--s6)">
                <sc-if value="{{selectedOrder.needsCodePick}}" hint-placeholder-val="{{true}}">
                  <div style="display:flex;flex-direction:column;gap:var(--s2)">
                    <label style="font-size:14px;font-weight:600;color:var(--c2)">Chọn mã kích hoạt từ kho (*)</label>
                    <sc-raw-select value="{{orderActivationCode}}" sc-camel-on-change="{{setOrderActivationCode}}" style="height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-family:monospace;color:var(--c2);background:var(--c12)">
                      <option value="">— Chọn mã Sẵn hàng —</option>
                      <sc-for list="{{availableStockCodes}}" as="c" hint-placeholder-count="5">
                        <option value="{{c.code}}">{{c.label}}</option>
                      </sc-for>
                    </sc-raw-select>
                    <div style="font-size:11px;color:var(--c5)">Còn {{availableStockCount}} mã Sẵn hàng trong kho. Mã đã chọn sẽ chuyển sang <strong>Đã gán đơn hàng</strong>.</div>
                  </div>
                  <div style="display:flex;flex-direction:column;gap:var(--s2)">
                    <label style="font-size:14px;font-weight:600;color:var(--c2)">Mã giao dịch ngân hàng (*)</label>
                    <input type="text" value="{{bankTxnCode}}" sc-camel-on-change="{{setBankTxnCode}}" placeholder="FT26090312345" style="height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-family:monospace" style-focus="border-color:#00ADEE;box-shadow:0 0 0 3px rgba(0,173,238,.25)">
                    <div style="font-size:11px;color:var(--c5);line-height:1.5">Số tham chiếu trên sao kê ngân hàng, dùng để đối soát về sau.</div>
                  </div>
                  <sc-if value="{{orderCodeError}}" hint-placeholder-val="{{false}}">
                    <div style="font-size:12px;color:#D9342B;background:rgba(217,52,43,.08);border-radius:var(--r-sm);padding:var(--s4)">{{orderCodeError}}</div>
                  </sc-if>
                </sc-if>
                <sc-if value="{{selectedOrder.canConfirm}}" hint-placeholder-val="{{true}}">
                  <button sc-camel-on-click="{{confirmOrder}}" style="height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">{{selectedOrder.confirmLabel}}</button>
                </sc-if>
                <sc-if value="{{selectedOrder.canReject}}" hint-placeholder-val="{{true}}">
                  <button sc-camel-on-click="{{rejectOrder}}" style="height:42px;background:var(--c12);border:1px solid #D9342B;border-radius:var(--r-md);font-size:14px;font-weight:600;color:#D9342B" style-hover="background:rgba(217,52,43,.06)">Từ chối đơn</button>
                </sc-if>
                <div style="font-size:11px;color:var(--c5);line-height:1.6">{{selectedOrder.actHint}}</div>
              </div>
            </sc-if>
          </div>
        </div>
      </sc-if>

""" % {"ghost": _BTN_GHOST, "focus": _FOCUS}

_SEL = ('height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
        'border-radius:var(--r-md);font-size:14px;color:var(--c2);background:var(--c12)')

# Nối 2 mục này SAU khi B5_PRODUCTS / B6_ORDERS đã khai báo ở trên.
BG_PATCHES += [
    # (4) (5) Ngân hàng · Tỉnh/Thành · Phường/Xã -> dropdown có ô tìm kiếm,
    # dữ liệu nạp từ API công khai (VietQR banks, provinces.open-api.vn).
    ('<sc-raw-select style="%s"><option>TP. Hồ Chí Minh</option></sc-raw-select>' % _SEL,
     combo('province', 'Gõ để tìm tỉnh/thành…')),
    ('<sc-raw-select style="%s"><option>Phường Bến Nghé</option></sc-raw-select>' % _SEL,
     combo('ward', 'Gõ để tìm phường/xã…')),
    ('<sc-raw-select style="%s"><option>Vietcombank</option></sc-raw-select>' % _SEL,
     combo('bank', 'Gõ để tìm ngân hàng…')),

    # (1) Đổi tên khối + thêm Tên chủ tài khoản (viết hoa, không dấu).
    ('<div style="font-size:14px;font-weight:700;color:var(--c1)">'
     'Thông tin nhận hoa hồng</div>',
     '<div style="font-size:14px;font-weight:700;color:var(--c1)">'
     'Thông tin nhận ưu đãi (khi đạt điều kiện)</div>'),

    ('<div style="display:flex;flex-direction:column;gap:var(--s2)">'
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">Số tài khoản (*)</label>'
     '<input type="text" placeholder="Nhập số tài khoản" value="{{buyerBankAccount}}" '
     'sc-camel-on-change="{{setBuyerBankAccount}}" style="%s" style-focus="%s"></div>'
     % (_INP, _FOCUS),
     '<div style="display:flex;flex-direction:column;gap:var(--s2)">'
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">Số tài khoản (*)</label>'
     '<input type="text" placeholder="Nhập số tài khoản" value="{{buyerBankAccount}}" '
     'sc-camel-on-change="{{setBuyerBankAccount}}" style="%s" style-focus="%s"></div>\n'
     '            <div style="display:flex;flex-direction:column;gap:var(--s2)">'
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">Tên chủ tài khoản (*)</label>'
     '<input type="text" placeholder="NGUYEN VAN AN" value="{{accountHolder}}" '
     'sc-camel-on-change="{{setAccountHolder}}" style="%s;text-transform:uppercase" '
     'style-focus="%s">'
     '<div style="font-size:11px;color:var(--c5);line-height:1.5">Viết hoa, không dấu '
     '— hệ thống tự chuẩn hoá khi bạn gõ.</div></div>' % (_INP, _FOCUS, _INP, _FOCUS)),

    # (3) Checkbox điều khoản; chưa tích thì nút Thanh toán khoá.
    ('<button sc-camel-on-click="{{openQRPayment}}" style="height: 48px; '
     'color: var(--c12); border: none; border-radius: var(--r-md); font-size: 16px; '
     'font-weight: 700; box-shadow: var(--sh); background-color: #EE0000" '
     'style-hover="background:#0099d1" style-active="background:#0088ba" '
     'style-focus="box-shadow:0 0 0 3px rgba(0,173,238,.4)">Thanh toán</button>',
     # (17) Một thông báo duy nhất trước nút: lỗi đường truyền.
     '<sc-if value="{{payTimedOut}}" hint-placeholder-val="{{false}}">\n'
     '          <div style="display:flex;gap:var(--s3);align-items:flex-start;'
     'background:rgba(217,52,43,.08);border:1px solid rgba(217,52,43,.35);'
     'border-radius:var(--r-md);padding:var(--s4) var(--s5);font-size:12px;'
     'color:#D9342B;line-height:1.6">'
     '<span style="flex:none;font-weight:700">!</span>'
     '<span>Lỗi đường truyền, vui lòng gửi lại yêu cầu</span></div>\n'
     '          </sc-if>\n'
     '          <button sc-camel-on-click="{{submitPayment}}" disabled="{{payDisabled}}" '
     'style="{{payStyle}}">{{payLabel}}</button>\n'
     '          <label style="display:flex;gap:var(--s3);align-items:flex-start;'
     'cursor:pointer;font-size:12px;color:var(--c2);line-height:1.6">'
     '<input type="checkbox" checked="{{buyTcChecked}}" '
     'sc-camel-on-change="{{toggleBuyTc}}" style="margin-top:3px;flex:none;'
     'width:16px;height:16px;accent-color:#00ADEE">'
     '<span>Bằng cách đăng ký mua hàng và thanh toán, bạn đã đồng ý với '
     '<a href="policy.html?s=quy-che-website" style="color:#00ADEE;font-weight:600">'
     'Điều khoản sử dụng</a> và '
     '<a href="policy.html?s=bao-mat-thong-tin" style="color:#00ADEE;font-weight:600">'
     'Chính sách bảo mật</a> của HOMI365.</span></label>'),

    # (8) Modal QR: thêm tên đơn vị thụ hưởng và số tài khoản nhận.
    ('<div style="text-align:center;font-size:11px;color:var(--c5);'
     'font-family:monospace">Đơn hàng #{{orderId}} · {{cn02PackagePrice}}</div>',
     '<div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);'
     'padding:var(--s5);display:flex;flex-direction:column;gap:var(--s2);'
     'text-align:center;background:rgba(170,170,170,.05)">'
     '<div style="font-size:11px;color:var(--c5);text-transform:uppercase;'
     'letter-spacing:.04em">Đơn vị thụ hưởng</div>'
     '<div style="font-size:12px;font-weight:700;color:var(--c1);line-height:1.5">'
     'CONG TY CO PHAN GIAI PHAP VA DICH VU HOMI365</div>'
     '<div style="font-size:13px;font-weight:700;color:var(--c6);'
     'font-family:monospace;letter-spacing:.02em">TECHCOMBANK - 0009383764899</div>'
     '</div>\n'
     '        <div style="text-align:center;font-size:11px;color:var(--c5);'
     'font-family:monospace">Đơn hàng #{{orderId}} · {{cn02PackagePrice}}</div>'),

    # Modal tra cứu có 2 mặt: chưa có kết quả thì hỏi SĐT, có rồi thì khoe đơn.
    ('<div style="text-align:left"><div style="font-size:18px;font-weight:700;'
     'color:var(--c1)">Nhập số điện thoại</div><div style="font-size:12px;'
     'color:var(--c5);margin-top:var(--s1)">Hệ thống sẽ đối chiếu với đơn hàng '
     'để xác định agent bán hàng · thử SĐT 0901111111 (agent bán là hạng Bạc) '
     'hoặc 0902222222 (agent bán là hạng Đồng)</div></div>',
     '<div style="text-align:left">'
     '<div style="font-size:18px;font-weight:700;color:var(--c1)">'
     'Bạn đã từng mua hàng</div>'
     '<div style="font-size:12px;color:var(--c5);margin-top:var(--s1);'
     'line-height:1.6">Đơn hàng dưới đây gắn với số điện thoại bạn vừa nhập. '
     'Bấm <strong>Đăng ký thành viên</strong> để tiếp tục — thông tin sẽ được '
     'điền sẵn từ đơn.</div></div>'),

    # Bỏ hẳn ô nhập SĐT trong modal. Sau khi luồng đăng nhập đổi (C1 tự đối
    # chiếu SĐT rồi mở modal kèm kết quả), không còn nút nào mở nhánh "gõ số
    # để tra" nữa. Để lại thì bất kỳ ai biết URL cũng tra được họ tên, email,
    # số CCCD và địa chỉ của người khác chỉ bằng một số điện thoại.
    ('        <div style="display:flex;flex-direction:column;gap:var(--s2)">\n'
     '          <label style="font-size:14px;font-weight:600;color:var(--c2)">'
     'Số điện thoại khách hàng đã mua đơn</label>\n'
     '          <input type="text" placeholder="090xxxxxxx" '
     'value="{{orderLookupInput}}" sc-camel-on-change="{{setOrderLookupInput}}" '
     'style="height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
     'border-radius:var(--r-md);font-size:16px" style-focus="border-color:#00ADEE;'
     'box-shadow:0 0 0 3px rgba(0,173,238,.25)">\n'
     '          <sc-if value="{{orderLookupError}}" hint-placeholder-val="{{false}}">\n'
     '            <div style="font-size:12px;color:#E20707">Không tìm thấy đơn hàng '
     'với số điện thoại này. Vui lòng kiểm tra lại.</div>\n'
     '          </sc-if>\n'
     '        </div>\n',
     ''),

    # (10) Tra cứu đơn: hiện kết quả đơn hàng ngay trong modal thay vì nhảy
    # thẳng sang màn đăng ký.
    ('<button sc-camel-on-click="{{submitOrderLookup}}" style="height:46px;'
     'background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);'
     'font-size:16px;font-weight:600;box-shadow:var(--sh)" '
     'style-hover="background:#0099d1">Xác nhận</button>',
     '<sc-if value="{{hasLookupResult}}" hint-placeholder-val="{{false}}">\n'
     '          <div style="border:1px solid rgba(170,170,170,.35);'
     'border-radius:var(--r-md);padding:var(--s6);display:flex;'
     'flex-direction:column;gap:var(--s4);font-size:13px;'
     'background:rgba(170,170,170,.05)">\n'
     '            <div style="font-size:12px;color:var(--c5);text-transform:uppercase;'
     'letter-spacing:.04em">Đơn hàng tìm thấy</div>\n'
     '            <div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Mã đơn</span>'
     '<span style="font-family:monospace;font-weight:700;color:var(--c1)">'
     '{{lookupResult.orderId}}</span></div>\n'
     '            <div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Khách hàng</span>'
     '<span style="font-weight:600;color:var(--c1);text-align:right">'
     '{{lookupResult.buyerName}}</span></div>\n'
     '            <div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Gói</span>'
     '<span style="color:var(--c2);text-align:right">{{lookupResult.pkg}}</span></div>\n'
     '            <div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Số tiền</span>'
     '<span style="font-weight:700;color:var(--c6)">{{lookupResult.amount}}</span></div>\n'
     '            <div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Ngày đặt</span>'
     '<span style="color:var(--c2)">{{lookupResult.date}}</span></div>\n'
     '            <div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Người giới thiệu</span>'
     '<span style="color:var(--c2);text-align:right">{{lookupResult.referrer}}</span></div>\n'
     '            <div style="display:flex;justify-content:space-between;gap:var(--s5);'
     'align-items:center"><span style="color:var(--c5)">Trạng thái</span>'
     '<span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);'
     'font-size:11px;font-weight:600;background:{{lookupResult.badgeBg}};'
     'color:{{lookupResult.badgeColor}}">{{lookupResult.statusLabel}}</span></div>\n'
     '          </div>\n'
     '        </sc-if>\n'
     '        <sc-if value="{{hasLookupResult}}" hint-placeholder-val="{{false}}">\n'
     '          <button sc-camel-on-click="{{lookupContinue}}" style="height:46px;'
     'background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);'
     'font-size:16px;font-weight:600;box-shadow:var(--sh)" '
     'style-hover="background:#0099d1">Đăng ký thành viên</button>\n'
     '        </sc-if>'),

    # (9b) Tiêu đề modal thanh toán thành công kèm lời mời gia nhập.
    ('<div style="font-size:20px;font-weight:700;color:var(--c1)">'
     'Đơn hàng đã được ghi nhận</div>',
     '<div style="font-size:20px;font-weight:700;color:var(--c1);line-height:1.4">'
     'Đơn hàng đã được ghi nhận, mời gia nhập HOMI365</div>'),

    # (9) Đổi tiêu đề modal thanh toán thành công.
    ('Bạn có muốn đăng ký làm seller Homi365 để nhận hoa hồng giới thiệu không?',
     'Bạn có muốn đăng ký làm Thành viên HOMI365 để nhận các ưu đãi không?'),

    # A1: mã giới thiệu của người bán cũng là alias, không còn số 6 chữ số.
    ('<label style="font-size:14px;font-weight:600;color:var(--c2)">Mã giới thiệu</label>'
     '<input type="text" value="923983" readonly="{{true}}"',
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">Mã giới thiệu</label>'
     '<input type="text" value="TTB4123" readonly="{{true}}"'),

    # A3: dòng chào hiện ID thành viên; tên khớp với alias HTMT0083.
    ('<div style="font-size:12px;color:var(--c5)">aff_id: 923983</div>',
     '<div style="font-size:12px;color:var(--c5)">ID: {{refCode}}</div>'),
    ('<div style="font-size:18px;font-weight:700">Chào, Nguyễn Văn A</div>',
     '<div style="font-size:18px;font-weight:700">Chào, Hoàng Thị Mỹ Trinh</div>'),
    ('>LINK BÁN HÀNG CỦA BẠN<', '>LINK GIỚI THIỆU CỦA BẠN<'),
    ('>Link bán hàng của bạn<', '>Link giới thiệu của bạn<'),

    # (8) Ô OTP tự nhảy sang ô kế tiếp khi gõ, Backspace lùi lại.
    ('<input type="text" maxlength="1" style="width:44px;height:52px;'
     'text-align:center;font-size:20px;font-weight:700;'
     'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md)"',
     '<input type="text" maxlength="1" inputmode="numeric" class="otp-box" '
     'style="width:44px;height:52px;text-align:center;font-size:20px;'
     'font-weight:700;border:1px solid rgba(170,170,170,.6);'
     'border-radius:var(--r-md)"'),

    # (1) Tiêu đề màn đăng nhập.
    ('Đăng nhập để quản lý hoa hồng &amp; đơn hàng của bạn',
     'Đăng nhập để xem điểm thưởng và ưu đãi của bạn'),

    # (4) (5) Đổi nhãn ở dashboard.
    ('>Tổng đơn hàng<', '>Tổng đơn bán<'),
    ('>Hoa hồng đang tạm giữ<', '>Khoản ưu đãi đang tạm giữ<'),

    # (7) Mã giới thiệu ở form mua hàng kèm tên người giới thiệu.
    ('<input type="text" value="TTB4123" readonly="{{true}}"',
     '<input type="text" value="HTMT0083 — HOÀNG THỊ MỸ TRINH" readonly="{{true}}"'),

    # (2) Ngày sinh: nhập số, tự chèn dấu /.
    ('placeholder="dd/mm/yyyy" value="{{buyerDob}}" sc-camel-on-change="{{setBuyerDob}}"',
     'placeholder="22/01/1991" inputmode="numeric" maxlength="10" '
     'value="{{buyerDob}}" sc-camel-on-change="{{setBuyerDob}}"'),

    # ----- (11) A2: mọi trường gắn dấu (*), khoá email và SĐT --------------
    # Các nhãn không dấu sao chỉ tồn tại ở A2 (A1 đã có sẵn dấu sao).
    (">Họ và tên</label>", ">Họ và tên (*)</label>"),
    (">Số điện thoại</label>", ">Số điện thoại (*)</label>"),
    (">Email</label>", ">Email (*)</label>"),
    (">Số CCCD</label>", ">Số CCCD (*)</label>"),
    (">Địa chỉ</label>", ">Địa chỉ (*)</label>"),
    (">Tỉnh/Thành phố</label>", ">Tỉnh/Thành phố (*)</label>"),
    (">Phường/Xã</label>", ">Phường/Xã (*)</label>"),
    (">Ngân hàng</label>", ">Ngân hàng (*)</label>"),
    (">Số tài khoản nhận hoa hồng</label>", ">Số tài khoản nhận hoa hồng (*)</label>"),
    # Ngày sinh / Giới tính không có dấu sao ở CẢ A1 lẫn A2 -> neo kèm
    # font-size:16px để chỉ trúng A2.
    ('>Ngày sinh</label><input type="text" placeholder="22/01/1991" '
     'inputmode="numeric" maxlength="10" value="{{buyerDob}}" '
     'sc-camel-on-change="{{setBuyerDob}}" style="height:44px;padding:0 var(--s5);'
     'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:16px"',
     '>Ngày sinh (*)</label><input type="text" placeholder="22/01/1991" '
     'inputmode="numeric" maxlength="10" value="{{buyerDob}}" '
     'sc-camel-on-change="{{setBuyerDob}}" style="height:44px;padding:0 var(--s5);'
     'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:16px"'),

    # Email và SĐT lấy từ đơn hàng, không cho sửa.
    ('<input type="text" placeholder="090xxxxxxx" value="{{buyerPhone}}" '
     'sc-camel-on-change="{{setBuyerPhone}}" style="height:44px;padding:0 var(--s5);'
     'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:16px"',
     '<input type="text" value="{{buyerPhone}}" readonly="{{true}}" '
     'style="height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
     'border-radius:var(--r-md);font-size:16px;background:rgba(170,170,170,.08);'
     'color:var(--c4);cursor:not-allowed"'),
    ('<input type="text" placeholder="email@domain.com" value="{{buyerEmail}}" '
     'sc-camel-on-change="{{setBuyerEmail}}" style="height:44px;padding:0 var(--s5);'
     'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:16px"',
     '<input type="text" value="{{buyerEmail}}" readonly="{{true}}" '
     'style="height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
     'border-radius:var(--r-md);font-size:16px;background:rgba(170,170,170,.08);'
     'color:var(--c4);cursor:not-allowed"'),

    # Ghi chú đầu form: thông tin lấy sẵn từ đơn, sửa được trừ email/SĐT.
    ('<div style="font-size:13px;color:var(--c5);margin-top:var(--s1)">'
     'Bước 1/5 · Thông tin cá nhân &amp; nhận hoa hồng</div></div>',
     '<div style="font-size:13px;color:var(--c5);margin-top:var(--s1)">'
     'Bước 1/5 · Thông tin cá nhân &amp; nhận ưu đãi</div></div>\n'
     '          <div style="border:1px solid rgba(0,173,238,.3);'
     'background:rgba(0,173,238,.06);border-radius:var(--r-md);padding:var(--s6);'
     'display:flex;flex-direction:column;gap:var(--s3);font-size:13px">'
     '<div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Người giới thiệu</span>'
     '<span style="font-weight:700;color:var(--c1);text-align:right">'
     'HOÀNG THỊ MỸ TRINH</span></div>'
     '<div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Mã giới thiệu</span>'
     '<span style="font-weight:700;color:var(--c6);font-family:monospace">'
     'HTMT0083</span></div></div>'),

    # A2 cũng cần Tên chủ tài khoản như form mua hàng.
    ('<div style="font-size:11px;color:var(--c5)">Chỉ hiển thị đầy đủ trong '
     'khu vực quản trị nội bộ.</div></div>',
     '<div style="font-size:11px;color:var(--c5)">Chỉ hiển thị đầy đủ trong '
     'khu vực quản trị nội bộ.</div></div>\n'
     '          <div style="display:flex;flex-direction:column;gap:var(--s2)">'
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">'
     'Tên chủ tài khoản (*)</label>'
     '<input type="text" placeholder="NGUYEN VAN AN" value="{{accountHolder}}" '
     'sc-camel-on-change="{{setAccountHolder}}" style="height:44px;padding:0 var(--s5);'
     'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:16px;'
     'text-transform:uppercase" style-focus="%s">'
     '<div style="font-size:11px;color:var(--c5);line-height:1.5">Viết hoa, không dấu '
     '— hệ thống tự chuẩn hoá khi bạn gõ.</div></div>' % _FOCUS),

    # ----- (12) Ngày cấp / Nơi cấp ngay dưới số CCCD ----------------------
    ('<div style="display:flex;flex-direction:column;gap:var(--s2)">'
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">Địa chỉ (*)</label>'
     '<input type="text" placeholder="Nhập địa chỉ" value="{{buyerAddress}}" '
     'sc-camel-on-change="{{setBuyerAddress}}" style="height:44px;padding:0 var(--s5);'
     'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:16px"',
     '<div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s7)">'
     '<div style="display:flex;flex-direction:column;gap:var(--s2)">'
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">Ngày cấp (*)</label>'
     '<input type="text" placeholder="22/01/2021" inputmode="numeric" maxlength="10" '
     'value="{{cccdIssueDate}}" sc-camel-on-change="{{setCccdIssueDate}}" '
     'style="height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
     'border-radius:var(--r-md);font-size:16px" style-focus="%s"></div>'
     '<div style="display:flex;flex-direction:column;gap:var(--s2)">'
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">Nơi cấp (*)</label>'
     '<input type="text" placeholder="Cục Cảnh sát QLHC về TTXH" '
     'value="{{cccdIssuePlace}}" sc-camel-on-change="{{setCccdIssuePlace}}" '
     'style="height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
     'border-radius:var(--r-md);font-size:16px" style-focus="%s"></div></div>\n'
     '          <div style="display:flex;flex-direction:column;gap:var(--s2)">'
     '<label style="font-size:14px;font-weight:600;color:var(--c2)">Địa chỉ (*)</label>'
     '<input type="text" placeholder="Nhập địa chỉ" value="{{buyerAddress}}" '
     'sc-camel-on-change="{{setBuyerAddress}}" style="height:44px;padding:0 var(--s5);'
     'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:16px"'
     % (_FOCUS, _FOCUS)),

    # ----- (13) Đính kèm ảnh CCCD mặt trước / mặt sau ---------------------
    ('<button sc-camel-on-click="{{regStep1Submit}}" style="height:46px;'
     'background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);'
     'font-size:16px;font-weight:600;box-shadow:var(--sh)" '
     'style-hover="background:#0099d1">Tiếp tục</button>',
     '<div style="height:1px;background:rgba(170,170,170,.25);margin:var(--s2) 0"></div>\n'
     '          <div style="font-size:14px;font-weight:700;color:var(--c1)">'
     'Đính kèm tệp</div>\n'
     '          <div style="font-size:12px;color:var(--c2);line-height:1.7">'
     'Chụp ảnh CCCD từ <strong>bản gốc</strong>, đủ mặt trước và mặt sau: không mất '
     'góc, không chói loá, không che khuất thông tin.</div>\n'
     '          <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s7)">\n'
     '            <label style="border:1px dashed rgba(170,170,170,.6);'
     'border-radius:var(--r-md);padding:var(--s7);display:flex;flex-direction:column;'
     'align-items:center;gap:var(--s2);cursor:pointer;color:var(--c5);text-align:center" '
     'style-hover="border-color:#00ADEE;color:#00ADEE">'
     '<span style="font-size:22px">&#11014;</span>'
     '<span style="font-size:13px;font-weight:600">Ảnh CCCD mặt trước (*)</span>'
     '<span style="font-size:11px">JPG hoặc PNG, tối đa 5MB</span>'
     '<input type="file" accept="image/*" style="display:none"></label>\n'
     '            <label style="border:1px dashed rgba(170,170,170,.6);'
     'border-radius:var(--r-md);padding:var(--s7);display:flex;flex-direction:column;'
     'align-items:center;gap:var(--s2);cursor:pointer;color:var(--c5);text-align:center" '
     'style-hover="border-color:#00ADEE;color:#00ADEE">'
     '<span style="font-size:22px">&#11014;</span>'
     '<span style="font-size:13px;font-weight:600">Ảnh CCCD mặt sau (*)</span>'
     '<span style="font-size:11px">JPG hoặc PNG, tối đa 5MB</span>'
     '<input type="file" accept="image/*" style="display:none"></label>\n'
     '          </div>\n'
     '          <button sc-camel-on-click="{{regStep1Submit}}" style="height:46px;'
     'background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);'
     'font-size:16px;font-weight:600;box-shadow:var(--sh)" '
     'style-hover="background:#0099d1">Tiếp tục</button>'),

    # ----- (14) Nội dung điều khoản tham gia ------------------------------
    # (14) + rà soát pháp lý 10/09: hiển thị TOÀN VĂN T&C, buộc cuộn hết mới
    # bật ô đồng ý, và ghi lại bằng chứng chấp thuận.
    # Lưu ý: bản vá "Medigo -> HOMI365" chạy trước nên neo phải dùng chữ mới.
    # Khung điều khoản: cao hơn, gắn class để JS bắt sự kiện cuộn.
    ('height:180px;overflow:auto;font-size:13px;line-height:1.6;color:var(--c4)">',
     'height:280px;overflow-y:auto;font-size:13px;line-height:1.75;'
     'color:var(--c4)" class="tnc-doc">'),
    # Thay đoạn tóm tắt bằng toàn văn, và thêm dòng nhắc cuộn hết.
    ('            Điều khoản chương trình affiliate HOMI365 — Homi365. Bằng việc '
     'tích chọn xác nhận, bạn đồng ý với chính sách hoa hồng, quy định về tuyến '
     'trên/tuyến dưới, và các điều kiện rút tiền được Homi365 quy định. Nội dung '
     'đầy đủ do bộ phận Pháp lý cung cấp trước khi go‑live.\n'
     '          </div>',
     '            ' + TNC_TOP + TNC_BODY + '\n          </div>' + TNC_HINT),
    # Nhãn checkbox phải nằm trong MỘT thẻ span — label là flex nên mỗi thẻ con
    # sẽ thành một cột riêng, chữ bị vỡ thành nhiều khối hẹp.
    ('Tôi đã đọc và đồng ý với điều khoản tham gia chương trình affiliate HOMI365.',
     '<span style="line-height:1.6">Tôi đã đọc và đồng ý với '
     '<strong>Chính sách ưu đãi thành viên HOMI365</strong> (phiên bản 1.0, hiệu lực '
     'từ 01/10/2026), cùng Điều kiện giao dịch chung và Chính sách bảo mật, bảo vệ '
     'dữ liệu cá nhân của HOMI365.</span>'),
    ('<input type="checkbox" checked="{{tncChecked}}" sc-camel-on-change="{{toggleTnc}}" '
     'style="width:18px;height:18px;margin-top:2px;accent-color:#00ADEE">',
     '<input type="checkbox" class="tnc-agree" disabled checked="{{tncChecked}}" '
     'sc-camel-on-change="{{toggleTnc}}" '
     'style="width:18px;height:18px;margin-top:2px;accent-color:#00ADEE;'
     'flex:none;opacity:.4;cursor:not-allowed">'),

    # Bộ lọc hạng ở B2 dùng đủ 6 hạng chính thức, không dịch sang tiếng Việt.
    ('<option>Tất cả hạng</option><option>Đồng</option><option>Bạc</option>'
     '<option>Vàng</option>',
     '<option>Tất cả hạng</option><option>Copper</option><option>Silver</option>'
     '<option>Gold</option><option>Diamond</option><option>Titanium</option>'
     '<option>Lithium</option>'),

    # A3: bỏ nút "Xem: Agent mới / Đã tính hoa hồng" — đó là công tắc để trình
    # diễn, agent thật không được thấy. Hai trạng thái vẫn mở được từ index.
    ('<button sc-camel-on-click="{{toggleAgentStage}}" style="font-size:11px;'
     'font-weight:600;color:var(--c6);background:rgba(0,173,238,.08);'
     'border:1px solid rgba(0,173,238,.3);border-radius:var(--r-xl);'
     'padding:var(--s2) var(--s4)">{{agentStageToggleLabel}}</button>', ''),

    # Modal rút tiền: hiện đủ tên chủ tài khoản / ngân hàng / số tài khoản.
    ('<div style="display:flex;justify-content:space-between"><span style="color:var(--c5)">'
     'Nhận vào</span><span style="font-weight:600">Vietcombank</span></div>',
     '<div style="font-size:12px;color:var(--c5);text-transform:uppercase;'
     'letter-spacing:.04em;margin-bottom:var(--s1)">Tài khoản nhận tiền</div>'
     '<div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Tên chủ tài khoản</span>'
     '<span style="font-weight:600;text-align:right">{{withdrawHolder}}</span></div>'
     '<div style="display:flex;justify-content:space-between;gap:var(--s5)">'
     '<span style="color:var(--c5)">Ngân hàng</span>'
     '<span style="font-weight:600;text-align:right">{{withdrawBank}}</span></div>'),
    ('<span style="font-weight:600;font-family:monospace">{{buyerBankAccount}}</span>',
     '<span style="font-weight:600;font-family:monospace">{{withdrawAccount}}</span>'),

    # (2) B2 chỉ giữ MỘT link, đổi tên thành "Link giới thiệu".
    ('<div>Tên</div><div>Liên hệ</div><div>Mã TV</div><div>Link form</div>'
     '<div>Link đăng nhập</div><div>Tuyến trên</div>',
     '<div>Tên</div><div>Liên hệ</div><div>Mã TV</div><div>Link giới thiệu</div>'
     '<div>Tuyến trên</div>'),
    ('grid-template-columns:1.3fr 1fr .8fr 1fr 1.1fr .9fr .6fr .8fr .8fr .6fr;'
     'min-width:1080px',
     'grid-template-columns:1.3fr 1fr .8fr 1.2fr .9fr .7fr .9fr .9fr .6fr;'
     'min-width:1020px'),
    ('                <div title="{{m.loginLink}}" style="position:relative;display:flex;'
     'align-items:center;gap:4px;color:var(--c6);font-family:monospace;font-size:12px;'
     'overflow:hidden" style-hover="background:rgba(0,173,238,.08)">\n'
     '                  <span style="overflow:hidden;text-overflow:ellipsis;'
     'white-space:nowrap">{{m.loginLinkShort}}</span>\n'
     '                  <button sc-camel-on-click="{{m.copyLoginLink}}" '
     'title="Sao chép link" style="flex:none;width:20px;height:20px;border:none;'
     'background:none;color:var(--c6);cursor:pointer;opacity:0;font-size:13px;'
     'line-height:1" style-hover="opacity:1">{{m.loginLinkCopyIcon}}</button>\n'
     '                </div>\n', ''),

    # (6) Ô thống kê kho: 3 -> 5 trạng thái.
    ('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s5)">\n'
     '            <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Sẵn hàng</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{stockAvailable}}</div></div>\n'
     '            <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Đã gán đơn hàng</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{stockAssigned}}</div></div>\n'
     '            <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Đã kích hoạt</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{stockActivated}}</div></div>',
     '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:var(--s5)">\n'
     '            <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Nhập kho</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{stockReceived}}</div></div>\n'
     '            <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Sẵn hàng</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{stockAvailable}}</div></div>\n'
     '            <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Đã gán đơn hàng</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{stockAssigned}}</div></div>\n'
     '            <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Xuất kho</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{stockShipped}}</div></div>\n'
     '            <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Giao thành công</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{stockDelivered}}</div></div>'),

    # Ngăn chi tiết thiết bị: bổ sung mã vận đơn.
    ('<div style="display:flex;justify-content:space-between"><span style="color:var(--c5)">'
     'Seller</span><span style="font-weight:600">{{selectedStock.seller}}</span></div>',
     '<div style="display:flex;justify-content:space-between"><span style="color:var(--c5)">'
     'Thành viên</span><span style="font-weight:600">{{selectedStock.seller}}</span></div>'
     '<div style="display:flex;justify-content:space-between"><span style="color:var(--c5)">'
     'Mã vận đơn</span><span style="font-weight:600;font-family:monospace">'
     '{{selectedStock.tracking}}</span></div>'),

    # (16) B3: thêm 3 cột tiền và một hàng tổng ngay dưới tiêu đề.
    ('<div>Seller</div><div>Số tiền</div><div>Ngày yêu cầu</div>'
     '<div>Số tài khoản nhận</div><div>Tên ngân hàng</div><div>Chi nhánh</div>'
     '<div>Trạng thái</div><div></div>\n            </div>',
     '<div>Thành viên</div><div>Khoản thưởng hiện tại</div><div>Yêu cầu rút tiền</div>'
     '<div>Số dư còn lại</div><div>Ngày yêu cầu</div><div>Số tài khoản nhận</div>'
     '<div>Tên ngân hàng</div><div>Chi nhánh</div><div>Trạng thái</div><div></div>\n'
     '            </div>\n'
     '            <div style="display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr .9fr 1.1fr 1fr .9fr .9fr .6fr;'
     'min-width:1320px;padding:var(--s5) var(--s6);font-size:13px;font-weight:700;'
     'color:var(--c1);background:rgba(0,173,238,.06);'
     'border-top:1px solid rgba(170,170,170,.2)">'
     '<div>TỔNG</div><div>{{sumRewardLabel}}</div><div>{{sumRequestLabel}}</div>'
     '<div>{{sumRemainLabel}}</div><div></div><div></div><div></div><div></div>'
     '<div></div><div></div></div>'),
    ('<div style="font-weight:600">{{w.seller}}</div>\n'
     '                <div style="font-weight:700">{{w.amount}}</div>\n'
     '                <div style="color:var(--c5)">{{w.date}}</div>',
     '<div style="font-weight:600">{{w.seller}}</div>\n'
     '                <div style="color:var(--c4)">{{w.rewardLabel}}</div>\n'
     '                <div style="font-weight:700">{{w.amount}}</div>\n'
     '                <div style="color:var(--c4)">{{w.remainLabel}}</div>\n'
     '                <div style="color:var(--c5)">{{w.date}}</div>'),
    ('grid-template-columns:1.2fr 1fr 1fr 1fr 1fr 1fr .9fr 1fr;min-width:920px',
     'grid-template-columns:1.2fr 1fr 1fr 1fr .9fr 1.1fr 1fr .9fr .9fr .6fr;'
     'min-width:1320px'),

    # (15) Nội dung chuyển khoản mặc định ở ngăn chi tiết rút tiền.
    ('<div style="display:flex;justify-content:space-between">'
     '<span style="color:var(--c5)">Chủ tài khoản</span>'
     '<span style="font-weight:600">{{selectedWithdrawal.accountHolder}}</span></div>',
     '<div style="display:flex;justify-content:space-between">'
     '<span style="color:var(--c5)">Chủ tài khoản</span>'
     '<span style="font-weight:600">{{selectedWithdrawal.accountHolder}}</span></div>'
     '<div style="border-top:1px solid rgba(170,170,170,.25);margin-top:var(--s3);'
     'padding-top:var(--s4);display:flex;flex-direction:column;gap:var(--s2)">'
     '<span style="color:var(--c5);font-size:12px">Nội dung chuyển khoản</span>'
     '<span style="font-weight:600;font-family:monospace;font-size:12px;'
     'word-break:break-all;background:rgba(170,170,170,.08);'
     'border-radius:var(--r-sm);padding:var(--s4)">'
     'Rut khoan thuong tich diem ct uu dai khach hang</span></div>'),

    # (3) (7) Cột "Seller" -> "Thành viên" ở màn rút tiền và màn kho.
    ('<div>Seller</div>', '<div>Thành viên</div>'),
    ('>Seller<', '>Thành viên<'),

    # ----- (15) B2: hiện mã tuyến trên cạnh tên tuyến trên ----------------
    ('<div style="color:var(--c4);overflow:hidden;text-overflow:ellipsis;'
     'white-space:nowrap">{{m.upline}}</div>',
     '<div style="color:var(--c4);overflow:hidden;text-overflow:ellipsis;'
     'white-space:nowrap">{{m.upline}}'
     '<span style="display:block;font-size:11px;color:var(--c5);font-family:monospace">'
     '{{m.uplineCode}}</span></div>'),

    # ----- (16) B4: thêm cột Ngày kích hoạt / Ngày hết hiệu lực / Mã vận đơn
    # LƯU Ý NEO: bản vá đổi "Seller" -> "Thành viên" nằm TRƯỚC trong danh sách
    # nên tới lượt bản vá này, chuỗi đã là "Thành viên". Neo theo "Seller" sẽ
    # trượt im lặng — đúng lỗi làm hàng tiêu đề thiếu 3 cột trên bản deploy.
    # Nhãn dùng "Ngày kích hoạt" cho khớp với bảng đơn hàng B6.
    ('<div>Mã sản phẩm</div><div>Mã kích hoạt</div><div>Đơn hàng gắn</div>'
     '<div>Thành viên</div><div>Ngày nhập kho</div><div>Trạng thái</div><div></div>',
     '<div>Mã sản phẩm</div><div>Mã kích hoạt</div><div>Đơn hàng gắn</div>'
     '<div>Thành viên</div><div>Ngày nhập kho</div><div>Ngày kích hoạt</div>'
     '<div>Ngày hết hiệu lực</div><div>Mã vận đơn</div><div>Trạng thái</div><div></div>'),
    ('<div style="color:var(--c5)">{{p.stockedAt}}</div>',
     '<div style="color:var(--c5)">{{p.stockedAt}}</div>\n'
     '                <div style="color:var(--c4)">{{p.activeFrom}}</div>\n'
     '                <div style="color:var(--c4)">{{p.activeTo}}</div>\n'
     '                <div style="color:var(--c4);font-family:monospace">{{p.tracking}}</div>'),
    # Lưới bảng kho: 7 cột -> 10 cột.
    ('grid-template-columns:1fr 1.4fr 1fr 1fr 1fr .9fr 1fr;min-width:900px',
     'grid-template-columns:1fr 1.2fr .9fr 1fr .9fr .9fr .9fr 1fr 1.1fr .8fr;'
     'min-width:1380px'),

    # Chèn màn Đơn hàng (B6), Sản phẩm (B5), Nhật ký (B8) trước khối B4.
    ("      <!-- B4 WAREHOUSE -->",
     B6_ORDERS + B5_PRODUCTS + B8_AUDIT + "      <!-- B4 WAREHOUSE -->"),
    # B4: thêm nút Import / Thêm hàng cạnh nút xuất Excel.
    # Neo phải gồm CẢ tiêu đề "Quản lý kho hàng" — nút "Xuất file Excel" xuất
    # hiện y hệt ở B3 (và ở B6 mới thêm), thay theo chuỗi ngắn sẽ dính cả ba.
    ('<div><div style="font-size:24px;font-weight:700">Quản lý kho hàng</div>'
     '<div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">'
     '{{stockTotal}} sản phẩm · mỗi sản phẩm gắn 1 mã kích hoạt</div></div>\n'
     '            <button style="%s" style-hover="background:rgba(170,170,170,.08)">'
     'Xuất file Excel</button>' % _BTN_GHOST,
     '<div><div style="font-size:24px;font-weight:700">Quản lý kho hàng</div>'
     '<div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">'
     '{{stockTotal}} sản phẩm · mỗi sản phẩm gắn 1 mã kích hoạt</div></div>\n'
     '            <div style="display:flex;gap:var(--s3);flex-wrap:wrap">'
     '<button style="%s" style-hover="background:rgba(170,170,170,.08)">'
     'Xuất file Excel</button>'
     '<button sc-camel-on-click="{{openImportStock}}" style="%s" '
     'style-hover="background:rgba(170,170,170,.08)">Import hàng loạt</button>'
     '<button sc-camel-on-click="{{openAddStock}}" style="%s" '
     'style-hover="background:#0099d1">+ Thêm hàng vào kho</button></div>'
     % (_BTN_GHOST, _BTN_GHOST, _BTN_PRIMARY)),
]

B7_ADMIN_USERS = """      <!-- B7 ADMIN USERS (bổ sung 7.9.1, không có trong mockup KH) -->
      <!-- 7.9.1 AC: Admin Specialist KHÔNG được truy cập màn này -->
      <sc-if value="{{isB7Denied}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;justify-content:center;padding:var(--s11) var(--s7)">
          <div style="width:100%%;max-width:460px;background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s10);display:flex;flex-direction:column;gap:var(--s5);text-align:center">
            <div style="font-size:40px;font-weight:900;color:var(--c7);letter-spacing:.04em">403</div>
            <div style="font-size:18px;font-weight:700;color:var(--c1)">Không có quyền truy cập</div>
            <div style="font-size:13px;color:var(--c2);line-height:1.7">Màn <strong>Tài khoản admin</strong> chỉ dành cho <strong>Head Admin</strong>. Tài khoản của bạn đang ở vai <strong>Admin Specialist</strong>.</div>
            <div style="font-size:12px;color:var(--c5);line-height:1.6">Cần tạo hoặc đổi vai trò một tài khoản admin? Liên hệ Head Admin.</div>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{isB7Allowed}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;flex-direction:column;gap:var(--s7)">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
            <div><div style="font-size:24px;font-weight:700">Tài khoản admin</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">{{adminUserCount}} tài khoản · mỗi tài khoản gán đúng 1 vai trò</div></div>
            <button sc-camel-on-click="{{openAdminUserForm}}" style="%(btn)s" style-hover="background:#0099d1">+ Thêm tài khoản</button>
          </div>

          <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);overflow:hidden">
            <table style="width:100%%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="background:rgba(170,170,170,.08);text-align:left">
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Họ tên</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Email đăng nhập</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Vai trò</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Trạng thái</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5);width:170px"></th>
                </tr>
              </thead>
              <tbody>
                <sc-for list="{{adminUsers}}" as="u" hint-placeholder-count="3">
                  <tr style="border-top:1px solid rgba(170,170,170,.2)">
                    <td style="padding:var(--s5);font-weight:600;color:var(--c1)">{{u.name}}</td>
                    <td style="padding:var(--s5);color:var(--c2);font-family:monospace">{{u.email}}</td>
                    <td style="padding:var(--s5)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{u.roleBg}};color:{{u.roleColor}}">{{u.roleLabel}}</span></td>
                    <td style="padding:var(--s5)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{u.badgeBg}};color:{{u.badgeColor}}">{{u.statusLabel}}</span></td>
                    <td style="padding:var(--s5)">
                      <div style="display:flex;gap:var(--s3)">
                        <button sc-camel-on-click="{{u.onEdit}}" style="height:32px;padding:0 var(--s5);background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:12px;font-weight:600;color:var(--c2)" style-hover="background:rgba(170,170,170,.08)">Sửa</button>
                        <button sc-camel-on-click="{{u.onToggleLock}}" style="{{u.lockStyle}}">{{u.lockLabel}}</button>
                      </div>
                    </td>
                  </tr>
                </sc-for>
              </tbody>
            </table>
          </div>

          <div style="font-size:12px;color:var(--c5);line-height:1.7;background:rgba(170,170,170,.05);border-radius:var(--r-md);padding:var(--s6)">
            <strong style="color:var(--c2)">Admin Specialist</strong> làm bước 1 của mọi quy trình duyệt 2 lớp: xác nhận tiền về của đơn hàng, duyệt hồ sơ thành viên, duyệt yêu cầu rút tiền.<br>
            <strong style="color:var(--c2)">Head Admin</strong> làm bước 2 và là người duy nhất được kích hoạt tài khoản, cấp mã kích hoạt, đánh dấu đã chi trả, và quản lý chính màn này.
          </div>
        </div>
      </sc-if>

      <sc-if value="{{showAdminUserForm}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:center;justify-content:center;z-index:220;padding:var(--s7)">
          <div style="width:100%%;max-width:430px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
              <div style="font-size:18px;font-weight:700;color:var(--c1)">{{adminUserFormTitle}}</div>
              <button sc-camel-on-click="{{closeAdminUserForm}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Họ tên (*)</label>
              <input type="text" value="{{adminUserFormName}}" placeholder="Nguyễn Thị Trinh" style="%(inp)s" style-focus="%(focus)s">
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Email đăng nhập (*)</label>
              <input type="text" value="{{adminUserFormEmail}}" placeholder="trinh@homi365.com.vn" style="%(inp)s;font-family:monospace" style-focus="%(focus)s">
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Vai trò (*)</label>
              <sc-raw-select style="%(inp)s;color:var(--c2);background:var(--c12)">
                <option>Admin Specialist</option>
                <option>Head Admin</option>
              </sc-raw-select>
              <div style="font-size:11px;color:var(--c5);line-height:1.6">Mỗi tài khoản chỉ được gán đúng một vai trò. Đổi vai trò có hiệu lực ở lần đăng nhập kế tiếp.</div>
            </div>
            <div style="display:flex;gap:var(--s5)">
              <button sc-camel-on-click="{{closeAdminUserForm}}" style="flex:1;height:44px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c2)">Huỷ</button>
              <button sc-camel-on-click="{{closeAdminUserForm}}" style="flex:1;height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Lưu tài khoản</button>
            </div>
          </div>
        </div>
      </sc-if>

""" % {"btn": _BTN_PRIMARY, "inp": _INP, "focus": _FOCUS}

# B7 khai báo sau khối BG_PATCHES += ở trên nên phải nối riêng ở đây.
# Neo vẫn còn trong chuỗi thay thế của lần trước, nên lần này chèn tiếp được.
BG_PATCHES.append(("      <!-- B4 WAREHOUSE -->",
                   B7_ADMIN_USERS + "      <!-- B4 WAREHOUSE -->"))

KEEP = {
    "#ED1C24": "logo Techcombank",
    "#00A19A": "logo napas247",
    "#003DA5": "logo napas247",
}


def recolor(s):
    for old, new in COLORS:
        s = s.replace(old, new)
    return s


# (13) Đổi tên hai vai quản trị. Thay ở CẢ markup lẫn JS, thay toàn bộ chứ
# không chỉ lần đầu — nên tách riêng khỏi hai bảng vá theo neo.
# Thứ tự quan trọng: "Head Admin" phải đi trước vì nó chứa chữ "Admin".
RENAMES = [
    ("Head Admin", "Head"),
    ("Admin Specialist", "Admin"),
    # Nhãn nút còn ghi trơ "(Specialist)" chứ không kèm chữ Admin.
    ("(Specialist)", "(Admin)"),
    ("Chờ Manager duyệt", "Chờ Head duyệt"),
    ("Manager duyệt thành viên", "Head duyệt thành viên"),
]


def rename_roles(s):
    for old, new in RENAMES:
        s = s.replace(old, new)
    return s


# ============================================================================
# 2. VỊ TRÍ CÁC KHỐI TRONG template.html (số dòng, 1-based)
# ============================================================================

L_FONTS = (12, 731)      # nội dung <style> chứa @font-face
L_BASE = (734, 738)      # nội dung <style> reset
L_ROOTDIV = 741          # <div style="--c1:…"> — nơi khai báo biến
L_TOPBAR_WRAP = 744      # thẻ <div> bọc thanh trên (giữ nguyên style)
L_SCRIPT = (1611, 2114)  # cả <script type="text/x-dc"> … </script>

# Khối bắt đầu tại dòng nào (nếu là dòng comment thì <sc-if> nằm ngay sau).
# (18) Hộp thoại cập nhật cấp — chèn ngay trước cụm modal duyệt/từ chối
# sẵn có của mockup. Trình và duyệt làm ngoài hệ thống, ở đây chỉ ghi nhận.
_RK_INP = ('height:40px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
           'border-radius:var(--r-md);font-size:13px')
RANK_MODALS = """  <!-- MODAL: cập nhật cấp thành viên (bổ sung 17/09) -->
  <sc-if value="{{showRankEdit}}" hint-placeholder-val="{{false}}">
    <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:flex-start;justify-content:center;z-index:260;padding:var(--s7);overflow-y:auto">
      <div style="width:100%;max-width:440px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25);margin:var(--s8) 0">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:var(--s5)">
          <div>
            <div style="font-size:18px;font-weight:700;color:var(--c1)">Cập nhật cấp</div>
            <div style="font-size:12px;color:var(--c5);margin-top:var(--s1);line-height:1.6">{{rankEditName}} · đang ở cấp <strong>{{rankEditCurrent}}</strong></div>
          </div>
          <button sc-camel-on-click="{{closeRankEdit}}" style="background:none;border:none;font-size:18px;color:var(--c5);flex:none">&#10005;</button>
        </div>

        <div style="font-size:12px;color:var(--c4);background:rgba(0,173,238,.07);border:1px solid rgba(0,173,238,.3);border-radius:var(--r-md);padding:var(--s4) var(--s5);line-height:1.6">Chọn đúng cấp đã được duyệt trong phiếu. Hệ thống không xét duyệt lại — lưu là áp dụng ngay.</div>

        <div style="display:flex;flex-direction:column;gap:var(--s2)">
          <div style="font-size:13px;font-weight:600;color:var(--c2)">Cấp đã được duyệt</div>
          <sc-for list="{{rankOptions}}" as="ro" hint-placeholder-count="6">
            <button sc-camel-on-click="{{ro.onClick}}" disabled="{{ro.disabled}}" style="{{ro.style}}"><span>{{ro.name}}</span><span style="font-size:11px;text-align:right;line-height:1.5">{{ro.note}}</span></button>
          </sc-for>
          <div style="font-size:11px;color:var(--c5);line-height:1.6">Chỉ đổi cấp của riêng thành viên này — tuyến dưới giữ nguyên. Cấp bị làm mờ là cấp phá vỡ trật tự tuyến; gặp trường hợp này phải trình lại bên ngoài, không tự phá rào.</div>
        </div>

        <div style="display:flex;flex-direction:column;gap:var(--s4)">
          <div style="font-size:13px;font-weight:600;color:var(--c2)">Minh chứng phê duyệt (bắt buộc)</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s5)">
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;color:var(--c5)">Số phiếu / mã email</label><input type="text" placeholder="PD-2026-014" value="{{rankDocNo}}" sc-camel-on-change="{{setRankDocNo}}" style="RKINP" style-focus="border-color:#00ADEE;box-shadow:0 0 0 3px rgba(0,173,238,.25)"></div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;color:var(--c5)">Ngày duyệt</label><input type="text" placeholder="dd/mm/yyyy" value="{{rankDocDate}}" sc-camel-on-change="{{setRankDocDate}}" style="RKINP" style-focus="border-color:#00ADEE;box-shadow:0 0 0 3px rgba(0,173,238,.25)"></div>
          </div>
          <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:12px;color:var(--c5)">Người duyệt</label><input type="text" placeholder="Họ tên người đã duyệt" value="{{rankApprover}}" sc-camel-on-change="{{setRankApprover}}" style="RKINP" style-focus="border-color:#00ADEE;box-shadow:0 0 0 3px rgba(0,173,238,.25)"></div>
          <div style="display:flex;flex-direction:column;gap:var(--s2)">
            <label style="font-size:12px;color:var(--c5)">File minh chứng (ảnh chụp email / phiếu duyệt đã ký)</label>
            <label style="border:1px dashed rgba(170,170,170,.6);border-radius:var(--r-md);padding:var(--s6);display:flex;align-items:center;justify-content:center;gap:var(--s3);cursor:pointer;color:var(--c5);font-size:13px;font-weight:600;text-align:center" style-hover="border-color:#00ADEE;color:#00ADEE">
              <span style="font-size:18px">&#11014;</span> Chọn file từ thiết bị
              <input type="file" accept="image/*,.pdf,.eml,.msg" sc-camel-on-change="{{setRankDocFile}}" style="display:none">
            </label>
            <sc-if value="{{hasRankDocFile}}" hint-placeholder-val="{{false}}">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:var(--s4);background:rgba(154,163,176,.1);border-radius:var(--r-md);padding:var(--s3) var(--s5);font-size:12px;color:var(--c2)"><span style="font-family:monospace;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{rankDocFile}}</span><button sc-camel-on-click="{{clearRankDocFile}}" style="background:none;border:none;color:var(--c5);font-size:14px;flex:none;cursor:pointer">&#10005;</button></div>
            </sc-if>
            <div style="font-size:11px;color:var(--c5);line-height:1.6">Ảnh, PDF hoặc file email, tối đa 10MB. Không bắt buộc, nhưng nên có — ba trường phía trên chỉ là số hiệu, file mới là bằng chứng.</div>
          </div>
        </div>

        <div style="display:flex;gap:var(--s3)">
          <button sc-camel-on-click="{{closeRankEdit}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Huỷ</button>
          <button sc-camel-on-click="{{submitRankEdit}}" disabled="{{rankSubmitDisabled}}" style="{{rankSubmitStyle}}">Lưu &amp; áp dụng</button>
        </div>
      </div>
    </div>
  </sc-if>

""".replace("RKINP", _RK_INP)

BG_PATCHES.append(
    ("  <!-- MODAL: approve/reject/paid confirm -->",
     RANK_MODALS + "  <!-- MODAL: approve/reject/paid confirm -->"))


BLOCKS = {
    "A1": 754, "QR": 839, "PAYOK": 878, "LOOKUP": 893, "BLOCKED": 912,
    "A2": 922, "A3": 1040, "WDFORM": 1100, "WDOK": 1125,
    "C1": 1136, "B1": 1244, "ADMIN": 1259,
    "SLIDE_MEMBER": 1412, "SLIDE_STOCK": 1458, "SLIDE_WD": 1487,
    "MODALS": 1544,
}

# ============================================================================
# 3. DANH SÁCH MÀN HÌNH
# ============================================================================

FILES = {
    "A1": "a1-buy.html", "A2": "a2-register.html", "A3": "a3-dashboard.html",
    "C1": "c1-login.html", "B1": "b1-admin-login.html",
    "B2": "b2-members.html", "B3": "b3-withdrawals.html", "B4": "b4-warehouse.html",
    "B5": "b5-products.html", "B6": "b6-orders.html",
    "B7": "b7-admin-users.html", "B8": "b8-audit-log.html",
    # (UAT 02/10) màn mới Xét thăng / hạ cấp — xem tools/update_uat0210.py
    "B9": "b9-rank-review.html",
}
ADMIN_CODES = ("B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9")   # B9: sau UAT 02/10

ADMIN_BLOCKS = ["ADMIN", "SLIDE_MEMBER", "SLIDE_WD", "SLIDE_STOCK", "MODALS"]

SCREENS = [
    {
        "code": "A1", "title": "A1 · Thông tin nhận hàng", "group": "Người mua",
        # Modal tra cứu đơn (LOOKUP) và modal tuyến trên bị chặn (BLOCKED) đã
        # chuyển hẳn sang C1: từ khi luồng đăng nhập đổi, A1 không còn nút nào
        # mở chúng, chỉ gõ hash mới vào được.
        "blocks": ["A1", "QR", "PAYOK"],
        "states": [
            ("", "Mặc định — form mua hàng", {}),
            ("qr", "Modal quét QR thanh toán", {"showQRPayment": True}),
            ("thanh-toan-ok", "Modal thanh toán thành công", {"showPaymentSuccess": True}),
            ("loi-duong-truyen", "Lỗi đường truyền — cho gửi lại yêu cầu",
             {"buyTcChecked": True, "payStage": "timeout"}),
        ],
    },
    {
        "code": "A2", "title": "A2 · Đăng ký Agent", "group": "Người mua",
        "blocks": ["A2", "BLOCKED"],
        "states": [
            ("", "Bước 1 — thông tin", {"regStep": 1}),
            ("buoc-2", "Bước 2 — xác thực OTP", {"regStep": 2}),
            ("buoc-3", "Bước 3 — đặt mật khẩu", {"regStep": 3}),
            ("buoc-4", "Bước 4 — điều khoản", {"regStep": 4}),
            ("buoc-5", "Bước 5 — hoàn tất", {"regStep": 5}),
        ],
    },
    {
        "code": "A3", "title": "A3 · Dashboard thành viên", "group": "Thành viên",
        "blocks": ["A3", "WDFORM", "WDOK"],
        "states": [
            ("", "Agent mới — chưa có hoa hồng", {"agentStage": "new"}),
            ("da-tinh-hh", "Agent đang hoạt động", {"agentStage": "active"}),
            ("rut-tien", "Form yêu cầu rút tiền", {"agentStage": "active", "showWithdrawForm": True}),
            ("rut-tien-ok", "Rút tiền — gửi thành công", {"agentStage": "active", "showWithdrawSuccess": True}),
        ],
    },
    {
        "code": "C1", "title": "C1 · Đăng nhập thành viên", "group": "Thành viên",
        # BLOCKED đi kèm LOOKUP: bấm "Đăng ký thành viên" mà người giới thiệu
        # hạng Copper thì mở modal chặn. Trước đây khối này chỉ có ở A1 nên
        # trên C1 nhánh đó bấm xong không hiện gì.
        "blocks": ["C1", "LOOKUP", "BLOCKED"],
        "states": [
            ("", "Bước 1 — nhập số điện thoại", {"agentLoginStep": "login"}),
            ("mat-khau", "Bước 2 — nhập mật khẩu", {"agentLoginStep": "login",
                                                     "agentPhone": "0901234567",
                                                     "loginPhoneChecked": True}),
            ("chua-du-dk", "SĐT chưa mua hàng — chưa đủ điều kiện",
             {"agentLoginStep": "login", "agentPhone": "0900000000",
              "loginNotEligible": True}),
            ("otp", "Xác thực OTP", {"agentLoginStep": "otp"}),
            ("quen-sdt", "Quên mật khẩu — nhập SĐT", {"agentLoginStep": "forgot_phone"}),
            ("quen-otp", "Quên mật khẩu — OTP", {"agentLoginStep": "forgot_otp"}),
            ("quen-dat-lai", "Quên mật khẩu — đặt lại", {"agentLoginStep": "forgot_reset"}),
            ("quen-ok", "Quên mật khẩu — thành công", {"agentLoginStep": "forgot_success"}),
            ("tuyen-tren-chan", "Modal tuyến trên bị chặn",
             {"agentLoginStep": "login", "showUplineBlockedModal": True}),
        ],
    },
    {
        "code": "B1", "title": "B1 · Đăng nhập quản trị", "group": "Quản trị",
        "blocks": ["B1"],
        "states": [("", "Đăng nhập admin", {})],
    },
    {
        "code": "B2", "title": "B2 · Thành viên", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách thành viên", {}),
            ("chi-tiet", "Ngăn chi tiết thành viên", {"selectedMemberId": 6}),
            ("duyet", "Modal duyệt hồ sơ", {"selectedMemberId": 6,
                                            "actionModal": {"type": "approve", "kind": "member", "id": 6}}),
            ("tu-choi", "Modal từ chối hồ sơ", {"selectedMemberId": 6,
                                                "actionModal": {"type": "reject", "kind": "member", "id": 6}}),
            # (18) Cập nhật cấp theo phiếu duyệt ngoài. Chọn Lê Văn Cường
            # (id 2) vì có cả tuyến trên (Trần Thị Bích · Silver) lẫn tuyến
            # dưới (Ngô Thị Em · Copper) — thấy được cả trần lẫn sàn.
            ("cap-nhat-cap", "Modal cập nhật cấp theo phiếu duyệt",
             {"selectedMemberId": 2, "rankEditId": 2, "rankEditChoice": "Copper"}),
            ("da-cap-nhat-cap", "Hồ sơ đã cập nhật cấp — xem lịch sử",
             {"selectedMemberId": 2, "rankOverrides": {"2": "Silver"},
              "rankLogs": {"2": [{
                  "label": "Copper → Silver · phiếu PD-2026-014 ngày 16/09/2026"
                           " · duyệt: Phùng Thị Thúy Linh"
                           " · file: PD-2026-014-da-ky.pdf",
                  "time": "16/09/2026 14:20"}]}}),
        ],
    },
    {
        "code": "B3", "title": "B3 · Yêu cầu rút tiền", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách yêu cầu", {}),
            ("chi-tiet", "Ngăn chi tiết yêu cầu", {"selectedWithdrawalId": 1}),
            ("duyet", "Modal duyệt rút tiền", {"selectedWithdrawalId": 1,
                                               "actionModal": {"type": "approve", "kind": "withdrawal", "id": 1}}),
            ("tu-choi", "Modal từ chối rút tiền", {"selectedWithdrawalId": 1,
                                                   "actionModal": {"type": "reject", "kind": "withdrawal", "id": 1}}),
            ("da-chi-tra", "Modal đánh dấu đã chi trả", {"selectedWithdrawalId": 3,
                                                         "actionModal": {"type": "paid", "kind": "withdrawal", "id": 3}}),
        ],
    },
    {
        "code": "B4", "title": "B4 · Quản lý kho hàng", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách kho", {}),
            ("chi-tiet", "Ngăn chi tiết thiết bị", {"selectedStockId": 3}),
            ("them-hang", "Modal thêm hàng vào kho", {"showAddStock": True}),
            ("import", "Modal import hàng loạt", {"showImportStock": True}),
        ],
    },
    {
        "code": "B6", "title": "B6 · Quản lý đơn hàng", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách đơn hàng", {}),
            ("cho-doi-soat", "Chi tiết đơn chờ đối soát", {"selectedOrderId": "DH923983"}),
            ("cho-head", "Chi tiết đơn chờ Head Admin", {"selectedOrderId": "DH100511"}),
            ("da-thanh-toan", "Chi tiết đơn đã cấp mã", {"selectedOrderId": "DH100234"}),
            ("head", "Xem với vai Head Admin", {"adminRole": "head",
                                                "selectedOrderId": "DH100511"}),
        ],
    },
    {
        "code": "B7", "title": "B7 · Tài khoản admin", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách tài khoản admin", {}),
            ("them", "Modal thêm tài khoản", {"showAdminUserForm": True}),
        ],
    },
    {
        "code": "B8", "title": "B8 · Nhật ký hệ thống", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Nhật ký thay đổi dữ liệu", {"auditTab": "changes"}),
            ("file", "Danh sách file đã tải lên", {"auditTab": "files"}),
        ],
    },
    {
        "code": "B5", "title": "B5 · Quản lý sản phẩm", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách sản phẩm", {}),
            ("them", "Modal thêm sản phẩm", {"showProductForm": True}),
            ("sua", "Modal sửa sản phẩm", {"showProductForm": True,
                                           "editingProductId": "CN02"}),
        ],
    },
]

# ============================================================================
# 4. SỬA JS: điều hướng giữa các file thay vì đổi state trong một trang
# ============================================================================

JS_PATCHES = [
    # Thêm helper GO() và cho nav dùng nó.
    ("    const set = (id) => () => this.setState({ screen: id });",
     "    const GO = (id, carry) => {\n"
     "      const f = (window.__FILES || {})[id];\n"
     "      if (!f) return;\n"
     "      try { sessionStorage.setItem('__homi_carry', JSON.stringify(carry || {})); } catch (e) {}\n"
     "      location.href = f;\n"
     "    };\n"
     "    const set = (id) => () => GO(id);"),

    # Mua xong -> chọn đăng ký seller.
    # 7.2.2 AC: form đăng ký phải autofill từ dữ liệu đơn, "không hiển thị
    # trống". Mockup gốc để chung một trang nên state còn nguyên; tách file rồi
    # thì phải mang tay toàn bộ thông tin người mua sang.
    # Chốt 09/09: tuyến trên hạng Đồng thì BÁO LỖI ngay khi bấm, không đưa
    # khách đi hết 5 bước rồi mới chặn.
    ("this.setState({ showPaymentSuccess: false, screen: 'A2', regStep: 1 })",
     "(s.uplineRank === 'bronze'\n"
     "        ? this.setState({ showPaymentSuccess: false, showUplineBlockedModal: true })\n"
     "        : GO('A2', { regStep: 1, orderId: s.orderId, uplineRank: s.uplineRank,\n"
     "            buyerName: s.buyerName, buyerPhone: s.buyerPhone, buyerEmail: s.buyerEmail,\n"
     "            buyerCccd: s.buyerCccd, buyerAddress: s.buyerAddress, buyerDob: s.buyerDob,\n"
     "            buyerBankAccount: s.buyerBankAccount }))"),

    # Đăng ký xong -> dashboard
    ("goToA3: () => this.setState({ screen: 'A3' })",
     "goToA3: () => GO('A3')"),

    # Đăng nhập agent thành công -> dashboard
    ("{ this.setState({ screen: 'A3', agentLoginError: false }); }",
     "{ GO('A3'); }"),
    ("agentOtpConfirm: () => this.setState({ screen: 'A3', agentLoginStep: 'login', agentLoginError: false })",
     "agentOtpConfirm: () => GO('A3', { agentStage: 'active' })"),

    # Đăng nhập admin -> màn Thành viên
    ("adminLoginSubmit: () => this.setState({ screen: 'B2' })",
     "adminLoginSubmit: () => GO('B2')"),

    # ----- (19) B8 Nhật ký hệ thống ---------------------------------------
    # Dữ liệu dựng sẵn, trải đều 6 phân hệ để KH thấy phạm vi là toàn hệ
    # thống. Bản thật lấy từ bảng audit_log do backend ghi.
    # Neo vào MEMBERS vì đây là trường có sẵn trong bản gốc của KH. Không neo
    # vào RANKS — trường đó do một bản vá KHÁC thêm vào, mà bản vá ấy nằm sau
    # bản vá này trong danh sách nên lúc chạy tới đây nó chưa tồn tại.
    ("  MEMBERS = [",
     "  // (19) Nhật ký hệ thống — bản mẫu dựng sẵn.\n"
     "  AUDIT = [\n"
     "    { time:'17/09/2026 09:12', actor:'Nguyễn Thị Hạnh', role:'Admin',\n"
     "      module:'Thành viên', target:'Lê Văn Cường · LVC5456',\n"
     "      action:'Cập nhật', before:'Copper', after:'Silver',\n"
     "      evidence:'PD-2026-014-da-ky.pdf', ip:'113.161.46.118' },\n"
     "    { time:'17/09/2026 08:55', actor:'Nguyễn Thị Hạnh', role:'Admin',\n"
     "      module:'Đơn hàng', target:'DH923983',\n"
     "      action:'Duyệt', before:'Chờ đối soát', after:'Đã thanh toán',\n"
     "      evidence:'GD-VCB-77120394', ip:'113.161.46.118' },\n"
     "    { time:'17/09/2026 08:40', actor:'Hệ thống', role:'Tự động',\n"
     "      module:'Kho hàng', target:'ACT-100037',\n"
     "      action:'Cập nhật', before:'Sẵn hàng', after:'Đã gán đơn hàng',\n"
     "      evidence:'—', ip:'—' },\n"
     "    { time:'16/09/2026 17:20', actor:'Phùng Thị Thúy Linh', role:'Head',\n"
     "      module:'Rút tiền', target:'YC-2026-0088 · Trần Thị Bích',\n"
     "      action:'Duyệt', before:'Chờ Head duyệt', after:'Đã duyệt',\n"
     "      evidence:'—', ip:'118.70.12.4' },\n"
     "    { time:'16/09/2026 16:02', actor:'Nguyễn Thị Hạnh', role:'Admin',\n"
     "      module:'Kho hàng', target:'Import 120 mã kích hoạt',\n"
     "      action:'Tải file lên', before:'—', after:'118 nhận / 2 bỏ qua',\n"
     "      evidence:'kho-nhap-1609.xlsx', ip:'113.161.46.118' },\n"
     "    { time:'16/09/2026 14:31', actor:'Phùng Thị Thúy Linh', role:'Head',\n"
     "      module:'Tài khoản admin', target:'tranvanminh@homi365.com.vn',\n"
     "      action:'Tạo mới', before:'—', after:'Vai trò Admin',\n"
     "      evidence:'—', ip:'118.70.12.4' },\n"
     "    { time:'16/09/2026 11:08', actor:'Nguyễn Thị Hạnh', role:'Admin',\n"
     "      module:'Thành viên', target:'Phạm Thị Dung · PTD4789',\n"
     "      action:'Khoá / mở khoá', before:'Đang hoạt động', after:'Đã khoá',\n"
     "      evidence:'—', ip:'113.161.46.118' },\n"
     "    { time:'16/09/2026 10:44', actor:'Nguyễn Thị Hạnh', role:'Admin',\n"
     "      module:'Sản phẩm', target:'CN02',\n"
     "      action:'Cập nhật', before:'Mô tả cũ', after:'Mô tả mới',\n"
     "      evidence:'cn02-moi.png', ip:'113.161.46.118' },\n"
     "    { time:'15/09/2026 15:26', actor:'Đặng Văn Phúc', role:'Thành viên',\n"
     "      module:'Thành viên', target:'Đặng Văn Phúc · DVP8221',\n"
     "      action:'Tạo mới', before:'—', after:'Chờ xác nhận thanh toán',\n"
     "      evidence:'cccd-truoc-dvp8221.jpg', ip:'171.224.88.9' },\n"
     "    { time:'15/09/2026 15:26', actor:'Đặng Văn Phúc', role:'Thành viên',\n"
     "      module:'Thành viên', target:'Chấp thuận T&C v1.0',\n"
     "      action:'Tạo mới', before:'—', after:'Đã đồng ý',\n"
     "      evidence:'—', ip:'171.224.88.9' },\n"
     "    { time:'15/09/2026 09:03', actor:'Phùng Thị Thúy Linh', role:'Head',\n"
     "      module:'Rút tiền', target:'YC-2026-0085 · Vũ Minh Khang',\n"
     "      action:'Từ chối', before:'Chờ Head duyệt', after:'Từ chối',\n"
     "      evidence:'—', ip:'118.70.12.4' },\n"
     "    { time:'14/09/2026 13:47', actor:'Nguyễn Thị Hạnh', role:'Admin',\n"
     "      module:'Đơn hàng', target:'DH100511',\n"
     "      action:'Từ chối', before:'Chờ đối soát', after:'Từ chối',\n"
     "      evidence:'—', ip:'113.161.46.118' }\n"
     "  ];\n"
     "\n"
     "  AUDIT_FILES = [\n"
     "    { name:'PD-2026-014-da-ky.pdf', kind:'PDF', module:'Thành viên',\n"
     "      linkedTo:'Cập nhật cấp · Lê Văn Cường', by:'Nguyễn Thị Hạnh',\n"
     "      time:'17/09/2026 09:12', size:'412 KB' },\n"
     "    { name:'kho-nhap-1609.xlsx', kind:'Excel / CSV', module:'Kho hàng',\n"
     "      linkedTo:'Import 120 mã kích hoạt', by:'Nguyễn Thị Hạnh',\n"
     "      time:'16/09/2026 16:02', size:'38 KB' },\n"
     "    { name:'cn02-moi.png', kind:'Ảnh', module:'Sản phẩm',\n"
     "      linkedTo:'Sản phẩm CN02', by:'Nguyễn Thị Hạnh',\n"
     "      time:'16/09/2026 10:44', size:'1,2 MB' },\n"
     "    { name:'cccd-truoc-dvp8221.jpg', kind:'Ảnh', module:'Thành viên',\n"
     "      linkedTo:'Hồ sơ Đặng Văn Phúc', by:'Đặng Văn Phúc',\n"
     "      time:'15/09/2026 15:26', size:'820 KB' },\n"
     "    { name:'cccd-sau-dvp8221.jpg', kind:'Ảnh', module:'Thành viên',\n"
     "      linkedTo:'Hồ sơ Đặng Văn Phúc', by:'Đặng Văn Phúc',\n"
     "      time:'15/09/2026 15:26', size:'795 KB' },\n"
     "    { name:'uy-nhiem-chi-dh923983.jpg', kind:'Ảnh', module:'Đơn hàng',\n"
     "      linkedTo:'Đơn DH923983', by:'Nguyễn Văn A',\n"
     "      time:'15/09/2026 08:11', size:'1,0 MB' }\n"
     "  ];\n"
     "\n"
     "  AUDIT_BADGE = {\n"
     "    'Tạo mới': ['rgba(0,173,238,.12)', '#00ADEE'],\n"
     "    'Cập nhật': ['rgba(170,170,170,.18)', '#414445'],\n"
     "    'Duyệt': ['rgba(132,190,82,.16)', '#4c7a2e'],\n"
     "    'Từ chối': ['rgba(217,52,43,.12)', '#D9342B'],\n"
     "    'Khoá / mở khoá': ['rgba(255,165,0,.15)', '#FFA500'],\n"
     "    'Tải file lên': ['rgba(0,173,238,.12)', '#00ADEE']\n"
     "  };\n"
     "\n"
     "  MEMBERS = ["),

    ("    stockSearch: '', stockStatusFilter: 'all', stockPage: 1,",
     "    stockSearch: '', stockStatusFilter: 'all', stockPage: 1,\n"
     "    auditTab: 'changes', auditSearch: '',"),

    # ----- (18) Điều chỉnh cấp thành viên ---------------------------------
    # Dấu thời gian cho lịch sử điều chỉnh — dd/mm/yyyy hh:mm.
    ("  badge(status) {",
     "  nowStamp() {\n"
     "    const d = new Date(), p = (n) => String(n).padStart(2, '0');\n"
     "    return p(d.getDate()) + '/' + p(d.getMonth() + 1) + '/' + d.getFullYear()\n"
     "      + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());\n"
     "  }\n"
     "\n"
     "  badge(status) {"),

    ("    memberSearch: '', memberStatusOverrides: {}, memberAuditLog: {},",
     "    memberSearch: '', memberStatusOverrides: {}, memberAuditLog: {},\n"
     "    // (18) Trình - duyệt làm NGOÀI hệ thống; trong hệ thống chỉ ghi\n"
     "    // nhận. rankOverrides: cấp đang áp dụng. rankLogs: lưu vết.\n"
     "    rankOverrides: {}, rankLogs: {},\n"
     "    rankEditId: null, rankEditChoice: null,\n"
     "    rankDocNo: '', rankDocDate: '', rankApprover: '', rankDocFile: '',"),

    # Khối tính toán đặt ngay trước phần kho, tức là sau khi selectedMember
    # đã dựng xong.
    ("    const selectedStockRaw = s.selectedStockId "
     "? stockData.find(p => p.id === s.selectedStockId) : null;",
     "    // ----- (18) Điều chỉnh cấp ------------------------------------\n"
     "    // Cấp hiệu lực của một thành viên = cấp admin đã chỉnh, nếu chưa\n"
     "    // chỉnh thì lấy cấp gốc theo doanh số.\n"
     "    const rankOf = (m) => s.rankOverrides[m.id]\n"
     "      || this.RANK_LABEL[m.rank] || m.rank;\n"
     "    const rankIdx = (r) => this.RANKS.indexOf(r);\n"
     "    let rankEditName = '', rankEditCurrent = '', rankOptions = [];\n"
     "    const rankTarget = s.rankEditId\n"
     "      ? this.MEMBERS.find(m => m.id === s.rankEditId) : null;\n"
     "    if (rankTarget) {\n"
     "      rankEditName = rankTarget.name;\n"
     "      rankEditCurrent = rankOf(rankTarget);\n"
     "      // Trần: không được cao hơn người giới thiệu trực tiếp.\n"
     "      const up = this.MEMBERS.find(x => x.name === rankTarget.upline);\n"
     "      const ceil = up ? rankIdx(rankOf(up)) : this.RANKS.length - 1;\n"
     "      // Sàn: cũng không được thấp hơn tuyến dưới trực tiếp, nếu không\n"
     "      // chính nước đi này lại làm tuyến dưới vượt tuyến trên.\n"
     "      const kids = (rankTarget.tree || [])\n"
     "        .map(t => this.MEMBERS.find(x => x.name === t.name))\n"
     "        .filter(Boolean);\n"
     "      const floor = kids.length\n"
     "        ? Math.max(...kids.map(k => rankIdx(rankOf(k)))) : 0;\n"
     "      rankOptions = this.RANKS.map((r, i) => {\n"
     "        const tooHigh = i > ceil, tooLow = i < floor;\n"
     "        const off = tooHigh || tooLow;\n"
     "        const on = s.rankEditChoice === r;\n"
     "        return {\n"
     "          name: r, disabled: off,\n"
     "          note: tooHigh ? 'Cao hơn tuyến trên (' + rankOf(up) + ')'\n"
     "            : tooLow ? 'Thấp hơn tuyến dưới (' + this.RANKS[floor] + ')'\n"
     "            : (r === rankEditCurrent ? 'Cấp hiện tại' : ''),\n"
     "          style: 'display:flex;justify-content:space-between;'\n"
     "            + 'align-items:center;gap:var(--s4);width:100%;min-height:42px;'\n"
     "            + 'padding:var(--s3) var(--s5);border-radius:var(--r-md);'\n"
     "            + 'font-size:13px;text-align:left;'\n"
     "            + (off\n"
     "                ? 'border:1px dashed rgba(170,170,170,.5);background:transparent;'\n"
     "                  + 'color:rgba(170,170,170,.9);cursor:not-allowed'\n"
     "                : on\n"
     "                  ? 'border:1px solid var(--c6);background:rgba(0,173,238,.08);'\n"
     "                    + 'color:var(--c1)'\n"
     "                  : 'border:1px solid rgba(170,170,170,.6);background:var(--c12);'\n"
     "                    + 'color:var(--c2)'),\n"
     "          onClick: () => this.setState({ rankEditChoice: r })\n"
     "        };\n"
     "      });\n"
     "    }\n"
     "    // Phải chọn cấp khác cấp hiện tại VÀ nhập đủ ba trường minh chứng.\n"
     "    // Thiếu minh chứng thì sau này không nối được số liệu trong hệ thống\n"
     "    // với quyết định đã duyệt bên ngoài.\n"
     "    const rankReady = !!s.rankEditChoice\n"
     "      && s.rankEditChoice !== rankEditCurrent\n"
     "      && s.rankDocNo.trim().length > 0\n"
     "      && s.rankDocDate.trim().length > 0\n"
     "      && s.rankApprover.trim().length > 0;\n"
     "\n"
     "    const selectedStockRaw = s.selectedStockId "
     "? stockData.find(p => p.id === s.selectedStockId) : null;"),

    # Xuất giá trị + hành động của luồng điều chỉnh cấp ra cho markup.
    ("      toggleLockSelected, lockButtonLabel, lockButtonStyle,",
     "      toggleLockSelected, lockButtonLabel, lockButtonStyle,\n"
     "\n"
     "      // ----- (18) Điều chỉnh cấp -----------------------------------\n"
     "      effRank: selectedMember ? rankOf(selectedMember) : '',\n"
     "      hasRankLog: !!(selectedMember\n"
     "        && (s.rankLogs[selectedMember.id] || []).length),\n"
     "      rankLog: selectedMember ? (s.rankLogs[selectedMember.id] || []) : [],\n"
     "\n"
     "      showRankEdit: !!s.rankEditId,\n"
     "      rankEditName, rankEditCurrent, rankOptions,\n"
     "      rankDocNo: s.rankDocNo,\n"
     "      setRankDocNo: (e) => this.setState({ rankDocNo: e.target.value }),\n"
     "      rankDocDate: s.rankDocDate,\n"
     "      setRankDocDate: (e) => this.setState({ rankDocDate: this.dateMask(e.target.value) }),\n"
     "      rankApprover: s.rankApprover,\n"
     "      setRankApprover: (e) => this.setState({ rankApprover: e.target.value }),\n"
     "      rankDocFile: s.rankDocFile,\n"
     "      hasRankDocFile: !!s.rankDocFile,\n"
     "      // Bản mẫu chỉ giữ tên file; bản thật tải file lên kho lưu trữ.\n"
     "      setRankDocFile: (e) => this.setState({\n"
     "        rankDocFile: (e.target.files && e.target.files[0])\n"
     "          ? e.target.files[0].name : '' }),\n"
     "      clearRankDocFile: () => this.setState({ rankDocFile: '' }),\n"
     "      openRankEdit: () => selectedMember && this.setState({\n"
     "        rankEditId: selectedMember.id,\n"
     "        rankEditChoice: rankOf(selectedMember),\n"
     "        rankDocNo: '', rankDocDate: '', rankApprover: '', rankDocFile: ''\n"
     "      }),\n"
     "      closeRankEdit: () => this.setState({ rankEditId: null,\n"
     "        rankEditChoice: null,\n"
     "        rankDocNo: '', rankDocDate: '', rankApprover: '',\n"
     "        rankDocFile: '' }),\n"
     "      rankSubmitDisabled: !rankReady,\n"
     "      rankSubmitStyle: 'flex:2;height:44px;border:none;'\n"
     "        + 'border-radius:var(--r-md);font-size:14px;font-weight:600;'\n"
     "        + 'color:#FFFFFF;background:'\n"
     "        + (rankReady ? 'var(--c6)' : 'rgba(170,170,170,.5)')\n"
     "        + ';cursor:' + (rankReady ? 'pointer' : 'not-allowed'),\n"
     "      // Không xét duyệt lại trong hệ thống: lưu là áp dụng ngay.\n"
     "      submitRankEdit: () => {\n"
     "        if (!rankReady || !rankTarget) return;\n"
     "        const id = rankTarget.id;\n"
     "        const log = (s.rankLogs[id] || []).slice();\n"
     "        log.unshift({\n"
     "          label: rankEditCurrent + ' → ' + s.rankEditChoice\n"
     "            + ' · phiếu ' + s.rankDocNo.trim()\n"
     "            + ' ngày ' + s.rankDocDate.trim()\n"
     "            + ' · duyệt: ' + s.rankApprover.trim()\n"
     "            + (s.rankDocFile ? ' · file: ' + s.rankDocFile : ''),\n"
     "          time: this.nowStamp()\n"
     "        });\n"
     "        this.setState({\n"
     "          rankOverrides: { ...s.rankOverrides, [id]: s.rankEditChoice },\n"
     "          rankLogs: { ...s.rankLogs, [id]: log },\n"
     "          rankEditId: null, rankEditChoice: null,\n"
     "          rankDocNo: '', rankDocDate: '', rankApprover: '', rankDocFile: ''\n"
     "        });\n"
     "      },\n"),

    # ----- (17) Gửi yêu cầu thanh toán: chống bấm trùng + lỗi đường truyền --
    # Ba trạng thái của nút: idle -> sending -> (mở QR | timeout).
    # payOrderId giữ nguyên qua mọi lần gửi lại — đây chính là khoá chống trùng
    # (idempotency key) mà backend phải dùng, bản mẫu mô phỏng bằng cách không
    # sinh mã mới.
    ("    showQRPayment: false, orderId: 'DH923983',",
     "    showQRPayment: false, orderId: 'DH923983',\n"
     "    payStage: 'idle', orderCreated: false,"),

    ("      openQRPayment: () => this.setState({ showQRPayment: true }),",
     "      // (17) Bấm Thanh toán. Ba nhánh: đang gửi thì bỏ qua, đơn đã tạo\n"
     "      // thì mở lại đúng đơn đó, còn lại mới gửi yêu cầu mới.\n"
     "      payLabel: s.payStage === 'sending' ? 'Đang gửi yêu cầu…'\n"
     "        : s.payStage === 'timeout' ? 'Gửi lại yêu cầu thanh toán'\n"
     "        : 'Thanh toán',\n"
     "      payTimedOut: s.payStage === 'timeout',\n"
     "      submitPayment: () => {\n"
     "        if (s.payStage === 'sending') return;      // chặn bấm dồn\n"
     "        // Đơn đã tạo thì mở lại đúng đơn đó, không sinh mã đơn mới.\n"
     "        if (s.orderCreated) { this.setState({ showQRPayment: true }); return; }\n"
     "        this.setState({ payStage: 'sending' });\n"
     "        clearTimeout(this.__payTimer);\n"
     "        // Bản mẫu: 1,2s cho thấy trạng thái chờ. Bản thật đặt ngưỡng chờ\n"
     "        // 5 giây, quá thì chuyển sang payStage 'timeout'.\n"
     "        this.__payTimer = setTimeout(() => this.setState({\n"
     "          payStage: 'idle', orderCreated: true, showQRPayment: true\n"
     "        }), 1200);\n"
     "      },\n"
     "      openQRPayment: () => this.setState({ showQRPayment: true }),"),

    # (10) Mở / đóng modal tra cứu thì xoá kết quả cũ.
    # openOrderLookup được khai báo 2 lần trong renderVals (bản gốc của KH),
    # và bản sau đè bản trước — nên phải vá cả hai.
    ("this.setState({ showOrderLookup: true, orderLookupInput: '', orderLookupError: false });",
     "this.setState({ showOrderLookup: true, orderLookupInput: '', orderLookupError: false, lookupResult: null });"),
    ("this.setState({ showOrderLookup: true, orderLookupInput: '', orderLookupError: false });",
     "this.setState({ showOrderLookup: true, orderLookupInput: '', orderLookupError: false, lookupResult: null });"),
    ("      closeOrderLookup: () => this.setState({ showOrderLookup: false }),",
     "      closeOrderLookup: () => this.setState({ showOrderLookup: false, lookupResult: null }),"),

    # (10) Tra cứu đơn: hiện kết quả trong modal, chưa chuyển màn ngay.
    ("""        this.setState({
          showOrderLookup: false, screen: 'A2', regStep: 1,
          orderId: order.orderId, uplineRank,
          buyerName: order.buyerName, buyerPhone: phone, buyerEmail: order.buyerEmail,
          buyerCccd: order.buyerCccd, buyerAddress: order.buyerAddress, buyerDob: order.buyerDob
        });""",
     """        this.setState({
          orderLookupError: false, uplineRank,
          lookupResult: {
            orderId: order.orderId, buyerName: order.buyerName, phone,
            email: order.buyerEmail, cccd: order.buyerCccd,
            address: order.buyerAddress, dob: order.buyerDob,
            pkg: 'Gói 1 năm · CN02', amount: '10.000.000đ', date: '03/09/2026',
            referrer: (agent && agent.name) || '—',
            statusLabel: 'Đã thanh toán',
            badgeBg: 'rgba(132,190,82,.14)', badgeColor: '#4c7a2e'
          }
        });"""),

    # (2) Ngày sinh nhập số, tự chèn dấu / — dùng chung dateMask().
    ("buyerDob: s.buyerDob, setBuyerDob: (e) => this.setState({ buyerDob: e.target.value }),",
     "buyerDob: s.buyerDob, setBuyerDob: (e) => this.setState({ buyerDob: this.dateMask(e.target.value) }),"),

    # 7.3.2 — số đơn đổi theo khoảng thời gian đang chọn.
    ("      metricOrders: s.agentStage === 'active' ? '10' : '1',",
     "      metricOrders: (s.agentStage === 'active' ? this.ORDER_RANGE_VALUES\n"
     "        : this.ORDER_RANGE_VALUES_NEW)[s.orderRange || 'month'],\n"
     "      // Chưa kích hoạt thì hoa hồng bị giữ, chưa được tính điểm.\n"
     "      heldCommissionLabel: '1.200.000đ',"),

    # Chưa kích hoạt -> điểm tích luỹ = 0 (chốt 09/09).
    ("      metricPoints: s.agentStage === 'active' ? '1.240' : '80',",
     "      metricPoints: s.agentStage === 'active' ? '1.240' : '0',"),

    # Tên hạng dùng đúng 6 hạng chính thức, không dịch.
    ("      metricRank: s.agentStage === 'active' ? 'Bạc' : 'Đồng',",
     "      metricRank: s.agentStage === 'active' ? 'Silver' : 'Copper',"),

    # (6) Tiêu đề biểu đồ đổi theo bộ lọc đang chọn, chỉ thay cụm đầu
    # "Xu hướng hoa hồng" thành "Khoản ưu đãi".
    ("title: 'Xu hướng hoa hồng · 7 ngày gần nhất'",
     "title: 'Khoản ưu đãi · 7 ngày gần nhất'"),
    ("title: 'Xu hướng hoa hồng · Theo tuần trong tháng'",
     "title: 'Khoản ưu đãi · Theo tuần trong tháng'"),
    ("title: 'Xu hướng hoa hồng · Theo tháng trong năm'",
     "title: 'Khoản ưu đãi · Theo tháng trong năm'"),
    # (Hạng của từng dòng trong bảng thành viên được đổi ngay trong bản vá
    #  "(15) Mã tuyến trên" bên dưới — cùng một dòng return nên gộp lại.)
    # (8) Bỏ duyệt 2 lượt ở màn thành viên. Đơn hàng được admin xác nhận
    # thanh toán trước (màn Đơn hàng), sau đó Manager duyệt thành viên để mở
    # khoá điểm và ưu đãi đang tạm giữ.
    ("        canApproveMember: (isSpecialist && effStatus === 'pending') || (!isSpecialist && effStatus === 'specialist_approved'),\n"
     "        canRejectMember: ['pending', 'specialist_approved'].includes(effStatus),\n"
     "        approveMemberButtonLabel: isSpecialist ? 'Duyệt hồ sơ (Specialist)' : 'Duyệt & kích hoạt (Head Admin)',\n"
     "        approvalStageNote: effStatus === 'pending' ? 'Đang chờ Admin Specialist duyệt hồ sơ (bước 1/2).' : effStatus === 'specialist_approved' ? 'Đã qua Specialist — chờ Head Admin xác nhận để kích hoạt (bước 2/2).' : (effStatus === 'rejected' ? 'Hồ sơ đã bị từ chối.' : null)",
     "        canApproveMember: !isSpecialist && effStatus === 'specialist_approved',\n"
     "        canRejectMember: !isSpecialist && effStatus === 'specialist_approved',\n"
     "        approveMemberButtonLabel: 'Xác nhận, kích hoạt Thành viên hoạt động (Head)',\n"
     "        approvalStageNote: effStatus === 'pending'\n"
     "          ? 'Chưa xác nhận thanh toán. Vào màn Đơn hàng xác nhận tiền về trước, hồ sơ này mới duyệt được.'\n"
     "          : effStatus === 'specialist_approved'\n"
     "            ? 'Đơn hàng đã được xác nhận thanh toán. Manager duyệt để thành viên nhận điểm và ưu đãi đang tạm giữ.'\n"
     "            : (effStatus === 'rejected' ? 'Hồ sơ đã bị từ chối.' : null)"),

    # Duyệt thành viên chỉ còn MỘT lượt, do Manager (Head Admin) thực hiện.
    ("          const nextStatus = isSpecialist ? 'specialist_approved' : 'active';\n"
     "          const label = isSpecialist ? 'Admin Specialist duyệt hồ sơ (chờ Head Admin)' : 'Head Admin xác nhận & kích hoạt thành viên';\n"
     "          const actor = isSpecialist ? 'Admin Specialist' : 'Head Admin';",
     "          const nextStatus = 'active';\n"
     "          const label = 'Manager duyệt thành viên — mở khoá điểm và ưu đãi đang tạm giữ';\n"
     "          const actor = 'Head Admin';"),


    # (Hạng trong ngăn chi tiết cũng gộp vào bản vá lịch sử hạng bên dưới —
    #  cùng một dòng nên không tách được.)

    # Mã thành viên = alias (8.1.C-4), trùng thì -2, -3…
    ("        const affCode = m.name.split(' ').map(w => w[0]).join('').toUpperCase() + m.phone.slice(-4);",
     "        const affCode = ALIAS[m.id];"),
    ("    const members = this.MEMBERS",
     "    const ALIAS = this.aliasMap();\n    const members = this.MEMBERS"),

    # Thêm một thành viên trùng alias để thấy quy tắc hậu tố -2 hoạt động.
    ("upline:'Trần Thị Bích', rank:'Đồng', joined:'02/09/2026', status:'pending', tree:[] }",
     "upline:'Trần Thị Bích', rank:'Đồng', joined:'02/09/2026', status:'pending', tree:[] },\n"
     "    { id:7, name:'Trương Thanh Bình', phone:'0938884123', contact:'093•••123',\n"
     "      affId:'780314', upline:'Vũ Minh Khang', rank:'Đồng', joined:'05/09/2026',\n"
     "      status:'specialist_approved', tree:[] }"),

    # (15) Mã tuyến trên hiển thị cạnh tên tuyến trên — cũng dùng alias.
    ("        return { ...m, status: effStatus, badgeBg: bg, badgeColor: color, statusLabel: label,",
     "        const up = this.MEMBERS.find(u => u.name === m.upline);\n"
     "        return { ...m, affId: affCode,\n"
     "          // (18) Cấp admin đã chỉnh thắng cấp gốc theo doanh số.\n"
     "          rank: s.rankOverrides[m.id] || this.RANK_LABEL[m.rank] || m.rank,\n"
     "          status: effStatus, badgeBg: bg, badgeColor: color,\n"
     "          // Nhãn riêng cho thành viên — badge() dùng chung với rút tiền,\n"
     "          // mà rút tiền vẫn giữ mô hình duyệt 2 lượt.\n"
     "          statusLabel: this.MEMBER_STATUS_LABEL[effStatus] || label,\n"
     "          uplineCode: up ? ALIAS[up.id] : '',"),

    # Link form của agent cũng về đúng một dạng homi365.com.vn/<alias>.
    ("formLink: 'portal.homi365.com.vn/' + affCode",
     "formLink: 'homi365.com.vn/' + affCode"),
    ("navigator.clipboard.writeText('portal.homi365.com.vn/' + affCode)",
     "navigator.clipboard.writeText('homi365.com.vn/' + affCode)"),

    # (6) Đếm theo 5 trạng thái kho.
    ("      stockTotal: stockData.length, stockAvailable: stockData.filter(p => p.status === 'available').length,",
     "      stockTotal: stockData.length,\n"
     "      stockReceived: stockData.filter(p => p.status === 'received').length,\n"
     "      stockShipped: stockData.filter(p => p.status === 'shipped').length,\n"
     "      stockDelivered: stockData.filter(p => p.status === 'delivered').length,\n"
     "      stockAvailable: stockData.filter(p => p.status === 'available').length,"),

    # (6) Vòng đời kho 5 bước: Nhập kho -> Sẵn hàng -> Gán đơn (kích hoạt)
    # -> Xuất kho -> Giao hàng thành công (kèm mã vận đơn).
    ("  STOCK_FILTERS = [['all','Tất cả'],['available','Sẵn hàng'],['assigned','Đã gán đơn hàng'],['activated','Đã kích hoạt']];",
     "  STOCK_FILTERS = [['all','Tất cả'],['received','Nhập kho'],['available','Sẵn hàng'],"
     "['assigned','Đã gán đơn hàng'],['shipped','Xuất kho'],['delivered','Giao hàng thành công']];"),

    ("""    const statuses = ['available','available','assigned','activated'];""",
     """    const statuses = ['received','available','available','assigned','shipped','delivered'];"""),

    ("""        stockedAt: '0' + (1 + i % 9) + '/08/2026', status,
        log: [{ label: 'Nhập kho', time: '0' + (1 + i % 9) + '/08/2026 08:00' }]""",
     """        stockedAt: d, status, tracking: track, log: chain"""),

    # Lịch sử trạng thái phải dựng đủ các bước đã đi qua, không chỉ "Nhập kho".
    ("      const status = statuses[i % statuses.length];",
     """      const status = statuses[i % statuses.length];
      const d = '0' + (1 + i % 9) + '/08/2026';
      const ord = ['received', 'available'].includes(status) ? '—' : 'DH' + (100000 + i * 13);
      const track = ['shipped', 'delivered'].includes(status)
        ? 'VN' + (830000000 + i * 137) : '—';
      const STEPS = ['received', 'available', 'assigned', 'shipped', 'delivered'];
      const STEP_TXT = {
        received: 'Nhập kho',
        available: 'Kiểm hàng xong · chuyển sang Sẵn hàng',
        assigned: 'Gán đơn hàng ' + ord + ' · cấp mã kích hoạt cho khách',
        shipped: 'Xuất kho, bàn giao đơn vị vận chuyển',
        delivered: 'Giao hàng thành công · mã vận đơn ' + track
      };
      const chain = STEPS.slice(0, STEPS.indexOf(status) + 1).map((st, k) => ({
        label: STEP_TXT[st],
        time: d + ' ' + String(8 + k * 2).padStart(2, '0') + ':00'
      }));"""),

    # Đơn hàng gắn / thành viên chỉ trống khi hàng chưa được gán.
    ("        orderId: status === 'available' ? '—' : 'DH' + (100000 + i * 13),\n"
     "        seller: status === 'available' ? '—' : this.MEMBERS[i % this.MEMBERS.length].name,",
     "        orderId: ord,\n"
     "        seller: ord === '—' ? '—' : this.MEMBERS[i % this.MEMBERS.length].name,"),

    # (16) Cột Khoản thưởng · Yêu cầu rút · Số dư còn lại, và hàng tổng.
    ("        return { ...w, badgeBg: bg, badgeColor: color, statusLabel: label, onClick: () => this.setState({ selectedWithdrawalId: w.id }) };\n"
     "      });\n"
     "    const withdrawalsEmpty = withdrawals.length === 0;",
     "        const reward = this.SELLER_BALANCE[w.seller] || 5000000;\n"
     "        return { ...w, badgeBg: bg, badgeColor: color, statusLabel: label,\n"
     "          rewardNum: reward, remainNum: reward - w.amountNum,\n"
     "          rewardLabel: reward.toLocaleString('vi-VN') + 'đ',\n"
     "          remainLabel: (reward - w.amountNum).toLocaleString('vi-VN') + 'đ',\n"
     "          onClick: () => this.setState({ selectedWithdrawalId: w.id }) };\n"
     "      });\n"
     "    const withdrawalsEmpty = withdrawals.length === 0;\n"
     "    const sumReward = withdrawals.reduce((t, w) => t + w.rewardNum, 0);\n"
     "    const sumRequest = withdrawals.reduce((t, w) => t + w.amountNum, 0);"),

    ("      withdrawals, withdrawalsEmpty,",
     "      withdrawals, withdrawalsEmpty,\n"
     "      sumRewardLabel: sumReward.toLocaleString('vi-VN') + 'đ',\n"
     "      sumRequestLabel: sumRequest.toLocaleString('vi-VN') + 'đ',\n"
     "      sumRemainLabel: (sumReward - sumRequest).toLocaleString('vi-VN') + 'đ',"),

    # (16) Ngày hiệu lực = lúc admin xác nhận thanh toán và gửi mã cho khách.
    # Ngày hết hiệu lực = cộng thời hạn gói (bản mẫu dùng gói 1 năm).
    ("""    const stockItems = stockFiltered.slice((stockPage - 1) * stockPageSize, stockPage * stockPageSize).map(p => {
      const [bg, color, label] = this.badge(p.status);
      return { ...p, badgeBg: bg, badgeColor: color, statusLabel: label, onClick: () => this.setState({ selectedStockId: p.id }) };
    });""",
     """    const plusYear = (d) => {
      const q = (d || '').split('/');
      return q.length === 3 ? q[0] + '/' + q[1] + '/' + (parseInt(q[2], 10) + 1) : '—';
    };
    const stockItems = stockFiltered.slice((stockPage - 1) * stockPageSize, stockPage * stockPageSize).map(p => {
      const [bg, color, label] = this.badge(p.status);
      const live = !['received', 'available'].includes(p.status);
      return { ...p, badgeBg: bg, badgeColor: color, statusLabel: label,
        activeFrom: live ? p.stockedAt : '—',
        activeTo: live ? plusYear(p.stockedAt) : '—',
        onClick: () => this.setState({ selectedStockId: p.id }) };
    });"""),

    # 7.5.2 — dữ liệu cây tuyến thêm cấp F2 (markup đã có vòng lặp con).
    ("      tree:[{name:'Lê Văn Cường', orders:4},{name:'Phạm Thị Dung', orders:1}] },",
     "      tree:[{name:'Lê Văn Cường', orders:4, children:[{name:'Ngô Thị Em', orders:2},"
     "{name:'Đỗ Anh Tuấn', orders:9}]},{name:'Phạm Thị Dung', orders:1, children:[]}] },"),
    ("      tree:[{name:'Ngô Thị Em', orders:2}] },",
     "      tree:[{name:'Ngô Thị Em', orders:2, children:[{name:'Vũ Minh Khang', orders:5}]}] },"),

    # 7.5.2 — lịch sử thăng/giáng hạng trong ngăn chi tiết thành viên.
    ("      selectedMember = {\n        ...selectedMemberRaw, status: effStatus,",
     "      selectedMember = {\n        ...selectedMemberRaw, status: effStatus,\n"
     "        rank: this.RANK_LABEL[selectedMemberRaw.rank] || selectedMemberRaw.rank,\n"
     "        // (1) Hồ sơ đăng ký đầy đủ, đúng những gì thành viên đã khai.\n"
     "        email: (selectedMemberRaw.name.split(' ').slice(-1)[0] || 'user')\n"
     "          .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase()\n"
     "          + selectedMemberRaw.phone.slice(-4) + '@gmail.com',\n"
     "        cccd: '079' + selectedMemberRaw.phone.slice(-9),\n"
     "        cccdIssue: '22/01/2021 · Cục Cảnh sát QLHC về TTXH',\n"
     "        dobGender: '15/03/1992 · Nữ',\n"
     "        address: '12 Nguyễn Huệ, Phường Bến Thành, TP. Hồ Chí Minh',\n"
     "        bank: 'Vietcombank — NH TMCP Ngoại thương Việt Nam',\n"
     "        bankAccount: '0071' + selectedMemberRaw.phone.slice(-9),\n"
     "        bankHolder: this.vnUpper(selectedMemberRaw.name),\n"
     "        cccdFront: 'cccd-truoc-' + ALIAS[selectedMemberRaw.id] + '.jpg',\n"
     "        cccdBack: 'cccd-sau-' + ALIAS[selectedMemberRaw.id] + '.jpg',\n"
     "        // (10) Cấp tuyến: F0 nếu không có tuyến trên, F1 nếu tuyến trên là\n"
     "        // gốc, F2 nếu tuyến trên lại có tuyến trên nữa.\n"
     "        tierLabel: (function (m, all) {\n"
     "          let lv = 0, cur = m;\n"
     "          while (cur && cur.upline && cur.upline !== '—' && lv < 6) {\n"
     "            cur = all.find(x => x.name === cur.upline); lv++;\n"
     "          }\n"
     "          return 'F' + lv;\n"
     "        })(selectedMemberRaw, this.MEMBERS),\n"
     "        // Bằng chứng chấp thuận T&C — bốn trường bắt buộc theo rà soát\n"
     "        // pháp lý: định danh, thời điểm, phiên bản, địa chỉ IP.\n"
     "        tncVersion: 'v1.0',\n"
     "        tncAt: selectedMemberRaw.joined + ' 09:' + (10 + selectedMemberRaw.id) + ':07',\n"
     "        tncIp: '113.161.' + (40 + selectedMemberRaw.id) + '.' + (100 + selectedMemberRaw.id * 3),\n"
     "        tncUser: 'MB' + String(selectedMemberRaw.id).padStart(5, '0')\n"
     "          + ' · ' + selectedMemberRaw.phone,\n"
     "        // Ghi đè bằng phần admin đã sửa (nếu có).\n"
     "        ...(s.memberEdits[selectedMemberRaw.id] || {}),\n"
     "        rankHistory: this.RANK_HISTORY[selectedMemberRaw.id]\n"
     "          || [{ label: 'Tham gia · hạng '\n"
     "                 + (this.RANK_LABEL[selectedMemberRaw.rank] || selectedMemberRaw.rank),\n"
     "               time: selectedMemberRaw.joined }],"),

    # Cho phép trang bơm state ban đầu (chọn màn, chọn bước, mở modal)
    # + state cho màn Quản lý sản phẩm và modal Thêm hàng vào kho.
    ("    actionModal: null, rejectReason: '', paidNote: ''\n  };",
     "    actionModal: null, rejectReason: '', paidNote: '',\n"
     "    showProductForm: false, editingProductId: null,\n"
     "    showAddStock: false, addStockSku: '', addStockCode: '', addStockError: '',\n"
     "    showImportStock: false, importText: '', importResult: null,\n"
     "    orderActivationCode: '', orderCodeError: '',\n"
     "    copyPersonalLabel: 'Copy link',\n"
     "    banks: null, provinceData: null,\n"
     "    bankQuery: 'Vietcombank', bankOpen: false,\n"
     "    provinceQuery: 'Thành phố Hồ Chí Minh', provinceOpen: false,\n"
     "    wardQuery: 'Phường Bến Thành', wardOpen: false,\n"
     "    accountHolder: '', buyTcChecked: false,\n"
     "    cccdIssueDate: '', cccdIssuePlace: '', lookupResult: null,\n"
     "    loginPhoneChecked: false, loginPhoneEmpty: false, loginNotEligible: false,\n"
     "    profileOpen: false, profileEdit: false, profileDraft: {}, memberEdits: {},\n"
     "    bankTxnCode: '',\n"
     "    showAdminUserForm: false, editingAdminUserId: null, adminUserLocks: {},\n"
     "    orderRange: 'month',\n"
     "    ordersData: null, orderSearch: '', orderStatusFilter: 'all',\n"
     "    selectedOrderId: null,\n"
     "    ...(window.__STATE__ || {})\n  };"),

    # Sidebar quản trị: thêm mục Quản lý sản phẩm.
    ("  ADMIN_NAV = [['B2','Thành viên'],['B3','Yêu cầu rút tiền'],"
     "['B4','Quản lý kho hàng']];",
     "  ADMIN_NAV = [['B2','Thành viên'],['B3','Yêu cầu rút tiền'],"
     "['B6','Đơn hàng'],['B4','Kho hàng'],['B5','Sản phẩm'],"
     "['B8','Nhật ký hệ thống'],['B7','Tài khoản admin']];"),

    # B5 cũng nằm trong khung quản trị.
    ("const adminOn = ['B2','B3','B4'].includes(s.screen);",
     "const adminOn = ['B2','B3','B4','B5','B6','B7','B8'].includes(s.screen);"),

    ("isB3: s.screen === 'B3', isB4: s.screen === 'B4',",
     "isB3: s.screen === 'B3', isB4: s.screen === 'B4', "
     "isB5: s.screen === 'B5', isB6: s.screen === 'B6', isB7: s.screen === 'B7',\n"
     "      isB8: s.screen === 'B8',\n"
     "      // (19) Nhật ký hệ thống\n"
     "      isAuditChanges: s.auditTab === 'changes',\n"
     "      isAuditFiles: s.auditTab === 'files',\n"
     "      auditTabs: [['changes', 'Thay đổi dữ liệu'], ['files', 'File đã tải lên']]\n"
     "        .map(([k, label]) => ({\n"
     "          label, onClick: () => this.setState({ auditTab: k, auditSearch: '' }),\n"
     "          style: 'height:36px;padding:0 var(--s6);border-radius:var(--r-xl);'\n"
     "            + 'font-size:13px;font-weight:600;'\n"
     "            + (s.auditTab === k\n"
     "                ? 'border:1px solid var(--c6);background:rgba(0,173,238,.1);color:var(--c6)'\n"
     "                : 'border:1px solid rgba(170,170,170,.6);background:var(--c12);color:var(--c2)')\n"
     "        })),\n"
     "      auditSearch: s.auditSearch,\n"
     "      setAuditSearch: (e) => this.setState({ auditSearch: e.target.value }),\n"
     "      auditRows: this.AUDIT\n"
     "        .filter(a => !s.auditSearch.trim()\n"
     "          || (a.actor + ' ' + a.target + ' ' + a.evidence)\n"
     "               .toLowerCase().includes(s.auditSearch.trim().toLowerCase()))\n"
     "        .map(a => {\n"
     "          const [bg, color] = this.AUDIT_BADGE[a.action]\n"
     "            || ['rgba(170,170,170,.18)', '#414445'];\n"
     "          return { ...a, badgeBg: bg, badgeColor: color };\n"
     "        }),\n"
     "      auditFiles: this.AUDIT_FILES\n"
     "        .filter(f => !s.auditSearch.trim()\n"
     "          || (f.name + ' ' + f.by + ' ' + f.linkedTo)\n"
     "               .toLowerCase().includes(s.auditSearch.trim().toLowerCase())),\n"
     "      isB7Allowed: s.screen === 'B7' && s.adminRole !== 'specialist',\n"
     "      isB7Denied: s.screen === 'B7' && s.adminRole === 'specialist',"),

    # 7.9.1 AC: Specialist không thấy cả mục Tài khoản admin trên sidebar.
    ("    const adminNav = this.ADMIN_NAV.map(([id, label]) => ({",
     "    const adminNav = this.ADMIN_NAV\n"
     "      .filter(([id]) => id !== 'B7' || s.adminRole !== 'specialist')\n"
     "      .map(([id, label]) => ({"),

    # 7.9.4 — nhãn trạng thái duyệt hiện rõ số lượt: 0/2 · 1/2 · 2/2.
    ("      pending: ['rgba(255,165,0,.15)', '#a36400', 'Chờ duyệt'],",
     "      pending: ['rgba(255,165,0,.15)', '#a36400', 'Chờ duyệt (0/2)'],"),
    ("      specialist_approved: ['rgba(255,165,0,.15)', '#a36400', 'Chờ Head Admin duyệt'],",
     "      specialist_approved: ['rgba(255,165,0,.15)', '#a36400', 'Chờ Head Admin (1/2)'],"),
    ("      approved: ['rgba(0,173,238,.14)', '#00728f', 'Đã duyệt'],",
     "      approved: ['rgba(0,173,238,.14)', '#00728f', 'Đã duyệt (2/2)'],"),

    # Thêm một SĐT đăng nhập được nhưng CHƯA qua bước Head duyệt — để demo
    # trạng thái "bán hàng ngay, ưu đãi tạm giữ". Ứng với Trương Thanh Bình
    # trong bảng thành viên (đang Chờ Head duyệt).
    ("  REGISTERED_PHONES = ['0901234567', '0912345678', '0987654321'];",
     "  REGISTERED_PHONES = ['0901234567', '0912345678', '0987654321', '0938884123'];\n"
     "  // Đăng nhập được nhưng hồ sơ chưa qua bước Head duyệt.\n"
     "  PENDING_PHONES = ['0938884123'];"),

    # 7.1.3 — đã mua hàng nhưng chưa là agent thì đưa sang màn đăng ký,
    # mang theo dữ liệu đơn cũ để autofill (khớp luôn 7.2.8).
    ("""      agentLoginSubmit: () => {
        if (s.agentPhone.trim() && s.agentPassword === '123456') { GO('A3'); }
        else { this.setState({ agentLoginError: true, agentLoginStep: 'otp' }); }
      },""",
     """      agentLoginSubmit: () => {
        const ph = s.agentPhone.trim();
        const boughtOrder = this.ORDERS_BY_PHONE[ph];
        const isAgent = this.REGISTERED_PHONES.includes(ph);
        if (boughtOrder && !isAgent) {
          GO('A2', { regStep: 1, orderId: boughtOrder.orderId,
            buyerName: boughtOrder.buyerName, buyerPhone: ph, buyerEmail: boughtOrder.buyerEmail,
            buyerCccd: boughtOrder.buyerCccd, buyerAddress: boughtOrder.buyerAddress,
            buyerDob: boughtOrder.buyerDob });
          return;
        }
        // Agent đã được Head duyệt -> dashboard hoạt động (rút tiền được).
        // Agent chưa duyệt -> dashboard chờ kích hoạt (ưu đãi tạm giữ).
        if (ph && s.agentPassword === '123456') {
          GO('A3', { agentStage: this.PENDING_PHONES.includes(ph) ? 'new' : 'active' });
        }
        else { this.setState({ agentLoginError: true, agentLoginStep: 'otp' }); }
      },

      loginPhoneChecked: s.loginPhoneChecked,
      loginPhoneUnchecked: !s.loginPhoneChecked,
      loginPhoneEmpty: s.loginPhoneEmpty,
      loginNotEligible: s.loginNotEligible,
      checkLoginPhone: () => {
        const ph = s.agentPhone.trim();
        if (!ph) { this.setState({ loginPhoneEmpty: true, loginNotEligible: false }); return; }
        // Đã có tài khoản -> mở ô mật khẩu.
        if (this.REGISTERED_PHONES.includes(ph)) {
          this.setState({ loginPhoneChecked: true, loginPhoneEmpty: false,
            loginNotEligible: false, agentLoginError: false });
          return;
        }
        // Đã mua hàng nhưng chưa đăng ký -> mở modal khoe đơn cũ trước.
        // Bấm "Đăng ký thành viên" trong modal mới sang form, điền sẵn.
        const o = this.ORDERS_BY_PHONE[ph];
        if (o) {
          const ag = this.MEMBERS.find(m => m.id === o.agentId);
          const rankMap = { 'Đồng': 'bronze', 'Bạc': 'silver', 'Vàng': 'gold' };
          this.setState({
            loginNotEligible: false, loginPhoneEmpty: false,
            uplineRank: ag ? (rankMap[ag.rank] || 'silver') : 'silver',
            showOrderLookup: true, orderLookupInput: ph, orderLookupError: false,
            lookupResult: {
              orderId: o.orderId, buyerName: o.buyerName, phone: ph,
              email: o.buyerEmail, cccd: o.buyerCccd,
              address: o.buyerAddress, dob: o.buyerDob,
              pkg: 'Gói 1 năm · CN02', amount: '10.000.000đ', date: '03/09/2026',
              referrer: (ag && ag.name) || '—',
              statusLabel: 'Đã thanh toán',
              badgeBg: 'rgba(132,190,82,.14)', badgeColor: '#4c7a2e'
            }
          });
          return;
        }
        // Chưa mua đơn nào -> chưa đủ điều kiện.
        this.setState({ loginNotEligible: true, loginPhoneEmpty: false, agentLoginError: false });
      },"""),

    # Nút copy phải chép đúng link alias duy nhất.
    ("navigator.clipboard.writeText('homi365.vn/san-pham/CN02?aff_id=923983')",
     "navigator.clipboard.writeText('homi365.com.vn/htmt0083')"),

    # 8.1.C-4 / 8.1.C-5 — sinh alias từ họ tên + 4 số cuối SĐT, trùng thì
    # thêm hậu tố -2, -3… theo thứ tự đăng ký.
    ("  makeWithdrawals() {",
     """  aliasOf(name, phone) {
    const ini = (name || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
      .replace(/đ/g, 'd').replace(/Đ/g, 'D')
      .trim().split(/\\s+/).map(w => w[0] || '').join('').toUpperCase();
    return ini + (phone || '').slice(-4);
  }

  aliasMap() {
    const seen = {}, out = {};
    this.MEMBERS.forEach(m => {
      const base = this.aliasOf(m.name, m.phone);
      seen[base] = (seen[base] || 0) + 1;
      out[m.id] = seen[base] === 1 ? base : base + '-' + seen[base];
    });
    return out;
  }

  makeWithdrawals() {"""),

    # Badge cho vòng đời đơn hàng (khác badge rút tiền: 'paid' đã dùng cho chi trả).
    ("      activated: ['rgba(0,173,238,.14)', '#00728f', 'Đã kích hoạt']",
     "      activated: ['rgba(0,173,238,.14)', '#00728f', 'Đã kích hoạt'],\n"
     "      received: ['rgba(170,170,170,.18)', '#5c5c5c', 'Nhập kho'],\n"
     "      shipped: ['rgba(0,173,238,.14)', '#00728f', 'Xuất kho'],\n"
     "      delivered: ['rgba(132,190,82,.14)', '#4c7a2e', 'Giao hàng thành công'],\n"
     "      order_pending: ['rgba(255,165,0,.15)', '#a36400', 'Chờ đối soát'],\n"
     "      order_paid: ['rgba(132,190,82,.14)', '#4c7a2e', 'Đã thanh toán · đã cấp mã'],\n"
     "      order_rejected: ['rgba(217,52,43,.12)', '#D9342B', 'Từ chối']"),

    # Khởi tạo dữ liệu đơn hàng.
    ("    if (!this.state.stockData) this.setState({ stockData: this.makeStock() });",
     "    if (!this.state.stockData) this.setState({ stockData: this.makeStock() });\n"
     "    if (!this.state.ordersData) this.setState({ ordersData: this.makeOrders() });\n"
     "    // Nạp danh sách ngân hàng và địa giới hành chính từ API công khai.\n"
     "    // Lỗi mạng thì giữ nguyên danh sách rút gọn, prototype vẫn dùng được.\n"
     "    try {\n"
     "      fetch('https://api.vietqr.io/v2/banks')\n"
     "        .then(r => r.json())\n"
     "        .then(j => { const b = (j && j.data || []).map(x => x.shortName + ' — ' + x.name);\n"
     "                     if (b.length) this.setState({ banks: b }); })\n"
     "        .catch(() => {});\n"
     "      fetch('https://provinces.open-api.vn/api/v2/?depth=2')\n"
     "        .then(r => r.json())\n"
     "        .then(j => { const p = (j || []).map(x => ({ name: x.name,\n"
     "                       wards: (x.wards || []).map(w => w.name) }));\n"
     "                     if (p.length) this.setState({ provinceData: p }); })\n"
     "        .catch(() => {});\n"
     "    } catch (e) {}"),

    # Dữ liệu sản phẩm + đơn hàng (mockup KH không có 2 màn này).
    ("  componentDidMount() {",
     """  ORDER_FILTERS = [['all','Tất cả'],['order_pending','Chờ đối soát'],['order_paid','Đã thanh toán'],['order_rejected','Từ chối']];

  makeOrders() {
    const raw = [
      { id:'DH923983', buyer:'Nguyễn Văn A', phone:'0901111111', email:'nguyenvana@gmail.com',
        address:'12 Nguyễn Huệ, Phường Bến Nghé, TP. Hồ Chí Minh',
        pkg:'Gói 1 năm · CN02', amountNum:10000000, referrer:'Trần Thị Bích', refCode:'TTB4123',
        date:'03/09/2026 09:12', status:'order_pending', proof:'bill-DH923983.jpg', activationCode:null,
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'03/09/2026 09:12'},
                  {label:'Khách tải ảnh chuyển khoản', actor:'Nguyễn Văn A', time:'03/09/2026 09:20'}] },
      { id:'DH100511', buyer:'Lý Thị Hoa', phone:'0902222222', email:'lythihoa@gmail.com',
        address:'45 Lê Lợi, Phường Bến Thành, TP. Hồ Chí Minh',
        pkg:'Gói nửa năm · CN02-6M', amountNum:6000000, referrer:'Lê Văn Cường', refCode:'LVC5456',
        date:'02/09/2026 15:40', status:'order_pending', proof:'bill-DH100511.jpg', activationCode:null,
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'02/09/2026 15:40'},
                  {label:'Khách tải ảnh chuyển khoản', actor:'Lý Thị Hoa', time:'02/09/2026 15:52'}] },
      { id:'DH100234', buyer:'Đỗ Anh Tuấn', phone:'0903333333', email:'doanhtuan@gmail.com',
        address:'88 Trần Hưng Đạo, Phường Cầu Ông Lãnh, TP. Hồ Chí Minh',
        pkg:'Gói 1 năm · CN02', amountNum:10000000, referrer:'Vũ Minh Khang', refCode:'VMK7998',
        date:'30/08/2026 08:05', status:'order_paid', proof:'bill-DH100234.jpg', activationCode:'ACT-100481', activatedAt:'30/08/2026',
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'30/08/2026 08:05'},
                  {label:'Khách tải ảnh chuyển khoản', actor:'Đỗ Anh Tuấn', time:'30/08/2026 08:19'},
                  {label:'Admin Specialist xác nhận tiền về (chờ Head Admin)', actor:'Admin Specialist', time:'30/08/2026 09:10'},
                  {label:'Head Admin xác nhận & cấp mã kích hoạt ACT-100481', actor:'Head Admin', time:'30/08/2026 10:02'}] },
      { id:'DH100088', buyer:'Ngô Thị Em', phone:'0904444444', email:'ngothiem@gmail.com',
        address:'7 Nguyễn Trãi, Phường Bến Thành, TP. Hồ Chí Minh',
        pkg:'Gói 1 năm · CN02', amountNum:10000000, referrer:'Lê Văn Cường', refCode:'LVC5456',
        date:'28/08/2026 11:30', status:'order_paid', proof:'bill-DH100088.jpg', activationCode:'ACT-100337', activatedAt:'28/08/2026',
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'28/08/2026 11:30'},
                  {label:'Head Admin xác nhận & cấp mã kích hoạt ACT-100337', actor:'Head Admin', time:'28/08/2026 14:00'}] },
      { id:'DH100012', buyer:'Phạm Quốc Bảo', phone:'0905555555', email:'pqbao@gmail.com',
        address:'201 Cách Mạng Tháng 8, Phường Hoà Hưng, TP. Hồ Chí Minh',
        pkg:'Gói nửa năm · CN02-6M', amountNum:6000000, referrer:'Trần Thị Bích', refCode:'TTB4123',
        date:'26/08/2026 19:12', status:'order_rejected', proof:'bill-DH100012.jpg', activationCode:null,
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'26/08/2026 19:12'},
                  {label:'Từ chối: số tiền chuyển khoản không khớp', actor:'Admin Specialist', time:'27/08/2026 09:00'}] }
    ];
    return raw.map(o => ({ ...o, amount: o.amountNum.toLocaleString('vi-VN') + 'đ' }));
  }

  // --- Danh sách ngân hàng & địa giới hành chính -------------------------
  // Nạp từ API công khai lúc khởi động; hỏng mạng thì rơi về danh sách rút gọn
  // bên dưới để prototype vẫn mở được bằng file://.
  BANKS_FALLBACK = ['Vietcombank — NH TMCP Ngoại thương Việt Nam','Techcombank — NH TMCP Kỹ thương Việt Nam','BIDV — NH Đầu tư và Phát triển Việt Nam','VietinBank — NH TMCP Công thương Việt Nam','Agribank — NH NN&PTNT Việt Nam','MB Bank — NH TMCP Quân đội','ACB — NH TMCP Á Châu','VPBank — NH TMCP Việt Nam Thịnh Vượng','Sacombank — NH TMCP Sài Gòn Thương Tín','TPBank — NH TMCP Tiên Phong','HDBank — NH TMCP Phát triển TP.HCM','SHB — NH TMCP Sài Gòn – Hà Nội','VIB — NH TMCP Quốc tế Việt Nam','MSB — NH TMCP Hàng Hải','OCB — NH TMCP Phương Đông','SeABank — NH TMCP Đông Nam Á','Eximbank — NH TMCP Xuất Nhập khẩu','LPBank — NH TMCP Lộc Phát Việt Nam','Nam A Bank — NH TMCP Nam Á','BVBank — NH TMCP Bản Việt'];

  PROVINCES_FALLBACK = [
    { name: 'Thành phố Hồ Chí Minh', wards: ['Phường Bến Thành','Phường Sài Gòn','Phường Cầu Ông Lãnh','Phường Bàn Cờ','Phường Chợ Lớn','Phường Bình Trưng','Phường An Khánh','Phường Thủ Đức','Phường Hoà Hưng','Phường Tân Sơn Nhất'] },
    { name: 'Thành phố Hà Nội', wards: ['Phường Hoàn Kiếm','Phường Ba Đình','Phường Cửa Nam','Phường Đống Đa','Phường Hai Bà Trưng','Phường Cầu Giấy','Phường Thanh Xuân','Phường Tây Hồ'] },
    { name: 'Thành phố Đà Nẵng', wards: ['Phường Hải Châu','Phường Thanh Khê','Phường Sơn Trà','Phường Ngũ Hành Sơn','Phường Liên Chiểu'] },
    { name: 'Thành phố Cần Thơ', wards: ['Phường Ninh Kiều','Phường Bình Thuỷ','Phường Cái Răng'] },
    { name: 'Thành phố Hải Phòng', wards: ['Phường Hồng Bàng','Phường Ngô Quyền','Phường Lê Chân'] },
    { name: 'Tỉnh Đồng Nai', wards: ['Phường Trấn Biên','Phường Biên Hoà','Phường Long Bình'] },
    { name: 'Tỉnh Tây Ninh', wards: ['Phường Tân Ninh','Phường Long Hoa'] },
    { name: 'Tỉnh Khánh Hoà', wards: ['Phường Nha Trang','Phường Bắc Nha Trang','Phường Cam Ranh'] }
  ];

  // Bỏ dấu tiếng Việt + viết hoa — dùng cho tên chủ tài khoản ngân hàng.
  vnUpper(s) {
    return (s || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
      .replace(/đ/g, 'd').replace(/Đ/g, 'D').toUpperCase();
  }

  // Nhập 22011991 -> hiển thị 22/01/1991
  dateMask(s) {
    const d = (s || '').replace(/\\D/g, '').slice(0, 8);
    if (d.length > 4) return d.slice(0, 2) + '/' + d.slice(2, 4) + '/' + d.slice(4);
    if (d.length > 2) return d.slice(0, 2) + '/' + d.slice(2);
    return d;
  }

  ADMIN_USERS = [
    { id:1, name:'Trần Quốc Head', email:'head@homi365.com.vn', role:'head', status:'active' },
    { id:2, name:'Hoàng Thị Mỹ Trinh', email:'trinh@homi365.com.vn', role:'head', status:'active' },
    { id:3, name:'Nguyễn Thu Hà', email:'ha.nt@homi365.com.vn', role:'specialist', status:'active' },
    { id:4, name:'Lê Minh Quân', email:'quan.lm@homi365.com.vn', role:'specialist', status:'active' },
    { id:5, name:'Phạm Bảo Ngọc', email:'ngoc.pb@homi365.com.vn', role:'specialist', status:'locked' }
  ];

  ORDER_RANGES = [['today','Hôm nay'],['week','Tuần này'],['month','Tháng này'],['all','Tất cả'],['custom','Khoảng ngày…']];
  ORDER_RANGE_VALUES = { today:'0', week:'3', month:'10', all:'27', custom:'6' };
  ORDER_RANGE_VALUES_NEW = { today:'0', week:'0', month:'1', all:'1', custom:'1' };

  // Trạng thái hồ sơ thành viên (khác vòng duyệt 2 lượt của rút tiền).
  MEMBER_STATUS_LABEL = {
    pending: 'Chờ xác nhận thanh toán',
    specialist_approved: 'Chờ Manager duyệt',
    active: 'Đang hoạt động',
    locked: 'Đã khoá',
    rejected: 'Từ chối'
  };

  // 6 hạng chính thức — không dịch sang tiếng Việt.
  RANKS = ['Copper', 'Silver', 'Gold', 'Diamond', 'Titanium', 'Lithium'];
  RANK_LABEL = { 'Đồng': 'Copper', 'Bạc': 'Silver', 'Vàng': 'Gold',
                 'Kim cương': 'Diamond', 'Titan': 'Titanium', 'Lithium': 'Lithium' };

  // 7.3.3 AC: hiển thị số đơn còn thiếu để lên hạng kế tiếp.
  // Ngưỡng Silver = 10 đơn. Copper vừa bán 1 đơn -> còn 9 đơn.
  RANK_PROGRESS = { new: 'Còn 9 đơn để lên hạng Silver',
                    active: 'Còn 8 đơn để lên hạng Gold' };

  RANK_HISTORY = {
    1: [{ label:'Thăng hạng Copper → Silver', time:'01/09/2026' },
        { label:'Tham gia · hạng Copper', time:'12/08/2026' }],
    5: [{ label:'Thăng hạng Silver → Gold', time:'01/09/2026' },
        { label:'Thăng hạng Copper → Silver', time:'20/08/2026' },
        { label:'Tham gia · hạng Copper', time:'01/08/2026' }],
    3: [{ label:'Giáng hạng Silver → Copper · 0 đơn trong tháng', time:'01/09/2026' },
        { label:'Tham gia · hạng Copper', time:'22/08/2026' }]
  };

  // 1 sản phẩm pilot duy nhất theo 6.1.C-3. Gói license (1 năm / nửa năm) và
  // giá KHÔNG quản ở màn này — chốt 09/09.
  PRODUCTS = [
    { id: 'CN02', sku: 'CN02', name: 'Gói Bác sĩ 24/7 · kèm đồng hồ HW01',
      imageLabel: 'cn02.png',
      desc: 'Gói chăm sóc sức khoẻ từ xa: 01 đồng hồ thông minh HW01 theo dõi nhịp tim / SOS giao tận nơi, kèm phần mềm Bác sĩ 24/7 (mã kích hoạt gửi qua SMS).' }
  ];

  componentDidMount() {"""),

    # Tính toán cho màn Đơn hàng, đặt ngay trước khối return của renderVals.
    ("    return {\n      nav, adminNav,",
     """    // Dữ liệu cho 3 dropdown có tìm kiếm. norm() bỏ dấu để gõ "ho chi minh"
    // vẫn ra "Hồ Chí Minh".
    const norm = (x) => (x || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
      .replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase().trim();
    const bankList = s.banks || this.BANKS_FALLBACK;
    const provList = s.provinceData || this.PROVINCES_FALLBACK;
    const curProv = provList.find(p => p.name === s.provinceQuery);
    const wardList = (curProv && curProv.wards) || [];

    // Đơn hàng (B6) — bổ sung, không có trong mockup KH
    const ordersRaw = s.ordersData || [];
    const orderRows = ordersRaw
      .filter(o => (s.orderStatusFilter === 'all' || !s.orderStatusFilter) || o.status === s.orderStatusFilter)
      .filter(o => !s.orderSearch
        || o.id.toLowerCase().includes(s.orderSearch.toLowerCase())
        || o.buyer.toLowerCase().includes(s.orderSearch.toLowerCase())
        || o.phone.includes(s.orderSearch))
      .map(o => {
        const [bg, color, label] = this.badge(o.status);
        return { ...o, badgeBg: bg, badgeColor: color, statusLabel: label,
          // Nội dung chuyển khoản đúng cú pháp hướng dẫn ở màn QR (A1).
          transferNote: o.buyer + ' - Chuyen khoan don hang ' + o.id,
          // Ngày kích hoạt = lúc admin xác nhận tiền về; hết hiệu lực theo gói.
          activatedLabel: o.activatedAt || '—',
          expiresLabel: o.activatedAt
            ? (function (d) { const q = d.split('/');
                return q.length === 3 ? q[0] + '/' + q[1] + '/' + (parseInt(q[2], 10) + 1) : '—'; })(o.activatedAt)
            : '—',
          proofLabel: o.proof ? 'Đã tải lên' : 'Chưa có',
          proofBg: o.proof ? 'rgba(132,190,82,.14)' : 'rgba(170,170,170,.18)',
          proofColor: o.proof ? '#4c7a2e' : '#5c5c5c',
          onClick: () => this.setState({ selectedOrderId: o.id }) };
      });
    const selOrderRaw = s.selectedOrderId ? ordersRaw.find(o => o.id === s.selectedOrderId) : null;
    let selectedOrder = null;
    if (selOrderRaw) {
      const [obg, ocolor, olabel] = this.badge(selOrderRaw.status);
      const isSpecO = s.adminRole === 'specialist';
      // Chốt 09/09 (bản mới): đơn hàng CHỈ CẦN 1 admin xác nhận, không duyệt
      // 2 lớp. Xác nhận tiền về + chọn mã kích hoạt -> gửi email cho khách ngay.
      const canConfirmO = selOrderRaw.status === 'order_pending';
      const canRejectO = selOrderRaw.status === 'order_pending';
      selectedOrder = { ...selOrderRaw, badgeBg: obg, badgeColor: ocolor, statusLabel: olabel,
        activationCodeLabel: selOrderRaw.activationCode || '— chưa cấp —',
        canConfirm: canConfirmO, canReject: canRejectO, canAct: canConfirmO || canRejectO,
        needsCodePick: canConfirmO,
        isRejected: selOrderRaw.status === 'order_rejected',
        confirmLabel: 'Xác nhận tiền về và kích hoạt mã đơn hàng (Admin)',
        stageNote: selOrderRaw.status === 'order_pending'
          ? 'Đang chờ admin đối soát tiền về. Xác nhận xong hệ thống gửi email kèm mã kích hoạt cho khách ngay.'
          : (selOrderRaw.status === 'order_rejected' ? 'Đơn đã bị từ chối.' : null),
        actHint: 'Chọn mã kích hoạt còn Sẵn hàng trong kho rồi xác nhận. Hệ thống gán mã cho đơn, chuyển mã sang Đã gán đơn hàng và gửi email báo thanh toán thành công kèm mã kích hoạt cho khách.' };
    }

    return {
      nav, adminNav,"""),

    # Giá trị cho màn Quản lý sản phẩm + modal Thêm hàng vào kho.
    ("      hasActionModal: !!s.actionModal,",
     """      // 7.9.1 — Tài khoản admin
      adminUsers: this.ADMIN_USERS.map(u => {
        const locked = (s.adminUserLocks[u.id] || u.status) === 'locked';
        return { ...u,
          roleLabel: u.role === 'head' ? 'Head Admin' : 'Admin Specialist',
          roleBg: u.role === 'head' ? 'rgba(0,173,238,.14)' : 'rgba(170,170,170,.18)',
          roleColor: u.role === 'head' ? '#00728f' : '#5c5c5c',
          statusLabel: locked ? 'Đã khoá' : 'Đang hoạt động',
          badgeBg: locked ? 'rgba(170,170,170,.18)' : 'rgba(132,190,82,.14)',
          badgeColor: locked ? '#5c5c5c' : '#4c7a2e',
          lockLabel: locked ? 'Mở khoá' : 'Khoá',
          lockStyle: 'height:32px;padding:0 var(--s5);background:var(--c12);border-radius:var(--r-md);font-size:12px;font-weight:600;border:1px solid '
            + (locked ? 'var(--c6);color:var(--c6)' : '#D9342B;color:#D9342B'),
          onToggleLock: () => this.setState({ adminUserLocks: { ...s.adminUserLocks, [u.id]: locked ? 'active' : 'locked' } }),
          onEdit: () => this.setState({ showAdminUserForm: true, editingAdminUserId: u.id }) };
      }),
      adminUserCount: this.ADMIN_USERS.length,
      showAdminUserForm: s.showAdminUserForm,
      adminUserFormTitle: s.editingAdminUserId ? 'Sửa tài khoản admin' : 'Thêm tài khoản admin',
      adminUserFormName: (this.ADMIN_USERS.find(u => u.id === s.editingAdminUserId) || {}).name || '',
      adminUserFormEmail: (this.ADMIN_USERS.find(u => u.id === s.editingAdminUserId) || {}).email || '',
      openAdminUserForm: () => this.setState({ showAdminUserForm: true, editingAdminUserId: null }),
      closeAdminUserForm: () => this.setState({ showAdminUserForm: false, editingAdminUserId: null }),

      // (12) Khối "Thông tin hồ sơ" — mở/đóng và sửa được.
      profileOpen: s.profileOpen, profileCaret: s.profileOpen ? '▴' : '▾',
      toggleProfile: () => this.setState({ profileOpen: !s.profileOpen, profileEdit: false }),
      profileRead: s.profileOpen && !s.profileEdit,
      profileEdit: s.profileOpen && s.profileEdit,
      startProfileEdit: () => this.setState({ profileEdit: true,
        profileDraft: { ...(selectedMember || {}) } }),
      cancelProfileEdit: () => this.setState({ profileEdit: false, profileDraft: {} }),
      saveProfileEdit: () => this.setState({
        memberEdits: { ...s.memberEdits, [s.selectedMemberId]: { ...s.profileDraft } },
        profileEdit: false, profileDraft: {} }),
      pfName: (s.profileDraft || {}).name || '',
      setPfName: (e) => this.setState({ profileDraft: { ...s.profileDraft, name: e.target.value } }),
      pfPhone: (s.profileDraft || {}).phone || '',
      setPfPhone: (e) => this.setState({ profileDraft: { ...s.profileDraft, phone: e.target.value } }),
      pfEmail: (s.profileDraft || {}).email || '',
      setPfEmail: (e) => this.setState({ profileDraft: { ...s.profileDraft, email: e.target.value } }),
      pfCccd: (s.profileDraft || {}).cccd || '',
      setPfCccd: (e) => this.setState({ profileDraft: { ...s.profileDraft, cccd: e.target.value } }),
      pfDob: (s.profileDraft || {}).dobGender || '',
      setPfDob: (e) => this.setState({ profileDraft: { ...s.profileDraft, dobGender: e.target.value } }),
      pfAddress: (s.profileDraft || {}).address || '',
      setPfAddress: (e) => this.setState({ profileDraft: { ...s.profileDraft, address: e.target.value } }),
      pfBankAccount: (s.profileDraft || {}).bankAccount || '',
      setPfBankAccount: (e) => this.setState({ profileDraft: { ...s.profileDraft, bankAccount: e.target.value } }),
      pfBankHolder: (s.profileDraft || {}).bankHolder || '',
      setPfBankHolder: (e) => this.setState({ profileDraft: { ...s.profileDraft, bankHolder: this.vnUpper(e.target.value) } }),

      // (10) Kết quả tra cứu đơn hàng
      lookupResult: s.lookupResult,
      hasLookupResult: !!s.lookupResult,
      noLookupResult: !s.lookupResult,
      lookupContinue: () => {
        const r = s.lookupResult;
        if (!r) return;
        if (s.uplineRank === 'bronze') {
          this.setState({ showOrderLookup: false, showUplineBlockedModal: true });
          return;
        }
        GO('A2', { regStep: 1, orderId: r.orderId, uplineRank: s.uplineRank,
          buyerName: r.buyerName, buyerPhone: r.phone, buyerEmail: r.email,
          buyerCccd: r.cccd, buyerAddress: r.address, buyerDob: r.dob });
      },

      // --- Dropdown có tìm kiếm: ngân hàng / tỉnh thành / phường xã --------
      bankQuery: s.bankQuery, bankOpen: s.bankOpen,
      toggleBank: () => this.setState({ bankOpen: !s.bankOpen }),
      setBankQuery: (e) => this.setState({ bankQuery: e.target.value, bankOpen: true }),
      bankOptions: bankList.filter(b => norm(b).includes(norm(s.bankQuery)) || s.bankQuery === b)
        .slice(0, 60).map(b => ({ label: b,
          onPick: () => this.setState({ bankQuery: b, bankOpen: false }) })),
      bankEmpty: bankList.filter(b => norm(b).includes(norm(s.bankQuery))).length === 0,
      bankCount: bankList.length,

      provinceQuery: s.provinceQuery, provinceOpen: s.provinceOpen,
      toggleProvince: () => this.setState({ provinceOpen: !s.provinceOpen }),
      setProvinceQuery: (e) => this.setState({ provinceQuery: e.target.value, provinceOpen: true }),
      provinceOptions: provList.filter(p => norm(p.name).includes(norm(s.provinceQuery)) || s.provinceQuery === p.name)
        .slice(0, 80).map(p => ({ label: p.name,
          onPick: () => this.setState({ provinceQuery: p.name, provinceOpen: false,
            wardQuery: (p.wards && p.wards[0]) || '' }) })),
      provinceEmpty: provList.filter(p => norm(p.name).includes(norm(s.provinceQuery))).length === 0,

      wardQuery: s.wardQuery, wardOpen: s.wardOpen,
      toggleWard: () => this.setState({ wardOpen: !s.wardOpen }),
      setWardQuery: (e) => this.setState({ wardQuery: e.target.value, wardOpen: true }),
      wardOptions: wardList.filter(w => norm(w).includes(norm(s.wardQuery)) || s.wardQuery === w)
        .slice(0, 120).map(w => ({ label: w,
          onPick: () => this.setState({ wardQuery: w, wardOpen: false }) })),
      wardEmpty: wardList.filter(w => norm(w).includes(norm(s.wardQuery))).length === 0,

      // Tên chủ tài khoản — tự viết hoa, bỏ dấu.
      accountHolder: s.accountHolder,
      setAccountHolder: (e) => this.setState({ accountHolder: this.vnUpper(e.target.value) }),

      // Điều khoản mua hàng — chưa tích thì không bấm thanh toán được.
      buyTcChecked: s.buyTcChecked,
      toggleBuyTc: () => this.setState({ buyTcChecked: !s.buyTcChecked }),
      // (17) Khoá nút khi chưa tích điều khoản HOẶC đang chờ phản hồi —
      // vế sau là cách chặn bấm dồn tạo hai đơn.
      payDisabled: !s.buyTcChecked || s.payStage === 'sending',
      payStyle: 'height:48px;color:var(--c12);border:none;border-radius:var(--r-md);'
        + 'font-size:16px;font-weight:700;box-shadow:var(--sh);background:'
        + ((s.buyTcChecked && s.payStage !== 'sending')
             ? 'var(--c6)' : 'rgba(170,170,170,.5)')
        + ';cursor:' + ((s.buyTcChecked && s.payStage !== 'sending')
             ? 'pointer' : 'not-allowed'),

      // CCCD — ngày cấp / nơi cấp (màn đăng ký agent)
      cccdIssueDate: s.cccdIssueDate,
      setCccdIssueDate: (e) => this.setState({ cccdIssueDate: this.dateMask(e.target.value) }),
      cccdIssuePlace: s.cccdIssuePlace,
      setCccdIssuePlace: (e) => this.setState({ cccdIssuePlace: e.target.value }),

      // Tài khoản nhận tiền hiển thị ở modal rút tiền — lấy từ hồ sơ agent,
      // agent không sửa được ở đây (muốn đổi phải qua CSKH).
      withdrawHolder: this.vnUpper(s.accountHolder) || 'HOANG THI MY TRINH',
      withdrawBank: 'Vietcombank — NH TMCP Ngoại thương Việt Nam',
      withdrawAccount: s.buyerBankAccount || '0071001234567',

      // 7.3.3 — còn thiếu bao nhiêu đơn để lên hạng kế tiếp
      rankProgress: this.RANK_PROGRESS[s.agentStage === 'active' ? 'active' : 'new'],

      // 7.3.2 — lọc số đơn theo khoảng thời gian, có cả khoảng ngày tuỳ chỉnh
      isCustomRange: s.orderRange === 'custom',
      orderRanges: this.ORDER_RANGES.map(([id, label]) => ({
        id, label, onClick: () => this.setState({ orderRange: id }),
        style: 'font-size:12px;font-weight:600;padding:6px 14px;border-radius:30px;border:1px solid '
          + ((s.orderRange || 'month') === id ? '#00ADEE;background:rgba(0,173,238,.08);color:#00ADEE'
                                              : 'rgba(170,170,170,.4);background:transparent;color:var(--c5)')
      })),

      // Chốt 09/09: agent chỉ có MỘT link. Mã giới thiệu = alias theo
      // 8.1.C-4 (viết tắt họ tên + 4 số cuối SĐT), trùng thì thêm -2, -3…
      refCode: 'HTMT0083',
      refLink: 'homi365.com.vn/htmt0083',

      orderTotal: (s.ordersData || []).length,
      orderPendingCount: (s.ordersData || []).filter(o => o.status === 'order_pending').length,
      orderRejectedCount: (s.ordersData || []).filter(o => o.status === 'order_rejected').length,
      orderPaidCount: (s.ordersData || []).filter(o => o.status === 'order_paid').length,
      orderRevenue: (s.ordersData || []).filter(o => o.status === 'order_paid')
        .reduce((t, o) => t + o.amountNum, 0).toLocaleString('vi-VN') + 'đ',
      orderSearch: s.orderSearch,
      setOrderSearch: (e) => this.setState({ orderSearch: e.target.value }),
      orderFilters: this.ORDER_FILTERS.map(([id, label]) => ({
        id, label, onClick: () => this.setState({ orderStatusFilter: id }),
        style: 'height:34px;padding:0 14px;border-radius:30px;font-size:12px;font-weight:600;border:1px solid ' +
          ((s.orderStatusFilter || 'all') === id ? '#00ADEE;background:rgba(0,173,238,.08);color:#00ADEE'
                                                 : 'rgba(170,170,170,.4);background:transparent;color:var(--c5)')
      })),
      orders: orderRows, ordersEmpty: orderRows.length === 0,
      hasSelectedOrder: !!selectedOrder, selectedOrder,
      closeOrder: () => this.setState({ selectedOrderId: null }),
      availableStockCodes: stockData.filter(p => p.status === 'available').slice(0, 60)
        .map(p => ({ code: p.activationCode, sku: p.sku,
                     label: p.activationCode + '  ·  ' + p.sku })),
      availableStockCount: stockData.filter(p => p.status === 'available').length,
      orderActivationCode: s.orderActivationCode,
      setOrderActivationCode: (e) => this.setState({ orderActivationCode: e.target.value, orderCodeError: '' }),
      orderCodeError: s.orderCodeError,
      bankTxnCode: s.bankTxnCode,
      setBankTxnCode: (e) => this.setState({ bankTxnCode: e.target.value, orderCodeError: '' }),
      confirmOrder: () => {
        const o = (s.ordersData || []).find(x => x.id === s.selectedOrderId);
        if (!o) return;
        const now = '08/09/2026 10:00';
        const who = s.adminRole === 'specialist' ? 'Admin Specialist' : 'Head Admin';
        const code = s.orderActivationCode;
        if (!code) { this.setState({ orderCodeError: 'Chọn mã kích hoạt từ kho trước khi xác nhận.' }); return; }
        if (!(s.bankTxnCode || '').trim()) { this.setState({ orderCodeError: 'Nhập mã giao dịch ngân hàng để đối soát.' }); return; }
        const item = stockData.find(p => p.activationCode === code && p.status === 'available');
        if (!item) { this.setState({ orderCodeError: 'Mã ' + code + ' không còn ở trạng thái Sẵn hàng.' }); return; }
        this.setState({
          ordersData: s.ordersData.map(x => x.id === o.id
            ? { ...x, status: 'order_paid', activationCode: code,
                activatedAt: now.slice(0, 10),
                auditLog: [...x.auditLog,
                  { label: 'Xác nhận tiền về (GD ' + s.bankTxnCode.trim() + ') và kích hoạt mã ' + code, actor: who, time: now },
                  { label: 'Gửi email báo thanh toán thành công kèm mã kích hoạt cho khách', actor: 'Hệ thống', time: now }] }
            : x),
          stockData: stockData.map(p => p.activationCode === code
            ? { ...p, status: 'assigned', orderId: o.id, seller: o.referrer,
                log: [...p.log, { label: 'Gán cho đơn ' + o.id, time: now }] }
            : p),
          orderActivationCode: '', orderCodeError: '', bankTxnCode: ''
        });
      },
      rejectOrder: () => {
        const now = '08/09/2026 10:05';
        const actor = s.adminRole === 'specialist' ? 'Admin Specialist' : 'Head Admin';
        this.setState({ ordersData: s.ordersData.map(x => x.id === s.selectedOrderId
          ? { ...x, status: 'order_rejected',
              auditLog: [...x.auditLog, { label: 'Từ chối đơn', actor, time: now }] }
          : x) });
      },

      products: this.PRODUCTS.map(p => ({ ...p,
        onEdit: () => this.setState({ showProductForm: true, editingProductId: p.id }) })),
      productCount: this.PRODUCTS.length,
      showProductForm: s.showProductForm,
      productFormTitle: s.editingProductId ? 'Sửa sản phẩm' : 'Thêm sản phẩm',
      productFormName: (this.PRODUCTS.find(p => p.id === s.editingProductId) || {}).name || '',
      productFormDesc: (this.PRODUCTS.find(p => p.id === s.editingProductId) || {}).desc || '',
      openProductForm: () => this.setState({ showProductForm: true, editingProductId: null }),
      closeProductForm: () => this.setState({ showProductForm: false, editingProductId: null }),

      showAddStock: s.showAddStock,
      openAddStock: () => this.setState({ showAddStock: true, addStockSku: '', addStockCode: '', addStockError: '' }),
      closeAddStock: () => this.setState({ showAddStock: false }),
      addStockSku: s.addStockSku, setAddStockSku: (e) => this.setState({ addStockSku: e.target.value, addStockError: '' }),
      addStockCode: s.addStockCode, setAddStockCode: (e) => this.setState({ addStockCode: e.target.value, addStockError: '' }),
      addStockError: s.addStockError,
      submitAddStock: () => {
        const sku = (s.addStockSku || '').trim(), code = (s.addStockCode || '').trim();
        if (!sku || !code) { this.setState({ addStockError: 'Nhập đủ mã sản phẩm và mã kích hoạt.' }); return; }
        if (stockData.some(p => p.activationCode.toLowerCase() === code.toLowerCase())) {
          this.setState({ addStockError: 'Mã kích hoạt ' + code + ' đã có trong kho.' }); return; }
        if (stockData.some(p => p.sku.toLowerCase() === sku.toLowerCase())) {
          this.setState({ addStockError: 'Mã sản phẩm ' + sku + ' đã có trong kho.' }); return; }
        this.setState({
          stockData: [{ id: 900000 + stockData.length, sku, activationCode: code,
            orderId: '—', seller: '—', stockedAt: '08/09/2026', status: 'available',
            log: [{ label: 'Nhập kho (thủ công)', time: '08/09/2026 10:00' }] }, ...stockData],
          showAddStock: false, addStockError: ''
        });
      },

      showImportStock: s.showImportStock,
      openImportStock: () => this.setState({ showImportStock: true, importText: '', importResult: null }),
      closeImportStock: () => this.setState({ showImportStock: false }),
      importText: s.importText, setImportText: (e) => this.setState({ importText: e.target.value }),
      importResult: s.importResult, hasImportResult: !!s.importResult,
      runImportStock: () => {
        // Nhập từng phần: dòng nào hợp lệ thì nhận, dòng trùng hoặc thiếu dữ
        // liệu thì bỏ qua và liệt kê lý do. Chặn trùng cả với kho hiện có lẫn
        // trùng nhau trong chính danh sách đang dán.
        const lines = (s.importText || '').split('\\n').map(l => l.trim()).filter(Boolean);
        const seenCode = new Set(stockData.map(p => p.activationCode.toLowerCase()));
        const seenSku = new Set(stockData.map(p => p.sku.toLowerCase()));
        const added = [], skipped = [];
        lines.forEach((line, i) => {
          const parts = line.split(/[,;\\t]+/).map(x => x.trim());
          const sku = parts[0], code = parts[1];
          if (!sku || !code) { skipped.push({ line, reason: 'Thiếu mã sản phẩm hoặc mã kích hoạt' }); return; }
          if (seenCode.has(code.toLowerCase())) { skipped.push({ line, reason: 'Trùng mã kích hoạt' }); return; }
          if (seenSku.has(sku.toLowerCase())) { skipped.push({ line, reason: 'Trùng mã sản phẩm' }); return; }
          seenCode.add(code.toLowerCase()); seenSku.add(sku.toLowerCase());
          added.push({ id: 950000 + i, sku, activationCode: code, orderId: '—', seller: '—',
            stockedAt: '08/09/2026', status: 'available',
            log: [{ label: 'Nhập kho (import hàng loạt)', time: '08/09/2026 10:00' }] });
        });
        this.setState({
          stockData: [...added, ...stockData],
          importResult: { total: lines.length, ok: added.length, skip: skipped.length,
            hasSkipped: skipped.length > 0, skipped: skipped.slice(0, 30) }
        });
      },

      hasActionModal: !!s.actionModal,"""),
]

# ============================================================================

# Thanh trên giờ chỉ còn logo, nên logo phải đủ lớn để không bị lọt thỏm.
# Đổi 2 số này là đổi được cả chiều cao thanh.
LOGO_H = 71           # px — chiều cao ảnh logo. Ảnh tỉ lệ 2.44:1 nên 71px cao
                      # = 174px ngang = đúng 15% khung nội dung 1160px.
BAR_PAD_Y = 16        # px trên/dưới (mockup gốc là --s5 = 12px)
BAR_H = BAR_PAD_Y * 2 + LOGO_H + 1        # +1 = đường kẻ dưới
CONTENT_MAX = 1160    # px — bằng khung nội dung màn A1, để logo thẳng hàng

# (12/10) Bỏ trang danh sách màn hình ở bản prod.
LOGO_HOME = {"a3-dashboard.html": "a3-dashboard.html",
             "b1-admin-login.html": "b1-admin-login.html"}
INDEX_REDIRECT = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HOMI365</title>
<link rel="icon" href="assets/Icon_viewweb_final.jpg">
<meta name="theme-color" content="#1E3A66">
<meta http-equiv="refresh" content="0; url=screens/a1-buy.html">
<script>location.replace('screens/a1-buy.html' + location.search + location.hash);</script>
</head>
<body></body>
</html>
"""

LOGO_HTML = (
    '<a href="../index.html" title="Danh sách màn hình" class="homi-logo" '
    'style="display:flex;align-items:center;text-decoration:none">'
    '<img src="../assets/logo homi-01.png" alt="HOMI365" '
    'style="height:%dpx;width:auto;display:block"></a>' % LOGO_H
)

# Nút "Đăng nhập Agent" ở góc phải thanh trên — chỉ hiện trên màn công khai
# (A1 mua hàng, A2 đăng ký). Không hiện ở C1 vì đang đứng sẵn ở đó, không hiện
# ở A3 vì đã đăng nhập, không hiện ở khung quản trị.
LOGIN_BTN = (
    # flex:none + nowrap: logo to lên thì nút không được phép co lại rồi vỡ chữ
    # thành cột hẹp như trước.
    '<a href="c1-login.html" class="homi-login" '
    'style="margin-left:auto;flex:none;white-space:nowrap;'
    'display:inline-flex;'
    'align-items:center;gap:var(--s3);height:38px;padding:0 var(--s6);'
    # Viền dùng đúng màu viền chung của mockup (ô nhập, nút phụ như "Xuất CSV")
    # để thanh trên không lệch tông với phần bên dưới.
    'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);color:var(--c6);'
    'background:var(--c12);font-size:14px;font-weight:600;text-decoration:none"'
    ' style-hover="background:rgba(170,170,170,.08)">Đăng nhập thành viên HOMI365</a>'
)


def drop_district(html):
    """Bỏ ô 'Quận/Huyện' khỏi hàng địa chỉ, đưa hàng từ 3 cột về 2 cột.

    Từ 01/07/2025 Việt Nam bỏ cấp huyện, địa chỉ hành chính chỉ còn
    tỉnh/thành -> phường/xã. Mockup KH soạn trước mốc này nên vẫn còn ô huyện.
    """
    ls = html.split("\n")
    out, i, n = [], 0, 0
    while i < len(ls):
        # A1 ghi "Quận/Huyện (*)", A2 ghi "Quận/Huyện" — bắt cả hai.
        if re.search(r">Quận/Huyện( \(\*\))?</label>", ls[i]):
            # 3 dòng: <div><label>, <sc-raw-select>, </div>
            if "sc-raw-select" not in ls[i + 1] or ls[i + 2].strip() != "</div>":
                die("khối Quận/Huyện không đúng dạng 3 dòng như dự kiến")
            i += 3
            n += 1
            continue
        out.append(ls[i])
        i += 1
    if n:
        for k, l in enumerate(out):
            out[k] = l.replace("grid-template-columns:1fr 1fr 1fr",
                               "grid-template-columns:1fr 1fr")
    return "\n".join(out), n


def die(msg):
    sys.exit("LỖI: " + msg)


def main():
    if not SRC.exists():
        die("chưa có %s — chạy extract-bundle.py trước." % SRC)

    text = SRC.read_text(encoding="utf-8")
    lines = text.split("\n")

    # (UAT 02/10) Thêm / đổi tên các trạng thái xem thử.
    uat.patch_screens(SCREENS)

    def seg(a, b):
        """Lấy các dòng a..b (1-based, bao gồm cả hai đầu)."""
        return "\n".join(lines[a - 1:b])

    # --- cắt khối <sc-if> theo cặp thẻ, không đoán dòng kết thúc ----------
    def block(start_line):
        start_off = sum(len(l) + 1 for l in lines[:start_line - 1])
        i = text.find("<sc-if", start_off)
        if i < 0:
            die("không tìm thấy <sc-if> sau dòng %d" % start_line)
        depth, j = 0, i
        while True:
            no = text.find("<sc-if", j)
            nc = text.find("</sc-if>", j)
            if nc < 0:
                die("thiếu </sc-if> cho khối ở dòng %d" % start_line)
            if 0 <= no < nc:
                depth += 1
                j = no + 6
            else:
                depth -= 1
                j = nc + 8
                if depth == 0:
                    return text[start_off:j]

    # --- CSS -------------------------------------------------------------
    (V3 / "css").mkdir(parents=True, exist_ok=True)
    (V3 / "css" / "fonts").mkdir(exist_ok=True)
    (V3 / "js").mkdir(exist_ok=True)
    (V3 / "screens").mkdir(exist_ok=True)

    fonts_css = seg(*L_FONTS).replace('url("res/', 'url("fonts/')
    fonts_css = re.sub(r"^\s*<style>", "", fonts_css)   # dòng 12 dính thẻ mở
    (V3 / "css" / "fonts.css").write_text(
        "/* Nunito + Roboto — trích nguyên xi từ mockup KH, không đổi. */\n" + fonts_css,
        encoding="utf-8")

    (V3 / "css" / "base.css").write_text(
        "/* Reset — trích nguyên xi từ mockup KH. */\n" + seg(*L_BASE), encoding="utf-8")

    (V3 / "css" / "responsive.css").write_text(RESPONSIVE_CSS, encoding="utf-8")

    # --- tokens.css: bóc biến ra khỏi style inline của thẻ gốc ------------
    m = re.search(r'style="([^"]*)"', lines[L_ROOTDIV - 1])
    if not m:
        die("không đọc được style của thẻ gốc ở dòng %d" % L_ROOTDIV)
    decls = [d.strip() for d in m.group(1).split(";") if d.strip()]
    tokens = [d for d in decls if d.startswith("--")]
    rest = [d for d in decls if not d.startswith("--")]

    tok_lines = []
    for d in tokens:
        k, v = d.split(":", 1)
        nv = recolor(v.strip())
        note = ("   /* was %s */" % v.strip()) if nv != v.strip() else ""
        tok_lines.append("  %s: %s;%s" % (k.strip(), nv, note))

    (V3 / "css" / "tokens.css").write_text(
        "/* ============================================================\n"
        "   HOMI365 · prototype-v3 — bảng màu\n"
        "   Tên biến giữ NGUYÊN của mockup KH, chỉ đổi giá trị.\n"
        "   Sinh tự động bởi tools/build-v3.py — đừng sửa tay,\n"
        "   sửa bảng COLORS trong script rồi chạy lại.\n"
        "   ============================================================ */\n"
        ":root {\n" + "\n".join(tok_lines) + "\n"
        "\n  /* Bổ sung: nền trang ấm của HOMI365 (prototype-v2 --warm-50).\n"
        "     Thẻ/card vẫn dùng --c12 trắng -> section xen kẽ ấm / trắng. */\n"
        "  --warm-50: " + WARM + ";\n"
        "\n  /* Bổ sung: màu cột biểu đồ — teal-500 của HOMI365.\n"
        "     Dùng teal thay navy để biểu đồ tách khỏi nút/link màu chính. */\n"
        "  --c-chart: " + CHART + ";\n}\n\n"
        "/* Vòng focus — mockup KH không có, thêm để đạt WCAG 2.4.7.\n"
        "   Không ảnh hưởng layout. */\n"
        ":where(a, button, input, select, textarea):focus-visible {\n"
        "  outline: 2px solid #0F7F96;\n"
        "  outline-offset: 2px;\n"
        "}\n", encoding="utf-8")

    # Khung gốc là cột co giãn để footer luôn nằm đáy, kể cả khi nội dung màn
    # ngắn hơn màn hình (màn OTP, màn đăng nhập…).
    root_open = ('<div style="%s; display:flex; flex-direction:column">'
                 % "; ".join(rest)).replace(
        "background:var(--c12)", "background:var(--warm-50)")

    # --- runtime + font ---------------------------------------------------
    js_src = [p for p in (RAW / "res").glob("*.js")]
    runtime = RAW / "res" / "d3a2f2c4-e44e-4524-ab01-ec4bd8675302.js"
    if not runtime.exists():
        die("thiếu runtime %s" % runtime.name)
    shutil.copy(runtime, V3 / "js" / "dc-runtime.js")

    # (8) Ô OTP tự nhảy — viết ngoài runtime của KH để khỏi đụng vào nó.
    (V3 / "js" / "otp.js").write_text(uat.patch_otp(OTP_JS, die), encoding="utf-8")
    n_font = 0
    for f in (RAW / "res").glob("*.woff2"):
        shutil.copy(f, V3 / "css" / "fonts" / f.name)
        n_font += 1

    # --- thanh trên: chỉ còn logo -----------------------------------------
    # Bỏ theo yêu cầu: chữ "Homi365 ●", dòng "WhiteCoat Việt Nam · 7 màn hình
    # MVP", và dãy nút chuyển màn A1…B4 (đó là khung điều khiển của bản mockup,
    # không thuộc sản phẩm). Giữ nguyên style của thẻ bọc để chiều cao và
    # đường kẻ dưới không đổi. Bấm logo -> về trang mục lục.
    wrap0 = lines[L_TOPBAR_WRAP - 1].strip()
    if not wrap0.startswith("<div style=\"position:sticky"):
        die("dòng %d không phải thẻ bọc thanh trên" % L_TOPBAR_WRAP)
    if "padding:var(--s5) var(--s8)" not in wrap0:
        die("không tìm thấy padding của thanh trên để nới")

    def make_topbar(pad_x, inner_max=None, right=""):
        """Thanh trên. pad_x quyết định logo thẳng hàng với cái gì."""
        w = wrap0.replace("padding:var(--s5) var(--s8)",
                          "padding:%dpx %s" % (BAR_PAD_Y, pad_x))
        # Móc class để css/responsive.css bám vào — markup gốc toàn style inline.
        w = w.replace('<div style="position:sticky',
                      '<div class="homi-topbar" style="position:sticky', 1)
        if inner_max is None:
            return ("  " + w + "\n    " + LOGO_HTML +
                    (("\n    " + right) if right else "") + "\n  </div>")
        return ("  " + w + "\n"
                '    <div class="homi-topbar-in" style="width:100%;max-width:' +
                str(inner_max) +
                'px;margin:0 auto;display:flex;align-items:center">\n'
                "      " + LOGO_HTML +
                (("\n      " + right) if right else "") +
                "\n    </div>\n  </div>")

    # Màn người mua / thành viên: nội dung nằm trong khung 1160px canh giữa,
    # đệm ngang var(--s7)=16px -> logo dùng đúng khung đó thì mép trái trùng nhau.
    TOPBAR_WEB = make_topbar("var(--s7)", CONTENT_MAX)
    TOPBAR_PUBLIC = make_topbar("var(--s7)", CONTENT_MAX, LOGIN_BTN)
    # (08/10) A1: ô SĐT + nút Tiếp tục nằm ngay trên thanh trên, sát logo;
    # nút đăng nhập thành viên vẫn ở góc phải.
    TOPBAR_A1 = make_topbar("var(--s7)", CONTENT_MAX, uat.A1_HEADER_PHONE + LOGIN_BTN)
    # Màn quản trị: bố cục tràn màn hình, sidebar đệm ngang var(--s5)=12px
    # -> logo canh theo mép trái của các mục sidebar.
    TOPBAR_ADMIN = make_topbar("var(--s5)")

    # --- JS ---------------------------------------------------------------
    script = seg(*L_SCRIPT)
    for old, new in JS_PATCHES:
        if old not in script:
            die("không khớp đoạn JS cần sửa:\n---\n%s\n---" % old[:120])
        script = script.replace(old, new, 1)

    # (13) Đổi tên vai — chạy sau mọi bản vá theo neo để khỏi phá neo.
    script = rename_roles(script)

    # --- đổi màu toàn bộ ---------------------------------------------------
    TOPBAR_WEB = recolor(TOPBAR_WEB)
    TOPBAR_PUBLIC = recolor(TOPBAR_PUBLIC)
    TOPBAR_A1 = recolor(TOPBAR_A1)
    TOPBAR_ADMIN = recolor(TOPBAR_ADMIN)
    script = recolor(script)
    # (UAT 02/10) Bản vá JS đợt 06/10 — chạy sau cùng, neo chặt.
    script = uat.patch_script(script, die)
    # Bản vá markup thay chuỗi trực tiếp và IM LẶNG khi neo không khớp — khác
    # JS_PATCHES vốn die() ngay. Đã dính hai lần: neo bị một bản vá chạy trước
    # sửa mất (Seller -> Thành viên) làm hàng tiêu đề bảng kho thiếu 3 cột mà
    # build vẫn báo "Xong". Ghi lại bản vá nào chưa khớp ở đâu để in cảnh báo.
    bg_hit = set()

    def bg_patch(s):
        for i, (old, new) in enumerate(BG_PATCHES):
            if old in s:
                bg_hit.add(i)
                s = s.replace(old, new)
        return s

    blocks_html = {k: rename_roles(recolor(bg_patch(block(v))))
                   for k, v in BLOCKS.items()}

    # Bỏ ô Quận/Huyện theo yêu cầu ngày 08/09.
    n_district = 0
    for k, v in blocks_html.items():
        blocks_html[k], n = drop_district(v)
        n_district += n

    # Thanh trên cao hơn trước -> sửa mọi phép trừ chiều cao cho khớp,
    # nếu không màn quản trị sẽ dư ra một thanh cuộn dọc.
    n_calc = 0
    for k, v in blocks_html.items():
        if "calc(100vh - 65px)" in v:
            n_calc += v.count("calc(100vh - 65px)")
            blocks_html[k] = v.replace("calc(100vh - 65px)",
                                       "calc(100vh - %dpx)" % BAR_H)

    # (UAT 02/10) Bản vá markup đợt 06/10 — chạy sau cùng, neo chặt.
    blocks_html = uat.patch_blocks(blocks_html, die)

    files_js = json.dumps(FILES, ensure_ascii=False)

    # --- sinh từng màn -----------------------------------------------------
    n_nested = []
    for sc in SCREENS:
        # Một số khối (modal QR, ngăn chi tiết…) nằm LỒNG sẵn bên trong khối màn
        # hình chứ không phải anh em cùng cấp. Nối thêm sẽ ra 2 modal chồng nhau.
        # Bỏ khối nào đã là con của khối khác trong cùng danh sách.
        chosen = []
        for b in sc["blocks"]:
            if any(blocks_html[b] in blocks_html[o]
                   for o in sc["blocks"] if o != b):
                n_nested.append("%s/%s" % (sc["code"], b))
                continue
            chosen.append(b)
        body = "\n\n".join(blocks_html[b] for b in chosen)
        base_state = dict(sc["states"][0][2])
        base_state["screen"] = sc["code"]
        hash_map = {h: st for h, label, st in sc["states"] if h}

        head_js = (
            "window.__FILES = %s;\n"
            "window.__STATE__ = %s;\n"
            "// dữ liệu mang sang từ màn trước (bấm nút điều hướng)\n"
            "try { var c = sessionStorage.getItem('__homi_carry');\n"
            "      if (c) { Object.assign(window.__STATE__, JSON.parse(c)); "
            "sessionStorage.removeItem('__homi_carry'); } } catch (e) {}\n"
            "// mở thẳng một trạng thái: %s#%s\n"
            "var H = %s, h = location.hash.slice(1);\n"
            "if (H[h]) Object.assign(window.__STATE__, H[h]);\n"
            % (files_js, json.dumps(base_state, ensure_ascii=False),
               FILES[sc["code"]], (sc["states"][1][0] if len(sc["states"]) > 1 else "..."),
               json.dumps(hash_map, ensure_ascii=False))
        )

        # Footer chỉ gắn ở màn công khai / thành viên; khung quản trị không có.
        foot = footer_html("../") if sc["code"] in ("A1", "A2", "A3", "C1") else ""

        page = (
            "<!DOCTYPE html>\n<html lang=\"vi\">\n<head>\n"
            "<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>%s · HOMI365</title>\n"
            "<link rel=\"icon\" href=\"../assets/Icon_viewweb_final.jpg\">\n"
            "<meta name=\"theme-color\" content=\"#1E3A66\">\n"
            "<link rel=\"stylesheet\" href=\"../css/fonts.css\">\n"
            "<link rel=\"stylesheet\" href=\"../css/base.css\">\n"
            "<link rel=\"stylesheet\" href=\"../css/tokens.css\">\n"
            "<link rel=\"stylesheet\" href=\"../css/responsive.css\">\n"
            "<script>\n%s</script>\n"
            "<script src=\"../js/dc-runtime.js\"></script>\n"
            "<script src=\"../js/otp.js\" defer></script>\n"
            "</head>\n<body>\n<x-dc>\n<helmet data-dc-atomics=\"\"></helmet>\n"
            "%s\n\n%s\n\n%s\n%s\n</div>\n</x-dc>\n%s\n</body>\n</html>\n"
            % (sc["title"], head_js, root_open,
               TOPBAR_ADMIN if sc["code"] in ADMIN_CODES
               else TOPBAR_A1 if sc["code"] == "A1"
               else TOPBAR_PUBLIC if sc["code"] == "A2"
               else TOPBAR_WEB,
               body, foot, script)
        )
        (V3 / "screens" / FILES[sc["code"]]).write_text(page, encoding="utf-8")

    # --- trang chính sách (lấy nội dung từ prototype-v2) --------------------
    # (08/10) HOMI365 chốt: trang chính sách CHỈ gồm 2 văn bản KH gửi (Chính
    # sách ưu đãi thành viên + Chính sách mua hàng & bảo mật dữ liệu). Bỏ 7 trang
    # mẫu chép từ prototype-v2 (gốc gocare.vn) — không còn đọc file v2 nữa.
    (V3 / "js" / "policies.js").write_text(
        "/**\n * Nội dung trang Chính sách (screens/policy.html) — chỉ gồm các văn bản\n"
        " * HOMI365 ban hành. Sinh từ tools/policy_docs.py, đừng sửa tay.\n */\n"
        "const POLICIES = [];"
        + uat.patch_policy(TNC_POLICY_JS, die), encoding="utf-8")
    n_pol = len(pdoc.DOCS)
    (V3 / "screens" / "policy.html").write_text(
        POLICY_PAGE.replace('<div id="foot"></div>', footer_html("../")),
        encoding="utf-8")

    # --- index -------------------------------------------------------------
    # (12/10) Bản prod bỏ trang danh sách màn hình: index.html chỉ chuyển thẳng
    # tới màn mua hàng A1; logo mỗi màn trỏ về trang chủ của khu vực đó.
    n_states = sum(len(sc["states"]) for sc in SCREENS)
    (V3 / "index.html").write_text(INDEX_REDIRECT, encoding="utf-8")
    for f in (V3 / "screens").glob("*.html"):
        if f.name.startswith("b") and f.name != "b1-admin-login.html":
            home = "b2-members.html"
        else:
            home = LOGO_HOME.get(f.name, "a1-buy.html")
        t = f.read_text(encoding="utf-8")
        t2 = (t.replace('title="Danh sách màn hình"', 'title="Trang chủ"')
               .replace("../index.html", home))
        if t2 != t:
            f.write_text(t2, encoding="utf-8")

    # --- báo cáo đổi màu ---------------------------------------------------
    all_out = "".join((V3 / "screens" / f).read_text(encoding="utf-8")
                      for f in FILES.values())
    left = sorted({c for c, _ in COLORS if c.startswith("#") and c in all_out})

    # Bản vá markup nào không khớp ở bất kỳ khối nào -> nhiều khả năng neo đã
    # bị một bản vá chạy trước sửa mất. In ra 60 ký tự đầu của neo để dò.
    bg_miss = ["#%d: %s" % (i, BG_PATCHES[i][0][:60].replace("\n", "⏎"))
               for i in range(len(BG_PATCHES)) if i not in bg_hit]

    # Soát mã chết: ô nhập SĐT trong modal tra cứu phải biến mất hẳn. Bản vá
    # markup im lặng khi không khớp neo, nên phải kiểm lại ở đầu ra — sót lại
    # là ai gõ đúng URL cũng tra được dữ liệu cá nhân của người khác.
    leaks = sorted(f for f in FILES.values()
                   if "setOrderLookupInput" in
                   (V3 / "screens" / f).read_text(encoding="utf-8"))

    # Soát trùng: mỗi khối chỉ được xuất hiện đúng 1 lần trong mỗi file.
    dup = []
    for f in FILES.values():
        t = (V3 / "screens" / f).read_text(encoding="utf-8")
        for name, h in blocks_html.items():
            tag = h[h.find("<sc-if"):h.find(">", h.find("<sc-if")) + 1]
            if tag and t.count(tag) > 1:
                dup.append("%s: %s xuất hiện %d lần" % (f, name, t.count(tag)))

    diff = ["# DIFF — prototype-v3 so với mockup của khách hàng", "",
            "Sinh tự động bởi `tools/build-v3.py`. Ngoài 13 mục dưới đây, "
            "**không có thay đổi nào khác**: layout, khoảng cách, bo góc, font "
            "giữ nguyên 100%.", "",
            "## 1. Đổi giá trị màu", "",
            "| Màu cũ (mockup KH) | Màu mới (HOMI365) |", "|---|---|"]
    for old, new in COLORS:
        diff.append("| `%s` | `%s` |" % (old, new))
    diff += ["", "## 2. Màu giữ nguyên — logo bên thứ ba", "",
             "| Màu | Lý do |", "|---|---|"]
    for c, why in KEEP.items():
        diff.append("| `%s` | %s |" % (c, why))
    diff += ["", "## 3. Thanh trên", "",
             "Chữ `Homi365 ●` đổi thành ảnh logo chính thức "
             "(`assets/logo homi-01.png`), bấm vào về trang mục lục. "
             "Favicon dùng `assets/Icon_viewweb_final.jpg`.", "",
             "Bỏ hai thành phần vốn là khung điều khiển của bản mockup, "
             "không thuộc sản phẩm:", "",
             "- Dòng chú thích `WhiteCoat Việt Nam · 7 màn hình MVP`.",
             "- Dãy nút chuyển màn `A1 · Thông tin nhận hàng … B4 · Kho hàng`. "
             "Việc chuyển màn giờ nằm ở `index.html`.", "",
             "Vì thanh chỉ còn một phần tử, logo nâng lên %dpx và đệm dọc nới từ "
             "12px lên %dpx — thanh cao %dpx thay vì 65px. Mọi phép "
             "`calc(100vh - 65px)` trong mockup đã được sửa theo (%d chỗ) để màn "
             "quản trị không dư thanh cuộn." % (LOGO_H, BAR_PAD_Y, BAR_H, n_calc), "",
             "Thêm nút **Đăng nhập Agent** ở góc phải thanh trên, chỉ trên 2 màn "
             "công khai A1 và A2 (trỏ sang `c1-login.html`). Không đặt ở C1 vì "
             "đang đứng sẵn ở đó, không đặt ở A3 vì đã đăng nhập, không đặt ở "
             "khung quản trị. Đây là thành phần mới so với mockup KH — cần nêu "
             "khi gửi.", "",
             "Logo canh thẳng hàng với nội dung bên dưới: màn người mua và thành "
             "viên dùng chung khung %dpx canh giữa; màn quản trị canh theo mép "
             "trái các mục sidebar. Đây là thay đổi layout duy nhất của bản này, "
             "và chỉ ở thanh trên." % CONTENT_MAX, "",
             "### 3b. Responsive", "",
             "Mockup KH chỉ có bản desktop. Bổ sung `css/responsive.css` — "
             "**mọi quy tắc bố cục đều nằm trong media query**, nên từ 901px trở "
             "lên giao diện KH đã duyệt không đổi một pixel nào (ngoài media "
             "query chỉ có đúng một dòng `img{max-width:100%}`, ở desktop không "
             "ảnh nào chạm ngưỡng đó).", "",
             "| Bề ngang | Thay đổi |",
             "|---|---|",
             "| ≤ 900px | A1 bỏ cột tóm tắt đơn 380px, xếp dọc · footer 1 cột · "
             "khung quản trị: cột điều hướng 220px thành dải nút ngang cuộn "
             "được · thẻ tổng hợp 4 cột → 2 |",
             "| ≤ 720px | Nút *Đăng nhập thành viên HOMI365* xuống hàng riêng, "
             "rộng hết khung; logo thanh trên còn 40px |",
             "| ≤ 640px | Cặp ô nhập trong form A1/A2 về 1 cột · thẻ tổng hợp về "
             "1 cột · ngăn chi tiết quản trị rộng hết màn |",
             "| ≤ 420px | Logo thanh trên còn 34px |", "",
             "Bảng quản trị **vẫn cuộn ngang** trong khung của nó thay vì ép về "
             "một cột: 9–10 cột số liệu mà nén lại thì dính vào nhau, đọc còn "
             "khó hơn vuốt ngang.", "",
             "Lưu ý kỹ thuật cho dev: markup KH không có class nào, style viết "
             "inline hết, nên các quy tắc phải nhắm bằng `[style*=\"…\"]` kèm "
             "`!important`. Runtime của mockup ghi lại style qua "
             "`el.style.cssText` nên chuỗi bị trình duyệt chuẩn hoá "
             "(`1fr 1fr;gap:` → `1fr 1fr; gap: `); selector viết cả hai dạng. "
             "Khi dựng thật bằng React/Vue thì bỏ hết mẹo này, dùng class bình "
             "thường.", "",
             "Đã kiểm tra ở 360 · 390 · 768 · 1024px trên cả 12 màn: không màn "
             "nào bị tràn ngang ngoài các khung cố ý cho cuộn.", "",
             "## 4. Bỏ trường Quận/Huyện", "",
             "Hàng địa chỉ trong form mua hàng (A1) và form đăng ký (A2) đi từ "
             "**3 ô** `Tỉnh/Thành phố · Quận/Huyện · Phường/Xã` xuống **2 ô** "
             "`Tỉnh/Thành phố · Phường/Xã`. Đã bỏ %d ô, lưới đổi từ 3 cột sang "
             "2 cột." % n_district, "",
             "Đây là **thay đổi trường nhập liệu duy nhất** so với mockup KH — "
             "cần nêu rõ khi gửi, vì các trường còn lại đều giữ nguyên như đã "
             "duyệt. Lý do: từ 01/07/2025 Việt Nam bỏ cấp huyện, địa chỉ hành "
             "chính chỉ còn tỉnh/thành → phường/xã.", "",
             "Kéo theo: dữ liệu địa chỉ lưu xuống chỉ còn 2 cấp — cần thống nhất "
             "với dev trước khi thiết kế bảng, và chốt xem đơn hàng cũ (nếu có "
             "dữ liệu chuyển đổi) xử lý cấp huyện thế nào.", "",
             "## 5. Nền trang", "",
             "Nền trang đổi sang `--warm-50` = `%s` (lấy từ "
             "`prototype-v2/css/tokens.css`), thẻ và ô nhập giữ trắng `#FFFFFF` "
             "— tạo nhịp xen kẽ ấm / trắng thay vì trắng trên trắng." % WARM, "",
             "| Màn | Trước | Sau |", "|---|---|---|",
             "| A1 · C1 | `rgba(170,170,170,.05)` | `%s` |" % WARM,
             "| A3 | `#FFFFFF` | `%s` |" % WARM,
             "| A2 · B2 · B3 · B4 | `#FFFFFF` | `%s` |" % WARM,
             "| Thanh trên · thẻ · ô nhập | `#FFFFFF` | giữ nguyên |",
             "| B1 đăng nhập quản trị | `--c3` navy | giữ nguyên |", "",
             "Kéo theo: 30 thẻ trong mockup KH **chỉ khai báo viền, không khai "
             "báo nền** — trên nền trắng cũ thì không lộ, trên nền ấm sẽ bị chìm. "
             "Đã cho về trắng (A3 5 thẻ · B2/B3/B4 mỗi màn 8 · A2 1).", "",
             "Cột biểu đồ hoa hồng đổi sang teal `%s` để tách khỏi navy của "
             "nút và link — navy là màu hành động, teal là màu dữ liệu." % CHART, "",

             "## 6. Thêm link bán hàng vào A3", "",
             "Dashboard thành viên trong mockup KH **không có link bán hàng nào**. "
             "Agent rời màn \"Kích hoạt thành công\" (A2 bước 5) là mất đường lấy "
             "link, không có chỗ xem lại. Đã thêm thẻ **Link bán hàng của bạn** "
             "ngay dưới phần chào, gồm 1 link + nút copy, dùng lại đúng link và "
             "hàm `copyLink` sẵn có của A2 bước 5.", "",
             "**Đã chốt 08/09: 2 link**, đúng theo requirement 8.1.C-4 — agent "
             "nhận cả hai ngay lúc kích hoạt (A2 bước 5) và xem lại được ở "
             "dashboard (A3), mỗi link một nút copy riêng:", "",
             "| Link | Giá trị | Dùng để |", "|---|---|---|",
             "| Giới thiệu · ref_code | `homi365.vn/san-pham/CN02?aff_id=923983` | "
             "gán tuyến trên / tuyển thành viên |",
             "| Mua hàng cá nhân · alias | `homi365.com.vn/NVA1111` | "
             "chia sẻ để khách mua trực tiếp |", "",
             "`ref_code = 923983` là mã chính thức của agent. Alias sinh đúng cú "
             "pháp **8.1.C-4**: `Homi365.com.vn/[EEEE][PPPP]` — EEEE là chữ cái "
             "đầu (viết hoa, bỏ dấu) của mỗi từ trong họ tên, PPPP là 4 số cuối "
             "SĐT. *Nguyễn Văn A* · `0901111111` → `NVA1111`.", "",
             "Còn treo — **hai link của admin ở màn B2 chưa khớp mô hình này.** "
             "B2 hiện hiện *link form* `portal.homi365.com.vn/TTB4123` và *link "
             "đăng nhập* `homi365.com.vn/dang-nhap/TTB4123`, cả hai dựng từ alias "
             "chứ không có link mua hàng lẫn ref_code. Cần chốt admin nhìn thấy "
             "những link nào của agent, và 4 dạng link này rốt cuộc là mấy thứ "
             "khác nhau. Prototype giữ nguyên phần B2 như mockup KH.", "",

             "## 7. Tách hoa hồng theo trạng thái (A3)", "",
             "Thẻ số dư trong mockup KH chỉ có **2 con số** — khả dụng và \"đang "
             "chờ duyệt (đã khóa)\"; \"đã ghi nhận\" nằm lẫn trong một dòng chữ "
             "nhỏ, \"đã rút\" nằm tận ô chỉ số phía trên. Đã tách thành **4 mục**:",
             "",
             "| Mục | Giá trị mẫu |", "|---|---|",
             "| Đã ghi nhận | 6.000.000đ |",
             "| Đang chờ duyệt · tạm giữ | 800.000đ |",
             "| Đã rút | 1.200.000đ |",
             "| **Số dư khả dụng** | **4.000.000đ** |", "",
             "Số liệu mẫu khớp: `6.000.000 = 4.000.000 + 800.000 + 1.200.000`.", "",
             "Bổ sung dòng giải thích cơ chế hold: yêu cầu rút ở trạng thái **chờ "
             "duyệt** hoặc **đã duyệt** bị tạm giữ và trừ khỏi số dư khả dụng, tới "
             "khi chi trả xong hoặc bị từ chối; từ chối thì hoàn lại khả dụng.", "",
             "\"Đã rút\" hiển thị ở **2 nơi** — ô chỉ số phía trên (trường của "
             "mockup gốc) và thẻ hoa hồng này. **Đã chốt giữ cả hai** (BA quyết "
             "08/09): ô chỉ số cho cái nhìn nhanh, thẻ hoa hồng cho quan hệ giữa "
             "4 con số. Không phải lỗi trùng lặp.", "",

             "## 8. Bổ sung màn Quản lý sản phẩm (B5)", "",
             "Mockup KH không có màn này, dù requirement **7.7.1 Logic quản lý "
             "sản phẩm** là P0. Đã thêm màn `b5-products.html` trong khung quản "
             "trị, kèm mục **Quản lý sản phẩm** ở sidebar.", "",
             "Nội dung: bảng sản phẩm với 3 cột theo đúng yêu cầu — **Tên · Hình "
             "ảnh · Mô tả** — cùng nút *Thêm sản phẩm* và nút *Sửa* trên từng "
             "dòng, cả hai mở cùng một hộp thoại 3 trường.", "",
             "**Đã chốt 08–09/09** — phạm vi màn này đúng bằng 3 trường trên, "
             "không hơn: không quản lý giá, không quản lý gói, không có công tắc "
             "bật/tắt bán, mỗi sản phẩm **chỉ 1 ảnh**.", "",
             "Danh sách chỉ có **1 sản phẩm CN02**, đúng theo **6.1.C-3** "
             "(*\"cho 1 sản phẩm pilot (CN02)\"*). Hai lựa chọn *Gói 1 năm "
             "10.000.000đ* và *Gói nửa năm 6.000.000đ* ở màn mua hàng là **gói "
             "license của cùng sản phẩm đó**, không phải 2 sản phẩm — khớp với "
             "kho B4, nơi cả 1.200 thiết bị đều mang một dòng SKU `CN02-xxxx`.",
             "",

             "## 9. Bổ sung Thêm hàng vào kho (B4)", "",
             "Màn Quản lý kho hàng của mockup KH **chỉ xem, không nhập được hàng** "
             "— 1.200 mã trong bản demo là dữ liệu dựng sẵn. Đã thêm nút **+ Thêm "
             "hàng vào kho** cạnh nút xuất Excel, mở hộp thoại 2 trường theo yêu "
             "cầu: **Mã sản phẩm** và **Mã kích hoạt**. Hàng thêm vào mặc định ở "
             "trạng thái *Sẵn hàng*.", "",
             "**Đã chốt 08/09** — thêm nút **Import hàng loạt** bên cạnh, mở hộp "
             "thoại cho chọn file Excel/CSV hoặc dán danh sách, mỗi dòng "
             "`mã sản phẩm, mã kích hoạt`.", "",
             "**Chặn trùng ở cả hai đường nhập:**", "",
             "- Nhập tay: trùng mã kích hoạt hoặc mã sản phẩm thì báo lỗi ngay "
             "trong hộp thoại, không cho lưu.",
             "- Import: xử lý **từng phần** — dòng nào hợp lệ thì nhận, dòng nào "
             "trùng hoặc thiếu dữ liệu thì bỏ qua. Kết thúc hiện bảng tổng kết "
             "`tổng dòng / đã nhập / bỏ qua` kèm danh sách dòng bị bỏ và lý do.",
             "- Chặn trùng tính cả với kho hiện có **lẫn trùng nhau trong chính "
             "danh sách đang dán** — dán 2 dòng cùng mã thì chỉ nhận dòng đầu.", "",

             "## 10. Bổ sung màn Quản lý đơn hàng (B6)", "",
             "Mockup KH **không có màn đơn hàng nào**, dù luồng mua của chính "
             "mockup là chuyển khoản + khách tự tải ảnh bill lên. Nghĩa là tiền "
             "về tài khoản nhưng không ai xác nhận được, đơn treo vĩnh viễn và "
             "khách không bao giờ nhận mã kích hoạt. Đây là mắt xích đứt, không "
             "phải tính năng phụ.", "",
             "Màn `b6-orders.html` gồm: 4 ô thống kê (chờ đối soát · chờ Head "
             "Admin · đã thanh toán · doanh thu đã đối soát), bộ lọc theo trạng "
             "thái, ô tìm theo mã đơn / tên / SĐT, bảng đơn, và ngăn chi tiết bên "
             "phải với thông tin khách, thông tin đơn, ảnh chuyển khoản, lịch sử "
             "xử lý và nút hành động.", "",
             "⚠ Bản 08/09 làm duyệt 2 cấp cho đơn hàng. **Đã bỏ ngày 09/09** — "
             "xem mục 13 để biết mô hình duyệt cuối cùng.", "",
             "**Đã chốt 08/09:**", "",
             "- **Tách vai theo bước, không tách theo người.** Specialist làm "
             "bước 1; bước 2 thuộc về Head Admin, và Head Admin làm luôn việc "
             "kích hoạt tài khoản. Khác luồng rút tiền ở chỗ rút tiền cấm cùng "
             "một người làm cả hai bước, còn ở đây phân quyền theo vai là đủ.",
             "- **Mã kích hoạt do Head Admin chọn tay** từ danh sách thả xuống, "
             "chỉ liệt kê mã đang ở trạng thái *Sẵn hàng* trong kho (B4). Không "
             "chọn thì không xác nhận được. Xác nhận xong mã đó chuyển sang *Đã "
             "gán đơn hàng* và ghi vào lịch sử của cả đơn lẫn thiết bị.",
             "- **Đơn bị từ chối là chấm dứt.** Phase 1 không mở lại đơn cũ; "
             "khách muốn mua thì đặt đơn mới qua link giới thiệu. Ngăn chi tiết "
             "hiển thị rõ dòng này để admin khỏi đi tìm nút mở lại.", "",
             "- **Hoàn tiền nằm ngoài hệ thống.** Đơn bị từ chối nhưng tiền đã "
             "về tài khoản thì bộ phận kế toán xử lý thủ công bên ngoài; hệ "
             "thống không có màn hoàn tiền, không lưu trạng thái hoàn tiền, "
             "không đối soát khoản hoàn. Dev không cần làm gì cho phần này.", "",

             "## 11. Bổ sung theo rà soát requirement 09/09", "",
             "Nguồn: `docs/GAP-Requirement-vs-prototype-v3.md`. Sáu mục nhóm B "
             "đã làm xong:", "",
             "| Mã YC | Bổ sung |", "|---|---|",
             "| **7.9.1** | Màn **B7 · Tài khoản admin** — danh sách 5 tài khoản "
             "mẫu, cột vai trò (Head Admin / Admin Specialist), khoá–mở khoá, "
             "thêm–sửa tài khoản, kèm bảng giải thích quyền của từng vai. |",
             "| **7.1.3** | Đăng nhập bằng SĐT **đã mua hàng nhưng chưa là "
             "agent** → tự chuyển sang màn đăng ký và autofill từ đơn cũ "
             "(khớp luôn 7.2.8). Thêm dòng gợi ý ngay dưới nút Đăng nhập. |",
             "| **7.5.2** | Thêm khối **Lịch sử thăng/giáng hạng** vào ngăn chi "
             "tiết thành viên. |",
             "| **7.5.2** | Cây tuyến mở rộng lên **3 cấp** F0 → F1 → F2. |",
             "| **7.3.2** | Dashboard thêm bộ chọn **Hôm nay / Tuần này / Tháng "
             "này / Tất cả**, số Tổng đơn hàng đổi theo. |",
             "| **7.9.4** | Nhãn trạng thái duyệt hiện rõ số lượt: **Chờ duyệt "
             "(0/2)** · **Chờ Head Admin (1/2)** · **Đã duyệt (2/2)**. |", "",
             "Chưa làm, chờ KH quyết — xem mục A3 của file rà soát: theo **7.9.2** "
             "agent đăng ký xong phải ở trạng thái *Chờ duyệt* chứ không vào thẳng "
             "dashboard như mockup KH. Sửa chỗ này kéo theo cả màn A2, luồng duyệt "
             "và cách tính hoa hồng lúc chờ, nên chưa đụng vào.", "",

             "## 12. Sửa theo rà soát bản deploy 09/09", "",
             "Nguồn: `docs/AUDIT-deploy-vs-requirement.md`.", "",
             "| Mã YC | Đã sửa |", "|---|---|",
             "| **7.2.2** | **Autofill khi đăng ký ngay sau khi mua.** Nút *Đăng "
             "ký thành viên* ở modal thanh toán thành công giờ mang toàn bộ thông "
             "tin người mua sang màn A2 (họ tên, SĐT, email, CCCD, địa chỉ, ngày "
             "sinh, số tài khoản, mã đơn, hạng tuyến trên). Trước đó form mở ra "
             "trống trơn — lỗi phát sinh do tách mỗi màn một file. |",
             "| **7.9.1** | **Chặn Admin Specialist khỏi màn Tài khoản admin.** "
             "Mục *Tài khoản admin* biến mất khỏi sidebar khi đang ở vai "
             "Specialist; vào thẳng URL thì ra màn **403**. |",
             "| **7.3.3** | Thêm dòng **còn thiếu bao nhiêu đơn để lên hạng kế "
             "tiếp** ngay dưới ô *Hạng hiện tại*. |",
             "| **7.3.2** | Thêm mốc **Khoảng ngày…** mở ra 2 ô chọn ngày và nút "
             "Áp dụng, cạnh 4 mốc có sẵn. |",
             "| **7.5.2** | Cây tuyến **3 cấp** F0 → F1 → F2 giờ mới thật sự "
             "chạy — bản vá dữ liệu trước đó đặt nhầm vào nhóm xử lý markup nên "
             "chưa từng có hiệu lực. Tiêu đề đổi thành *Sơ đồ tuyến dưới (3 cấp)*. |",
             "| — | Thay hết **Medigo** còn sót thành **HOMI365** (điều khoản "
             "T&C, câu chúc mừng ở A2, lời chào ở A3, tiêu đề đăng nhập quản trị). |",
             "| — | Sửa nhãn **Bước 1/3 → Bước 1/5** ở màn đăng ký cho khớp số "
             "bước thật. |", "",
             "### Ba điểm đã chốt 09/09 — requirement phải sửa theo", "",
             "Cả ba quyết định đều **giữ nguyên hành vi prototype**, nhưng **trái "
             "với Acceptance Criteria trong sheet**. Không sửa sheet thì dev đọc "
             "spec sẽ code ra thứ khác với bản KH đã duyệt.", "",
             "**1. Duyệt 2 lớp tách theo VAI TRÒ** (Specialist bước 1 · Head Admin "
             "bước 2). Cần sửa 3 dòng:", "",
             "- `7.9.2 AC` đang ghi *\"lượt 1: bất kỳ Admin Specialist hoặc Head "
             "Admin nào\"* và *\"lượt 2 phải do người KHÁC\"* → viết lại thành "
             "tách theo vai trò.",
             "- `7.9.3 AC` đang ghi *\"2 người khác nhau, hoặc Head Admin tự "
             "chốt\"* → bỏ vế Head Admin tự chốt.",
             "- `7.9.4 AC` đang ghi *\"nút Xác nhận của chính người đó bị vô hiệu "
             "hoá\"* → đổi thành khoá theo vai trò.", "",
             "Rủi ro vận hành cần KH biết trước: **Specialist nghỉ là mọi thứ "
             "nghẽn ở bước 1**, kể cả khi Head Admin đang trực. Requirement bản "
             "cũ thiết kế để tránh đúng chuyện này. Nếu KH muốn chặn rủi ro mà "
             "vẫn giữ tách vai trò, cách gọn nhất là thêm một câu: *Head Admin "
             "được phép làm thay bước 1 khi cần*.", "",
             "**2. Tuyến trên hạng Đồng → báo lỗi** (không giấu lời mời). "
             "`7.2.1 AC` đang ghi ngược lại (*\"không hiển thị thông báo cho đăng "
             "ký thành viên, mà chỉ báo đơn hàng thành công\"*) → phải viết lại "
             "cho khớp dòng *Logic điều kiện đăng ký thành viên mới*.", "",
             "Đã chỉnh prototype: báo lỗi **ngay khi bấm** nút Đăng ký thành "
             "viên, thay vì để khách điền hết 5 bước rồi mới chặn ở bước cuối.",
             "",
             "**3. Agent sau đăng ký vào thẳng dashboard**, không qua *Chờ duyệt "
             "(0/2)*. `7.9.2` đang bắt hồ sơ đăng ký phải đủ 2 lượt xác nhận mới "
             "kích hoạt → phải bỏ phần đăng ký ra khỏi phạm vi duyệt 2 lớp, chỉ "
             "giữ cho rút tiền và đơn hàng.", "",
             "**Cơ chế tạm giữ hoa hồng — chốt 09/09.** Đăng ký xong là **active ngay**, "
             "nhưng kích hoạt của admin mới mở khoá phần tiền:", "",
             "| | Sau khi đăng ký | Sau khi admin kích hoạt |", "|---|---|---|",
             "| Link giới thiệu & link mua hàng | có, dùng được ngay | có |",
             "| Bán hàng, ghi nhận đơn & tuyến dưới | bình thường | bình thường |",
             "| Hoa hồng phát sinh | **tạm giữ** | được giải phóng |",
             "| Điểm tích luỹ | **không cộng** (= 0) | cộng đủ, kể cả phần trước đó |",
             "| Rút tiền | **không được** | được |", "",
             "Đã dựng vào prototype:", "",
             "- A2 bước 5: đổi *\"Kích hoạt thành công · đã chính thức là seller\"* "
             "→ **\"Đăng ký thành công\"** kèm câu giải thích hoa hồng bị giữ.",
             "- A3 agent mới: thay banner chào mừng bằng khối **CHỜ KÍCH HOẠT** — "
             "nêu rõ bán được ngay nhưng hoa hồng tạm giữ, chưa tính điểm, chưa "
             "rút được; hiện số **hoa hồng đang tạm giữ** và **số dư khả dụng 0đ**; "
             "nút rút tiền để trạng thái khoá.",
             "- Điểm tích luỹ của agent chưa kích hoạt đổi từ 80 về **0**.", "",
             "Nhờ vậy màn duyệt hồ sơ ở B2 vẫn có lý do tồn tại: nó là chỗ mở "
             "khoá tiền, không phải chỗ cho phép bán hàng.", "",
             "**Chốt 09/09: cộng dồn toàn bộ về quá khứ.** Khi admin kích hoạt, "
             "hoa hồng đã tạm giữ và điểm tích luỹ được tính **từ đơn đầu tiên**, "
             "không phải từ thời điểm kích hoạt. Hộp xác nhận duyệt ở B2 đã ghi "
             "rõ điều này để admin biết mình đang mở khoá cái gì.", "",
             "Kéo theo cho dev: bản ghi hoa hồng phải tồn tại **ngay khi đơn "
             "thanh toán**, mang một cờ *đang giữ*, chứ không phải sinh ra lúc "
             "kích hoạt — nếu sinh lúc kích hoạt thì không còn dữ liệu quá khứ để "
             "cộng dồn. Điểm tích luỹ cũng vậy.", "",

             "## 13. Mô hình duyệt — bản chốt cuối 09/09", "",
             "Mô hình duyệt đã đổi ba lần trong hai ngày. Đây là bản cuối, **ghi "
             "đè mọi mô tả duyệt ở các mục trên**:", "",
             "| Luồng | Số lượt duyệt | Ai làm | Ghi chú |", "|---|---|---|---|",
             "| **Đơn hàng** (B6) | **1** | Admin bất kỳ (Specialist hoặc Head) | "
             "Xác nhận tiền về + chọn mã kích hoạt từ kho → đơn `Đã thanh toán`, "
             "mã sang `Đã gán đơn hàng`, hệ thống gửi email kèm mã cho khách ngay |",
             "| **Thành viên** (B2) | **1** | Chỉ Manager / Head Admin | "
             "Chỉ duyệt được khi đơn của thành viên đó đã xác nhận thanh toán. "
             "Duyệt xong mở khoá điểm và ưu đãi đang tạm giữ |",
             "| **Rút tiền** (B3) | **2** | Specialist bước 1, Head Admin bước 2 | "
             "Giữ nguyên duyệt 2 lượt — chốt 09/09, khác hai luồng trên |", "",
             "Vòng đời hồ sơ thành viên: `Chờ xác nhận thanh toán` → "
             "`Chờ Manager duyệt` → `Đang hoạt động`. Bước một không nằm ở màn "
             "Thành viên mà ở màn Đơn hàng — đây là điểm dễ hiểu nhầm nhất, cần "
             "nói rõ khi bàn giao cho dev.", "",
             "Kỹ thuật: hai trạng thái `pending` và `specialist_approved` dùng "
             "chung giữa thành viên và rút tiền, nhưng nhãn hiển thị khác nhau "
             "(thành viên có bảng nhãn riêng). Khi dev thiết kế bảng nên tách "
             "hẳn hai bộ trạng thái, đừng dùng chung enum.", "",

             "## 14. Gỡ ô tra cứu đơn theo số điện thoại (11/09)", "",
             "Mockup KH có một hộp thoại **Nhập số điện thoại → Tra cứu đơn "
             "hàng** trên A1. Từ khi luồng đăng nhập đổi (C1 tự đối chiếu SĐT "
             "rồi mở hộp thoại kèm sẵn kết quả), **không còn nút nào trên giao "
             "diện mở nhánh gõ số để tra** — nó chỉ còn vào được bằng cách gõ "
             "tay `a1-buy.html#tra-cuu-don`.", "",
             "Đã gỡ hẳn: bỏ ô nhập, bỏ nút *Tra cứu đơn hàng*, bỏ khối modal "
             "khỏi A1 cùng mục `#tra-cuu-don` trong `index.html`. Phần thẻ "
             "**Đơn hàng tìm thấy** giữ nguyên và vẫn chạy trên C1.", "",
             "Lý do không chỉ là dọn mã chết: nhánh đó nhận **một số điện "
             "thoại bất kỳ, không xác thực gì**, rồi trả về họ tên, email, số "
             "CCCD và địa chỉ của chủ đơn. Deploy lên là ai biết URL cũng tra "
             "được dữ liệu cá nhân của người khác. Nếu sau này KH muốn có tính "
             "năng tra cứu đơn thật thì phải kèm OTP về đúng số đó, và chỉ trả "
             "mã đơn + trạng thái, không trả thông tin định danh.", "",
             "Kèm theo, sửa một lỗi lộ ra khi rà: modal **tuyến trên bị chặn** "
             "trước đây chỉ được nhúng vào A1, trong khi nhánh gọi nó "
             "(`lookupContinue`, khi người giới thiệu hạng Copper) lại nằm ở "
             "C1 — bấm xong không hiện gì. Đã chuyển khối này sang C1.", "",
             "Build in cảnh báo `ô tra cứu SĐT còn sót` nếu bản vá gỡ markup "
             "không khớp neo, vì bản vá markup im lặng khi trượt.", "",

             "## 15. Sửa hàng tiêu đề bảng Kho hàng (15/09)", "",
             "Bảng kho ở B4 có **10 cột dữ liệu nhưng hàng tiêu đề chỉ có 7 ô** "
             "— ba nhãn *Ngày kích hoạt · Ngày hết hiệu lực · Mã vận đơn* bị "
             "thiếu, kéo theo nhãn *Trạng thái* nằm lệch ba cột so với ô trạng "
             "thái thật.", "",
             "Nguyên nhân: bản vá thêm cột neo vào chuỗi `<div>Seller</div>`, "
             "nhưng bản vá đổi *Seller → Thành viên* đứng trước nó trong danh "
             "sách. Tới lượt bản vá thêm cột thì neo đã biến mất, `str.replace` "
             "không tìm thấy gì và **bỏ qua không báo lỗi**. Hàng dữ liệu vẫn "
             "được thêm cột (neo khác, không bị đụng) nên bảng lệch.", "",
             "Đã sửa neo và bổ sung bộ soát: build giờ đếm bản vá markup nào "
             "không khớp ở bất kỳ khối nào rồi in cảnh báo kèm 60 ký tự đầu của "
             "neo. Dòng `bản vá markup: n/n khớp hết` là bình thường; thấy ⚠ thì "
             "có neo bị hỏng, phải xem lại trước khi gửi.", "",
             "Dev lưu ý: đây là hạn chế của cách dựng bản mẫu (vá chuỗi trên "
             "markup của KH), không phải vấn đề nghiệp vụ. Bản dựng thật không "
             "có chuyện này.", "",

             "## 16. Gửi yêu cầu thanh toán — chống đơn trùng & lỗi mạng (16/09)",
             "",
             "Mockup KH bấm **Thanh toán** là mở ngay mã QR, không có trạng "
             "thái chờ. Thực tế gọi cổng thanh toán mất vài giây và có thể "
             "hỏng giữa chừng, nên bổ sung ba trạng thái cho nút:", "",
             "| Trạng thái | Nút | Hiển thị thêm |",
             "|---|---|---|",
             "| `idle` | *Thanh toán*, bấm được | — |",
             "| `sending` | *Đang gửi yêu cầu…*, **khoá** | — |",
             "| `timeout` | *Gửi lại yêu cầu thanh toán*, bấm được | Dải đỏ "
             "*Lỗi đường truyền, vui lòng gửi lại yêu cầu* |", "",
             "Đây là **thông báo duy nhất** của luồng này — chốt 16/09. Trường "
             "hợp bấm lại khi đơn đã tạo **không hiện thông báo**: hệ thống "
             "lặng lẽ mở lại mã thanh toán của đúng đơn cũ, người mua không cần "
             "biết chuyện gì vừa xảy ra. Chống trùng vẫn phải làm đủ ở tầng "
             "dưới, chỉ là không nói ra trên giao diện.", "",
             "**Ba quy tắc dev phải làm đúng, không chỉ là giao diện:**", "",
             "1. **Ngưỡng chờ 5 giây.** Quá 5s chưa nhận được phản hồi mở mã "
             "thanh toán thì chuyển nút sang `timeout`. Bản mẫu để 1,2s cho dễ "
             "xem, con số thật là 5s.",
             "2. **Giữ nguyên form.** Gửi lại không được xoá hay nạp lại bất kỳ "
             "trường nào người mua đã nhập.",
             "3. **Khoá chống trùng (idempotency key).** Mã đơn sinh **một "
             "lần** rồi dùng lại cho mọi lần gửi lại; server thấy khoá cũ thì "
             "trả về đơn cũ chứ không tạo đơn mới. Không có khoá này thì người "
             "mua mạng yếu bấm ba lần là ba đơn, ba mã kích hoạt bị giữ.", "",
             "Trong lúc `sending` nút bị khoá hẳn — đó là lớp chặn bấm dồn thứ "
             "nhất; khoá chống trùng là lớp thứ hai, phòng khi người dùng tải "
             "lại trang rồi bấm tiếp.", "",
             "Xem thử: `a1-buy.html#loi-duong-truyen`. Bấm *Gửi lại yêu cầu "
             "thanh toán* sẽ chạy hết luồng và mở mã QR bình thường.", "",
             "Chưa làm, cần KH chốt: sau bao nhiêu lần gửi lại liên tiếp thì "
             "dừng và mời liên hệ hotline, và đơn đã tạo nhưng chưa thanh toán "
             "thì giữ hiệu lực bao lâu trước khi tự huỷ.", "",

             "## 17. Cập nhật cấp thành viên (17/09)", "",
             "Trước đây cấp chỉ do hệ thống gán theo doanh số, không ai sửa "
             "được. Bổ sung luồng cho phép sửa tay.", "",
             "**Chốt 17/09: việc trình – xét – duyệt làm NGOÀI hệ thống** "
             "(email hoặc biểu mẫu nội bộ). Hệ thống không ra quyết định, chỉ "
             "ghi nhận quyết định đã có và áp dụng nó. Bản dựng trước đó có "
             "luồng *Admin đề nghị → Head duyệt* ngay trong hệ thống — đã gỡ "
             "bỏ.", "",
             "| Bước | Ở đâu | Ai làm | Ra cái gì |", "|---|---|---|---|",
             "| 1. Trình tăng cấp | Ngoài | Người phụ trách | Phiếu trình: "
             "thành viên, cấp hiện tại, cấp đề xuất, lý do, số liệu |",
             "| 2. Review nội dung | Ngoài | Người duyệt | Ý kiến, yêu cầu bổ "
             "sung |",
             "| 3. Quyết định | Ngoài | Người duyệt | Duyệt · Sửa rồi duyệt · "
             "Từ chối. Kết quả là phiếu/email chốt có **mã phiếu, người duyệt, "
             "ngày duyệt, cấp cuối cùng** |",
             "| 4. Cập nhật | **Trong** | Admin | Mở hồ sơ → *Cập nhật cấp* → "
             "chọn cấp đã duyệt + nhập minh chứng → Lưu |",
             "| 5. Áp dụng | **Trong** | Hệ thống | Cấp mới hiệu lực ngay, ghi "
             "lịch sử. Không duyệt lại |", "",
             "**Bị từ chối thì không thao tác gì trong hệ thống** — chốt "
             "17/09: ngoài core xem như chưa từng đề xuất, nên hệ thống không "
             "ghi nhận gì cả. Hệ quả cần biết: nhìn vào hồ sơ sẽ không thấy "
             "dấu vết đã từng trình rồi bị bác; muốn tra thì phải tìm ở nguồn "
             "ngoài.", "",
             "**Quyền cập nhật: Admin** — chốt 17/09. Admin tự cập nhật và tự "
             "đính kèm minh chứng, không cần Head thao tác. Head vẫn làm được "
             "vì là vai cao hơn.", "",
             "**Giao diện.** Ngăn chi tiết thành viên (B2) có nút **Cập nhật "
             "cấp**, kèm dòng nhắc *việc trình và duyệt làm ngoài hệ thống*. "
             "Hộp thoại gồm: danh sách 6 cấp, và **ba trường minh chứng bắt "
             "buộc** — số phiếu / mã email, ngày duyệt, người duyệt — cộng ô "
             "**tải file minh chứng** (ảnh, PDF, hoặc file email `.eml`/`.msg`). "
             "Thiếu một trong ba trường bắt buộc thì nút *Lưu & áp dụng* vẫn "
             "xám; file không bắt buộc.", "",
             "Không có ô nhập lý do — chốt 17/09. Lý do nằm trong phiếu duyệt "
             "ngoài, gõ lại vào đây chỉ sinh ra một bản chép tay có thể sai "
             "khác với bản gốc.", "",
             "Ba trường kia chỉ là số hiệu do người nhập gõ vào — **file mới "
             "là bằng chứng thật**. Khuyến nghị KH quy định bắt buộc đính kèm "
             "file trong quy chế nội bộ, kể cả khi hệ thống không chặn. Bản "
             "mẫu chỉ giữ tên file; bản thật phải tải lên kho lưu trữ, gắn với "
             "bản ghi và không cho xoá.", "",
             "**Hai ràng buộc khi chọn cấp.** Cấp vi phạm bị làm mờ kèm dòng "
             "giải thích:", "",
             "- **Trần:** không cao hơn cấp của người giới thiệu trực tiếp.",
             "- **Sàn:** không thấp hơn cấp của tuyến dưới trực tiếp. Ràng "
             "buộc này KH chưa nêu nhưng bắt buộc phải có — vì chỉ sửa cấp của "
             "riêng một người, hạ người trên xuống cũng làm tuyến dưới vượt "
             "tuyến trên, đúng cái điều mà trần đang cấm.", "",
             "Ràng buộc vẫn áp **kể cả khi phiếu ngoài đã duyệt**. Gặp trường "
             "hợp bị chặn thì Admin không tự phá rào, phải trình lại bên "
             "ngoài. Cần nói rõ điều này với bộ phận duyệt, nếu không họ sẽ "
             "duyệt ra thứ hệ thống không nhận.", "",
             "Sửa cấp **chỉ đổi đúng thành viên đó**, tuyến dưới giữ nguyên.",
             "",
             "**Lưu vết:** mỗi lượt ghi cấp cũ → cấp mới, mã phiếu, ngày "
             "duyệt, người duyệt, tên file minh chứng, thời điểm cập nhật. "
             "Hiện ở mục *Lịch sử điều chỉnh cấp* trong hồ sơ.", "",
             "Xem thử: `b2-members.html#cap-nhat-cap` và `#da-cap-nhat-cap`.",
             "",
             "**Rủi ro khi đưa duyệt ra ngoài — cần bù lại bằng quy trình:**",
             "",
             "1. **Mất dấu vết ai duyệt.** Quyết định nằm trong hộp thư cá "
             "nhân. Ba trường minh chứng là sợi dây duy nhất nối số liệu trong "
             "hệ thống với phiếu ngoài — vì vậy để bắt buộc.",
             "2. **Không còn cơ chế hai người.** Trước phải Admin trình + Head "
             "duyệt mới đổi được cấp; giờ một Admin gõ là xong. Đề xuất bù: "
             "log chỉ thêm, không sửa/xoá, và định kỳ xuất báo cáo các lượt "
             "đổi cấp để đối chiếu với phiếu ngoài.", "",
             "**Còn chờ KH chốt:**", "",
             "1. Hướng của ràng buộc — em hiểu là *tuyến dưới không được vượt "
             "tuyến trên*; nếu KH muốn ngược lại thì phải đảo cả trần lẫn sàn.",
             "2. Có hồi tố không — đơn đã chốt theo cấp cũ có tính lại ưu đãi, "
             "hay chỉ áp cấp mới từ lúc cập nhật.", "",
             "Hai câu còn lại đã chốt 17/09, xem ở trên: không ghi nhận lượt "
             "bị từ chối; Admin là người cập nhật.", "",

             "## 18. Bổ sung màn Nhật ký hệ thống (B8) — 17/09", "",
             "Màn mới, **phạm vi toàn hệ thống**, không riêng phân hệ nào. Hai "
             "tab:", "",
             "**Tab 1 — Thay đổi dữ liệu.** 9 cột: thời điểm · người thực hiện "
             "(kèm vai) · phân hệ · đối tượng · hành động · giá trị trước · giá "
             "trị sau · minh chứng · địa chỉ IP. Lọc theo phân hệ, hành động, "
             "khoảng ngày, và tìm theo người thực hiện / đối tượng / mã phiếu.",
             "",
             "Sáu phân hệ được ghi: Thành viên · Đơn hàng · Kho hàng · Sản "
             "phẩm · Rút tiền · Tài khoản admin. Sáu nhóm hành động: Tạo mới · "
             "Cập nhật · Duyệt · Từ chối · Khoá/mở khoá · Tải file lên. Cả "
             "thao tác của **hệ thống tự động** (gán mã kích hoạt khi xác nhận "
             "đơn) lẫn của **thành viên** (đăng ký, chấp thuận T&C) đều vào "
             "nhật ký, không chỉ thao tác của admin.", "",
             "**Tab 2 — File đã tải lên.** Tên file · loại · gắn với đối tượng "
             "nào · người tải · thời điểm · dung lượng · nút tải về. Gom mọi "
             "file trong hệ thống: ảnh CCCD, phiếu duyệt điều chỉnh cấp, file "
             "import kho, ảnh sản phẩm, uỷ nhiệm chi.", "",
             "**Hai nguyên tắc ghi rõ trên màn:**", "",
             "- Nhật ký **chỉ ghi thêm** — không sửa, không xoá, kể cả Head.",
             "- File đã tải lên **không xoá được**. Nộp nhầm thì tải bản đúng "
             "lên rồi ghi chú, bản cũ vẫn giữ.", "",
             "Không có hai điều này thì nhật ký vô nghĩa: ai xoá được dấu vết "
             "thì dấu vết không còn là bằng chứng.", "",
             "Xem thử: `b8-audit-log.html` và `#file`.", "",
             "**Cần chốt với dev:**", "",
             "1. **Thời gian lưu.** Giữ bao lâu rồi chuyển sang lưu trữ lạnh? "
             "Nhật ký toàn hệ thống phình rất nhanh.",
             "2. **Ai được xem.** Bản mẫu cho cả Admin lẫn Head. Nhật ký chứa "
             "IP và thao tác của mọi người — KH cân nhắc có nên giới hạn ở "
             "Head không.",
             "3. Dữ liệu trong bản mẫu là **dựng sẵn**, không nối với thao tác "
             "thật trên các màn khác — bản thật backend ghi vào bảng "
             "`audit_log` ngay trong cùng giao dịch với thay đổi dữ liệu, "
             "không ghi sau bằng job riêng.", "",

             "## Ghi chú", "",
             "- Nút **Thanh toán** ở màn A1 trong mockup KH đang để nền đỏ `#EE0000` "
             "nhưng màu hover lại là cyan `#0099d1` — gần như chắc chắn là lỗi sót. "
             "Bản này đưa về màu chính. Cần KH xác nhận.",
             "- Điều hướng giữa các màn đổi từ `setState` sang chuyển file thật, "
             "vì mỗi màn giờ là một file `.html` riêng. Dữ liệu mang sang màn sau "
             "đi qua `sessionStorage`.",
             "- Thêm vòng focus bàn phím (WCAG 2.4.7) — không ảnh hưởng layout."]
    if left:
        diff += ["", "## ⚠ Còn sót màu cũ", ""] + ["- `%s`" % c for c in left]
    diff = uat.patch_diff(diff)      # (UAT 02/10) mục 19
    (V3 / "DIFF-vs-mockup-KH.md").write_text("\n".join(diff) + "\n", encoding="utf-8")

    # --- tổng kết ----------------------------------------------------------
    print("Xong.")
    print("  màn hình      : %d file trong screens/" % len(SCREENS))
    print("  trạng thái    : %d (mở bằng #hash)" % n_states)
    print("  font chép     : %d" % n_font)
    print("  runtime       : js/dc-runtime.js (%.1f KB)"
          % (runtime.stat().st_size / 1024))
    print("  bỏ ô Quận/Huyện: %d chỗ" % n_district)
    print("  responsive    : css/responsive.css (%d dòng, 4 điểm gãy)"
          % RESPONSIVE_CSS.count("\n"))
    print("  trang chính sách: %s" % ("%d mục" % n_pol if n_pol else "KHÔNG dựng"))
    print("  khối lồng sẵn, không nối thêm: %s"
          % (", ".join(n_nested) if n_nested else "không"))
    print("  còn sót màu cũ: %s" % (", ".join(left) if left else "không"))
    print("  khối bị trùng : %s" % ("; ".join(dup) if dup else "không"))
    print("  ô tra cứu SĐT còn sót: %s"
          % ("⚠ " + ", ".join(leaks) if leaks else "không"))
    if bg_miss:
        print("  ⚠ bản vá markup KHÔNG khớp neo (%d/%d):"
              % (len(bg_miss), len(BG_PATCHES)))
        for m in bg_miss:
            print("      " + m)
    else:
        print("  bản vá markup: %d/%d khớp hết" % (len(BG_PATCHES), len(BG_PATCHES)))
    print("")
    print("Mở: %s" % (V3 / "index.html"))


if __name__ == "__main__":
    main()
