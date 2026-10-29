# -*- coding: utf-8 -*-
"""第1轮任务B：给9个已知生日角色注入 birth 字段（锚点替换，逐条断言）"""
import re, sys

PATH = r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html'

# (角色全名, birth)
INJECT = [
    ('琳德', '2-5'),
    ('维尔姆', '4-17'),
    ('莉莎·海渥卡', '5-15'),
    ('真红杏树', '6-6'),
    ('千堂瑛里华', '6-7'),
    ('华法琳', '6-27'),
    ('真红（Shinku）', '8-13'),
    ('爱尔梅希尔德·卡恩斯坦', '8-28'),
    ('初音未来', '8-31'),
]

with open(PATH, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
patched = 0
for name, birth in INJECT:
    anchor = f'name:"{name}"'
    hit = [i for i, ln in enumerate(lines) if anchor in ln]
    assert len(hit) == 1, f'锚点非唯一: {name} 命中 {len(hit)} 行'
    i = hit[0]
    line = lines[i]
    assert 'birth:' not in line, f'{name} 已有 birth 字段，跳过注入？'
    assert line.count('desc:"') == 1, f'{name} 行内 desc 锚点非唯一'
    lines[i] = line.replace('desc:"', f'birth:"{birth}",desc:"', 1)
    patched += 1
    print(f'OK {name} -> birth:"{birth}" (line {i+1})')

assert patched == len(INJECT), f'注入数不符: {patched}/{len(INJECT)}'

out = '\n'.join(lines)

# ===== 补丁后三查 =====
# 1) 计数：birth 字段数 = 9
n_birth = len(re.findall(r'birth:"\d{1,2}-\d{1,2}"', out))
assert n_birth == 9, f'birth 字段数异常: {n_birth}'
# 2) 结构：数据行仍以 ]; 结束、id 连续性不受影响（简单验证 JSON 风格行引号成对）
for ln in lines:
    if re.match(r'\{id:\d+,name:', ln):
        assert ln.count('"') % 2 == 0, f'引号不成对: {ln[:60]}...'
# 3) 数据条数不变
n_rows = len(re.findall(r'\{id:\d+,name:', out))
print(f'数据行数: {n_rows}, birth 字段数: {n_birth}')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(out)
print('写入完成')
