'''
aneeshpanoli@gmail.com. All rights reserved. Not for distribution.
For my own personal use only.

This function is called from ***Program_modded.py***.
rawData() takes OHLC as a list and creates csv out of it.
realtimeData() computes features in the above data
buySellRecommendation() evaluates the features to come up with buy/sell signals
'''

import os
import pandas as pd
from datetime import datetime
import pytz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #points to static folder

def rawData(tickr, stockData, interval):
    fName = "csv\\realtimeData\\" + tickr + "_raw_realtime_ib.csv"
    csvPath = os.path.join(BASE_DIR,  fName ) # original data
    columns = ['Time', 'Open', 'High', 'Low', 'Close']
    try:
        if datetime.fromtimestamp(os.path.getmtime(csvPath)).date() < \
                    datetime.now(tz=pytz.timezone('US/Eastern')).date():
            df = pd.DataFrame(columns=columns)
        else:
            df = pd.read_csv(csvPath)
    except:
        df = pd.DataFrame(columns=columns)

    df.loc[len(df.index)] = stockData # write data to the last row
    df.tail(25).to_csv(csvPath, sep=',', index=False)
    n = int(interval/-5) # IB pulls quote every 5secs use this to adjust the time interval
    if len(df.index) > abs(n)+1: # if an interval is specified return this
        return [df['Time'].iloc[-1]\
                , df['Open'].iloc[n]\
                , df['High'].iloc[n:].max()\
                , df['Low'].iloc[n:].min()\
                , df['Close'].iloc[-1]]
    else:
        return [df['Time'].iloc[-1]\
                , df['Open'].iloc[-1]\
                , df['High'].iloc[-1]\
                , df['Low'].iloc[-1]\
                , df['Close'].iloc[-1]]


def realTimeData(tickr, stockData, interval, position, cost):
    """bar interval in seconds
    30sec = 25 rows (5*5)"""
    stockData = rawData(tickr, stockData, interval)
    fName = "csv\\realtimeData\\" + tickr + "_realTime_ib.csv"
    csvPath = os.path.join(BASE_DIR,  fName ) # original data
    columns = ['Time', 'Open', 'High', 'Low', 'Close', 'OHLC-Mean', 'stopPriceBuy', 'stopPriceSell'
                , 'buysell', 'position', 'avgcost', 'atr12min']

    try:## check if the file exists
        if datetime.fromtimestamp(os.path.getmtime(csvPath), tz=pytz.timezone('US/Eastern')).date() < \
                    datetime.now(tz=pytz.timezone('US/Eastern')).date(): # check if the file is older than a day
            df = pd.DataFrame(columns=columns)
        else:
            df = pd.read_csv(csvPath)
    except:# if file doest exist, create new file
        df = pd.DataFrame(columns=columns)
    dfLength = len(df.index)
    stockData.append(round(sum(stockData[1:])/len(stockData[1:]), 2)) # calculate OHLC average
    if dfLength < 12: # need atleast 5 rows to do the necessory calculation. otherwise fill with 0
        stockData.extend((0, 0, 0, position, cost, 0))
    else:
        #----------------------------------------------------------------
        # value for moving stop price
        # do not modify aything in this section
        lowToLowhighToHigh = []
        for i in range(-1, -12, -1):
            lowToLowhighToHigh.append(abs(df['Low'].iloc[i-1] - df['Low'].iloc[i]))
            lowToLowhighToHigh.append(abs(df['High'].iloc[i-1] - df['High'].iloc[i]))

        #----------------------------------------------------------------
        #----------- to make sure that the stops never move in the opposite direction---------
        # adding this directly to pandas dataframe will cause the value to keep on
        # incrementing or decrementing
        # we need this behavior to modify out stop order when a position exists
        # otherwise we want the computation to proceed unconditionally/normally
        # therfore when position size is > 0 we modify the last cell to reflect stopPrice
        # if short we want the value to decrement and vice versa for long
        stopPriceBuy = df['High'].iloc[-16:].max() + max(lowToLowhighToHigh)
        stopPriceSell = df['Low'].iloc[-16:].min() - max(lowToLowhighToHigh)
        if position > 0:
            if df['stopPriceSell'].iloc[-1] > 0 and stopPriceSell < df['stopPriceSell'].iloc[-1]:
                stopPriceSell = df['stopPriceSell'].iloc[-1]
        elif position < 0:
            if df['stopPriceBuy'].iloc[-1] > 0 and stopPriceBuy > df['stopPriceBuy'].iloc[-1]:
                stopPriceBuy = df['stopPriceBuy'].iloc[-1]
        # long short decision making
        if len(df.index) > 51:
            atr12min = df['High'].iloc[-50:].max() - df['Low'].iloc[-50:].min()
            currentBarAvg = df['OHLC-Mean'].iloc[-1]
            previousBarAvg = df['OHLC-Mean'].iloc[-2]
            sma5 = df['OHLC-Mean'].iloc[-21:].mean()
            if previousBarAvg <= sma5 and currentBarAvg > sma5: #LONG
                recommed = 1
            elif previousBarAvg >= sma5 and currentBarAvg < sma5: #SHORT
                recommed = 2
            else:
                recommed = 0
        else:
            recommed = 0
            atr12min = 0
        # append data to the stockData list
        stockData.extend((stopPriceBuy, stopPriceSell, recommed\
                        , position, cost, atr12min))
    df.loc[dfLength] = stockData # data should be equal to number of columns
    df.tail(300).to_csv(csvPath, sep=',', index=False) # prevents file from getting too big
    # with open(csvPath, 'a', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(stockData) # write stockData to file

