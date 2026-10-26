# 美少女图鉴 · Agent 编辑使用教程

> 写给后续接手编辑本项目的 AI Agent。2026-10-26 实测总结，全部为本日踩坑实录。
> 项目路径：`D:\zhumian\工作区\项目归档\美少女图鉴\`
> 前置阅读：`D:\zhumian\工作区\经验资料\通用经验\静态图鉴HTML数据项目-通用经验.md`（通用坑）
> 以及本目录 `交接任务书-v2.md`（任务背景）

---

## 一、项目结构（30秒速览）

```
美少女图鉴/
├─ index.html          # 核心：单文件应用（UI+CSS+JS+DEFAULT_DATA 数据全在一个文件）
├─ server.py           # 本地服务器，端口 8899，提供 /save /upload /delete /orphans 接口
├─ 启动图鉴.bat         # 双击启动 server.py 并自动开浏览器
├─ 同步到网站.bat       # 部署 GitHub Pages（github.com/373737gG/beautiful-girls-gallery）
├─ images/             # 角色图片，按种族分子目录（龙族/吸血鬼/机娘/魔女/其他）
├─ 工具脚本/            # 历史一次性脚本（迁移/清理用），文件名引用已统一为 index.html
├─ 交接任务书-v2.md     # 本轮交接任务
└─ *.bak-*             # 历次修改的备份（改文件前必须先做备份，命名：xxx.bak-YYYYMMDD-用途）
```

**部署形态有两套，内容同源：**
- 本地：`http://localhost:8899/index.html`（服务器模式，可写回数据）
- 线上：GitHub Pages（只读，无 /save）

---

## 二、最重要的机制：DEFAULT_DATA + localStorage + DATA_VERSION ⭐⭐⭐

页面加载数据的顺序（index.html 内）：

```js
const DATA_VERSION = '20261026-v24';
if(localStorage.getItem('dg_version') !== DATA_VERSION){
  localStorage.removeItem('dg_data');          // 版本变了→清缓存
  localStorage.setItem('dg_version', DATA_VERSION);
}
let data = JSON.parse(localStorage.getItem('dg_data') || 'null') || DEFAULT_DATA;
```

**由此推出三条铁律：**

1. **改了 DEFAULT_DATA（或让 /save 写回了新数据）之后，必须同步升 DATA_VERSION**，否则所有看过旧版的浏览器继续显示 localStorage 里的旧数据——表现为"文件里 233 人，页面显示 230 人"这种灵异现象（2026-10-26 实际发生）。
2. 升版本的副作用：**收藏、页面里自改的角色信息会重置为文件内容**（dg_history 最近浏览不受影响）。这是设计如此，不是 bug，但要提前告知用户。
3. localStorage 按 origin 隔离：localhost:8899 和 file://（直接双击 index.html）是**两份不同的缓存**，所以两种打开方式人数可能不一样——先怀疑缓存，再怀疑文件。

---

## 三、"龙族"人数对不上？先分清 race 和 type ⭐⭐⭐

页面种族 Tab 按 **race 字段**统计：`getRace(c) = c.race || '龙族'`（**缺省=龙族**）。

- 文件里**没有任何一条显式 `race:"龙族"`**——69+ 条无 race 字段的角色全部默认计入龙族
- `type` 是另一个维度（如 type:"龙娘" 是龙族种族下的类型；还有"龙之巫女""真龙"等）
- 所以：数 `race:"龙族"` = 0，数 `type:"龙娘"` ≈ 58，页面龙族 Tab ≈ 72——三个数字都不相等，**都对**
- 新增种族（兽耳娘/精灵）已在 `RACE_ORDER` 常量里常驻显示，细分标签（狐/猫/犬/狼、约会大作战）在 `SUBTYPES` 常量里，匹配逻辑 `matchSubType()` 按 type→tags→source 三层兜底
- 编辑表单的种族下拉列表在 `openEdit()` 里，加新种族要同步改那里

---

## 四、server.py 的接口与注意事项

| 接口 | 说明 |
|---|---|
| `/save` (POST JSON数组) | 把整个 data 数组写回 index.html 的 DEFAULT_DATA 块（括号配对定位，与布局无关） |
| `/upload` (multipart) | 图片存入 `images/{race}/`，返回相对路径 |
| `/delete/文件名` (DELETE) | 按文件名在 images/ 下递归查找删除 |
| `/orphans` (GET) | 列出磁盘有但数据未引用的孤儿图，供前端"清理孤儿图"按钮用 |

