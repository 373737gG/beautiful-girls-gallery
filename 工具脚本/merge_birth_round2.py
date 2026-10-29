# -*- coding: utf-8 -*-
"""第2轮：生日数据合并（106条 = 105新增 + 1改值）
数据来源：生日数据查证/09-生日合并总表-109项.md + 10-第8批补遗.md（已验收，零编造）
规则：只碰 birth 字段；按 id 行首定位；M-D 不补零；不重排不格式化
"""
import re

PATH = r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html'

# (id, name校验, birth) —— 105 新增
ADD = [
    # 龙族 15
    (12, '古蕾雅', '11-3'), (18, '缇亚·莱特宁', '10-2'), (27, '上杉绘梨衣', '12-25'),
    (33, '伊丽莎白·巴托里', '5-17'), (43, '龙和', '2-2'), (44, '青龙元君', '2-7'),
    (45, '丹妮', '4-27'), (49, '塔露拉', '1-9'), (63, '帆稀', '4-17'),
    (56, '物部深月', '3-3'), (55, '今汐', '3-6'), (60, '夕', '11-11'),
    (61, '黍', '6-6'), (67, '夭夭', '1-19'),
    # 机娘 33
    (182, '伊卡洛斯', '12-25'), (183, '妮姆芙', '12-25'), (184, '小叽', '4-13'),
    (181, '结衣', '8-1'), (176, '薇薇', '6-19'), (188, 'HK416/可露凯', '4-16'),
    (191, 'WA2000', '7-5'), (193, '黛烟', '5-20'), (194, '赛琳娜·希声', '9-27'),
    (195, '丽芙·霁梦', '8-10'), (197, '拉弥亚·深谣', '2-21'), (198, '伊什梅尔·幻日', '1-1'),
    (199, '露娜·终焉', '10-26'), (200, '布偶熊·觅语', '11-1'), (201, '含英·檀心', '7-24'),
    (210, '企业', '10-3'), (211, '贝尔法斯特', '3-17'), (220, '岛风', '7-18'),
    (221, '大和', '8-8'), (223, '巡音流歌', '1-30'), (224, '洛天依', '7-12'),
    (225, '时乃空', '5-15'), (226, 'Neuro-sama', '12-19'), (179, '守岸人', '2-27'),
    (242, '桑多涅', '1-13'), (259, '天童爱丽丝', '3-25'), (260, '凯伊', '3-25'),
    (261, '水银灯', '11-10'), (262, '金丝雀', '9-22'), (263, '翠星石', '10-14'),
    (287, '信浓', '10-8'), (289, '武藏', '11-1'), (290, '长门', '11-9'),
    # 吸血鬼 15
    (74, '克鲁鲁·采佩西', '10-27'), (77, '缇拉鞠·加德斯布拉德', '2-18'),
    (78, '薇尔赫泽', '3-12'), (79, '卡莲·艾露维希娅斯', '6-26'), (87, '早园瑠佳', '11-27'),
    (89, '红玛利亚', '6-20'), (95, '爱尔奎特·布伦史塔德', '12-25'), (98, '赤夜萌香', '5-8'),
    (100, '黎榭莉亚·雷·克里斯塔利亚', '12-15'), (101, '伊琳娜·卢米涅斯克', '9-19'),
    (105, '依文洁琳·AK·麦道威尔', '6-20'), (106, '伊丽莎白', '8-21'),
    (110, '桐敷沙子', '12-8'), (115, 'Diva', '8-4'), (117, '紫苑·艾尔特拉姆·阿特拉西亚', '6-1'),
    # 魔女 21
    (120, '艾姬多娜', '1-24'), (122, '奥萝拉', '3-25'), (124, '席尔薇雅·琉奈海姆', '10-1'),
    (127, '伊蕾娜', '10-17'), (129, '莫妮卡·艾瓦雷特', '12-1'), (130, '亚梓莎', '5-17'),
    (133, '潘朵拉', '5-3'), (134, '贝阿朵莉切', '11-29'), (137, '尤莉丝', '4-23'),
    (138, '尼可', '9-29'), (139, '贞德Alter', '1-6'), (142, '久远寺有珠', '9-30'),
    (144, '丽塔·洛丝薇瑟', '3-1'), (147, '佩特拉·雷蒂', '2-14'), (152, '密涅瓦', '7-20'),
    (153, '赛赫麦特', '8-13'), (155, '火火里绫火', '12-31'), (160, '白石丽', '12-24'),
    (161, '木幡真琴', '2-22'), (162, '戴安娜·卡文迪什', '4-30'), (163, '莫娜', '8-31'),
    # 兽耳娘 4
    (250, '巧克力', '7-3'), (251, '香草', '7-3'), (249, '绯鞠', '12-21'), (238, '赫萝', '3-10'),
    # 精灵 12
    (268, '夜刀神十香', '4-10'), (269, '鸢一折纸', '11-11'), (270, '五河琴里', '8-3'),
    (271, '四糸乃', '3-20'), (272, '八舞耶俱矢', '10-18'), (273, '八舞夕弦', '10-18'),
    (274, '诱宵美九', '1-19'), (275, '七罪', '7-23'), (276, '时崎狂三', '6-10'),
    (277, '本条二亚', '2-29'), (278, '星宫六喰', '9-12'), (279, '崇宫澪', '12-25'),
    # 人族 1
    (291, '楪祈', '9-12'),
    # 第8批补遗 5（无 race 字段，不补 race）
    (48, '苇草', '10-16'), (50, '爱布拉娜', '10-16'), (51, '风笛', '7-17'),
    (58, '祀', '9-15'), (70, '伊莉丝·芙蕾雅', '7-10'),
]

