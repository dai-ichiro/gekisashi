import sys
import re
import glob
import os
import collections

def make_list(str):
    skip = False    
    result = []
    for i in range(len(str)):
        if skip == True:
            skip = False
            continue
        if str[i] == '+':
            skip = True
            result.append(str[i:i+2])
        else:
            result.append(str[i])
    return result

def mochigoma_list_to_str(mochigoma_list):
    if len(mochigoma_list) == 0:
        return '-'
    else:
        mochigoma_dict = collections.Counter(mochigoma_list)
        mochigoma_str = ''
        for x in koma_kigo2:
            if mochigoma_dict[x] == 1:
                mochigoma_str += x
            elif mochigoma_dict[x] > 1:
                mochigoma_str += (str(mochigoma_dict[x]) + x)
        return mochigoma_str

def mochigoma_str_to_list(mochigoma_str):
    if mochigoma_str == '-':
        return []
    else:
        mochigoma_list = []
        for i in range(len(mochigoma_str)):
            if mochigoma_str[i].isdigit():
                for n in range(int(mochigoma_str[i])-1):
                    mochigoma_list.append(mochigoma_str[i+1])
            else:
                mochigoma_list.append(mochigoma_str[i])
        return mochigoma_list

koma_kigo = ['r', 'b', 'g', 's', 'n', 'l', 'p']
koma_kigo2 = [x.swapcase() for x in koma_kigo] + koma_kigo

sfen_files = glob.glob('sfen/*.sfen')

while True:
    input_text = input('sfenを入力して下さい、終了時はq\n')

    if input_text == 'q':
        break
    else:
        input_text = input_text.replace('sfen ', '')
        print('\n')
    
    text_list = input_text.split(' ')

    if len(text_list) !=  4:
        print('データが不適です')
        continue

    banmen, teban, mochigoma, tesu = text_list

    banmen_row_list = [make_list(x) for x in banmen.swapcase().split('/')]
    r_banmen_row_list = [x[::-1] for x in banmen_row_list[::-1]]

    r_banmen = '/'.join([''.join(x) for x in r_banmen_row_list])

    r_mochigoma = mochigoma_list_to_str(mochigoma_str_to_list(mochigoma.swapcase()))

    normal_pattern = r'^' + re.escape(banmen) + r'\s([w|b])\s' + re.escape(mochigoma) + r'\s' + r'(\d+)$'
    rotate_pattern = r'^' + re.escape(r_banmen) + r'\s([w|b])\s' + re.escape(r_mochigoma) + r'\s' + r'(\d+)$'
    
    for each_file in sfen_files:
        with open(each_file, 'r') as f:
            my_data = f.read()

        normal_result = re.finditer(normal_pattern, my_data, flags = re.MULTILINE)
        rotate_result = re.finditer(rotate_pattern, my_data, flags = re.MULTILINE)
        
        normal_result_list = list(normal_result)
        rotate_result_list = list(rotate_result)


        if (len(normal_result_list) + len(rotate_result_list)) != 0:
            print(os.path.basename(each_file))
            sente = re.search(r'^先手：.*$', my_data, flags = re.MULTILINE).group()
            gote = re.search(r'^後手：.*$', my_data, flags = re.MULTILINE).group()
            
            if len(normal_result_list) != 0:
                print('通常検索')
                for mm in normal_result_list:
                    teban = mm.groups()[0]
                    teban_text = sente if teban == 'b' else gote
                    sashite_pattern = r'^' + re.escape(mm.groups()[1]) + r'\s(\S+)$'
                    sashite_search = re.search(sashite_pattern, my_data, flags = re.MULTILINE) 
                    sashite = sashite_search.groups()[0]
                    print('%s手目　%s　が　%s　を指しました\n'%(mm.groups()[1], teban_text, sashite))
            
            if len(rotate_result_list) != 0:  
                print('反転検索')  
                for mm in rotate_result_list:
                    teban = mm.groups()[0]
                    teban_text = sente if teban == 'b' else gote
                    sashite_pattern = r'^' + re.escape(mm.groups()[1]) + r'\s(\S+)$'
                    sashite_search = re.search(sashite_pattern, my_data, flags = re.MULTILINE) 
                    sashite = sashite_search.groups()[0]
                    sashite = ''.join([str(10-int(x)) if x.isdigit() else x for x in sashite])
                    print('%s手目　%s　が　%s　を指しました\n'%(mm.groups()[1], teban_text, sashite))
sys.exit()
    