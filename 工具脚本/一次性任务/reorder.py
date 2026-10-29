# -*- coding: utf-8 -*-
"""调整角色顺序：把吸血鬼号移到阿尔萨斯后面"""
import re

html_path = r"D:\zhumian\工作区\项目归档\美少女图鉴\index.html"

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

# 找到吸血鬼号和阿尔萨斯
vampire = None
alsace_idx = None
for i, obj in enumerate(objects):
    if 'name:"吸血鬼号"' in obj:
        vampire = obj
        print(f"吸血鬼号在第 {i+1} 个")
    if 'name:"阿尔萨斯"' in obj:
        alsace_idx = i
        print(f"阿尔萨斯在第 {i+1} 个")

if vampire and alsace_idx is not None:
    # 从原位置删除吸血鬼号
    objects.remove(vampire)
    # 阿尔萨斯的位置可能变了，重新找
    for i, obj in enumerate(objects):
        if 'name:"阿尔萨斯"' in obj:
            alsace_idx = i
            break
    # 插入到阿尔萨斯后面
    objects.insert(alsace_idx + 1, vampire)
    print(f"已把吸血鬼号移到阿尔萨斯后面（第 {alsace_idx+2} 个）")
    
    # 重组数组
    new_data_str = ',\n'.join(objects)
    new_html = html[:match.start(1)] + new_data_str + html[match.end(1):]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("已保存")
else:
    print("没找到")
