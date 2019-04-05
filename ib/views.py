

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import pytz
import numpy as np
from datetime import datetime, time
import pandas as pd
import os, subprocess, psutil
from django.conf.urls.static import static
from . forms import SubmitTickerSymbolForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #points to static folder


class CommandCenterView(View):
    def __init__(self):
        self.the_form = SubmitTickerSymbolForm()
        self.month_year = datetime.now().strftime('%d | %B | %Y')

    def contextRender(self, request,*args,**kwargs):
        '''Common context renderer for the CommandCenterView'''
        context = {
            "title": "Command center",
            "form": self.the_form,
            "month_year": self.month_year,
            "twsRunning": kwargs['msg'],
        }
        return render(request, "ib/commandCenter.html", context)


    def get(self, request, *args, **kwargs):
        t_msg = "Keep up the good work :)"
        return self.contextRender(request\
                                    ,msg=t_msg)

    def post(self, request, *args, **kwargs):
        form = SubmitTickerSymbolForm(request.POST)
        # launch trader work station(TWS)
        if request.method == 'POST' and 'launchTws' in request.POST.keys():
            if "tws.exe" in (p.name() for p in psutil.process_iter()):
                t_msg = "TWS is running..."
                return self.contextRender(request\
                                            ,msg=t_msg)
            else:
                subprocess.Popen(['C:\\Jts\\tws.exe'])
                t_msg = "Launching TWS..."
                return self.contextRender(request\
                                            ,msg=t_msg)
        #add a ticker to forex list
        elif request.method == 'POST' and 'forexQuote0' in request.POST.keys():
            fName = "static\\csv\\forexWatchList.csv"
            csvPathForex = os.path.join(BASE_DIR,  fName )
            forex_ticker = form.data['tickerSymbol'].upper()
            columns = ['ticker', 'pid', 'clientid']
            emptydf = pd.DataFrame(columns=columns)
            try:
                df = pd.read_csv(csvPathForex)
            except:
                emptydf.to_csv(csvPathForex, sep=',', index=False)
                df = pd.read_csv(csvPathForex)

            client_id = [i for i in range(20, 25) if i not in df['clientid'].values ][0]

            if forex_ticker in df['ticker'].values:
                t_msg = "FAILED! "+forex_ticker+ " is already in the STOCK list"
                return self.contextRender(request\
                                            ,msg=t_msg)
            else:
                insertPoint = len(df['ticker'].values)
                df.loc[insertPoint, 'ticker'] = forex_ticker # df.loc is the trick to add to eend of row
                df.loc[insertPoint, 'clientid'] = client_id
                df.to_csv(csvPathForex, sep=',', index=False)

                t_msg = " Added " + forex_ticker+ " to FOREX list"
                return self.contextRender(request\
                                            ,msg=t_msg)

        #add a ticker to stock list
        elif request.method == 'POST' and 'stockQuote0' in request.POST.keys():
            fName = "static\\csv\\stockWatchList.csv"
            csvPathStock = os.path.join(BASE_DIR,  fName )
            stock_ticker = form.data['tickerSymbol'].upper()

            columns = ['ticker', 'pid', 'clientid']
            emptydf = pd.DataFrame(columns=columns)
            try:
                df = pd.read_csv(csvPathStock)
            except:
                emptydf.to_csv(csvPathStock, sep=',', index=False)
                df = pd.read_csv(csvPathStock)
            # insertPoint = len([i for i in df['ticker'].values if isinstance(i, str)])
            client_id = [i for i in range(5, 20) if i not in df['clientid'].values ][0]
            if stock_ticker in df['ticker'].values:
                t_msg = "FAILED! "+stock_ticker+ " is already in the STOCK list"
                return self.contextRender(request\
                                            ,msg=t_msg)
            else:
                #create emty csv to deal with file not found error
                fName = "static\\csv\\realtimeData\\" + stock_ticker + "_raw_realtime_ib.csv"
                csvPath = os.path.join(BASE_DIR,  fName ) # original data
                columns = ['Time', 'Open', 'High', 'Low', 'Close']
                try:
                    if datetime.fromtimestamp(os.path.getmtime(csvPath)).date() < \
                                datetime.now(tz=pytz.timezone('US/Eastern')).date():
                        emptyDf = pd.DataFrame(columns=columns)
                        emptyDf.to_csv(csvPath, sep=',', index=False)
                except:
                    emptyDf = pd.DataFrame(columns=columns)
                    emptyDf.to_csv(csvPath, sep=',', index=False)
                insertPoint = len(df['ticker'].values)
                df.loc[insertPoint, 'ticker'] = stock_ticker # df.loc is the trick to add to eend of row
                df.loc[insertPoint, 'clientid'] = client_id
                df.to_csv(csvPathStock, sep=',', index=False)

                t_msg = " Added " + stock_ticker+ " to STOCK list"
                return self.contextRender(request\
                                            ,msg=t_msg)

        #remove a ticker from the forex list
        elif request.method == 'POST' and 'forexRow' in request.POST.keys():
            fName = "static\\csv\\forexWatchList.csv"
            csvPathForex = os.path.join(BASE_DIR,  fName )
            row_number = int(request.POST['forexRow'])
            f_ticker = request.POST['forexTicker']
            df = pd.read_csv(csvPathForex)
            pid_insert_point = df['ticker'].values.tolist().index(f_ticker)
            pid = df['pid'].iloc[pid_insert_point].astype(int)
            try:
                p = psutil.Process(pid)
                p.terminate()
                try:
                    fName_rt_raw = "static\\csv\\realtimeData\\"+f_ticker+"_raw_realtime_ib.csv"
                    fName_rt = "static\\csv\\realtimeData\\"+f_ticker+"_realtime_ib.csv"
                    csvPathForex_rt_raw = os.path.join(BASE_DIR,  fName_rt)
                    csvPathForex_rt = os.path.join(BASE_DIR,  fName_rt_raw)
                    os.remove(csvPathForex_rt_raw)
                    os.remove(csvPathForex_rt)
                except:
                    pass
                df.drop(df.index[row_number], inplace=True)
                df.to_csv(csvPathForex, sep=',', index=False)
                t_msg = "Process terminated! \n Successfully removed CSV and "\
                 + f_ticker+" from FOREX list"
                return self.contextRender(request\
                                            ,msg=t_msg)
            except:
                try:
                    fName_rt_raw = "static\\csv\\realtimeData\\"+f_ticker+"_raw_realtime_ib.csv"
                    fName_rt = "static\\csv\\realtimeData\\"+f_ticker+"_realtime_ib.csv"
                    csvPathForex_rt_raw = os.path.join(BASE_DIR,  fName_rt)
                    csvPathForex_rt = os.path.join(BASE_DIR,  fName_rt_raw)
                    os.remove(csvPathForex_rt_raw)
                    os.remove(csvPathForex_rt)
                except:
                    pass
                df.drop(df.index[row_number], inplace=True)
                df.to_csv(csvPathForex, sep=',', index=False)
                t_msg = "Successfully removed "\
                 + f_ticker+" from FOREX list! \n No active "+ f_ticker+" downloads!"
                return self.contextRender(request\
                                            ,msg=t_msg)

        #remove a ticker from the stock list
        elif request.method == 'POST' and 'stockRow' in request.POST.keys():
            fName = "static\\csv\\stockWatchList.csv"
            csvPathStock = os.path.join(BASE_DIR,  fName )
            row_number = int(request.POST['stockRow'])
            s_ticker = request.POST['stockTicker']
            df = pd.read_csv(csvPathStock)
            pid_insert_point = df['ticker'].values.tolist().index(s_ticker)
            pid = df['pid'].iloc[pid_insert_point].astype(int)
            try:
                # terminate quote downloads
                p = psutil.Process(pid)
                p.terminate()
                #remove csv files
                try:
                    fName_rt_raw = "static\\csv\\realtimeData\\"+s_ticker+"_raw_realtime_ib.csv"
                    fName_rt = "static\\csv\\realtimeData\\"+s_ticker+"_realtime_ib.csv"
                    csvPathForex_rt_raw = os.path.join(BASE_DIR,  fName_rt)
                    csvPathForex_rt = os.path.join(BASE_DIR,  fName_rt_raw)
                    os.remove(csvPathForex_rt_raw)
                    os.remove(csvPathForex_rt)
                except:
                    pass
                # remove from list
                df.drop(df.index[row_number], inplace=True)
                df.to_csv(csvPathStock, sep=',', index=False)
                t_msg = "Process terminated! \n Successfully removed "\
                 + s_ticker+" from STOCK list"
                return self.contextRender(request\
                                            ,msg=t_msg)
            except:
                try:
                    fName_rt_raw = "static\\csv\\realtimeData\\"+s_ticker+"_raw_realtime_ib.csv"
                    fName_rt = "static\\csv\\realtimeData\\"+s_ticker+"_realtime_ib.csv"
                    csvPathForex_rt_raw = os.path.join(BASE_DIR,  fName_rt)
                    csvPathForex_rt = os.path.join(BASE_DIR,  fName_rt_raw)
                    os.remove(csvPathForex_rt_raw)
                    os.remove(csvPathForex_rt)
                except:
                    pass
                df.drop(df.index[row_number], inplace=True)
                df.to_csv(csvPathStock, sep=',', index=False)
                t_msg = " Successfully removed "\
                 + s_ticker+" from STOCK list! \n No active "+ s_ticker+" downloads!"
                return self.contextRender(request\
                                            ,msg=t_msg)

        # get forex quote for a clicked ticker
        elif request.method == 'POST' and 'forexQuote' in request.POST.keys():
            fName = "static\\csv\\forexWatchList.csv"
            csvPathForex = os.path.join(BASE_DIR,  fName )
            f_ticker = request.POST['forexQuote']
            df = pd.read_csv(csvPathForex)
            pid_insert_point = df['ticker'].values.tolist().index(f_ticker)
            try:
                q = psutil.Process(df['pid'].iloc[pid_insert_point].astype(int))
                t_msg = "FAILED to download FOREX "+ f_ticker\
                +"!\n Terminate the ongoing download to start again"
                return self.contextRender(request\
                                            ,msg=t_msg)
            except:
                client_id_no = df['clientid'].iloc[pid_insert_point].astype(int) # type conversion from np dtype to python datatype
                scriptPath= ['E:\\ProgramData\\Anaconda3\\python.exe'\
                            , 'E:\\ProgramData\\Anaconda3\\Scripts\\mysite\\static\\py\\Forex1RealtimeIB.py']
                args = ["-t", f_ticker, "-i", str(client_id_no)]
                scriptPath.extend(args)
                proc1 = subprocess.Popen(scriptPath)
                df['pid'].iloc[pid_insert_point] = proc1.pid
                df.to_csv(csvPathForex, sep=',', index=False)
                if "tws.exe" in (p.name() for p in psutil.process_iter()):
                    try:
                        p = psutil.Process(proc1.pid)
                        t_msg = "Downloading FOREX "+ f_ticker+" now!"
                        return self.contextRender(request\
                                                    ,msg=t_msg)
                    except:
                        t_msg = "FAILED to download FOREX "+ f_ticker+" check TWS status"
                        return self.contextRender(request\
                                                    ,msg=t_msg)
                else:
                    t_msg = "FAILED to download FOREX "+ f_ticker\
                            +" Please lauch TWS and try again "
                    return self.contextRender(request\
                                            ,msg=t_msg)

        # get stock quote for the clicked ticker
        elif request.method == 'POST' and 'stockQuote' in request.POST.keys():
            fName = "static\\csv\\stockWatchList.csv"
            csvPathStock = os.path.join(BASE_DIR,  fName )
            s_ticker = request.POST['stockQuote']
            df = pd.read_csv(csvPathStock)
            pid_insert_point = df['ticker'].values.tolist().index(s_ticker)
            if "tws.exe" not in (p.name() for p in psutil.process_iter()):
                t_msg = "FAILED to download STOCK "+ s_ticker\
                        +" Please lauch TWS and try again "
                return self.contextRender(request\
                                            ,msg=t_msg)
            try:
                q = psutil.Process(df['pid'].iloc[pid_insert_point].astype(int))
                t_msg = "FAILED to download FOREX "+ s_ticker\
                +"!\n Terminate the ongoing download to start again"
                return self.contextRender(request\
                                            ,msg=t_msg)
            except:
                client_id_no = df['clientid'].iloc[pid_insert_point].astype(int)
                scriptPath= ['E:\\ProgramData\\Anaconda3\\python.exe'\
                            , 'E:\\ProgramData\\Anaconda3\\Scripts\\mysite\\static\\py\\USStock1RealTimeIB.py']
                args = ["-t", s_ticker, "-i", str(client_id_no)]
                scriptPath.extend(args)
                proc1 = subprocess.Popen(scriptPath)

                df['pid'].iloc[pid_insert_point] = proc1.pid
                df.to_csv(csvPathStock, sep=',', index=False)
                if "tws.exe" in (p.name() for p in psutil.process_iter()):
                    try:
                        time.sleep(4)
                        p = psutil.Process(proc1.pid)
                        t_msg = "Downloading STOCK "+ s_ticker+" now!"
                        return self.contextRender(request\
                                                    ,msg=t_msg)
                    except:
                        t_msg = "FAILED to download STOCK "+ s_ticker+" check TWS status"
                        return self.contextRender(request\
                                                    ,msg=t_msg)
    #add to live trading list
        elif request.method == 'POST' and 'addtolivetrade' in request.POST.keys():
            fNamelive = "static\\csv\\liveTradeList.csv"
            csvPathLive = os.path.join(BASE_DIR,  fNamelive )
            stock_ticker = request.POST['addtolivetrade']
            columns = ['ticker', 'pid', 'clientid']
            emptydf = pd.DataFrame(columns=columns)
            try:
                df = pd.read_csv(csvPathLive)
            except:
                emptydf.to_csv(csvPathLive, sep=',', index=False)
                df = pd.read_csv(csvPathLive)
            client_id = [i for i in range(20, 25) if i not in df['clientid'].values ][0]
            if len(df.index) == 0:
                if stock_ticker in df['ticker'].values:
                    t_msg = "FAILED! "+stock_ticker+ " is already in the LIVE TRADE list"
                    return self.contextRender(request\
                                                ,msg=t_msg)
                insertPoint = len(df['ticker'].values)
                df.loc[insertPoint, 'ticker'] = stock_ticker # df.loc is the trick to add to eend of row
                df.loc[insertPoint, 'clientid'] = client_id
                df.to_csv(csvPathLive, sep=',', index=False)

                t_msg = " Added " + stock_ticker+ " to LIVE TRADE list"
            else:
                t_msg = " Failed to add " + stock_ticker+ " to LIVE TRADE list. Ccurrently the no of live trades are restricted to '1'!"
            return self.contextRender(request\
                                        ,msg=t_msg)
    # remove ticker from live trade list
        elif request.method == 'POST' and 'livelistRow' in request.POST.keys():
            fNamelive = "static\\csv\\liveTradeList.csv"
            csvPathLive = os.path.join(BASE_DIR,  fNamelive )
            row_number = int(request.POST['livelistRow'])
            f_ticker = request.POST['liveTicker']
            df = pd.read_csv(csvPathLive)
            pid_insert_point = df['ticker'].values.tolist().index(f_ticker)
            pid = df['pid'].iloc[pid_insert_point].astype(int)
            try:
                p = psutil.Process(pid)
                p.terminate()
                df.drop(df.index[row_number], inplace=True)
                df.to_csv(csvPathLive, sep=',', index=False)
                t_msg = "Process terminated! \n Successfully removed "\
                 + f_ticker+" from LIVE trading list"
                return self.contextRender(request\
                                            ,msg=t_msg)
            except:
                df.drop(df.index[row_number], inplace=True)
                df.to_csv(csvPathLive, sep=',', index=False)
                t_msg = "Successfully removed "\
                 + f_ticker+" from LIVE trading list!"
                return self.contextRender(request\
                                            ,msg=t_msg)

    #start trading.. launch algorithm
        elif request.method == 'POST' and 'startrade' in request.POST.keys():
            fNamelive = "static\\csv\\liveTradeList.csv"
            csvPathLive = os.path.join(BASE_DIR,  fNamelive )
            s_ticker = request.POST['startrade']
            df = pd.read_csv(csvPathLive)
            pid_insert_point = df['ticker'].values.tolist().index(s_ticker)
            try:
                q = psutil.Process(df['pid'].iloc[pid_insert_point].astype(int))
                t_msg = "FAILED to start "+ s_ticker\
                +"trade!\n A trade is already in progress"
                return self.contextRender(request\
                                            ,msg=t_msg)
            except:
                client_id_no = 0#df['clientid'].iloc[pid_insert_point].astype(int)
                scriptPath= ['E:\\ProgramData\\Anaconda3\\python.exe'\
                            , 'E:\\ProgramData\\Anaconda3\\Scripts\\mysite\\static\\py\\ExecutionStockUS_IB.py']
                args = ["-t", s_ticker, "-i", str(client_id_no)]
                scriptPath.extend(args)
                proc1 = subprocess.Popen(scriptPath)

                df['pid'].iloc[pid_insert_point] = proc1.pid
                df.to_csv(csvPathLive, sep=',', index=False)
                if "tws.exe" in (p.name() for p in psutil.process_iter()):
                    try:
                        p = psutil.Process(proc1.pid)
                        t_msg = "Launching "+ s_ticker+" trade now!"
                        return self.contextRender(request\
                                                    ,msg=t_msg)
                    except:
                        t_msg = "FAILED to start "+ s_ticker+" check TWS status"
                        return self.contextRender(request\
                                                    ,msg=t_msg)
                else:
                    t_msg = "FAILED to start "+ s_ticker\
                            +"trade. Please lauch TWS and try again "
                    return self.contextRender(request\
                                                ,msg=t_msg)
        elif request.method == 'POST' and '13Fupdate' in request.POST.keys():
            t_msg = "running update"
            return self.contextRender(request\
                                        ,msg=t_msg)

