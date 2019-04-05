from bs4 import BeautifulSoup as bs
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ncbiBooksGlossay():
    link_name ="htmlXml\\row_data.html"
    output_name = "htmlXml\\dict.txt"
    link_path = os.path.join(BASE_DIR, link_name)
    output_path = os.path.join(BASE_DIR, output_name)

    with open(link_path) as fp:
        soup = bs(fp,'html.parser')
    print(soup)
#r'(?<=[a-z])\r?\n' is a positive lookbehind assertion that checks if the character before the current position is a lowercase ASCII character. Only then the regex engine will try to match a line break.
    clean_data = re.sub(r'<a[\s\S]*?">', '', str(soup))
    clean_data = re.sub(r'</a>', '', clean_data)
    clean_data = re.sub(r'<div[\s\S]*?">', '', clean_data)
    clean_data = re.sub(r'<span[\s\S]*?">', '', clean_data)
    clean_data = re.sub(r'<img[\s\S]*?">', '', clean_data)
    clean_data = re.sub(r'</dl>[\s\S]*?<dl>', '', clean_data)
    clean_data = re.sub(r'see[\s\S]*?\.', '', clean_data)
    clean_data = re.sub(r'See[\s\S]*?\.', '', clean_data)
    clean_data = re.sub(r'\(Fig[\s\S]*?\d\)', '', clean_data)
    clean_data = re.sub(r'\(See[\s\S]*?\d\)', '', clean_data)
    clean_data = re.sub(r'\(Tab[\s\S]*?\d\)', '', clean_data)
    clean_data = re.sub(r'<sup>', '^', clean_data)
    clean_data = re.sub(r'<dd>|</dd>|</span>|</img>|</div>|<h2>|</h2>|<sub>|</sub>|<b>|</b>|<i>|</i>|<dl>|</dl>|</sup>', '', clean_data)
    clean_data = re.sub(r'\r?\n', ' ', clean_data)
    clean_data_key = re.findall(r'<dt[\s\S]*?</dt>', clean_data)
    # print(clean_data)
    dict_keys = []
    for i in clean_data_key:
        process_key = re.sub(r'<dt[\s\S]*?>|</dt>', '', i)
        dict_keys.append(process_key.strip())
        # print ("<----", process_key)
    # print(dict_keys)

    #-----------------value--------------------
    dict_values = []
    clean_data_value = re.findall(r'<p>[\s\S]*?<dt', clean_data)
    for j in clean_data_value:
        process_value = re.sub(r'<p>|</p>|<dt', '', j)
        dict_values.append(process_value.strip())
        # print("---->", process_value)
    # print(dict_values)
    print(len(dict_values))
    print(len(dict_keys))
    output_file = open(output_path, 'wb')
    for i, j in enumerate(dict_values):
        if j != "":
            line = '"{}"{}"{}"{}'.format(dict_keys[i],':',j,', \n')
            output_file.write(line.encode('utf-8'))
            # print(j, ": ", dict_values[i])



