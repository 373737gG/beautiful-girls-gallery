# -*- coding: utf-8 -*-
"""更新音乐播放清单：扫描 assets/music/ 下的音频文件 → 生成 playlist.json
（线上 GitHub Pages 无法扫目录，靠这份清单显示音乐按钮；本地服务器不受影响）
用法：往 assets/music/ 加完歌后，双击或 python 运行本脚本，然后执行「同步到网站.bat」即可。
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.join(HERE, '..', 'assets', 'music')
EXTS = ('.mp3', '.ogg', '.wav', '.m4a', '.flac')

files = sorted(fn for fn in os.listdir(MUSIC)
               if os.path.isfile(os.path.join(MUSIC, fn))
               and fn.lower().endswith(EXTS) and not fn.startswith('_'))
out = os.path.join(MUSIC, 'playlist.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(files, f, ensure_ascii=False, indent=1)
print(f'playlist.json 已更新：{len(files)} 首')
for fn in files:
    print('  ·', fn)