class LiveTradeListRefresh(View):
    def get(self, request, *args, **kwargs):
        fNamelive = "static\\csv\\liveTradeList.csv"
        csvPathLive = os.path.join(BASE_DIR,  fNamelive )
        df = pd.read_csv(csvPathLive)
        list_live = df['ticker'].values
        rt_close_data = []
        if len(df.index) > 0:
            for i in list_live:
                fName_rt = "static\\csv\\realtimeData\\"+i+"_realtime_ib.csv"
                csvPathlive_rt = os.path.join(BASE_DIR,  fName_rt)
                try:
                    df_rt = pd.read_csv(csvPathlive_rt)
                    rt_close_data.append(df_rt['Close'].iloc[-1])
                    atr12m = df_rt['atr12min'].iloc[-1]
                    position = df_rt['position'].iloc[-1]
                    if df_rt['position'].iloc[-2] != 0 and position == 0:
                        p = psutil.Process(df['pid'].iloc[0].astype(int))
                        p.terminate()
                    avgcst = df_rt['avgcost'].iloc[-1]
                    current_price = df_rt['OHLC-Mean'].iloc[-1]
                except:
                    rt_close_data.append(0)
                    atr12m = 0
                    position = 0
                    avgcst = 0
                    current_price = 0
                try:
                    p = psutil.Process(df['pid'].iloc[0].astype(int))
                    trade_status = "<text class='green-letter'>ON</text>"
                except:
                    trade_status = "<text class='red-letter'>OFF</text>"

            dict_live = dict(zip(list_live, rt_close_data))
            if position < 0:
                pnl = abs(position) * (avgcst - current_price)
            elif position > 0:
                pnl = abs(position) * (current_price - avgcst)
            else:
                pnl = 0

            context = {
                "live_dict": dict_live,
                "atr": atr12m,
                "pos": position,
                "cost": avgcst,
                "status" : trade_status,
                "pNl" : pnl,
            }
            return render(request, "ib/liveTradeList.html", context)
        else:
            content_nothing = "<div> No Active trades </div>"
            return HttpResponse(content_nothing)

