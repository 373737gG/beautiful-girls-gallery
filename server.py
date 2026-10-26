# -*- coding: utf-8 -*-
"""美少女图鉴本地服务器 - 双击启动后自动打开浏览器"""
import http.server
import socketserver
import json
import os
import re
import time
import urllib.parse
from datetime import datetime

PORT = 8899
DIR = os.path.dirname(os.path.abspath(__file__))

def parse_default_data(text):
    """从 index.html 文本中解析 DEFAULT_DATA 数组为 Python list（括号配对定位，与布局无关）。
    解析失败抛异常。仅供 /selfcheck 只读核对使用，不修改任何文件。"""
    start_m = re.search(r'const\s+DEFAULT_DATA\s*=\s*\[', text)
    if not start_m:
        raise ValueError('未找到 DEFAULT_DATA 数据块开头')
    depth = 0; in_str = False; esc = False; end_idx = -1
    i = start_m.end() - 1  # '[' 位置
    while i < len(text):
        ch = text[i]
        if in_str:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': in_str = False
        else:
            if ch == '"': in_str = True
            elif ch == '[': depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    end_idx = i; break
        i += 1
    if end_idx < 0:
        raise ValueError('未找到 DEFAULT_DATA 数据块结尾')
    block = text[start_m.end():end_idx]
    # 按顶层大括号逐条切出对象字面量（字符串感知）
    entries = []; buf = []; d = 0; in_str = False; esc = False
    for ch in block:
        if in_str:
            buf.append(ch)
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': in_str = False
        else:
            if ch == '"': in_str = True; buf.append(ch)
            elif ch == '{':
                d += 1
                if d == 1: buf = []
                else: buf.append(ch)
            elif ch == '}':
                d -= 1
                if d == 0: entries.append('{' + ''.join(buf) + '}')
                else: buf.append(ch)
            elif d > 0:
                buf.append(ch)
    data = []
    for js in entries:
        js2 = re.sub(r'([{,])([A-Za-z_][A-Za-z0-9_]*):', r'\1"\2":', js)
        data.append(json.loads(js2))
    return data

