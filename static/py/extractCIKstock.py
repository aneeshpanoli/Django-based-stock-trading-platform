from bs4 import BeautifulSoup as bs
import os
import re
import urllib
import pandas as pd
from institutionList import institutions
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SecEdgarCrawler():
    def __init__(self):
        pass
    def get_valid_13F_HR_ciks(self): # Only those CIKs of 13F filers
        '''This script can get the CIKs and names of anyone who file 13F_HR connected to given keyword'''
        #-----re compilers ----------------
        rawstringcik = re.compile(r'CIK=[\s\S]*?&amp')
        rawstringSubCik = re.compile(r'CIK=|&amp')
        rawstring = re.compile(r'<[\s\S]*?>')
        #-------------------------------------------------------------------------------------------------------
        filename = "csv\\StockOwnership\\stocks.csv"
        csvPath = os.path.join(BASE_DIR,  filename)
        columns = ['cik', 'name', 'ticker']
        choose = input("Please Enter 1 to add a single institution to the institutions list or 2 add a  list: ")
        instListname =  "csv\\StockOwnership\\stock_names.csv"
        instListname = os.path.join(BASE_DIR,  instListname)
        if choose == "1":
            comNames = [input("Please enter the company name/Keyword: ")]
        else:
            comNames = set(pd.read_csv(instListname, encoding = "ISO-8859-1")['name'].tolist())
        try:
            df = pd.read_csv(csvPath, encoding = "ISO-8859-1") # converter was added retain left side zeros
        except:
            df = pd.DataFrame(columns=columns)

        for ind, kw in enumerate(comNames):
            namesSet = set(df['name'].tolist())
            print(ind/len(comNames)*100, end="\r")
            print(kw)
            if kw not in namesSet:
                comName = str(kw).strip().lower()
                comName = comName.replace(' ', "+")
                url = "https://www.sec.gov/cgi-bin/browse-edgar?company="+comName+"&owner=exclude&output=xml&action=getcompany"
                url = re.sub(r'\s', '', url)
                with urllib.request.urlopen(url) as f:
                    soup =bs(f, 'lxml')
                ciks = re.findall(rawstringcik, str(soup))
                for i in ciks:
                    t1  = time.time()
                    cik = re.sub(rawstringSubCik, '', i)
                    cikSet = set(df['cik'].tolist())
                    if int(cik) not in cikSet:
                        for j in ["10-Q"]:#, "13G", "13D"]:
                            urlCheckIf13F = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+cik+"&type="+j+"&output=xml&dateb=20180101&owner=exclude&count=1"#"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+i+"&type=13F&dateb=20180101&owner=exclude&output=xml&count=10"
                            urlCheckIf13F = re.sub(r'\s', '', urlCheckIf13F)
                            with urllib.request.urlopen(urlCheckIf13F) as v:
                                soup1 = bs(v, 'lxml')
                                if "10-Q" in str(soup1):
                                    print("yes in 10-q")
                                    ticker = re.sub(rawstring, '', str(soup1.find('dei:TradingSymbol')))
                                    # name = name.replace("&amp;amp;amp;","and")
                                    # name = name.replace("&amp;","and")
                                    df.loc[len(df.index)] = [int(cik), kw, ticker]
                                else:
                                    ticker = "No filings exist"
                        try:
                            df.to_csv(csvPath, sep=',', index=False, encoding = "utf-8")
                        except:
                            print(ticker)

                    else:
                        print("Cik Already in the database! ")
                    t2 = time.time()
                    print(t2-t1, end="\r")
                    if t2-t1 < 0.1:
                        time.sleep(0.1)
            else:
                print("Name already in the databse")
if __name__ == '__main__':
    crawl = SecEdgarCrawler()
    crawl.get_valid_13F_HR_ciks()
