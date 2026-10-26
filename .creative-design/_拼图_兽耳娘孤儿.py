# -*- coding: utf-8 -*-
"""拼图目检：兽耳娘 8 张孤儿图 contact sheet"""
import os
from PIL import Image, ImageDraw

base = r"D:\zhumian\工作区\项目归档\美少女图鉴\images\兽耳娘"
files = ["118467754.jpg", "images_5.jpg", "images_6.jpg", "images_7.jpg",
         "images_8.jpg", "images_9.jpg", "images_10.jpg", "images_11.jpg"]

cols, rows = 4, 2
cell_w, cell_h = 300, 420
label_h = 28
pad = 8

sheet = Image.new("RGB", (cols * cell_w + pad * (cols + 1),
                          rows * (cell_h + label_h) + pad * (rows + 1)), "#20242e")
draw = ImageDraw.Draw(sheet)

for i, fn in enumerate(files):
    r, c = divmod(i, cols)
    x0 = pad + c * (cell_w + pad)
    y0 = pad + r * (cell_h + label_h + pad)
    try:
        img = Image.open(os.path.join(base, fn))
        img = img.convert("RGB")
        img.thumbnail((cell_w, cell_h), Image.LANCZOS)
        # 居中放置
        ox = x0 + (cell_w - img.width) // 2
        oy = y0 + (cell_h - img.height) // 2
        sheet.paste(img, (ox, oy))
        draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], outline="#4a5568", width=1)
    except Exception as e:
        draw.text((x0 + 10, y0 + 10), "ERR: %s" % e, fill="#ff6666")
    draw.text((x0 + 8, y0 + cell_h + 4), fn, fill="#d1d5db")
    draw.text((x0 + 8, y0 + cell_h + 14), "%dx%d" % (img.width, img.height) if 'img' in dir() else "", fill="#9ca3af")

out = os.path.join(os.path.dirname(base), "_孤儿图拼图_兽耳娘8张.png")
sheet.save(out)
print("saved:", out, sheet.size)
