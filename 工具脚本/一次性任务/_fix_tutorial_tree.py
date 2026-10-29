# -*- coding: utf-8 -*-
"""修正 Agent编辑教程.md 结构树代码块（正则定位）"""
import re
from pathlib import Path

p = Path(r"D:\zhumian\工作区\项目归档\美少女图鉴\文档\Agent编辑教程.md")
text = p.read_text(encoding="utf-8")

new_block = """```
美少女图鉴/
├─ index.html              # 核心：单文件应用（UI+CSS+JS+DEFAULT_DATA 数据全在一个文件）
├─ server.py               # 本地服务器，端口 8899，/save /upload /delete /orphans /selfcheck
├─ 启动图鉴.bat             # 双击启动 server.py 并自动开浏览器
├─ 同步到网站.bat           # 部署 GitHub Pages（github.com/373737gG/beautiful-girls-gallery）
├─ 文档/                    # Agent编辑教程.md + 交接任务书-生日功能.md
├─ 过程文件/                # 设计/预览过程产物（生日功能预览/ 等）
├─ images/                 # 角色图片，按种族子目录；文件名一律 角色名_序号.扩展名
├─ assets/                 # 站点静态资源
├─ 工具脚本/                # 正式工具（接图助手.py、更新音乐列表.py、check_*.py）
│  └─ 一次性任务/           # 历史一次性/临时脚本（已归档，勿再使用）
└─ 归档-20261027/          # 历史归档（保留不动）
```"""

m = re.search(r"```\n美少女图鉴/.*?\n```", text, re.S)
print("找到结构树块:", bool(m))
if m:
    text = text[:m.start()] + new_block + text[m.end():]

p.write_text(text, encoding="utf-8", newline="")
print("=== 结构树已更新 ===")