class forexWatchlistRefresh(View):
    def get(self, request, *args, **kwargs):
        fName = "static\\csv\\forexWatchList.csv"
        csvPathForex = os.path.join(BASE_DIR,  fName )
        the_form = SubmitTickerSymbolForm()
        df = pd.read_csv(csvPathForex)
        list_forex = df['ticker'].values
        rt_close_data = []
        atr_list = []
        dld_btn = "<input class='button dwnld-btn red-btn' title='Download real time quote' value='&#x21e9 &#x204e' type='submit'>"
        for i, j in enumerate(list_forex):
            if df['pid'].iloc[i].astype(int) != -2147483648: # negative number is the int value of nan
                fName_rt = "static\\csv\\realtimeData\\"+j+"_raw_realtime_ib.csv"
                csvPathForex_rt = os.path.join(BASE_DIR,  fName_rt)
                fname_computed = "static\\csv\\realtimeData\\"+j+"_realtime_ib.csv"
                csv_path_computed = os.path.join(BASE_DIR, fname_computed)
                try:
                    p = psutil.Process(df['pid'].iloc[i].astype(int))
                    dld_btn = "<input class='button dwnld-btn' title='Download real time quote' value='&#x21e9' type='submit'>"
                except:
                    dld_btn = "<input class='button dwnld-btn red-btn' title='Download real time quote' value='&#x21e9 &#x204e' type='submit'>"
                    os.remove(csv_path_computed)
                    os.remove(csvPathForex_rt)
                try:
                    df_rt = pd.read_csv(csvPathForex_rt)
                    df_computed = pd.read_csv(csv_path_computed)
                    rt_close_data.append(df_rt['Close'].iloc[-1])
                    atr_list.append(round(df_computed['atr12min'].iloc[-1], 2))
                except:
                    rt_close_data.append(0)
                    atr_list.append(0)
            else:
                rt_close_data.append(0)
                atr_list.append(0)
        master_list = [{'ticker': t[0], 'close': t[1], 'atr':t[2]}\
                        for t in zip(list_forex, rt_close_data, atr_list)]
        # dict_stock = dict(zip(list_stock, rt_close_data))
        context = {
            "form": the_form,
            "forex_dict": master_list,
            "dwnld_btn": dld_btn,
            # "atr": atr_list,
        }
        return render(request, "ib/forexWatchlist.html", context)

