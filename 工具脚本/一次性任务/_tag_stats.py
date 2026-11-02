# -*- coding: utf-8 -*-
"""统计 index.html DEFAULT_DATA 的 tags 分布"""
import re, collections

t = open(r"D:\zhumian\工作区\项目归档\美少女图鉴\index.html", encoding="utf-8").read()
m = re.search(r"DEFAULT_DATA\s*=\s*\[(.*?)\];", t, re.S)
print("数据块找到:", bool(m))
body = m.group(1)

# 角色对象（含tags字段的）
tag_blocks = re.findall(r"tags:\s*\[(.*?)\]", body)
print("含tags字段的角色数:", len(tag_blocks))

all_tags = []
for blk in tag_blocks:
    all_tags.extend(re.findall(r'"([^"]+)"', blk))

cnt = collections.Counter(all_tags)
print("总标签引用次数:", len(all_tags), "| 去重标签数:", len(cnt))
print("\n=== 全部标签及频次（按频次降序）===")
for k, v in cnt.most_common():
    print(f"{k}: {v}")