def buySellRecommendation(tickr, positionSize, cost):
    '''
    dont use the to pass values to d3 csv.
    instead use it to pass buy sell to Program_modded.py
    this can be incorporated to realtimeData()
    - upper limit for rows set at line 96 to 300
    # how to find the index of max and min values?
    # locationOf15minHigh = df['High'].iloc[-100:].idxmax() #iindex of the max value
    # locationOf15minLow = df['Low'].iloc[-100:].idxmin() # index of the min value

    # what does support means - ideally the low of the next  bar should liewithin the last quarter of the previos bar
    # calculate the high-low difference of the last bar ddivide by 4 - then if the current bar low is
    # wihtin the +/- range
    # or if the high of the last bar is with in the
    # --- how to avoid trading choppiness
    '''
    fName = "csv\\realtimeData\\" + tickr + "_realTime_ib.csv"
    csvPath = os.path.join(BASE_DIR,  fName)
    df = pd.read_csv(csvPath)
    # LONG/SHORT decision making
    if len(df.index) > 51:
        atr12min = df['atr12min'].iloc[-50:].mean()
        if atr12min > 0.5:
            atr12min = 0.5
        stopPriceBuy = df['stopPriceBuy'].iloc[-1]
        stopPriceSell = df['stopPriceSell'].iloc[-1]
        decision = "no"
        if abs(df['High'].iloc[-1] - cost) >= atr12min \
            or abs(df['Low'].iloc[-1] - cost) >= atr12min:
            if positionSize == 500:
                decision = "sellhalf"
            elif positionSize == -500:
                decision = "buyhalf"


        if df['buysell'].iloc[-1] == 1 and atr12min > 0.03:
            recommend = ["Buy"\
                        , stopPriceBuy\
                        , stopPriceSell\
                        , decision]
        elif df['buysell'].iloc[-1] == 2 and atr12min > 0.03 :
            recommend = ["Sell"\
                        , stopPriceBuy\
                        , stopPriceSell\
                        , decision] # Sell
        else:
            recommend = [0\
                        , stopPriceBuy\
                        , stopPriceSell\
                        , decision\
                        , atr12min]
        return recommend
    else:
        return [0]
