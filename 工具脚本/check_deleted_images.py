# -*- coding: utf-8 -*-
"""检查哪些图片被删除了，本地文件夹里还有没有残留"""
import os
import re

BASE = r"D:\zhumian\工作区\项目归档\美少女图鉴"
HTML = BASE + r"\美少女图鉴.html"
IMAGES_DIR = BASE + r"\images"

# 读取HTML，提取所有images字段里的图片路径
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# 匹配所有images:["xxx","xxx"]
used_images = set()
for match in re.finditer(r'images:\[([^\]]+)\]', html):
    items = match.group(1)
    for img_match in re.finditer(r'"([^"]+)"', items):
        used_images.add(img_match.group(1))

print(f"HTML里引用了 {len(used_images)} 张图片")

# 扫描images文件夹里的所有图片
all_images = set()
for race in os.listdir(IMAGES_DIR):
    race_dir = os.path.join(IMAGES_DIR, race)
    if os.path.isdir(race_dir):
        for img in os.listdir(race_dir):
            if not img.startswith('.'):
                rel_path = f"{race}/{img}"
                all_images.add(rel_path)

print(f"images文件夹里有 {len(all_images)} 张图片")

# 找出残留的（在文件夹里但没被引用的）
unused = all_images - used_images
print(f"\n残留的图片（被删了但本地还在的）：{len(unused)} 张")
for img in sorted(unused):
    print(f"  - {img}")
