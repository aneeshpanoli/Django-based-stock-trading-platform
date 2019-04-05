from django.conf.urls.static import static
from packages import stocklist
import os
import pandas as pd
import numpy as np
from pandas import DataFrame
import pandas_datareader as pdd
from datetime import datetime
from dateutil.relativedelta import relativedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #points to static folder


def recommendation(tickr):
    # fNameClean = "csv\cleanData\\" + tickr + "_clean.csv"
    # csvPathClean = os.path.join(BASE_DIR,  fNameClean )
    fnameSim = "csv\\simulationData\\" + tickr + "_historic_clean_sim.csv"
    csvPathSim = os.path.join(BASE_DIR,  fnameSim)
    fnameD3 = "csv\\simulationData\\" + tickr + "_historic_clean_D3.csv"
    csvPathD3 = os.path.join(BASE_DIR,  fnameD3)
    df = pd.read_csv(csvPathSim)

    columns =['Open', 'High', 'Low', 'Close']
    dfb = pd.read_csv(csvPathSim, usecols=columns)
    dfb['BuySell'] = np.nan
    dfb['BuySell'].iloc[-1] = "Buy"
    try:
        os.remove(csvPathD3)
    except:
        pass
    dfb.to_csv(csvPathD3, sep=',', index=False)
recommendation('jnj')
