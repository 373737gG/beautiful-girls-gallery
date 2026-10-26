# -*- coding: utf-8 -*-
with open(r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('const DEFAULT_DATA = [')
print(f'找到DEFAULT_DATA: {start != -1}')

# 括号配对检查
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

print(f'括号配对正确: {end != -1}')
print(f'璐米欧儿在文件里: {"璐米欧儿" in text}')
print(f'雅尔贞特在文件里: {"雅尔贞特" in text}')
print(f'リィベル在文件里: {"リィベル" in text}')
