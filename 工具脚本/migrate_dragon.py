# -*- coding: utf-8 -*-
"""迁移龙族图片到子文件夹"""
import os
import re
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, '美少女图鉴.html')
IMG_DIR = os.path.join(BASE, 'images')

# 创建龙族文件夹
race_dir = os.path.join(IMG_DIR, '龙族')
os.makedirs(race_dir, exist_ok=True)

# 移动根目录下的所有图片文件（跳过json和已迁移的）
moved = 0
for f in os.listdir(IMG_DIR):
    fpath = os.path.join(IMG_DIR, f)
    if os.path.isfile(fpath) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        new_path = os.path.join(race_dir, f)
        if not os.path.exists(new_path):
            shutil.move(fpath, new_path)
            moved += 1
            print(f"移动: {f} -> 龙族/")

print(f"\n共移动 {moved} 张图到龙族文件夹")

# 更新HTML里的路径：找到所有images数组里的文件名，加上"龙族/"前缀
# 但要小心：只更新那些没有子文件夹前缀的
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# 提取所有images数组里的文件名
# 匹配 "xxx.jpg" 或 "xxx.png" 这样的字符串
# 但要排除已经有子文件夹前缀的（比如"机娘/xxx.jpg"）
# 简单方法：找所有images:[...]数组里的内容

def update_images_block(match):
    block = match.group(0)
    # 找到所有 "xxx" 字符串
    def replace_img(m):
        name = m.group(1)
        # 已经有/的跳过
        if '/' in name:
            return f'"{name}"'
        # 是图片文件的才加前缀
        if name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            return f'"龙族/{name}"'
        return f'"{name}"'
    return re.sub(r'"([^"]*\.(?:jpg|jpeg|png|webp))"', replace_img, block, flags=re.IGNORECASE)

# 匹配images:[...]数组
html = re.sub(r'images:\[[^\]]*\]', update_images_block, html)

# 保存
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML路径已更新")