**要点：**
- 文件名引用必须是 `index.html`（4 处：/orphans、/save、启动提示、webbrowser.open）。历史上曾改名过，改名/改引用后要全局 grep 一遍
- 服务器是 ThreadingHTTPServer + allow_reuse_address——**Windows 下 SO_REUSEADDR 允许双绑定不报错**。如果测试时接口行为诡异（比如报错内容是旧代码的），先 `netstat -ano | findstr 8899` 查是不是有旧进程占着端口，有就杀掉
- `/save` 写回是**全量替换** DEFAULT_DATA 块：浏览器里的 data 是什么，文件就变成什么。测试接口后要么还原文件，要么升版本号
- 排查接口一律实测：起服务 → curl/urllib 请求 → 看响应体。报错信息在 500 的 JSON body 里（`{"ok":false,"error":...}`）

---

## 五、改代码的标准流程（Checklist）

1. **备份**：`index.html` → `index.html.bak-YYYYMMDD-用途`（用 Python shutil，别用 Git Bash mv 传中文）
2. **改前摸底**：先 grep 确认要改的锚点唯一；数据块每角色一行，别动 `DEFAULT_DATA = [` 到 `];` 之外的代码
3. **改完**：升 DATA_VERSION（若动了数据或想让用户端生效）
4. **验证**（三层，按需选做）：
   - 语法：提取 `<script>` 内容用 `node --check` 验 JS；`py_compile` 验 Python
   - 逻辑：jsdom 冒烟测试（装在 `C:\Users\Chong\.workbuddy\binaries\node\workspace\node_modules`），加载整个 HTML 跑断言
   - 接口：临时起 server 实测 /save /orphans，**测完把 index.html 字节级还原**（sha256 对比）
5. **git commit**（用户习惯 commit message 为"更新图鉴"）

---

## 六、当前功能清单（改代码别把这些弄坏）

- 列表：分页加载（首屏16，IntersectionObserver rootMargin 600px，搜索/筛选重置分页）
- 收藏：**原地更新星标**（toggleStar 不再整页 render，避免分页重置跳顶）；按收藏排序只在改排序时生效
- 拼图：顶部固定栏；两级选择（角色封面+右上角数字badge → 点进去选外观）；canvas 自动 cover 裁剪 + 拖动/滚轮微调；最多9张
- 分类：固定种族顺序 RACE_ORDER = 龙族/吸血鬼/机娘/魔女/兽耳娘/精灵；兽耳娘有狐/猫/犬/狼细分行，精灵有"约会大作战"细分
- 其他：轮播（封面/全部图两种模式）、随机、导入导出JSON、背景音乐（扫 assets/music/ 目录）、手机端滚动隐藏顶栏、右键/长按保存图片

---

## 七、工具链的坑（本日实测）

- **Git Bash 内联 python -c 传中文/引号必炸**：`race:\"...\"` 这类写进 bash 双引号会被改写。**一律写成 .py 脚本文件再执行**，别赌内联
- Git Bash `mv` 中文文件名会 GBK 乱码：改名用 Python `os.rename`
- Python 文本模式写文件 `\n` → `\r\n`（Windows），断言行尾时注意
- 读完文件再写回会丢 BOM/换行风格，正式文件改完要 sha256 与预期比对
- Python `print` 中文在 GBK 控制台乱码 ≠ 数据坏了：用 `ascii(name)` 转义输出核验真实内容
- jsdom 测试注意：`let` 声明的变量不挂 window（用 `window.eval()` 读内部状态）；IntersectionObserver 要打桩；每次 render 都会 new 观察器实例
- 测试会弹浏览器的代码（webbrowser.open）：用 `importlib` 导入 server.py（`__name__ != '__main__'`）自己起线程，不要直接跑 `__main__`

---

## 八、备份与版本记录

- `index.html.bak-20261026-分页拼图分类`：v23 改造前（分页/拼图两级/新分类 改动前）
- `server.py.bak-20261026-文件名修复`：文件名修复前（还引用 美少女图鉴.html 的版本）
- DATA_VERSION 演进：v22 → v23（2026-10-26 上午，分页/拼图/分类改造）→ v24（2026-10-26 傍晚，数据更新到233人后强制清缓存）

---

*最后提醒：任何"页面和文件对不上"的问题，九成是 localStorage 缓存——先升 DATA_VERSION，再查别的。*
