import glob, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def mergeCsv():
    inFname = "csv\\StockOwnership\\13F\\*.csv"
    inFnamePath = os.path.join(BASE_DIR, inFname)
    outFname = "csv\\StockOwnership\\13F\\13Fdata.csv"
    outFnamePath = os.path.join(BASE_DIR, outFname)
    myFiles = glob.glob(outFnamePath)
    header_saved = False
    while True:
        try:
            with open(outFnamePath,'wb') as fout:
                for filename in myFiles:
                    with open(filename) as fin:
                        header = next(fin)
                        if not header_saved:
                            fout.write(header)
                            header_saved = True
                        for line in fin:
                            fout.write(line)
                    os.rename(filename, filename+"~")
        except:
            continue

if __name__ == '__main__':
    mergeCsv()
