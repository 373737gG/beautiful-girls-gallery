# -*- coding: utf-8 -*-
import re
with open(r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

names = re.findall(r'name:"([^"]+)"', text)
print(f'总角色数: {len(names)}')
print(f'璐米欧儿在列表里: {"璐米欧儿" in names}')
print(f'雅尔贞特在列表里: {"雅尔贞特" in names}')
print(f'リィベル在列表里: {"リィベル" in names}')
