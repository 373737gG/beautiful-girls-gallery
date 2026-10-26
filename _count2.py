# -*- coding: utf-8 -*-
import re
with open(r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 找DEFAULT_DATA数组
start = text.find('const DEFAULT_DATA = [')
end = text.find(']', start)
data_block = text[start:end+1]

# 数一下有多少个{id:
ids = re.findall(r'\{id:\d+,name:"([^"]+)"', data_block)
print(f'DEFAULT_DATA数组里的角色数: {len(ids)}')
print(f'前5个: {ids[:5]}')
print(f'后5个: {ids[-5:]}')

# 单独数一下新增的3个
print(f'璐米欧儿: {"璐米欧儿" in data_block}')
print(f'雅尔贞特: {"雅尔贞特" in data_block}')
print(f'リィベル: {"リィベル" in data_block}')
