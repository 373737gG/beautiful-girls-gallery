# -*- coding: utf-8 -*-
"""删除露娜公主这个角色"""
import re

html_path = r"D:\zhumian\工作区\项目归档\美少女图鉴\美少女图鉴.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 提取DEFAULT_DATA数组
match = re.search(r'const DEFAULT_DATA = \[(.*?)\];', html, re.DOTALL)
if not match:
    print("没找到DEFAULT_DATA")
    exit()

data_str = match.group(1)
objects = re.findall(r'\{[^{}]*\}', data_str)
print(f"删除前共 {len(objects)} 个角色")

# 找到露娜公主并删除
new_objects = []
deleted = False
for obj in objects:
    if 'name:"露娜公主"' in obj:
        deleted = True
        print(f"已删除露娜公主")
        continue
    new_objects.append(obj)

print(f"删除后共 {len(new_objects)} 个角色")

if deleted:
    # 重组数组
    new_data_str = ',\n'.join(new_objects)
    new_html = html[:match.start(1)] + new_data_str + html[match.end(1):]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("已保存")
else:
    print("没找到露娜公主")
