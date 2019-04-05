import pandas as pd
import os, math, glob
import numpy as np
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class process13FHR:
    '''Process 13F-HR data csvs'''
    def __init__(self, term):
        self.df13FdataFname = "csv\\StockOwnership\\13Fdata.csv"
        self.df13FdataFnamePath = os.path.join(BASE_DIR, self.df13FdataFname)
        self.inFname = "csv\\StockOwnership\\13F\\*.csv"
        self.inFnamePath = os.path.join(BASE_DIR, self.inFname)
        self.myFiles = glob.glob(self.inFnamePath)
        self.term = term
    def summary_of_data(self):
        df13Fdata = pd.read_csv(self.df13FdataFnamePath, encoding = "ISO-8859-1")
        columns = df13Fdata.columns
        ciks = df13Fdata['cik'].tolist()
        instname = df13Fdata['institution'].tolist()
        summaryFname = "csv\\StockOwnership\\summary_13F.csv"
        summaryFnamePath = os.path.join(BASE_DIR, summaryFname)
        institutionDict = dict(zip(ciks, instname))
        summnaryList = []
        for ind, (i, n) in enumerate(institutionDict.items()):
            instiDf = df13Fdata[df13Fdata.cik == i]
            tempList = [i, n]
            cycle = 0
            for k in columns[4:]:
                if instiDf[k].sum() != 0:
                    tempList.append(instiDf[k].sum())
                    cycle +=1
                    if cycle > 1:
                        break
            summnaryList.append(tempList)
            print(round(ind/len(institutionDict)*100, 2), end ="\r")
        summaryDF = pd.DataFrame(summnaryList, columns=['cik', 'institution', 'sharesnow', 'shareslast'])
        summaryDF['change'] = (summaryDF['sharesnow'] - summaryDF['shareslast'])/summaryDF['shareslast']
        summaryDF.to_csv(summaryFnamePath, sep=',', index=False, encoding = "utf-8")
        return "done"
    def institution_of_interest(self):

        return self.term
    def com_of_interest(self):
        cusips = []
        stocks = []
        ciks = []
        insts = []
        for ind, i in enumerate(self.myFiles):
            df = pd.read_csv(i, encoding = "ISO-8859-1")
            cusips.extend(df['cusip'].tolist())
            stocks.extend(df['stock'].tolist())
            ciks.extend(df['cik'].tolist())
            insts.extend(df['institution'].tolist())
        cusips += ciks
        stocks += insts
        allDict = dict(zip(cusips, stocks))
        releventCusip = {key:value for key, value in allDict.items() if self.term.upper() in str(value).upper()}
        return releventCusip
    def com_data(self):
        cusips = []
        stocks = []
        stockDflist = []
        for ind, i in enumerate(self.myFiles):
            df = pd.read_csv(i, encoding = "ISO-8859-1", converters={'cusip': str})
            cusips.extend(df['cusip'].tolist())
            stocks.extend(df['stock'].tolist())
            stockDf = df[df.cusip == self.term]
            stockDflist.extend([[s for s in row if s != 0 ] for row in stockDf.values.tolist()])
        stockDict = dict(zip(cusips, stocks))
        summaryList = []
        for ind, i in enumerate(stockDflist):
            summaryList.append(i[:6])
        print(round(ind/len(stockDict)*100, 2), end ="\r")
        summaryFname = "csv\\StockOwnership\\"+self.term+".csv"
        summaryFnamePath = os.path.join(BASE_DIR, summaryFname)
        summaryDF = pd.DataFrame(summaryList, columns=['cusip', 'stock', 'cik', 'institution', 'sharesnow', 'shareslast'])
        summaryDF['change'] = round((summaryDF['sharesnow'] - summaryDF['shareslast'])/summaryDF['shareslast']*100, 2)
        summaryDF.to_csv(summaryFnamePath, sep=',', index=False, encoding = "utf-8")
        return self.term
    def holding_increased(self):
        cusips = []
        stocks = []
        stockDflist = []
        for ind, i in enumerate(self.myFiles):
            df = pd.read_csv(i, encoding = "ISO-8859-1", converters={'cusip': str})
            cusips.extend(df['cusip'].tolist())
            stocks.extend(df['stock'].tolist())
            stockDflist.extend([[s for s in row if s != 0 ] for row in df.values.tolist()])
        stockDict = dict(zip(cusips, stocks))
        summaryList = []
        for ind, i in enumerate(stockDflist):
            summaryList.append(i[:6])
        print(round(ind/len(stockDict)*100, 2), end ="\r")
        summaryFname = "csv\\StockOwnership\\positiveChange.csv"
        summaryFnamePath = os.path.join(BASE_DIR, summaryFname)
        summaryDF = pd.DataFrame(summaryList, columns=['cusip', 'stock', 'cik', 'institution', 'sharesnow', 'shareslast'])
        summaryDF['change'] = round((summaryDF['sharesnow'] - summaryDF['shareslast'])/summaryDF['shareslast']*100, 2)
        summaryDF = summaryDF[summaryDF.change > 10000]
        summaryDF.to_csv(summaryFnamePath, sep=',', index=False, encoding = "utf-8")
        return "Positive change saved"
    def testGlob(self):
        '''merge csvs to one big file - not for the website'''
        outFname = "csv\\StockOwnership\\13Fdata.csv"
        outFnamePath = os.path.join(BASE_DIR, outFname)
        dataList =[]
        for ind, i in enumerate(self.myFiles):
            dataList.extend(pd.read_csv(i, encoding = "ISO-8859-1").values.tolist())
            print(round(ind/len(self.myFiles)*100, 2), end ="\r")
        columns = pd.read_csv(i, encoding = "ISO-8859-1").columns
        df = pd.DataFrame(dataList, columns=columns)
        df.to_csv(outFnamePath, sep=',', index=False, encoding = "utf-8")
        return "Summary DF created"
    def list_of_stocks(self):
        cusips = []
        stocks = []
        for ind, i in enumerate(self.myFiles):
            df = pd.read_csv(i, encoding = "ISO-8859-1", converters={'cusip': str})
            cusips.extend(df['cusip'].tolist())
            stocks.extend(df['stock'].tolist())
        stockDict = dict(zip(cusips, stocks))
        stkListname =  "csv\\StockOwnership\\stock_names.csv"
        stkListnamepath = os.path.join(BASE_DIR,  stkListname)
        dfList = pd.DataFrame(list(stockDict.items()), columns=['cuisp', 'name'])
        dfList.to_csv(stkListnamepath, sep=',', index=False, encoding = "utf-8")
        return "Stock list created"
if __name__ == '__main__':
    start13Fprocess = process13FHR('037833100')
    print(start13Fprocess.holding_increased())
