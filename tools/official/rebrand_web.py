#!/usr/bin/env python3
"""Apply the SASMAN presentation layer to an extracted official airOS webroot."""
from pathlib import Path
import re
import shutil
import sys

webroot = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("rootfs/usr/www")
asset = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("assets/sasman_logo.png")
css = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("tools/official/sasman_official.css")

if not webroot.is_dir():
    raise SystemExit(f"webroot not found: {webroot}")
if not asset.is_file():
    raise SystemExit(f"logo asset not found: {asset}")
if not css.is_file():
    raise SystemExit(f"CSS file not found: {css}")

logo_dest = webroot / "images" / "sasman_logo.png"
logo_dest.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(asset, logo_dest)

head = webroot / "lib" / "head.tmpl"
head_text = head.read_text(encoding="utf-8")
old_head = '''  <tr>\n    <td height="70">\n<? if (strlen($img_product_logo) == 0) {'''
new_head = '''  <tr>\n    <td height="70" class="sasman-brand-cell">\n      <div class="sasman-brand">\n        <img src="images/sasman_logo.png" alt="SASMAN">\n        <span>SASMAN</span>\n      </div>\n      <div class="sasman-device-label">\n<? if (strlen($img_product_logo) == 0) {'''
if old_head not in head_text:
    raise SystemExit("official head.tmpl marker not found")
head_text = head_text.replace(old_head, new_head, 1)
old_head_end = '''<? } >    \n    </td>'''
new_head_end = '''<? } >\n      </div>\n    </td>'''
if old_head_end not in head_text:
    raise SystemExit("official head.tmpl closing marker not found")
head_text = head_text.replace(old_head_end, new_head_end, 1)
head.write_text(head_text, encoding="utf-8")

login = webroot / "login.cgi"
login_text = login.read_text(encoding="utf-8")
login_pattern = r'\t\t<td valign="top"><img src="/[^"]*/images/airos_logo\.png"></td>'
new_login = '''\t\t<td valign="top" class="sasman-login-brand">\n\t\t\t<img src="images/sasman_logo.png" alt="SASMAN">\n\t\t\t<div class="sasman-login-caption">SASMAN</div>\n\t\t</td>'''
login_text, login_count = re.subn(login_pattern, new_login, login_text, count=1)
if login_count != 1:
    raise SystemExit("official login.cgi marker not found")
login.write_text(login_text, encoding="utf-8")

style = webroot / "style.css"
style_text = style.read_text(encoding="utf-8")
marker = "\n/* SASMAN official airOS presentation layer */\n"
if marker not in style_text:
    style.write_text(style_text + marker + css.read_text(encoding="utf-8"), encoding="utf-8")

print(f"rebranded {webroot}")
print(f"logo_bytes={logo_dest.stat().st_size}")
