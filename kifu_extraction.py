import re

trans1 = ['１', '２', '３', '４', '５', '６', '７', '８', '９']
trans2 = ['一', '二', '三', '四', '五', '六', '七', '八', '九']

with open('shogigui.kif', 'r') as f:
    kifu = f.read()

for x in range(9):
    kifu = kifu.replace(trans1[x], str(x+1))
    kifu = kifu.replace(trans2[x], str(x+1))

kifu = kifu.replace('\u3000', '')

sashite = [x.groups(1)[0] 
    for x in re.finditer('^\s*[0-9]+\s+(\S+).*$', 
    kifu, 
    flags=re.MULTILINE)]

for x in range(1, len(sashite)):
    if ('同' in sashite[x]):
        sashite[x] = sashite[x].replace('同', sashite[x-1][:2])

if ('投了' in sashite):
    sashite.remove('投了')

print('\n'.join(sashite))