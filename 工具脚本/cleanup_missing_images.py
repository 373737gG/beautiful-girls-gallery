# -*- coding: utf-8 -*-
"""清理所有不存在的图片路径"""
import os
import re

html_path = r"D:\zhumian\工作区\项目归档\美少女图鉴\index.html"
img_dir = r"D:\zhumian\工作区\项目归档\美少女图鉴\images"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 提取DEFAULT_DATA数组
match = re.search(r'const DEFAULT_DATA = \[(.*?)\];', html, re.DOTALL)
if not match:
    print("没找到DEFAULT_DATA")
    exit()

data_str = match.group(1)
objects = re.findall(r'\{[^{}]*\}', data_str)
print(f"共 {len(objects)} 个角色")

fixed = 0
new_objects = []

for obj in objects:
    # 提取images字段
    img_match = re.search(r'images:\[([^\]]+)\]', obj)
    if not img_match:
        new_objects.append(obj)
        continue
    
    images_str = img_match.group(1)
    images = re.findall(r'"([^"]+)"', images_str)
    
    # 检查哪些图片存在
    valid_images = []
    for img in images:
        full_path = os.path.join(img_dir, img.replace('/', os.sep))
        if os.path.exists(full_path):
            valid_images.append(img)
        else:
            print(f"  删除不存在的图片: {img}")
    
    if len(valid_images) != len(images):
        fixed += 1
        # 替换images字段
        new_images_str = ','.join(f'"{x}"' for x in valid_images)
        new_obj = re.sub(r'images:\[[^\]]+\]', f'images:[{new_images_str}]', obj)
        new_objects.append(new_obj)
    else:
        new_objects.append(obj)

print(f"\n共修正 {fixed} 个角色的图片列表")

# 重组数组
new_data_str = ',\n'.join(new_objects)
new_html = html[:match.start(1)] + new_data_str + html[match.end(1):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)
print("已保存")
