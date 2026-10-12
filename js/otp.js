// Ô nhập OTP: gõ một số là nhảy sang ô kế, Backspace ở ô trống thì lùi lại,
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
    el.value = (el.value || '').replace(/\D/g, '').slice(0, 1);
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
    var digits = txt.replace(/\D/g, '');
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
// cuộn hết văn bản, hoặc mở một link chính sách. Từ 06/10 form mua hàng
// (A1) dùng chung cơ chế này: ô đồng ý khoá tới khi bấm link chính sách. Runtime dựng lại DOM mỗi lần
// đổi state nên phải áp lại trạng thái sau mỗi lần DOM thay đổi.
(function () {
  var read = false;

  function apply() {
    var box = document.querySelector('.tnc-agree');
    if (!box) return;
    var st0 = window.__STATE__ || {};
    if (st0.buyTcChecked || st0.tncChecked) read = true;
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
