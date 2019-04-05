from bs4 import BeautifulSoup as bs
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def dictCreator():
    link_name ="htmlXml\\row_data.html"
    output_name = "htmlXml\\dict.txt"
    link_path = os.path.join(BASE_DIR, link_name)
    output_path = os.path.join(BASE_DIR, output_name)


    with open(link_path) as fp:
        soup = bs(fp,'html.parser')
    clean_data = re.sub(r'<font face="Garamond-Book"><font size="1" style="font-size: 7pt">', '', str(soup))
    clean_data = re.sub(r'<font face="Garamond-Bold"><font size="1" style="font-size: 5pt">', '', clean_data)
    clean_data = re.sub(r'<font face="MathematicalPi-One"><font size="1" style="font-size: 5pt">', '', clean_data)
    clean_data = re.sub(r'<font face="MathematicalPi-Four"><font size="1" style="font-size: 7pt">', '', clean_data)
    clean_data = re.sub(r'<font face="Symbol"><font size="1" style="font-size: 7pt">', '', clean_data)
    clean_data = re.sub(r'</font><font face="Garamond-Bold"><font size="1" style="font-size: 7pt">', '', clean_data)
    clean_data = re.sub(r'<font face="Garamond-BoldItalic, cursive"><font size="1" style="font-size: 7pt"><i>', '', clean_data)
    clean_data = re.sub(r'<font face="Symb3l"><font size="1" style="font-size: 7pt">', '', clean_data)
    clean_data = re.sub(r'<font face="Garamond-Book"><font size="1" style="font-size: 5pt">', '', clean_data)
    clean_data = re.sub(r'</font><font face="Garamond-BookItalic, cursive"><font size="1" style="font-size: 7pt"><i>', '', clean_data)
    clean_data = re.sub(r'</font>|</i>', '', clean_data)
    clean_data = re.sub(r'<font face="MathematicalPi-One"><font size="1" style="font-size: 7pt">', '', clean_data)
    clean_data_key = re.findall(r'<b>[\s\S]*?<\/b>', clean_data)
    dict_keys = []
    for i in clean_data_key:
        process_key = re.sub(r'\n</b>', '', i)
        process_key = re.sub(r'<b>|</b>', '', process_key)
        process_key = re.sub(r'\n', ' ', process_key)
        dict_keys.append(process_key)
    print(len(dict_keys))
    dict_values = []
    clean_data_value = re.sub(r'</p>','<b>', clean_data)
    clean_data_value = re.findall(r'</b>[\s\S]*?<b>', clean_data_value)
    for j in clean_data_value:
        process_value = re.sub(r'\n</b>', '', j)
        process_value = re.sub(r'<b>|</b>', '', process_value)
        process_value = re.sub(r'\n', ' ', process_value)
        dict_values.append(process_value)
    output_file = open(output_path, 'wb')
    for i, j in enumerate(dict_keys):
        # line = '{}"{}"{}"{}"{}'.format('{',j.strip(),', ',dict_values[i].strip(),'}, \n')
        line = '"{}"{}"{}"{}'.format(j.strip(),':',dict_values[i].strip(),', \n')
        output_file.write(line.encode('utf-8'))
            # print(j, ": ", dict_values[i])
    print(len(dict_values))
dictCreator()
