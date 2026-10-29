# -*- coding: utf-8 -*-
"""迁移旧图片到种族子文件夹，并更新HTML里的路径"""
import os
import re
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, 'index.html')
IMG_DIR = os.path.join(BASE, 'images')

# 读取HTML
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# 提取所有角色数据：找 race:"xxx" 和 images:["xxx","xxx"]
# 简单方法：按 {id:... 块拆分
# 用正则匹配每个角色的race和images
pattern = r'\{id:(\d+),name:"([^"]*)"[^}]*?race:"([^"]*)"[^}]*?images:\[([^\]]*)\][^}]*?\}'
matches = re.findall(pattern, html, re.DOTALL)

print(f"找到 {len(matches)} 个角色")

# 统计要迁移的文件
moved = 0
not_found = []
updates = []  # (old_img_path, new_img_path)

for char_id, name, race, images_str in matches:
    # 解析images列表
    images = re.findall(r'"([^"]*)"', images_str)
    for img in images:
        if img.startswith('data:'):
            continue  # base64的跳过
        old_path = os.path.join(IMG_DIR, img)
        race_dir = os.path.join(IMG_DIR, race)
        new_path = os.path.join(race_dir, img)
        if os.path.exists(old_path):
            # 创建种族文件夹
            os.makedirs(race_dir, exist_ok=True)
            # 如果目标已存在，不覆盖
            if not os.path.exists(new_path):
                shutil.move(old_path, new_path)
                moved += 1
                print(f"  移动: {img} -> {race}/")
            else:
                print(f"  已存在: {race}/{img}，跳过")
            # 记录路径更新
            rel_new = f"{race}/{img}"
            updates.append((img, rel_new))
        else:
            # 可能已经在子文件夹里了
            if os.path.exists(new_path):
                # 已经在子文件夹里，更新路径
                updates.append((img, f"{race}/{img}"))
            else:
                not_found.append(img)

print(f"\n迁移完成: 移动了 {moved} 张图")
if not_found:
    print(f"未找到的文件 ({len(not_found)}):")
    for f in not_found[:10]:
        print(f"  - {f}")

# 更新HTML里的图片路径
if updates:
    print(f"\n更新HTML里的路径...")
    for old, new in updates:
        # 只替换 images: 里的，避免替换其他地方
        # 用精确匹配："old_img" -> "new_img"
        old_str = f'"{old}"'
        new_str = f'"{new}"'
        count = html.count(old_str)
        if count > 0:
            html = html.replace(old_str, new_str)
            print(f"  替换: {old} -> {new} ({count}处)")

    # 保存HTML
    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print("\nHTML已更新保存")
else:
    print("\n没有需要更新的路径")
