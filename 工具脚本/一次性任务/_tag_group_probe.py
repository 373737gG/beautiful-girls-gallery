# -*- coding: utf-8 -*-
"""统计高频标签(>=2次)数量并做分组预归类"""
import re, collections

t = open(r"D:\zhumian\工作区\项目归档\美少女图鉴\index.html", encoding="utf-8").read()
body = re.search(r"DEFAULT_DATA\s*=\s*\[(.*?)\];", t, re.S).group(1)
tag_blocks = re.findall(r"tags:\s*\[(.*?)\]", body)
all_tags = []
for blk in tag_blocks:
    all_tags.extend(re.findall(r'"([^"]+)"', blk))
cnt = collections.Counter(all_tags)
high = {k: v for k, v in cnt.items() if v >= 2}
print("高频标签(>=2次)总数:", len(high))

# 候选分组（预归类，供讨论）
groups = {
    "外貌特征": ["金发","红发","蓝发","粉发","银发","黑发","白发","灰白发","绿发","黑长直","粉白配色","双马尾","短发","异色瞳","萝莉","御姐","巨乳","幼女","大姐姐"],
    "服装风格": ["女仆","和服","旗袍","哥特","长裙","巫女服","JK","修女"],
    "性格/设定": ["傲娇","元气","三无","病娇","天然呆","毒舌","腹黑","怕生","社恐","中二病","呆萌","温柔","吃货","家里蹲","笨拙","不坦率","热血","天然","黑化","呆萌"],
    "身份/种族": ["舰娘","马娘","歌姬","偶像","公主","女王","妹妹","巫女","骑士","医生","天使","精灵","魔族","吸血鬼","龙娘","魔女","人偶","仿生人","真祖","圣女","皇女","王女","魔王","妖精","猫娘","狐娘","狼","兔","马","鸟","鹿","狐","羊","鼠","神","幼女","大妖","九尾","独角","半精灵","双子精灵","人工精灵","风之天使","万能天使","人形电脑","Chobits","智械","构造体","机械","机甲"],
    "出处/作品": ["明日方舟","FGO","原神","星穹铁道","NIKKE","崩坏3","鸣潮","LoveLive","μ's","孤独摇滚","MyGO!!!!!","CRYCHIC","赛马娘","公主连结","偶像事变","偶像议员","舞台少女","Revue","GFL2","VTuber","hololive","Chobits","SAO","SEED","GC"],
    "组织/阵营": ["七红天","AR小队","莱茵生命","罗德岛","企鹅物流","女神部队","反击部队","逐火十三英桀","天才俱乐部","莱茵生命","深海猎人","阿戈尔","什亭之匣","雪狼小队","404小队","灰鸦小队","目白家","纽带乐队","B小町","sumimi","Ave Mujica","Mortis"],
    "其他/待定": [],
}
covered = set()
for gname, tags in groups.items():
    hit = [k for k in high if k in tags]
    covered.update(hit)
    print(f"\n[{gname}] 命中{len(hit)}个: {'、'.join(sorted(hit))}")
uncovered = sorted(set(high) - covered)
print(f"\n=== 未归类高频标签 {len(uncovered)} 个 ===")
print("、".join(uncovered))
