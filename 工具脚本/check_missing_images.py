# -*- coding: utf-8 -*-
"""检查图鉴里引用的图片是否都存在"""
import os
import re

html_path = r"D:\zhumian\工作区\项目归档\美少女图鉴\美少女图鉴.html"
img_dir = r"D:\zhumian\工作区\项目归档\美少女图鉴\images"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 提取所有images:["..."]里的图片路径
pattern = r'images:\[([^\]]+)\]'
matches = re.findall(pattern, html)

all_images = []
for m in matches:
    imgs = re.findall(r'"([^"]+)"', m)
    all_images.extend(imgs)

print(f"HTML里共引用了 {len(all_images)} 张图片")

# 检查哪些不存在
missing = []
exist = []
for img in all_images:
    full_path = os.path.join(img_dir, img.replace('/', os.sep))
    if os.path.exists(full_path):
        exist.append(img)
    else:
        missing.append(img)

print(f"存在: {len(exist)} 张")
print(f"缺失: {len(missing)} 张")
print()
if missing:
    print("缺失的图片列表：")
    for m in missing:
        print(f"  - {m}")