# 改值：维尔姆 id65 4-17 → 2-5
FIX = [(65, '维尔姆', '4-17', '2-5')]

assert len(ADD) == 105, f'ADD 条数 {len(ADD)} != 105'
ids = [x[0] for x in ADD]
assert len(set(ids)) == 105, 'ADD 内 id 重复'
assert not set(ids) & {65}, '改值 id 不应同时出现在新增'

with open(PATH, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

def find_row(cid):
    """按行首 {id:NN, 定位唯一数据行"""
    hit = [i for i, ln in enumerate(lines) if ln.startswith('{id:%d,' % cid)]
    assert len(hit) == 1, f'id {cid} 命中 {len(hit)} 行'
    return hit[0]

# ===== 新增 105 条 =====
added = 0
for cid, name, birth in ADD:
    i = find_row(cid)
    line = lines[i]
    assert ('name:"%s"' % name) in line, f'id {cid} 名字不匹配（期望 {name}）'
    assert 'birth:' not in line, f'id {cid} {name} 已有 birth，不应在新增清单'
    assert line.count('desc:"') == 1, f'id {cid} desc 锚点非唯一'
    lines[i] = line.replace('desc:"', 'birth:"%s",desc:"' % birth, 1)
    added += 1

# ===== 改值：维尔姆 4-17 → 2-5 =====
fixed = 0
for cid, name, old, new in FIX:
    i = find_row(cid)
    line = lines[i]
    assert ('name:"%s"' % name) in line, f'id {cid} 名字不匹配'
    assert ('birth:"%s"' % old) in line, f'id {cid} 现值不是 {old}，改值前提不成立'
    lines[i] = line.replace('birth:"%s"' % old, 'birth:"%s"' % new, 1)
    fixed += 1

out = '\n'.join(lines)

# ===== 自检（交接文件要求） =====
names = re.findall(r'name:"([^"]+)"', out)
births = re.findall(r'birth:"([^"]+)"', out)
print('角色总数 :', len(names), '（应为 285）')
print('birth 总数:', len(births), '（应为 115）')
bad = [b for b in births if not re.fullmatch(r'\d{1,2}-\d{1,2}', b)]
print('格式异常 :', bad or '无')

# 抽样核对：按行首 {id:NN, 定位（txt.index(kw) 会错位到他人 desc 里先出现的名字，如琳德 desc 含"维尔姆"）
row_by_id = {}
for idx2, ln in enumerate(lines):
    m2 = re.match(r'\{id:(\d+),', ln)
    if m2:
        row_by_id[int(m2.group(1))] = ln
checks = [(63, '帆稀', '4-17'), (65, '维尔姆', '2-5'), (188, 'HK416/可露凯', '4-16'),
          (277, '本条二亚', '2-29'), (48, '苇草', '10-16'), (291, '楪祈', '9-12')]
all_ok = True
for cid, name, exp in checks:
    ln2 = row_by_id[cid]
    m3 = re.search(r'birth:"([^"]+)"', ln2)
    got = m3.group(1) if m3 else '未写入'
    ok = got == exp and ('name:"%s"' % name) in ln2
    all_ok = all_ok and ok
    print('id%-4d %-14s 期望 %-6s 实际 %-6s %s' % (cid, name, exp, got, 'OK' if ok else 'FAIL'))

# 追加校验：id 与 name/birth 对应关系逐条复核（防插错行）
txt_by_id = {}
for ln in lines:
    m = re.match(r'\{id:(\d+),', ln)
    if m:
        txt_by_id[int(m.group(1))] = ln
mismatch = []
for cid, name, birth in ADD:
    ln = txt_by_id[cid]
    if ('name:"%s"' % name) not in ln or ('birth:"%s"' % birth) not in ln:
        mismatch.append((cid, name, birth))
for cid, name, old, new in FIX:
    ln = txt_by_id[cid]
    if ('birth:"%s"' % new) not in ln:
        mismatch.append((cid, name, new))
print('id-name-birth 逐条复核:', '全部一致' if not mismatch else mismatch)

# 数据行结构：引号成对
for ln in lines:
    if re.match(r'\{id:\d+,name:', ln):
        assert ln.count('"') % 2 == 0, '引号不成对: ' + ln[:60]

assert len(names) == 285 and len(births) == 115 and not bad and all_ok and not mismatch, '自检未通过，禁止写入'

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(out)
print('\n写入完成：新增 %d 条，改值 %d 条' % (added, fixed))
