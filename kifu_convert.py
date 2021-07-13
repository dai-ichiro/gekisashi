import re
import collections
import glob, os

###########最初に設定しておくもの##################################
trans1 = ['１', '２', '３', '４', '５', '６', '７', '８', '９']
trans2 = ['一', '二', '三', '四', '五', '六', '七', '八', '九']

koma_moji = ['飛', '角', '金', '銀', '桂', '香', '歩']
koma_kigo = ['r', 'b', 'g', 's', 'n', 'l', 'p']

koma_kigo2 = [x.swapcase() for x in koma_kigo] + koma_kigo

def make_sfen(retu):    
    for i in range(9, 0, -1):
        retu = retu.replace('0'*i, str(i))
    return retu
#################################################################

files = glob.glob('kif/*.kif')
exit_kif_files = [os.path.splitext(os.path.basename(x))[0] for x in files]

files = glob.glob('sfen/*.sfen')
exit_sfen_files = [os.path.splitext(os.path.basename(x))[0] for x in files]

not_yet_files = list(set(exit_kif_files) - set(exit_sfen_files))

for each_file in not_yet_files:

    with open('kif/%s.kif'%each_file, 'r') as f:
        kifu = f.read()

    for x in range(9):
        kifu = kifu.replace(trans1[x], str(x+1))
        kifu = kifu.replace(trans2[x], str(x+1))

    kifu = kifu.replace('\u3000', '')

    m = re.search(r'^先手：.*$', kifu, flags = re.MULTILINE)
    sente = m.group()

    m = re.search(r'^後手：.*$', kifu, flags = re.MULTILINE)
    gote = m.group()

    m = re.finditer(r'^\s*[0-9]+\s+(\S+).*$', kifu, flags=re.MULTILINE)

    sashite = [x.groups()[0] for x in m]

    for x in range(1, len(sashite)):
        if ('同' in sashite[x]):
            sashite[x] = sashite[x].replace('同', sashite[x-1][:2])

    #SFENリスト
    sfen = []

    #持ち駒
    mochigoma = []

    #局面データをlistに変換
    kyokumen = 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL'
    sfen.append(kyokumen + ' ' + 'b' + ' ' + '-' + ' ' + '1')
    for i in range(1, 10):
        kyokumen = kyokumen.replace(str(i), '0'*i)
    kyokumen = [list(x) for x in kyokumen.split('/')]

    #駒を動かす
    for i, each_sashite in enumerate(sashite):

        if each_sashite == '投了':
            break

        if each_sashite[-1] != '打': #駒を動かすときの処理
            
            move = re.match(r'^(\d+)(\D+)\((\d+).*$', each_sashite).groups()

            after_x = 9 - int(move[0][0])
            after_y = int(move[0][1]) - 1 

            before_x = 9 - int(move[2][0])
            before_y = int(move[2][1]) - 1

            active_koma = kyokumen[before_y][before_x]
            
            #移動元は空きになる
            kyokumen[before_y][before_x] = '0'

            #「成」ならば「+」をつける
            if move[1][-1] == '成':
                active_koma = '+' + active_koma

            #移動先に駒があれば持ち駒とする
            #大文字、小文字は入れ替える必要がある
            if kyokumen[after_y][after_x] != '0':
                mochigoma.append(kyokumen[after_y][after_x][-1].swapcase())
            
            #移動先に駒をセットする
            kyokumen[after_y][after_x] = active_koma

        else: #駒を打つときの処理

            after_x = 9 - int(each_sashite[0])
            after_y = int(each_sashite[1]) -1

            active_koma = koma_kigo[koma_moji.index(each_sashite[2])]

            if i % 2 == 0: #先手が駒を打つ
                active_koma = active_koma.upper()

            kyokumen[after_y][after_x] = active_koma

            mochigoma.remove(active_koma)
        
        #SFENリストに保存    
        mochigoma_dict = collections.Counter(''.join(mochigoma))

        sfen_mochigoma = ''
        for x in koma_kigo2:
            if mochigoma_dict[x] == 1:
                sfen_mochigoma += x
            elif mochigoma_dict[x] > 1:
                sfen_mochigoma += (str(mochigoma_dict[x]) + x)
        
        if sfen_mochigoma =='':
            sfen_mochigoma = '-'

        sfen.append('/'.join([make_sfen(''.join(x)) for x in kyokumen]) 
                + ' ' + ('w' if i % 2 == 0 else 'b')
                + ' ' + sfen_mochigoma 
                + ' ' + str(i + 2))

    with open('sfen/%s.sfen'%each_file, "w") as f:
        f.write(sente + '\n')
        f.write(gote + '\n')
        f.write('\n'.join([str(i+1) + ' ' + x for i, x in enumerate(sashite)]))
        f.write('\n')
        f.write('\n'.join(sfen))
    
    print('convert %s.kif file'%each_file)


