# -*- coding: utf-8 -*-
import re
with open(r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 数龙族角色
dragon = re.findall(r'type:"龙[^"]*"', text)
print(f'龙族角色总数: {len(dragon)}')
print(f'璐米欧儿在文件里: {"璐米欧儿" in text}')
print(f'雅尔贞特在文件里: {"雅尔贞特" in text}')
print(f'リィベル在文件里: {"リィベル" in text}')

# 数所有角色
names = re.findall(r'name:"([^"]+)"', text)
print(f'总角色数: {len(names)}')
