# -*- coding: utf-8 -*-
# 用根目录 图标.jpg 生成 HunterHack 启动图标
# 1) 原图复制到 drawable-nodpi（自适应图标背景用）
# 2) 生成各密度方形/圆形 webp（兜底位图）
# 3) 重写 mipmap-anydpi 自适应图标 XML
import os, shutil
from PIL import Image, ImageDraw

ROOT = r"C:\Users\24920\Desktop\P201\SuperStart"
SRC = os.path.join(ROOT, "图标.jpg")
RES = os.path.join(ROOT, "mobile", "src", "main", "res")

img = Image.open(SRC).convert("RGB")
w, h = img.size
s = min(w, h)
img = img.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))

# 1) nodpi 原图
nodpi = os.path.join(RES, "drawable-nodpi")
os.makedirs(nodpi, exist_ok=True)
img.save(os.path.join(nodpi, "hunter_logo.jpg"), quality=95)

# 2) 密度位图
DENS = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for name, px in DENS.items():
    d = os.path.join(RES, "mipmap-" + name)
    os.makedirs(d, exist_ok=True)
    sq = img.resize((px, px), Image.LANCZOS)
    sq.save(os.path.join(d, "ic_launcher.webp"), "WEBP", quality=92, method=6)
    # 圆形：四周透明
    rd = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    rd.paste(sq.convert("RGBA"), (0, 0))
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, px - 1, px - 1), fill=255)
    rd.putalpha(mask)
    rd.save(os.path.join(d, "ic_launcher_round.webp"), "WEBP", quality=92, method=6)
    print("saved", name, px)

# 3) 自适应图标 XML：背景铺满照片，前景透明
bg_xml = '''<?xml version="1.0" encoding="utf-8"?>
<bitmap xmlns:android="http://schemas.android.com/apk/res/android"
    android:src="@drawable/hunter_logo"
    android:gravity="fill" />
'''
with open(os.path.join(RES, "drawable", "hunter_logo_bg.xml"), "w", encoding="utf-8") as f:
    f.write(bg_xml)

for fn in ("ic_launcher.xml", "ic_launcher_round.xml"):
    xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/hunter_logo_bg" />
    <foreground android:drawable="@android:color/transparent" />
</adaptive-icon>
'''
    with open(os.path.join(RES, "mipmap-anydpi", fn), "w", encoding="utf-8") as f:
        f.write(xml)
print("done")
