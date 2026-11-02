# -*- coding: utf-8 -*-
"""统计 race 字段分布，确认魔族角色数量"""
import re, collections

t = open(r"D:\zhumian\工作区\项目归档\美少女图鉴\index.html", encoding="utf-8").read()
body = re.search(r"DEFAULT_DATA\s*=\s*\[(.*?)\];", t, re.S).group(1)
races = re.findall(r'race:"([^"]*)"', body)
cnt = collections.Counter(races)
print("race 字段分布（按数量降序）:")
for k, v in cnt.most_common():
    print(f"  {k}: {v}")
print("总角色数:", len(races))
