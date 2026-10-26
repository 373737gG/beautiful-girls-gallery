# -*- coding: utf-8 -*-
import re
with open(r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 用括号配对找DEFAULT_DATA数组真正的结束位置
start = text.find('const DEFAULT_DATA = [')
depth = 0
in_str = False
esc = False
end = -1
i = start + len('const DEFAULT_DATA = ') - 1
while i < len(text):
    ch = text[i]
    if in_str:
        if esc:
            esc = False
        elif ch == '\\':
            esc = True
        elif ch == '"':
            in_str = False
    else:
        if ch == '"':
            in_str = True
        elif ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                end = i
                break
    i += 1

print(f'数组结束位置: {end}')
data_block = text[start:end+1]

# 数一下有多少个{id:
ids = re.findall(r'\{id:\d+,name:"([^"]+)"', data_block)
print(f'DEFAULT_DATA数组里的角色数: {len(ids)}')

# 单独数一下新增的3个
print(f'璐米欧儿: {"璐米欧儿" in data_block}')
print(f'雅尔贞特: {"雅尔贞特" in data_block}')
print(f'リィベル: {"リィベル" in data_block}')
