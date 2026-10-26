# -*- coding: utf-8 -*-
import io, re, sys

p = 'index.html'
s = io.open(p, encoding='utf-8', newline='').read()

STORIES = {
    239: 'ZipZipPipe创作的AI娘化图鉴一员，拟人对象为Google的Gemini模型。设计保留Gemini标志的四角星发饰与品牌蓝紫配色，因社区把Gemini读成「哈基米」而定为猫娘；又因有时聊得头头是道、办事却常掉链子，被戏称「北美豆包」。在AI娘小剧场里她活泼跳脱，常与GPT龙娘、鲸鱼娘等同框登场，随系列图在B站等社区广泛传播。',
    240: '拟人对象为马斯克旗下xAI的Grok模型。2025年7月xAI在Grok应用推出「伴侣模式」，首位角色是以《死亡笔记》弥海砂为原型的哥特金发双马尾少女Ani，内置从冷漠到热恋的好感度系统，上线后引发狂热追捧与内容尺度争议。社区娘化形象因此与Ani绑定，ZipZipPipe版沿用金发双马尾与黑色礼服，斧形饰物缀有「X」字样。二创中她以敢说、尺度放得开出名，常与规矩森严的Claude娘组成反差搭档。',
    241: '拟人对象为法国巴黎公司Mistral AI。公司名取自法国南部著名的密斯特拉冷风，社区娘化形象因此融入浓厚法式元素：随风扬起的金发、宽檐帽与法棍面包、红白配色衣裙。Mistral以开放权重模型路线（Mistral 7B、Mixtral等）和聊天助手Le Chat（法语意为「猫」）闻名，是欧洲AI的代表厂商。在AI娘图鉴中她与鲸鱼娘、GPT龙娘等同属ZipZipPipe绘制的「赛博女团」。',
}

lines = s.split('\r\n' if '\r\n' in s else '\n')
nl = '\r\n' if '\r\n' in s else '\n'
changed = 0
for i, l in enumerate(lines):
    m = re.match(r'\{id:(\d+),', l)
    if not m:
        continue
    cid = int(m.group(1))
    if cid in STORIES and 'story:""' in l:
        lines[i] = l.replace('story:""', 'story:"' + STORIES[cid] + '"')
        changed += 1
print('filled:', changed)
assert changed == 3
s2 = nl.join(lines)
assert "DATA_VERSION = '20261027-v34'" in s2
s2 = s2.replace("DATA_VERSION = '20261027-v34'", "DATA_VERSION = '20261027-v35'")
io.open(p, 'w', encoding='utf-8', newline='').write(s2)
print('written v35')
