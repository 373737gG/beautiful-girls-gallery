# -*- coding: utf-8 -*-
"""调整角色顺序：把结衣移到鲸鱼娘后面"""
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
# 按行分割每个角色对象
objects = re.findall(r'\{[^{}]*\}', data_str)
print(f"共找到 {len(objects)} 个角色")

# 找到结衣和鲸鱼娘
yui = None
whale_idx = None
for i, obj in enumerate(objects):
    if 'name:"结衣"' in obj:
        yui = obj
        print(f"结衣在第 {i+1} 个")
    if 'name:"鲸鱼娘"' in obj:
        whale_idx = i
        print(f"鲸鱼娘在第 {i+1} 个")

if yui and whale_idx is not None:
    # 从原位置删除结衣
    objects.remove(yui)
    # 鲸鱼娘的位置可能变了，重新找
    for i, obj in enumerate(objects):
        if 'name:"鲸鱼娘"' in obj:
            whale_idx = i
            break
    # 插入到鲸鱼娘后面
    objects.insert(whale_idx + 1, yui)
    print(f"已把结衣移到鲸鱼娘后面（第 {whale_idx+2} 个）")
    
    # 重组数组
    new_data_str = ',\n'.join(objects)
    new_html = html[:match.start(1)] + new_data_str + html[match.end(1):]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("已保存")
else:
    print("没找到")