# 线程版服务器：浏览器会保持空闲预连接，单线程版会被卡死不再响应
class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        # 列出未被数据引用的孤儿图片，供前端「清理孤儿图」按钮使用
        if self.path == '/orphans':
            try:
                html_path = os.path.join(DIR, 'index.html')
                with open(html_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                referenced = set()
                for block in re.findall(r'images:\[([^\]]*)\]', text):
                    for item in re.findall(r'"([^"]*)"', block):
                        referenced.add(item)
                orphans = []
                img_root = os.path.join(DIR, 'images')
                for root, dirs, files in os.walk(img_root):
                    for fn in files:
                        if fn.startswith('_'):
                            continue
                        rel = os.path.relpath(os.path.join(root, fn), img_root).replace(os.sep, '/')
                        if rel not in referenced:
                            orphans.append(rel)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'orphans': orphans}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8'))
            return
        return super().do_GET()

    def do_POST(self):
        # 自动保存数据到HTML文件
        if self.path == '/save':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
                if not isinstance(data, list):
                    raise ValueError('数据必须是数组')

                html_path = os.path.join(DIR, 'index.html')
                with open(html_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                def to_js_str(s):
                    return (s.replace('\\', '\\\\').replace('"', '\\"')
                             .replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t'))

                def to_js_obj(obj):
                    items = []
                    for k, v in obj.items():
                        if isinstance(v, str):
                            items.append(f'{k}:"{to_js_str(v)}"')
                        elif isinstance(v, list):
                            arr = ','.join(f'"{to_js_str(x)}"' if isinstance(x, str) else str(x) for x in v)
                            items.append(f'{k}:[{arr}]')
                        elif isinstance(v, bool):
                            items.append(f'{k}:{"true" if v else "false"}')
                        elif v is None:
                            items.append(f'{k}:null')
                        else:
                            items.append(f'{k}:{v}')
                    return '{' + ','.join(items) + '}'

                new_block = ('const DEFAULT_DATA = [\n'
                             + ''.join(to_js_obj(c) + ',\n' for c in data)
                             + ']')
                # 用括号配对+字符串状态扫描定位数据块结尾，
                # 兼容"行内 }];"与"独立 ]; 行"两种布局
                start_m = re.search(r'const\s+DEFAULT_DATA\s*=\s*\[', text)
                if not start_m:
                    raise ValueError('未找到 DEFAULT_DATA 数据块开头')
                depth = 0
                in_str = False
                esc = False
                end_idx = -1
                i = start_m.end() - 1  # '[' 位置
                while i < len(text):
                    ch = text[i]
                    if in_str:
                        if esc:
                            esc = False
                        elif ch == '\\':
                            esc = True
                        elif ch == '"':
                            in_str = False
                    else:
                        if ch == '"':
                            in_str = True
                        elif ch == '[':
                            depth += 1
                        elif ch == ']':
                            depth -= 1
                            if depth == 0:
                                end_idx = i
                                break
                    i += 1
                if end_idx < 0:
                    raise ValueError('未找到 DEFAULT_DATA 数据块结尾')
                new_text = text[:start_m.start()] + new_block + text[end_idx + 1:]

                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(new_text)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8'))
            return
        
        # 保存自检（只读核对，不修改任何文件）：
        # 核对 页面数据(前端POST) ↔ index.html 实际内容 ↔ 磁盘 images 三方一致性
        if self.path == '/selfcheck':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                page_data = json.loads(body.decode('utf-8'))
                if not isinstance(page_data, list):
                    raise ValueError('页面数据必须是数组')

                html_path = os.path.join(DIR, 'index.html')
                with open(html_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                file_data = parse_default_data(text)

                FIELD_MAP = [
                    ('name', '角色名'), ('race', '种族'), ('source', '出处'), ('type', '类型'),
                    ('cv', 'CV'), ('desc', '设定'), ('story', '剧情'), ('tags', '标签'), ('images', '图片'),
                ]
                issues = []
                page_map = {}
                for c in page_data:
                    if isinstance(c, dict) and isinstance(c.get('id'), int):
                        page_map[c['id']] = c
                file_map = {}
                for c in file_data:
                    if isinstance(c, dict) and isinstance(c.get('id'), int):
                        file_map[c['id']] = c

                # 一、页面 ↔ index.html 逐角色核对
                for cid, c in sorted(page_map.items()):
                    pname = c.get('name') or f'id:{cid}'
                    if cid not in file_map:
                        issues.append(f'[未保存] 角色「{pname}」(id:{cid}) 只存在于页面数据，index.html 中没有——点保存后才会写入文件')
                        continue
                    fc = file_map[cid]
                    for key, label in FIELD_MAP:
                        pv = c.get(key) if c.get(key) not in ('', None) else None
                        fv = fc.get(key) if fc.get(key) not in ('', None) else None
                        if isinstance(pv, list): pv = sorted(pv) or None
                        if isinstance(fv, list): fv = sorted(fv) or None
                        if pv != fv:
                            issues.append(f'[字段不一致] 「{pname}」(id:{cid}) 的{label}与 index.html 中不同——页面改动可能未保存成功')
                for cid, fc in sorted(file_map.items()):
                    if cid not in page_map:
                        issues.append(f'[页面已删] 角色「{fc.get("name")}」(id:{cid}) 在 index.html 中存在，但页面数据里没有——页面删除可能未保存成功')

                # 二、图片三方核对（页面引用 / 文件引用 / 磁盘文件）
                def collect_refs(lst):
                    refs = {}
                    for c in lst:
                        if not isinstance(c, dict): continue
                        for p in (c.get('images') or []):
                            if not isinstance(p, str) or not p.strip(): continue
                            p = p.strip()
                            if p.startswith('http') or p.startswith('data:'): continue
                            refs.setdefault(p.replace('\\', '/'), []).append(c.get('name') or f"id:{c.get('id')}")
                    return refs
                page_refs = collect_refs(page_data)
                file_refs = collect_refs(file_data)
                disk = set()
                img_root = os.path.join(DIR, 'images')
                for root, dirs, files in os.walk(img_root):
                    for fn in files:
                        if fn.startswith('_'): continue
                        disk.add(os.path.relpath(os.path.join(root, fn), img_root).replace(os.sep, '/'))

                for p in sorted(set(page_refs) | set(file_refs)):
                    if p not in disk:
                        who = page_refs.get(p) or file_refs.get(p) or []
                        issues.append(f'[图片缺失] {p} 被引用（{("、".join(who[:3]))}）但磁盘上不存在——图被移动/删除或引用写错')
                for p in sorted(disk - set(page_refs) - set(file_refs)):
                    issues.append(f'[孤儿图片] {p} 磁盘上存在但页面和 index.html 都没有引用')
                for p in sorted(set(page_refs) - set(file_refs)):
                    issues.append(f'[未保存引用] {p} 只在页面数据中，尚未写入 index.html——点保存后生效')
                for p in sorted(set(file_refs) - set(page_refs)):
                    issues.append(f'[引用已删] {p} 在 index.html 中有引用，但页面数据里已删除——页面改动可能未保存成功')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'issues': issues}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}, ensure_ascii=False).encode('utf-8'))
            return

        if self.path == '/upload':
            content_type = self.headers.get('Content-Type', '')
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # 解析multipart/form-data
            boundary_match = re.search(r'boundary=([^\s;]+)', content_type)
            if not boundary_match:
                self.send_error(400, 'No boundary')
                return
            boundary = boundary_match.group(1).encode()
            
            # 分割body
            parts = body.split(b'--' + boundary)
            
            filename = 'upload.jpg'
            race = '其他'
            charname = ''
            image_data = None

            for part in parts:
                if not part or part == b'--' or part == b'--\r\n' or part == b'\r\n':
                    continue
                # 去掉开头的\r\n
                if part.startswith(b'\r\n'):
                    part = part[2:]
                if part.endswith(b'\r\n'):
                    part = part[:-2]

                # 分离头部和内容
                header_end = part.find(b'\r\n\r\n')
                if header_end == -1:
                    continue
                headers = part[:header_end].decode('utf-8', errors='ignore')
                content = part[header_end+4:]

                # 找字段名
                name_match = re.search(r'name="([^"]+)"', headers)
                if not name_match:
                    continue
                field_name = name_match.group(1)

                if field_name == 'filename':
                    filename = content.decode('utf-8', errors='ignore').strip()
                elif field_name == 'race':
                    race = content.decode('utf-8', errors='ignore').strip()
                elif field_name == 'charname':
                    charname = content.decode('utf-8', errors='ignore').strip()
                elif field_name == 'image':
                    image_data = content

            if image_data and filename:
                # 安全处理文件名和种族名
                filename = os.path.basename(filename)
                race = os.path.basename(race)

                img_dir = os.path.join(DIR, 'images', race)
                os.makedirs(img_dir, exist_ok=True)

                # ===== 文件名强化：唯一 + 可追溯，杜绝 images_N.jpg 这类默认流水名 =====
                # 浏览器默认流水名/无意义名（保存网页图时最常见的 sources），一律改用生成名
                _GENERIC = re.compile(r'^(images?|photo|img|download|下载|下载 \(|未命名|截图|屏幕截图|\d+)$', re.I)
                base_orig, ext = os.path.splitext(filename)
                ext = ext.lower()
                if ext not in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.avif'):
                    ext = '.jpg'  # 无扩展名/异常扩展名兜底（浏览器上传的图片几乎都带扩展名）
                stem_ok = bool(base_orig) and not _GENERIC.match(base_orig)
                if charname:
                    # 有角色名：以「角色名_时间戳」为基底，同一角色同一秒传多张靠序号区分
                    stem = re.sub(r'[\\/:*?"<>|\s~]+', '_', charname)[:40] or 'img'
                    stem = f'{stem}_{datetime.now():%Y%m%d_%H%M%S}'
                elif stem_ok:
                    # 保留了有意义的原始文件名（可追溯）
                    stem = re.sub(r'[\\/:*?"<>|\s~]+', '_', base_orig)[:60]
                else:
                    stem = f'img_{datetime.now():%Y%m%d_%H%M%S}'
                save_path = os.path.join(img_dir, stem + ext)
                i = 1
                while os.path.exists(save_path):
                    save_path = os.path.join(img_dir, f'{stem}_{i}{ext}')
                    i += 1

                with open(save_path, 'wb') as f:
                    f.write(image_data)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                rel_path = f"{race}/{os.path.basename(save_path)}"
                self.wfile.write(json.dumps({'ok': True, 'filename': rel_path}).encode())
                return

        self.send_response(400)
        self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/delete/'):
            rel_path = urllib.parse.unquote(self.path[len('/delete/'):])
            # 防止路径穿越
            rel_path = os.path.basename(rel_path)
            img_dir = os.path.join(DIR, 'images')
            # 递归查找文件
            for root, dirs, files in os.walk(img_dir):
                if rel_path in files:
                    file_path = os.path.join(root, rel_path)
                    try:
                        os.remove(file_path)
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"ok":true}')
                        return
                    except:
                        pass
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # 静默默认日志

if __name__ == '__main__':
    os.chdir(DIR)
    print(f"美少女图鉴服务器启动中...")
    print(f"打开浏览器访问: http://localhost:{PORT}/index.html")
    print(f"按 Ctrl+C 停止")
    # 先绑定端口就绪，再打开浏览器：避免浏览器抢先访问时出现"无法访问/拒绝连接"
    httpd = None
    for attempt in range(3):
        try:
            httpd = Server(("", PORT), Handler)
            break
        except OSError:
            if attempt == 2:
                raise
            print(f"端口 {PORT} 暂时不可用，1 秒后重试…")
            time.sleep(1)
    print(f"服务器已就绪，即将自动打开浏览器")
    # 延迟半秒开浏览器，确保监听完全就绪
    import webbrowser
    import threading
    threading.Timer(0.5, lambda: webbrowser.open(f'http://localhost:{PORT}/index.html')).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
