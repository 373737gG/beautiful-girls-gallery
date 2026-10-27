# 美少女图鉴 · Agent 编辑使用教程

> 写给后续接手编辑本项目的 AI Agent。2026-10-26 首版实测总结，2026-10-27 七项优化后全面更新。
> 项目路径：`D:\zhumian\工作区\项目归档\美少女图鉴\`
> 前置阅读：`D:\zhumian\工作区\经验资料\通用经验\静态图鉴HTML数据项目-通用经验.md`（通用坑）
> 历史任务书与报告已归档于 `归档-20261027\任务书与设定文档\`

---

## 一、项目结构（30秒速览）

```
美少女图鉴/
├─ index.html          # 核心：单文件应用（UI+CSS+JS+DEFAULT_DATA 数据全在一个文件）
├─ server.py           # 本地服务器，端口 8899，/save /upload /delete /orphans /selfcheck
├─ 启动图鉴.bat         # 双击启动 server.py 并自动开浏览器
├─ 同步到网站.bat       # 部署 GitHub Pages（github.com/373737gG/beautiful-girls-gallery）
├─ Agent编辑教程.md     # 本文档
├─ images/             # 角色图片，按种族子目录；文件名一律 角色名_N.扩展名
├─ 工具脚本/            # 正式工具（接图助手.py 等）
└─ 归档-20261027/       # 历史备份（仅最新2个）、一次性脚本、研究数据、任务书与设定文档
```

**部署形态两套，内容同源：**
- 本地：`http://localhost:8899/index.html`（服务器模式，可写回数据）
- 线上：GitHub Pages（只读，无 /save /upload /selfcheck）

---

## 二、数据机制：DEFAULT_DATA + localStorage + DATA_VERSION ⭐⭐⭐

```js
const DATA_VERSION = '20261027-v39';
if(localStorage.getItem('dg_version') !== DATA_VERSION){
  localStorage.removeItem('dg_data');   // 版本变了→清缓存
  localStorage.setItem('dg_version', DATA_VERSION);
}
let data = JSON.parse(localStorage.getItem('dg_data') || 'null') || DEFAULT_DATA;
```

**三条铁律：**
1. **改了 DEFAULT_DATA（或 /save 写回）后必须 +1 DATA_VERSION**，否则老浏览器显示 localStorage 旧数据（"文件里 281 人，页面显示 230"级灵异现象都先查这个）。
2. 升版本副作用：收藏、页面自改信息重置为文件内容；dg_history 最近浏览不受影响。提前告知用户。
3. localStorage 按 origin 隔离：localhost:8899 与 file:// 是两份缓存。

版本演进：v37（20261027 七项优化前）→ v38（椰子挂图）→ **v39（引用规范化，当前）**。

---

## 三、图片命名规范（2026-10-27 起，防串图的根本）⭐⭐⭐

**全部图片一律 `角色名_序号.扩展名`**（如 `赫萝_1.jpg`、`艾姬多娜_3.png`）。历史上 270 张默认名（images_N.jpg、32位hash、~tplv CDN 名）已于 v39 全部规范化。

**为什么必须这样**：早期 images_N.jpg 这类浏览器默认名导致同名覆盖/误删，是"图跳串""图消失"系列事故的物理根源（详见归档中的交接回执-v3 根因说明）。

**三条上传路径的行为：**
| 路径 | 文件名 | 说明 |
|---|---|---|
| 页面拖拽/上传按钮（服务器模式） | 自动 `角色名_时间戳` | /upload 带 charname，无需手动改名 ✅ 用户日常用这条 |
| 手动复制文件进 images\ 目录 | 需跑 `工具脚本\接图助手.py` | 交互输入角色名 → 自动改名+接引用+升版本 |
| AI 批量接图 | 锚点替换 images 字段 | 改名用 Python os.rename（勿用 Git Bash mv 传中文） |

---

## 四、server.py 接口（v39 现状）

