# -*- coding: utf-8 -*-
"""一次性接口测试：GET/POST /tag-groups（临时端口，不弹浏览器，测完自清理）"""
import json
import os
import threading
import time
import urllib.request
import urllib.error

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import server  # 导入 Handler（__main__ 块不会执行）

PORT = 8137

class Quiet(server.Server):
    pass

httpd = Quiet(("", PORT), server.Handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
time.sleep(0.3)

BASE = f'http://127.0.0.1:{PORT}'
fails = []

def req(method, path, body=None, raw=False):
    r = urllib.request.Request(BASE + path, method=method)
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        r.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(r, data) as resp:
            b = resp.read()
            return resp.status, (b if raw else json.loads(b.decode('utf-8')))
    except urllib.error.HTTPError as e:
        b = e.read()
        try:
            return e.code, (b if raw else json.loads(b.decode('utf-8')))
        except Exception:
            return e.code, b

def check(cond, msg):
    print(('  PASS  ' if cond else '  FAIL  ') + msg)
    if not cond:
        fails.append(msg)

gf = os.path.join(server.DIR, 'tag-groups.json')
if os.path.exists(gf):
    os.rename(gf, gf + '.pretest')  # 已有配置则暂存，测完还原

try:
    # 1. 无文件 → 404
    st, j = req('GET', '/tag-groups')
    check(st == 404 and j.get('ok') is False, f'无配置文件 GET → 404 (实际 {st})')

    # 2. POST 合法配置 → ok，文件落盘
    cfg = {"外貌特征": ["萝莉", "金发"], "其他": []}
    st, j = req('POST', '/tag-groups', cfg)
    check(st == 200 and j.get('ok') is True, 'POST 合法配置 → ok')
    with open(gf, 'r', encoding='utf-8') as f:
        disk = json.load(f)
    check(disk == cfg, '写入 tag-groups.json 内容一致')
    check(open(gf, 'rb').read().decode('utf-8').find('萝莉') > 0, '中文未被转义（ensure_ascii=False）')

    # 3. GET 返回文件内容
    st, b = req('GET', '/tag-groups', raw=True)
    check(st == 200 and json.loads(b.decode('utf-8')) == cfg, 'GET 返回配置文件内容')

    # 4. POST 非法：组名>10字
    st, j = req('POST', '/tag-groups', {"超过十个字的组名是不允许的呀": []})
    check(st == 400 and 'ok' in j and j['ok'] is False, '组名>10字 → 400 拒绝')

    # 5. POST 非法：标签总数>200
    st, j = req('POST', '/tag-groups', {"组": [f"t{i}" for i in range(201)]})
    check(st == 400 and '200' in j.get('error', ''), '标签总数>200 → 400 拒绝')

    # 6. POST 非法：非对象
    st, j = req('POST', '/tag-groups', ["不是对象"])
    check(st == 400, '非 JSON 对象 → 400 拒绝')

    # 7. 页面可访问
    st, b = req('GET', '/index.html', raw=True)
    check(st == 200 and b'groupModal' in b, 'GET /index.html 正常且含分组管理弹窗')

    print('\n接口测试: ' + ('ALL PASS' if not fails else f'{len(fails)} FAIL'))
finally:
    httpd.shutdown()
    # 清理测试产物
    try:
        if os.path.exists(gf):
            os.remove(gf)
    except OSError:
        pass
    if os.path.exists(gf + '.pretest'):
        os.rename(gf + '.pretest', gf)
    print('清理完成，tag-groups.json 已还原为测试前状态')