class stockWatchlistRefresh(View):
    '''ajax async view to refresh STOCK watch list'''
    def get(self, request, *args, **kwargs):
        fName = "static\\csv\\stockWatchList.csv"
        csvPathStock = os.path.join(BASE_DIR,  fName )
        the_form = SubmitTickerSymbolForm()
        df = pd.read_csv(csvPathStock)
        list_stock = df['ticker'].tolist()
        rt_close_data = []
        atr_list = []
        dld_btn = "<input class='button dwnld-btn red-btn' title='Download real time quote' value='&#x21e9 &#x204e' type='submit'>"
        for i, j in enumerate(list_stock):
            if df['pid'].iloc[i].astype(int) != -2147483648: # negative number is the int value of nan
                fName_rt = "static\\csv\\realtimeData\\"+j+"_raw_realtime_ib.csv"
                fname_computed = "static\\csv\\realtimeData\\"+j+"_realtime_ib.csv"
                csv_path_computed = os.path.join(BASE_DIR, fname_computed)
                csvPathStock_rt = os.path.join(BASE_DIR,  fName_rt)

                try:
                    p = psutil.Process(df['pid'].iloc[i].astype(int))
                    dld_btn = "<input class='button dwnld-btn' title='Download real time quote' value='&#x21e9' type='submit'>"
                except:
                    dld_btn = "<input class='button dwnld-btn red-btn' title='Download real time quote' value='&#x21e9 &#x204e' type='submit'>"
                    os.remove(csv_path_computed)
                    os.remove(csvPathStock_rt)
                finally:
                    pass
                try:
                    df_rt = pd.read_csv(csvPathStock_rt)
                    df_computed = pd.read_csv(csv_path_computed)
                    rt_close_data.append(df_rt['Close'].iloc[-1])
                    atr_list.append(round(df_computed['atr12min'].iloc[-1], 2))
                except:
                    rt_close_data.append(0)
                    atr_list.append(0)
            else:
                rt_close_data.append(0)
                atr_list.append(0)
        master_list = [{'ticker': t[0], 'close': t[1], 'atr':t[2]}\
                        for t in zip(list_stock, rt_close_data, atr_list)]
        # dict_stock = dict(zip(list_stock, rt_close_data))
        context = {
            "form": the_form,
            "stock_dict": master_list,
            "dwnld_btn": dld_btn,
            # "atr": atr_list,
        }
        return render(request, "ib/stockWatchlist.html", context)

class MarketStatusView(View):
    '''ajax async view to update market open/close'''
    def __init__(self):
        self.local_time = datetime.now().strftime('%I:%M:%S %p %A')
        self.ny_time = datetime.now(tz=pytz.timezone('US/Eastern')).strftime('%I:%M:%S %p %A')
        self.market_status = self.marketStatus
    def marketStatus(self):
        if datetime.now(tz=pytz.timezone('US/Eastern')).weekday() not in [5, 6]:
            ny = datetime.now(tz=pytz.timezone('US/Eastern'))
            nynow = ny.time()
            if time(9, 30) <= nynow <= time(16, 00):
                return "<text class='green-letter'>Market is open now</text>"
            else:
                return "<text class='red-letter'>Market is closed now</text>"
        else:
            return "<text class='red-letter'>Market is closed now</text>"

    def contextRender(self, request,*args,**kwargs):
        context = {
            "local_time": self.local_time,
            "nytime": self.ny_time,
            "marketstatus": self.market_status,
        }
        return render(request, "ib/marketStatus.html", context)
    def get(self, request, *args, **kwargs):
        return self.contextRender(request)
