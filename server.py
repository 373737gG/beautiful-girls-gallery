# -*- coding: utf-8 -*-
"""美少女图鉴本地服务器 - 双击启动后自动打开浏览器"""
import http.server
import socketserver
import json
import os
import re
import urllib.parse

PORT = 8899
DIR = os.path.dirname(os.path.abspath(__file__))

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
                elif field_name == 'image':
                    image_data = content
            
            if image_data and filename:
                # 安全处理文件名和种族名
                filename = os.path.basename(filename)
                race = os.path.basename(race)
                
                img_dir = os.path.join(DIR, 'images', race)
                os.makedirs(img_dir, exist_ok=True)
                
                # 避免重名
                base, ext = os.path.splitext(filename)
                save_path = os.path.join(img_dir, filename)
                i = 1
                while os.path.exists(save_path):
                    save_path = os.path.join(img_dir, f"{base}_{i}{ext}")
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
    # 自动打开浏览器
    import webbrowser
    webbrowser.open(f'http://localhost:{PORT}/index.html')
    with Server(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
