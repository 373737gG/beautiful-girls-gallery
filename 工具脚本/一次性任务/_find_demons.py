# -*- coding: utf-8 -*-
"""找出 race:"恶魔" 的角色，供并入魔族"""
import re

t = open(r"D:\zhumian\工作区\项目归档\美少女图鉴\index.html", encoding="utf-8").read()
# 角色对象：{id:..,name:"..",...,race:".."}
objs = re.findall(r'\{id:(\d+),name:"([^"]*)",.*?race:"([^"]*)"', t)
demons = [(i, n) for i, n, r in objs if r == "恶魔"]
print(f"race:\"恶魔\" 角色 {len(demons)} 个:")
for i, n in demons:
    print(f"  id={i}  {n}")
