# -*- coding: utf-8 -*-
import re
import os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, '美少女图鉴.html')

with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# 统计角色数
ids = re.findall(r'\{id:(\d+),name:', html)
print(f'总角色数: {len(ids)}')

# 统计种族
races = re.findall(r'race:"([^"]+)"', html)
race_count = Counter(races)
print(f'\n种族分布（有race字段的）:')
for r, c in race_count.most_common():
    print(f'  {r}: {c}人')
print(f'  （其余默认龙族，共 {len(ids)-len(races)} 人）')

# 统计类型
types = re.findall(r'type:"([^"]+)"', html)
type_count = Counter(types)
print(f'\n类型分布:')
for t, c in type_count.most_common():
    print(f'  {t}: {c}人')

# 统计图片数
imgs = re.findall(r'images:\[([^\]]*)\]', html)
total_imgs = 0
base64_count = 0
missing_img = []
for i, img_list in enumerate(imgs):
    img_names = re.findall(r'"([^"]+)"', img_list)
    total_imgs += len(img_names)
    for name in img_names:
        if name.startswith('data:'):
            base64_count += 1
        else:
            # 检查文件是否存在
            img_path = os.path.join(BASE, 'images', name.replace('/', os.sep))
            if not os.path.exists(img_path):
                missing_img.append(name)

print(f'\n总图片数: {total_imgs}')
print(f'  base64内嵌: {base64_count}张')
print(f'  本地文件引用: {total_imgs - base64_count}张')
if missing_img:
    print(f'  缺失文件 ({len(missing_img)}):')
    for m in missing_img[:10]:
        print(f'    - {m}')
else:
    print(f'  本地文件全部存在 ✓')

# 检查images文件夹
img_dir = os.path.join(BASE, 'images')
print(f'\nimages文件夹结构:')
for d in sorted(os.listdir(img_dir)):
    dpath = os.path.join(img_dir, d)
    if os.path.isdir(dpath):
        count = len([f for f in os.listdir(dpath) if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))])
        print(f'  {d}/: {count}张')
