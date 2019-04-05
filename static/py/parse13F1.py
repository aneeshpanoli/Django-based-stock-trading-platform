from bs4 import BeautifulSoup as bs
import os
import re, contextlib
import urllib
import pandas as pd
from institutionList import institutions
import time, datetime
from dateutil.relativedelta import relativedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def parse_form_13F():
    #-----------re compilers-------------------------------------------
    t1 = time.time()
    rawstring = re.compile(r'<[\s\S]*?>') # general tag remover
    rawstringfilingref = re.compile(r'<[\s\S]*?>|\s') # general tag remover
    rawstringsecName = re.compile(r'<[\s\S]*?>|\*|/|\\|\'|,|"|\?|!') # format securties name from  13F-HR
    rawFindAhref = re.compile(r'href="[\s\S]*?>') # find href links
    rawSubAhref = re.compile(r'href="|">|\s') # remove a href tags
    rawFindFilingDate = re.compile(r'Filing Date</div>\n<div class="info">[\s\S]*?</div>')
    rawSubFilingDate = re.compile(r'Filing Date</div>\n<div class="info">|</div>')

    #get list of ciks/institution names from the master institutions.csv--------------------------------------
    instituionsFname = "csv\\StockOwnership\\institutions.csv"
    instituionsPath = os.path.join(BASE_DIR, instituionsFname)
    institutionsDf = pd.read_csv(instituionsPath, encoding = "ISO-8859-1")

    # create 13F-HR table
    df13FdataFname = "csv\\StockOwnership\\13Fdata.csv"
    df13FdataFnamePath = os.path.join(BASE_DIR, df13FdataFname)

    columns = ['cusip', 'stock', 'cik', 'institution']
    monthlist = monthList()
    columns.extend(monthlist)
    try:
        df13Fdata = pd.read_csv(df13FdataFnamePath, encoding = "ISO-8859-1")
    except:
        df13Fdata = pd.DataFrame(columns=columns)

    cikList = tuple(institutionsDf['cik'].tolist())
    instNameList = tuple(institutionsDf['name'].tolist())
    set13FCiks = set(df13Fdata['cik'].tolist())
    # look for filing information
    # iterate through the CIK number and look for 13F-HR filing info from SEC max 10 filings
    # parse the resulting page and  extract links to individual filing page. This is not-
    # the link to `3F form ` itself. Just a pointer to the filing page
    # make the list
    # multiplier = 1
    for ind, cik in enumerate(cikList):
        # if df13Fdata['cik'].astype(str).str.match(str(cik)).any(): # avoid duplicates when app is restarted
        if int(cik) in set13FCiks:
            print(instNameList[ind], " is already in 13Fdata.csv!")
            continue
        holdingDfIndex = 0
        holdingDf = pd.DataFrame(columns=columns)
        linkList = []
        priorTo = time.strftime('%Y%m%d')

        urlCheckIf13F = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)\
                        +"&type=13F-HR&output=xml&dateb="+priorTo+"&owner=exclude&count=10"
        urlCheckIf13F = re.sub(r'\s', '', urlCheckIf13F)
        print(urlCheckIf13F)
        with urllib.request.urlopen(urlCheckIf13F) as f:
            soup = bs(f, 'lxml')
            if "filinghref" in str(soup):
                for i in soup.findAll('filinghref'):
                    i = re.sub(rawstring, '', str(i))
                    if i[-1] != "l":
                        i +="l"
                    linkList.append(i)
            else:
                name = "No filings exist"
        soup = None
        # iterate through each link in the link list
        # parse the page to extract links to actual form 13F-HR
        # also extract the filing dates to use as the column names
        for link in linkList:
            xmlLinkList = []
            link = re.sub(r'\s', '', link)
            print(link)

            with urllib.request.urlopen(link) as xmlf:
                soup1 = bs(xmlf, 'lxml')
            for i in soup1.findAll("tr", { "class" : "blueRow" }):
                if "INFORMATION TABLE" in str(i):
                    xmlLinkList.append("https://www.sec.gov"+re.sub(rawSubAhref, '', re.findall(rawFindAhref, str(i))[0]))
            filingDate = re.sub(rawSubFilingDate, '', re.findall(rawFindFilingDate, str(soup1))[0]).strip()[:7]
            print("Institution:", instNameList[ind], cik,". (", ind+1, "of", len(cikList), ")")
            print(xmlLinkList)
            print (filingDate)
            if xmlLinkList == []: # if there are no xml links delete the institution from csv
                institutionsDf.drop(institutionsDf.index[ind], inplace=True)
                institutionsDf.to_csv(instituionsPath, sep=',', index=False, encoding = "utf-8")
                print("Deleted",instNameList[ind], "from institutions.csv" )
                break
            filingDateMax = "2015-01"
            soup1 = None
            #iterate through xmllink list
            # parse each page and extract security name and no of shares held
            if time.mktime(datetime.datetime.strptime(filingDate,"%Y-%m").timetuple())\
                >time.mktime(datetime.datetime.strptime(filingDateMax,"%Y-%m").timetuple()):
                for k in xmlLinkList:
                    k = re.sub(r'\s', '', k)
                    dataDict = {}
                    tk1 = time.time()
                    with urllib.request.urlopen(k) as xmls:
                        soup2 = bs(xmls, 'lxml')
                    securitesNames = soup2.findAll('nameofissuer')
                    noOfShareList = soup2.findAll('sshprnamt')
                    cusips = soup2.findAll('cusip')
                    for i, l in enumerate(securitesNames):
                        securitesName = re.sub(rawstringsecName, ' ', str(l)).strip().replace("&amp;", "and")
                        shares = re.sub(rawstring, '', str(noOfShareList[i]))
                        cusip = re.sub(rawstring, ' ', str(cusips[i])).strip()
                        dataDict[securitesName] = [cusip, shares]
                    if dataDict == {}:
                        securitesNames = re.findall(r'<ns1:nameofissuer>[\s\S]*?</ns1:nameofissuer>', str(soup2))
                        noOfShareList = re.findall(r'<ns1:sshprnamt>[\s\S]*?</ns1:sshprnamt>', str(soup2))
                        cusips = re.findall(r'<ns1:cusip>[\s\S]*?</ns1:cusip>', str(soup2))
                        for i, l in enumerate(securitesNames):
                            securitesName = re.sub(rawstringsecName, ' ', str(l)).strip().replace("&amp;", "and")
                            shares = re.sub(rawstring, '', str(noOfShareList[i]))
                            cusip = re.sub(rawstring, ' ', str(cusips[i])).strip()
                            dataDict[securitesName] = [cusip, shares]
                    if dataDict == {}:
                        securitesNames = re.findall(r'<n1:nameofissuer>[\s\S]*?</n1:nameofissuer>', str(soup2))
                        noOfShareList = re.findall(r'<n1:sshprnamt>[\s\S]*?</n1:sshprnamt>', str(soup2))
                        cusips = re.findall(r'<n1:cusip>[\s\S]*?</n1:cusip>', str(soup2))
                        for i, l in enumerate(securitesNames):
                            securitesName = re.sub(rawstringsecName, ' ', str(l)).strip().replace("&amp;", "and")
                            shares = re.sub(rawstring, '', str(noOfShareList[i]))
                            cusip = re.sub(rawstring, ' ', str(cusips[i])).strip()
                            dataDict[securitesName] = [cusip, shares]
                    if dataDict == {}:
                        securitesNames = re.findall(r'<ns4:nameofissuer>[\s\S]*?</ns4:nameofissuer>', str(soup2))
                        noOfShareList = re.findall(r'<ns4:sshprnamt>[\s\S]*?</ns4:sshprnamt>', str(soup2))
                        cusips = re.findall(r'<ns4:cusip>[\s\S]*?</ns4:cusip>', str(soup2))
                        for i, l in enumerate(securitesNames):
                            securitesName = re.sub(rawstringsecName, ' ', str(l)).strip().replace("&amp;", "and")
                            shares = re.sub(rawstring, '', str(noOfShareList[i]))
                            cusip = re.sub(rawstring, ' ', str(cusips[i])).strip()
                            dataDict[securitesName] = [cusip, shares]
                    securitesNames = noOfShareList = cusips= soup2 = None
                    tk2 = time.time()
                    if tk1-tk2 < 0.1:
                        time.sleep(0.1)
                    # iterate through the extracted securities name list
                    # create csv for each security
                    # insert the institution name , CIK, filing date as coulmn and shares held
                    # make pandas DataFrame
                    t1 = time.time()
                    for indx, (secName, value) in enumerate(dataDict.items()):

                        try:
                            indexToInsert = holdingDf.index[(holdingDf.cik == cik) & (holdingDf.cusip == value[0])][0]
                            sharesAlreadyOwn = holdingDf[filingDate].iat[indexToInsert]
                            holdingDf[filingDate].iloc[indexToInsert] = sharesAlreadyOwn + int(value[1])
                        except:
                            dataList = [value[0], secName, cik, instNameList[ind]]
                            dataList.extend([0]*len(monthlist)) #columns = ['cusip', 'stock', 'cik', 'institution']
                            dataList[columns.index(filingDate)] = value[1]
                            holdingDf.loc[holdingDfIndex] = dataList
                            holdingDfIndex += 1
                            t2 = time.time()
                            print(round(indx/len(dataDict)*100, 2), round(t2-t1, 2), end="\r")

        if xmlLinkList != []:
            df13Fdata = pd.concat([df13Fdata, holdingDf])
            set13FCiks.update(holdingDf['cik'].tolist())
            holdingDf = dataDict = dataList = None
            with atomic_overwrite(df13FdataFnamePath) as f:
                df13Fdata.to_csv(f, sep=',', index=False, encoding = "utf-8")


    df13Fdata.sort_values('cusip', inplace=True)
    with atomic_overwrite(df13FdataFnamePath) as f:
        df13Fdata.to_csv(f, sep=',', index=False, encoding = "utf-8")
    print("Time elapsed:", t2-t1)

def monthList():
    months = []
    today = datetime.date.today()
    current = datetime.date(2015, 1, 1)
    while current <= today:
        months.append(current.strftime("%Y-%m"))
        current += relativedelta(months=1)
    return months[::-1]

@contextlib.contextmanager
def atomic_overwrite(filename):
    originalToTemp = filename + "v1"
    temp = filename + '~'
    with open(temp, "w") as f:
        yield f
    os.rename(filename, originalToTemp)
    os.rename(temp, filename) # this will only happen if no exception was raised
    os.remove(originalToTemp)


if __name__ == '__main__':
    try:
        parse_form_13F()
    except:
        print("An error occured, restarting in 60 seconds...")
        time.sleep(60)
        parse_form_13F()
