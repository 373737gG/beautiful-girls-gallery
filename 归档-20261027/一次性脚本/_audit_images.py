# -*- coding: utf-8 -*-
import io, re, os, subprocess

s = io.open('index.html', encoding='utf-8').read()
refs = set()
for m in re.finditer(r'images:\[(.*?)\]', s):
    for t in re.findall(r'"([^"]+)"', m.group(1)):
        if t:
            refs.add(t.replace('\\', '/'))

out = subprocess.run(['git', '-c', 'core.quotepath=false', 'ls-files', 'images'],
                     capture_output=True, text=True).stdout
tracked = set(out.splitlines())

st = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--porcelain', '--', 'images'],
                    capture_output=True, text=True).stdout
deleted = [l[3:].strip().strip('"') for l in st.splitlines() if l.startswith(' D')]
untracked = [l[3:].strip().strip('"') for l in st.splitlines() if l.startswith('??')]

missing_disk = sorted(r for r in refs if not os.path.exists(os.path.join('images', r.replace('/', os.sep))))
ref_untracked = sorted(r for r in refs if 'images/' + r not in tracked)

print('数据引用图片:', len(refs))
print('git已跟踪图片:', len(tracked))
print('磁盘上被删除(git视角):', len(deleted))
print('未跟踪新文件:', len(untracked))
print('引用了但磁盘缺失:', len(missing_disk), missing_disk[:10])
print('引用了但git未跟踪:', len(ref_untracked), ref_untracked[:10])
