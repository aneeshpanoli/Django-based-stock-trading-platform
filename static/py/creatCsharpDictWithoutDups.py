# creates c# dictionary for biology trivia App

import dic_dict
import os
import re
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_name = "htmlXml\\uniq_dict.txt"
output_path = os.path.join(BASE_DIR, output_name)
output_file = open(output_path, 'wb')
uniq_dict = {}
data_dict = dic_dict.dictKeys()
for k, v in data_dict.items():
    if k in v:
        kList = k.split(' ')
        vlist = v.split(' ')
        print(kList[0])
        print(vlist[0])
        if kList[0].lower() == vlist[0].lower():
            v = v.replace(k+ " ", " ____ ")
        else:
            v = v.replace(" "+k+ " ", " ____ ")
    if k.strip().lower() not in uniq_dict.keys():
        uniq_dict.update({k.strip().lower() : v.strip()})
        line = '{}"{}"{}"{}"{}'.format('{',k.strip().lower(),', ',v.strip(),'}, \n')
        output_file.write(line.encode('utf-8'))

# print( uniq_dict)
