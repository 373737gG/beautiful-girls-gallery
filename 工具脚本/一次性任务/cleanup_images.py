# -*- coding: utf-8 -*-
"""列出残留的旧图片（不直接删除，安全版）"""
import os
import re

BASE = r"D:\zhumian\工作区\项目归档\美少女图鉴"
HTML = BASE + r"\index.html"
IMAGES_DIR = BASE + r"\images"

# 读取HTML，提取所有images字段里的图片路径
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

used_images = set()
for match in re.finditer(r'images:\[([^\]]+)\]', html):
    items = match.group(1)
    for img_match in re.finditer(r'"([^"]+)"', items):
        used_images.add(img_match.group(1))

# 扫描images文件夹里的所有图片
all_images = set()
for race in os.listdir(IMAGES_DIR):
    race_dir = os.path.join(IMAGES_DIR, race)
    if os.path.isdir(race_dir):
        for img in os.listdir(race_dir):
            if not img.startswith('.'):
                rel_path = f"{race}/{img}"
                all_images.add(rel_path)

# 找出残留的
unused = all_images - used_images
print(f"找到 {len(unused)} 张残留的旧图（HTML里没引用）")
print()

if unused:
    print("残留图片列表：")
    for rel_path in sorted(unused):
        abs_path = os.path.join(IMAGES_DIR, rel_path.replace('/', os.sep))
        size = os.path.getsize(abs_path) / 1024
        print(f"  - {rel_path}  ({size:.1f} KB)")
    
    print()
    print("⚠️  此脚本只列出，不删除！")
    print("如果确认要删，手动删除上面这些文件即可。")
else:
    print("没有残留图片。")
