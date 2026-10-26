# -*- coding: utf-8 -*-
import io, re

s = io.open('index.html', encoding='utf-8').read()
for l in re.split(r'\r?\n', s):
    if l.startswith('{id:'):
        n = re.match(r'\{id:(\d+)', l).group(1)
        if 230 <= int(n) <= 242:
            name = re.search(r'name:"([^"]+)"', l).group(1)
            if any(k in name for k in ('Gemini', 'Grok', 'Mistral', 'GLM', '鲸鱼', 'Claude', 'GPT')):
                story = re.search(r'story:"([^"]*)"', l)
                print('=== id', n, name)
                print('DESC:', re.search(r'desc:"([^"]*)"', l).group(1))
                print('STORY:', story.group(1) if story else '?')
                print()
