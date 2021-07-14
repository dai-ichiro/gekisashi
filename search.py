import sys
import re
import glob
import os

sfen_files = glob.glob('sfen/*.sfen')

while True:
    input_text = input('sfenを入力して下さい、終了時はq\n')

    if input_text == 'q':
        break
    else:
        print('\n')
    
    text_list = input_text.split(' ')

    if len(text_list) < 3:
        print('データが不適です')
        continue

    pattern = r'^' + re.escape(text_list[0]) + r'\s([w|b])\s' + re.escape(text_list[2]) + r'\s' + r'(\d+)$'

    for each_file in sfen_files:
        with open(each_file, 'r') as f:
            my_data = f.read()

        m = re.finditer(pattern, my_data, flags = re.MULTILINE)
        result_list = list(m)

        if len(result_list) != 0:
            print(os.path.basename(each_file))
            sente = re.search(r'^先手：.*$', my_data, flags = re.MULTILINE).group()
            gote = re.search(r'^後手：.*$', my_data, flags = re.MULTILINE).group()
            for mm in result_list:
                teban = mm.groups()[0]
                teban_text = sente if teban == 'b' else gote
                sashite_pattern = r'^' + re.escape(mm.groups()[1]) + r'\s(\S+)$'
                sashite_search = re.search(sashite_pattern, my_data, flags = re.MULTILINE) 
                sashite = sashite_search.groups()[0]
                print('%s手目　%s　が　%s　を指しました\n'%(mm.groups()[1], teban_text, sashite))

sys.exit()
    