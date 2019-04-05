import time
from crawlSEC import SecEdgarCrawler

def get13fFilings(): #13G 13F-HR
    t1 = time.time()
    seccrawler = SecEdgarCrawler()
    seccrawler.get_valid_13F_HR_ciks()
    t2= time.time()
    print("Total time taken: ", t2-t1)

if __name__ == '__main__':
        get13fFilings()
