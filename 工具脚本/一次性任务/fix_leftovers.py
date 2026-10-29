# -*- coding: utf-8 -*-
"""遗留解决：① 21 缺race角色补 race:"龙族"（08文档确认 type 均为龙娘/龙之巫女/真龙）
② 吉拉蒂亚(id46) 定案 birth 9-14（游戏内官方星痕档案 > 第三方百科 2-10）
③ 西施维持不写入（实装日≠生日）"""
import re

PATH = r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html'

# (id, name, type校验) —— 08 文件 21 人
RACE21 = [
    (5, '娜比', '龙娘'), (6, '托尔', '龙娘'), (8, '露科亚', '真龙'), (15, '白莲', '龙娘'),
    (19, '莉莎·海渥卡', '龙之巫女'), (25, '艾哈', '龙之巫女'), (26, '特娅', '龙娘'),
    (29, '艾拉', '龙娘'), (31, '提亚马特（幼体）', '真龙'), (34, '法露特（黑龙骑士）', '龙娘'),
    (35, '龙之魔女·莉莉乌姆', '龙娘'), (37, '清姬', '龙娘'), (41, '龙珏', '龙娘'),
    (46, '吉拉蒂亚', '龙娘'), (48, '苇草', '龙娘'), (50, '爱布拉娜', '龙娘'),
    (51, '风笛', '龙娘'), (52, '露娜', '龙娘'), (54, '西施', '龙娘'),
    (58, '祀', '龙娘'), (70, '伊莉丝·芙蕾雅', '龙之巫女'),
]
assert len(RACE21) == 21 and len(set(x[0] for x in RACE21)) == 21

with open(PATH, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

def find_row(cid):
    hit = [i for i, ln in enumerate(lines) if ln.startswith('{id:%d,' % cid)]
    assert len(hit) == 1, 'id %d 命中 %d 行' % (cid, len(hit))
    return hit[0]

# ① 补 race
n_race = 0
for cid, name, typ in RACE21:
    i = find_row(cid)
    line = lines[i]
    assert ('name:"%s"' % name) in line, 'id %d 名字不匹配' % cid
    assert 'race:' not in line, 'id %d 已有 race' % cid
    assert ('type:"%s"' % typ) in line, 'id %d type 不是 %s' % (cid, typ)
    assert line.count('type:"') == 1
    lines[i] = line.replace('type:"', 'race:"龙族",type:"', 1)
    n_race += 1

# ② 吉拉蒂亚 birth 9-14
i = find_row(46)
line = lines[i]
assert 'birth:' not in line, 'id46 已有 birth'
assert line.count('desc:"') == 1
lines[i] = line.replace('desc:"', 'birth:"9-14",desc:"', 1)

out = '\n'.join(lines)

# ===== 自检 =====
n_race_total = len(re.findall(r'race:"龙族"', out))
n_birth = len(re.findall(r'birth:"\d{1,2}-\d{1,2}"', out))
names = re.findall(r'name:"([^"]+)"', out)
print('角色总数:', len(names), '(应 285)')
print('race:"龙族" 总数:', n_race_total)
print('birth 总数:', n_birth, '(应 116)')
# 21 人行内 race 与 type 相邻且原 type 保留
ok = all('race:"龙族",type:"%s"' % typ in next(l for l in lines if l.startswith('{id:%d,' % cid))
         for cid, name, typ in RACE21)
print('21人 race+type 相邻校验:', 'OK' if ok else 'FAIL')
# 吉拉蒂亚 birth
g = re.search(r'\{id:46,[^\n]*?birth:"([^"]+)"', out)
print('吉拉蒂亚 birth:', g.group(1) if g else '未写入', '(应 9-14)')
# 引号成对
for ln in lines:
    if re.match(r'\{id:\d+,name:', ln):
        assert ln.count('"') % 2 == 0, '引号不成对'

assert len(names) == 285 and n_birth == 116 and ok and g and g.group(1) == '9-14', '自检未通过'
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(out)
print('\n写入完成：补 race %d 人，吉拉蒂亚 birth 9-14' % n_race)
