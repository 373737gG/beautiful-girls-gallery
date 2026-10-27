# -*- coding: utf-8 -*-
"""
美少女图鉴 · 接图助手
用途：把图片文件手动复制进 images/种族目录/ 之后，跑一次本脚本：
  1. 找出所有「磁盘有、但没被任何角色引用」的图（孤儿图）
  2. 逐张询问归属角色（回车=跳过这张）
  3. 自动重命名为「角色名_序号.原扩展名」，并把引用追加进 index.html
  4. 自动升级 DATA_VERSION（+1），浏览器下次打开自动生效
安全：只改名、只追加引用，不删除任何文件；改 index.html 前自动备份。
用法：双击运行，或命令行 python 接图助手.py
"""
import json, os, re, shutil, sys, time

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(PROJ, 'index.html')
IMG_ROOT = os.path.join(PROJ, 'images')

def main():
    # ---------- 读 index.html ----------
    with open(HTML, 'r', encoding='utf-8') as f:
        text = f.read()
    ver_m = re.search(r"const DATA_VERSION = '(\d{8})-v(\d+)'", text)
    if not ver_m:
        print('未找到 DATA_VERSION，退出'); return

    # ---------- 引用集合 ----------
    referenced = set()
    for block in re.findall(r'images:\[([^\]]*)\]', text):
        for item in re.findall(r'"([^"]*)"', block):
            referenced.add(item.replace('\\', '/'))

    # ---------- 扫描孤儿图（按目录分组）----------
    orphans = []   # (rel_path, dir_name, filename)
    for root, dirs, files in os.walk(IMG_ROOT):
        for fn in sorted(files):
            if fn.startswith('_'):
                continue
            rel = os.path.relpath(os.path.join(root, fn), IMG_ROOT).replace(os.sep, '/')
            if rel not in referenced:
                orphans.append((rel, os.path.basename(root), fn))
    if not orphans:
        print('没有发现待接入的图片（所有图片都已被引用），无需处理。')
        return

    # ---------- 各目录下的角色清单（用于提示） ----------
    chars_by_dir = {}
    for m in re.finditer(r'\{id:\d+,name:"([^"]*)"[^{}]*?images:\[', text):
        pass  # 角色所属目录以其 images 引用的第一段为准，下面从引用反查
    dir_chars = {}
    for m in re.finditer(r'\{id:\d+,name:"([^"]*)"[^{}]*?images:\[([^\]]*)\]', text):
        for p in re.findall(r'"([^"]*)"', m.group(2)):
            d = p.split('/')[0] if '/' in p else ''
            dir_chars.setdefault(d, set()).add(m.group(1))
            break

    print(f'\n发现 {len(orphans)} 张未被引用的图片：\n')
    changes = []   # (old_rel, new_rel, char_name)
    for rel, d, fn in orphans:
        hint = ''
        if d in dir_chars and dir_chars[d]:
            hint = '（本目录角色：' + '、'.join(sorted(dir_chars[d])[:8]) + '）'
        print(f'  [{d}] {fn}')
        print(f'      这张图是谁的？输入角色名后回车{hint}；直接回车=跳过；输入 q 结束：')
        ans = input('      > ').strip()
        if ans.lower() == 'q':
            break
        if not ans:
            print('      已跳过\n')
            continue
        changes.append((rel, d, fn, ans))
        print(f'      -> 将改名为 {ans}_N 并接入引用\n')

    if not changes:
        print('没有需要处理的图片，退出。')
        return

    # ---------- 备份 ----------
    stamp = time.strftime('%Y%m%d')
    bak = os.path.join(PROJ, f'index.html.bak-{stamp}-接图助手')
    if not os.path.exists(bak):
        shutil.copy2(HTML, bak)
        print(f'\n已备份 index.html -> {os.path.basename(bak)}')

    # ---------- 逐张改名 + 更新引用 ----------
    ok, fail = 0, 0
    for rel, d, fn, char in changes:
        ext = os.path.splitext(fn)[1].lower() or '.jpg'
        # 角色名安全化
        safe = re.sub(r'[\\/:*?"<>|\s]+', '_', char)[:40]
        # 序号 = 该角色已有引用数 + 1（全局找同名前缀避免重号）
        used = set()
        for block in re.findall(r'images:\[([^\]]*)\]', text):
            for item in re.findall(r'"([^"]*)"', block):
                base = item.rsplit('/', 1)[-1]
                m2 = re.match(rf'^{re.escape(safe)}_(\d+)$', base)
                if m2:
                    used.add(int(m2.group(1)))
        n = (max(used) + 1) if used else 1
        new_name = f'{safe}_{n}{ext}'
        new_rel = f'{d}/{new_name}' if d else new_name
        src = os.path.join(IMG_ROOT, rel.replace('/', os.sep))
        dst = os.path.join(IMG_ROOT, new_rel.replace('/', os.sep))
        if os.path.exists(dst):
            print(f'  跳过 {fn}：目标名 {new_name} 已存在')
            fail += 1
            continue
        # 1) 改名文件
        os.rename(src, dst)
        # 2) 追加引用：找到该角色那一行的 images 数组末尾插入
        char_m = re.search(rf'(\{{id:\d+,name:"{re.escape(char)}"[^{{}}]*?images:\[)([^\]]*)(\])', text)
        if not char_m:
            print(f'  警告：index.html 中找不到角色「{char}」的图片行，回滚改名')
            os.rename(dst, src)
            fail += 1
            continue
        inner = char_m.group(2).strip()
        add = f'"{new_rel}"'
        new_inner = (inner + ',' + add) if inner else add
        text = text[:char_m.start(2)] + new_inner + text[char_m.end(2):]
        print(f'  已接入：{fn} -> {new_rel}（{char}）')
        ok += 1

    if ok:
        # ---------- 升 DATA_VERSION ----------
        text = re.sub(r"const DATA_VERSION = '(\d{8})-v(\d+)'",
                      lambda m: f"const DATA_VERSION = '{m.group(1)}-v{int(m.group(2)) + 1}'", text)
        with open(HTML, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'\n完成：接入 {ok} 张，跳过/失败 {fail} 张。DATA_VERSION 已自动 +1（浏览器刷新后生效）。')
        print('提示：改完记得在页面上检查这几张图显示正常。')
    else:
        print('\n没有实际改动。')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n已中断，未完成的部分下次再跑即可。')
