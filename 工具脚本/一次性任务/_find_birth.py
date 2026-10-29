# -*- coding: utf-8 -*-
import re
with open(r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 找提到生日的角色行
# 匹配模式：月日 + 生日 相关词
patterns = [
    r'(\d{1,2})月(\d{1,2})日',      # X月X日
    r'(\d{1,2})月(\d{1,2})号',      # X月X号
    r'生日',
]

lines = text.split('\n')
found = []
for i, line in enumerate(lines):
    if '生日' in line or '生' in line and ('月' in line and '日' in line):
        # 提取角色名
        m = re.search(r'name:"([^"]+)"', line)
        bd = re.findall(r'(\d{1,2})月(\d{1,2})日', line)
        if m and bd:
            for mm, dd in bd:
                found.append((m.group(1), int(mm), int(dd)))

# 去重
seen = set()
unique = []
for name, mm, dd in found:
    if (name, mm, dd) not in seen:
        seen.add((name, mm, dd))
        unique.append((name, mm, dd))

# 按月份排序
unique.sort(key=lambda x: x[1] * 100 + x[2])
print(f'共找到 {len(unique)} 个角色提到生日：')
for name, mm, dd in unique:
    print(f'  {name}: {mm}月{dd}日')
