# -*- coding: utf-8 -*-
"""更新 Agent编辑教程.md：结构树/版本/功能清单/删除纪律/待办"""
from pathlib import Path

p = Path(r"D:\zhumian\工作区\项目归档\美少女图鉴\文档\Agent编辑教程.md")
text = p.read_text(encoding="utf-8")  # 无BOM UTF-8

def rep(old, new):
    global text
    if old not in text:
        print("未找到片段，跳过:", old[:40].replace("\n", "\\n"))
        return
    text = text.replace(old, new, 1)
    print("OK:", old[:24].replace("\n", "\\n"), "...")

# 1) 结构树
rep("""```
美少女图鉴/
├─ index.html          # 核心：单文件应用（UI+CSS+JS+DEFAULT_DATA 数据全在一个文件）
├─ server.py           # 本地服务器，端口 8899，/save /upload /delete /orphans /selfcheck
├─ 启动图鉴.bat         # 双击启动 server.py 并自动开浏览器
├─ 同步到网站.bat       # 部署 GitHub Pages（github.com/373737gG/beautiful-girls-gallery）
├─ Agent编辑教程.md     # 本文档
├─ images/             # 角色图片，按种族子目录；文件名一律 角色名_序号.扩展名
├─ 工具脚本/            # 正式工具（接图助手.py 等）
└─ 归档-20261027/       # 历史备份（仅最新2个）、一次性脚本、研究数据、任务书与设定文档
```""",
"""```
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
```""")

# 2) 版本演进
rep("版本演进：v37（20261027 七项优化前）→ v38（椰子挂图）→ **v39（引用规范化，当前）**。",
    "版本演进：v37（20261027 七项优化前）→ v38（椰子挂图）→ v39（引用规范化）→ v40-v48（生日功能分批实现+生日数据查证合并）→ **v49（生日功能收尾，当前）**。")

# 3) 功能清单：追加生日功能
rep("""- 图片保存菜单：右键/长按弹菜单下载原图""",
    """- 图片保存菜单：右键/长按弹菜单下载原图
- **生日功能（v40 起）**：birth 字段（M-D 格式）；🎂 生日按钮（选最爱后、主题前）；生日横幅（tab 上方，只显示本月未过生日角色，今天生日置顶金色高亮，点击开弹窗）；生日弹窗（12 月份宫格 + 角色列表）；卡片生日栏 + 详情弹窗生日行（有 birth 才显示）；生日搜索（8月/8-13/0813/8月13日）；stats 行"已知生日 N 个"；添加/编辑表单生日输入（10-30 或 10月30日）""")

# 4) 删除纪律（.creative-design 已删，更新）
rep("- 删除纪律：只归档移动不物理删除（`.creative-design\\撤回错图\\` 是用户暂存区，别动）；确需删除先列清单，且仅限 git 已 commit 的文件。",
    "- 删除纪律：删除走**回收站**（可恢复），先自查被删文件是否被 index.html 引用（防裂图），确需删除先列清单。`.creative-design\\`（设计过程文件）已于 2026-10-30 清理删除。")

# 5) 待办：清理过时项
rep("""- 手机端 content-visibility 滚动手感建议真机复验（contain-intrinsic-size 356px 如有跳动可调准）。
- `.creative-design\\撤回错图\\` 累积 16 张撤下图（12 错图 + 椰子相关 4 张），由用户自行处置。
- 引用规范化保留未改：角色id_N（4_1.jpg）、日期主题名（230801-wolf-01）、05_角色名 等有语义名——用户如要求统一再处理。""",
    """- 手机端 content-visibility 滚动手感建议真机复验（contain-intrinsic-size 356px 如有跳动可调准）。
- 引用规范化保留未改：角色id_N（4_1.jpg）、日期主题名（230801-wolf-01）、05_角色名 等有语义名——用户如要求统一再处理。
- 生日数据：现有已知生日角色约 60+（以 stats"已知生日 N 个"为准），部分出处带"？"的角色生日在待确认清单，未查证到的不写 birth 字段。""")

p.write_text(text, encoding="utf-8", newline="")
print("=== 全部完成 ===")
