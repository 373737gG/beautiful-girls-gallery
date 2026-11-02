# -*- coding: utf-8 -*-
"""一次性：清杂收尾（容错版）——send2trash 删完误报 WinError2，逐个尝试+核验"""
import os
import glob
from send2trash import send2trash

DIR = r'D:\zhumian\工作区\项目归档\美少女图鉴'

def clean(path):
    """尝试送回收站，按实际存在性判定结果"""
    name = os.path.basename(path) + ('/' if os.path.isdir(path) else '')
    try:
        send2trash(path)
    except OSError as e:
        if os.path.exists(path):
            print('  FAIL(仍存在)', name, '->', e)
            return False
        print('  OK(报错但已删)', name)
        return True
    if os.path.exists(path):
        print('  FAIL(调用成功但仍存在)', name)
        return False
    print('  OK', name)
    return True

ok = True
for p in sorted(glob.glob(os.path.join(DIR, 'index.html.bak-*'))):
    ok = clean(p) and ok
for name in ('__pycache__', '_cand'):
    p = os.path.join(DIR, name)
    if os.path.isdir(p):
        ok = clean(p) and ok

print('--- 最终核验 ---')
print('bak 剩余:', len(glob.glob(os.path.join(DIR, 'index.html.bak-*'))))
print('__pycache__ 剩余:', os.path.isdir(os.path.join(DIR, '__pycache__')))
print('_cand 剩余:', os.path.isdir(os.path.join(DIR, '_cand')))
print('index.html 在:', os.path.isfile(os.path.join(DIR, 'index.html')))
print('server.py 在:', os.path.isfile(os.path.join(DIR, 'server.py')))
print('RESULT:', 'ALL DONE' if ok else 'HAS FAILURES')
