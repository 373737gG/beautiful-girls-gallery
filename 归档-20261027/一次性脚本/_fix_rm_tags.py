# -*- coding: utf-8 -*-
import io, re, sys

p = 'index.html'
s = io.open(p, encoding='utf-8', newline='').read()

# 只替换序号式人偶标签，其余标签不动
s2, n1 = re.subn(r'"第[一二三四五六七]人偶"', '"人偶"', s)
s2, n2 = re.subn(r'"伪第七人偶"', '"人偶"', s2)
print('replaced:', n1, '+', n2)

if len(sys.argv) > 1 and sys.argv[1] == 'apply':
    assert "DATA_VERSION = '20261027-v33'" in s2
    s2 = s2.replace("DATA_VERSION = '20261027-v33'", "DATA_VERSION = '20261027-v34'")
    io.open(p, 'w', encoding='utf-8', newline='').write(s2)
    # 复验
    s3 = io.open(p, encoding='utf-8').read()
    assert '第' + '一人偶' not in s3 and '伪第七人偶' not in s3
    for l in re.split(r'\r?\n', s3):
        if l.startswith('{id:') and any(l.startswith('{id:%d,' % i) for i in range(261, 268)):
            print(re.search(r'name:"([^"]+)"', l).group(1), '->', re.search(r'tags:\[(.*?)\]', l).group(1))
    print('APPLIED, v34')
else:
    print('(dry-run)')