def amaParser():
    link_name ="htmlXml\\row_data.html"
    output_name = "htmlXml\\dict.txt"
    link_path = os.path.join(BASE_DIR, link_name)
    output_path = os.path.join(BASE_DIR, output_name)

    with open(link_path) as fp:
        soup = bs(fp,'html.parser')
    clean_data = re.sub(r'<a[\s\S]*?">', '', str(soup))
    clean_data = re.sub(r'</a>|</h1>|</p>|<span>', '', clean_data)
    clean_data = re.sub(r'<div[\s\S]*?">', '', clean_data)
    clean_data = re.sub(r'<p[\s\S]*?">', '', clean_data)
    clean_data = re.sub(r'<img[\s\S]*?"/>', '', clean_data)
    clean_data = re.sub(r'</dl>[\s\S]*?<dl>', '', clean_data)
    # clean_data = re.sub(r'see[\s\S]*?</span>', '', clean_data)
    # clean_data = re.sub(r'See[\s\S]*?\.', '', clean_data)
    clean_data = re.sub(r'\(Fig[\s\S]*?\d\)', '', clean_data)
    # clean_data = re.sub(r'\(See[\s\S]*?\d\)', '', clean_data)
    clean_data = re.sub(r'\(Tab[\s\S]*?\d\)', '', clean_data)
    clean_data = re.sub(r'<sup>', '^', clean_data)
    clean_data = re.sub(r'</span><br/>|<dd>|</dd>|</img>|</div>|<sub>|</sub>|<b>|</br>|</b>|<i>|</i>|<dl>|</dl>|</sup>|-\s', '', clean_data)
    clean_data = re.sub(r'\r?\n', ' ', clean_data)
    clean_data_key = re.findall(r'<h1>[\s\S]*?<span', clean_data)
    print(clean_data)
    dict_keys = []
    for i in clean_data_key:
        process_key = re.sub(r'<h1>|<span', '', i)
        dict_keys.append(process_key.strip())
        # print(process_key)
    dict_values = []
    clean_data_value = re.findall(r'"p">[\s\S]*?</span>', clean_data)
    for j in clean_data_value:
        process_value = re.sub(r'<span[\s\S]*?>|</span>|<p>|</p>|</h2>|<h2>|"p">:|"p">|"', '', j)
        dict_values.append(process_value.strip())
    print(len(dict_keys))
    print(len(dict_values))
    output_file = open(output_path, 'wb')
    for i, j in enumerate(dict_values):
        if j != "":
            line = '"{}"{}"{}"{}'.format(dict_keys[i].lower(),':',j.capitalize(),', \n')
            output_file.write(line.encode('utf-8'))
def copyPastedFromPdf():
    link_name ="htmlXml\\row_data.html"
    output_name = "htmlXml\\dict.txt"
    link_path = os.path.join(BASE_DIR, link_name)
    output_path = os.path.join(BASE_DIR, output_name)

    with open(link_path) as fp:
        soup = bs(fp,'html.parser')
    clean_data = re.sub(r'<a[\s\S]*?">', '', str(soup))
    clean_data = re.sub(r'</a>|</h1>|</p>|<span>', '', clean_data)
    clean_data = re.sub(r'<div[\s\S]*?">', '', clean_data)
    clean_data = re.sub(r'<font[\s\S]*?">', '', clean_data)
    clean_data = re.sub(r'<p[\s\S]*?">', '', clean_data)
    clean_data = re.sub(r'<img[\s\S]*?"/>', '', clean_data)
    clean_data = re.sub(r'</dl>[\s\S]*?<dl>', '', clean_data)
    # clean_data = re.sub(r'see[\s\S]*?</span>', '', clean_data)
    # clean_data = re.sub(r'See[\s\S]*?\.', '', clean_data)
    clean_data = re.sub(r'\(Fig[\s\S]*?\d\)', '', clean_data)
    clean_data = re.sub(r'\(see[\s\S]*?\)', '', clean_data)
    clean_data = re.sub(r'\(Tab[\s\S]*?\d\)', '', clean_data)
    clean_data = re.sub(r'<sup>', '^', clean_data)
    clean_data = re.sub(r'</span><br/>|<dd>|</dd>|</img>|</font>|</div>|<sub>|</sub>|</br>|<i>|</i>|<dl>|</dl>|</sup>|-\s', '', clean_data)
    clean_data = re.sub(r'\r?\n', ' ', clean_data)
    clean_data_key = re.findall(r'<b>[\s\S]*?</b>', clean_data)
    print(clean_data)
    dict_keys = []
    for i in clean_data_key:
        process_key = re.sub(r'<b>|</b>', '', i)
        dict_keys.append(process_key.strip())
        # print(process_key)
    dict_values = []
    clean_data_value = re.findall(r'</b>[\s\S]*?<b>', clean_data)
    for j in clean_data_value:
        process_value = re.sub(r'<span[\s\S]*?>|</span>|<p>|</p>|</h2>|<h2>|</b>|<b>|"', '', j)
        dict_values.append(process_value.strip())
    print(len(dict_keys))
    print(len(dict_values))
    output_file = open(output_path, 'wb')
    for i, j in enumerate(dict_values):
        if j != "":
            line = '"{}"{}"{}"{}'.format(dict_keys[i].lower(),':',j.capitalize(),', \n')
            output_file.write(line.encode('utf-8'))
copyPastedFromPdf()
