from bs4 import BeautifulSoup as bs
from urllib import request as req
from urllib.request import urlopen
import os
import re
import pandas as pd
from datetime import datetime
from nltk.tokenize import sent_tokenize
# from django.apps import apps # to deal with circular import error when importing models
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# django.setup()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #points to static folder


def contentExtractor():
    link_name ="essaybot\\htmlLinks\\Extracted_Links.html"
    output_name = "essaybot\\htmlLinks\\output1.html"
    para1_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para1.csv")
    para2_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para2.csv")
    para3_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para3.csv")
    para4_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para4.csv")
    para5_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para5.csv")
    para6_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para6.csv")
    para7_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para7.csv")
    para8_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para8.csv")
    para9_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para9.csv")
    para10_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para10.csv")
    para11_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para11.csv")
    para12_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para12.csv")
    para13_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para13.csv")
    para14_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para14.csv")
    para15_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para15.csv")
    para16_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para16.csv")
    para17_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para17.csv")
    para18_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para18.csv")
    para19_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para19.csv")
    para20_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para20.csv")
    para21_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para21.csv")
    para22_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para22.csv")
    para23_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para23.csv")
    para24_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para24.csv")
    para25_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para25.csv")
    para26_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para26.csv")
    para27_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para27.csv")
    para28_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para28.csv")
    para29_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para29.csv")
    para30_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para30.csv")
    para31_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para31.csv")
    para32_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para32.csv")
    para33_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para33.csv")
    para34_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para34.csv")
    para35_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para35.csv")
    para36_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para36.csv")
    para37_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para37.csv")
    para38_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para38.csv")
    para39_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para39.csv")
    para40_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para40.csv")
    para41_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para41.csv")
    para42_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para42.csv")
    para43_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para43.csv")
    para44_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para44.csv")
    para45_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para45.csv")
    para46_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para46.csv")
    para47_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para47.csv")
    para48_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para48.csv")
    para49_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para49.csv")
    para50_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para50.csv")
    link_path = os.path.join(BASE_DIR, link_name)
    output_path = os.path.join(BASE_DIR, output_name)

    para_name_list =[para1_name, para2_name, para3_name, para4_name\
                    , para5_name, para6_name, para7_name, para8_name\
                    , para9_name, para10_name, para11_name, para12_name\
                    , para13_name, para14_name, para15_name, para16_name\
                    , para17_name, para18_name, para19_name, para20_name\
                    , para21_name, para22_name, para23_name, para24_name\
                    , para25_name, para26_name, para27_name, para28_name\
                    , para29_name, para30_name, para31_name, para32_name\
                    , para33_name, para34_name, para35_name, para36_name\
                    , para37_name, para38_name, para39_name, para40_name\
                    , para41_name, para42_name, para43_name, para44_name\
                    , para45_name, para46_name, para47_name, para48_name\
                    , para49_name, para50_name]

    # essay_link = input("please enter the url: ")
    # r = req.urlopen(link_path).read()
    with open(link_path) as fp:
        soup = bs(fp,'html.parser')
    link_list =soup.find_all('a')
    big_list = []
    for i in link_list:
        list1 = re.findall(r'https[\s\S]*?%\d', str(i))
        list2 = re.findall(r'http[\s\S]*?%\d', str(i))
        if list1 != [] or list2 !=[]:
            big_list.extend(list2)
            big_list.extend(list1)
        big_list = [i for i in big_list if "google" not in i]

    clean_links = []
    for i in big_list:
        i=i.replace("%2", '')
        if i not in clean_links:
            clean_links.append(i)
    for i in clean_links:
        r = req.urlopen(i).read()
        soup = bs(r, 'html.parser')
        content_list = re.findall(r'<p>[\s\S]*?<\/p>', str(r))
        element_list = ['<p>', '<i>', '</i>', '<strong>', '</strong>', '&nbsp;'\
                        , '<em>', '</em>', '\\', '<b>', '</b>', '</a>']
        content_list = ' '.join(content_list)
        for i in element_list:
            content_list = content_list.replace(i, '')
        content_list = re.sub(r'<a[\s\S]*?>', '', content_list) # need to correct this then add bold tags
        content_list = re.sub(r'<sup[\s\S]*?<\/sup>', '', content_list)
        content_list = content_list.split("</p>")
        content_list = [i for i in content_list if len(i) > 200]
        content_list = [i for i in content_list if "JavaScript" not in i]
        content_list = [i.strip() for i in content_list]
        columns = ['line1', 'line2', 'line3', 'line4', 'line5', 'line6', 'line7'\
        , 'line8', 'line9', 'line10', 'line11', 'line12', 'line13', 'line14', 'line15'\
        , 'line16', 'line17', 'line18', 'line19']
        data_list = ["na", "na", "na", "na", "na", "na", "na", "na", "na", "na"\
                    , "na", "na", "na", "na", "na", "na", "na", "na", "na"]
        for i, j in enumerate(content_list):
            line_list = sent_tokenize(j)
            try:
                df = pd.read_csv(para_name_list[i])
            except:
                df = pd.DataFrame(columns=columns)
            for k, l in enumerate(line_list):
                data_list[k] = l
            dflen = len(df.index)
            df.loc[dflen] = data_list
            df.to_csv(para_name_list[i], sep=',', index=False)
    # for i in content_list:
    #     line_list = i.split('.')
    #     for i in line_list:


    # no_google = [i for i in link_list if "google" not in i]
def main():
    link_name ="essaybot\\htmlLinks\\Extracted_Links.html"
    para1_name = os.path.join(BASE_DIR,"essaybot\\csv\\geneEditing\\para1.csv")
    link_path = os.path.join(BASE_DIR, link_name)
    try:
        if datetime.fromtimestamp(os.path.getmtime(link_path)).date() > datetime.fromtimestamp(os.path.getmtime(para1_name)).date():
            contentExtractor()
    except:
        contentExtractor()
main()
