# -*- coding: utf-8 -*-
"""把导出的JSON数据同步到HTML文件里"""
import json

BASE = r"D:\zhumian\工作区\项目归档\美少女图鉴"
HTML = BASE + r"\index.html"
JSON_FILE = r"C:\Users\Chong\Downloads\龙娘图鉴_数据 (1).json"

# 读取JSON
with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"JSON里有 {len(data)} 个角色")

# 读取HTML
with open(HTML, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到DEFAULT_DATA的开始和结束行
start_line = -1
end_line = -1
for i, line in enumerate(lines):
    if 'const DEFAULT_DATA = [' in line:
        start_line = i
    if start_line >= 0 and line.strip() == '];':
        end_line = i
        break

print(f"DEFAULT_DATA从第{start_line+1}行到第{end_line+1}行")

# 把JSON数据转成JS格式的字符串（一行一个对象）
def to_js_obj(obj):
    items = []
    for k, v in obj.items():
        if isinstance(v, str):
            s = v.replace('\\', '\\\\').replace('"', '\\"')
            items.append(f'{k}:"{s}"')
        elif isinstance(v, list):
            arr = ','.join(f'"{x}"' if isinstance(x, str) else str(x) for x in v)
            items.append(f'{k}:[{arr}]')
        elif isinstance(v, bool):
            items.append(f'{k}:{"true" if v else "false"}')
        elif v is None:
            items.append(f'{k}:null')
        else:
            items.append(f'{k}:{v}')
    return '{' + ','.join(items) + '}'

new_data_lines = []
for char in data:
    new_data_lines.append(to_js_obj(char) + ',\n')

# 替换中间的内容
new_lines = lines[:start_line+1] + new_data_lines + lines[end_line:]

# 保存
with open(HTML, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"已同步 {len(data)} 个角色到HTML文件")