| 接口 | 说明 |
|---|---|
| `/save` (POST JSON) | 全量替换 DEFAULT_DATA 块（括号配对定位）。**写回是全量的：浏览器 data 是什么文件就变什么**——外部编辑文件后必须让用户刷新页面（或升版本强制清缓存）再操作页面，否则旧数据覆盖回来 |
| `/upload` (multipart) | 字段：image/filename/race/**charname**。文件名自动 `角色名_YYYYMMDD_HHMMSS_序号`；浏览器默认流水名一律替换；扩展名白名单 |
| `/delete/相对路径` | **按完整相对路径精确删除**（2026-10-27 修复：旧版按文件名全局递归删，曾误删 02 的同名图）；仅文件名回退时要求唯一匹配，多处同名返回 409 拒删 |
| `/orphans` (GET) | 磁盘有但数据未引用的图 |
| `/selfcheck` (POST 页面data) | 保存自检（只读）：页面↔index.html 十字段逐角色核对 + 图片三方核对，返回 issues 数组 |

- 启动顺序：先绑端口（失败重试3次）→ 延迟 0.5s 再开浏览器（根治"拒绝连接"）。
- 排查接口实测：Windows 下 SO_REUSEADDR 允许双绑定不报错，行为诡异先 `netstat -ano | findstr 8899` 杀旧进程。
- 改 server.py 后必须重启 bat 才生效。

---

## 五、改代码标准流程

1. **备份**：index.html → `index.html.bak-YYYYMMDD-用途`。**约定：全项目只保留最新一份备份**（旧备份删除，git 历史里永久可查）。
2. **摸底**：grep 确认锚点唯一；数据块每角色一行，不动 `DEFAULT_DATA=[` 到 `];` 之外的代码。
3. **改完**：动数据必升 DATA_VERSION。
4. **验证**：
   - 语法：提取 `<script>` 用 `node --check`；server.py 用 py_compile。
   - 逻辑：jsdom 冒烟（桩：matchMedia/IntersectionObserver/fetch/scrollY 内联注入，runScripts:'dangerously'，let 变量才能用 window.eval 读）。
   - 引用审计：missing / orphans / shared 三零即健康（审计脚本思路见通用经验 §2.2 补丁后三查）。
   - 接口：临时起 server 实测，测完 sha256 比对还原。
5. **git commit**（message 惯例"更新图鉴"）。

---

## 六、当前功能清单（别弄坏）

- 列表：分页（首屏16，哨兵 IO 追加）；手机端卡片 content-visibility:auto（仅窄屏媒体查询，桌面零改动）
- 弹窗：滚动位置记忆（openModalTracked/restoreScroll，关闭后双 rAF 恢复；saveEdit/delChar 用 render(false) 保分页高度不跳顶）
- 收藏：原地更新；拼图：两级选择+canvas 裁剪；轮播/随机/导入导出/主题/快捷键/背景音乐
- 服务器专属按钮：「清理孤儿图」「✅ 确认已保存」（selfCheck），非服务器模式 display:none
- 首屏：render 双 rAF 延后执行（骨架先绘，减少白屏）
- 图片保存菜单：右键/长按弹菜单下载原图

---

## 七、工具链的坑（实测）

- Git Bash 内联 `python -c` 传中文/引号/反引号必炸——**一律写 .py 文件执行**；`mv` 中文文件名会 GBK 乱码，改名用 os.rename。
- Python 文本写文件 \n→\r\n；print 中文 GBK 控制台乱码≠数据坏，用 ascii() 核验真实内容。
- 单线程 http.server 会被浏览器空闲预连接饿死——保持 ThreadingHTTPServer。
- /save 全量写回 + 用户页面同时操作 = 覆盖冲突：外部改文件前让用户先停手，改完让用户刷新。
- PIL save() 异常会把目标截断为 0 字节：批量转格式前逐文件备份，转后 verify()。
- 删除纪律：只归档移动不物理删除（`.creative-design\撤回错图\` 是用户暂存区，别动）；确需删除先列清单，且仅限 git 已 commit 的文件。

---

## 八、待办与遗留（2026-10-27 交接时点）

- 手机端 content-visibility 滚动手感建议真机复验（contain-intrinsic-size 356px 如有跳动可调准）。
- `.creative-design\撤回错图\` 累积 16 张撤下图（12 错图 + 椰子相关 4 张），由用户自行处置。
- 引用规范化保留未改：角色id_N（4_1.jpg）、日期主题名（230801-wolf-01）、05_角色名 等有语义名——用户如要求统一再处理。

---

*最后提醒：任何"页面和文件对不上"的问题，九成是 localStorage 缓存——先升 DATA_VERSION，再查别的。图片问题先跑引用审计（missing/orphans/shared 三零即健康）。*
