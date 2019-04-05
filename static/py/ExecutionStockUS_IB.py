"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable.

 modified by - aneeshpanoli@gmail.com. All rights reserved. Not for distribution.
 for my own personal use
"""

import sys
import argparse
import datetime
import collections
import inspect
#-----------------------------------------------------
import realTimeDataIB # my program that does the computation
from watchListForex import WatchListForex
import timeit
#--------------------------------------------------------
import logging
import time
import os.path


from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper

# types
from ibapi.common import *
from ibapi.order_condition import *
from ibapi.contract import *
from ibapi.order import *
from ibapi.order_state import *
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.scanner import ScannerSubscription
from ibapi.ticktype import *
from watchListStocks import WatchListStocks

from ibapi.account_summary_tags import *

from ContractSamples import ContractSamples
from OrderSamples import OrderSamples
from AvailableAlgoParams import AvailableAlgoParams
from ScannerSubscriptionSamples import ScannerSubscriptionSamples
from FaAllocationSamples import FaAllocationSamples


def SetupLogger():
    if not os.path.exists("log"):
        os.makedirs("log")

    time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

    timefmt = '%y%m%d_%H:%M:%S'

    # logging.basicConfig( level=logging.DEBUG,
    #                    format=recfmt, datefmt=timefmt)
    logging.basicConfig(filename=time.strftime("log/pyibapi.%y%m%d_%H%M%S.log"),
                        filemode="w",
                        level=logging.INFO,
                        format=recfmt, datefmt=timefmt)
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logger.addHandler(console)


def printWhenExecuting(fn):
    def fn2(self):
        print("   doing", fn.__name__)
        fn(self)
        print("   done w/", fn.__name__)

    return fn2


class Activity(Object):
    def __init__(self, reqMsgId, ansMsgId, ansEndMsgId, reqId):
        self.reqMsdId = reqMsgId
        self.ansMsgId = ansMsgId
        self.ansEndMsgId = ansEndMsgId
        self.reqId = reqId


class RequestMgr(Object):
    def __init__(self):
        # I will keep this simple even if slower for now: only one list of
        # requests finding will be done by linear search
        self.requests = []

    def addReq(self, req):
        self.requests.append(req)

    def receivedMsg(self, msg):
        pass


# ! [socket_declare]
class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
        # ! [socket_declare]

        # how many times a method is called to see test coverage
        self.clntMeth2callCount = collections.defaultdict(int)
        self.clntMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nReq = collections.defaultdict(int)
        self.setupDetectReqId()

    def countReqId(self, methName, fn):
        def countReqId_(*args, **kwargs):
            self.clntMeth2callCount[methName] += 1
            idx = self.clntMeth2reqIdIdx[methName]
            if idx >= 0:
                sign = -1 if 'cancel' in methName else 1
                self.reqId2nReq[sign * args[idx]] += 1
            return fn(*args, **kwargs)

        return countReqId_

    def setupDetectReqId(self):

        methods = inspect.getmembers(EClient, inspect.isfunction)
        for (methName, meth) in methods:
            if methName != "send_msg":
                # don't screw up the nice automated logging in the send_msg()
                self.clntMeth2callCount[methName] = 0
                # logging.debug("meth %s", name)
                sig = inspect.signature(meth)
                for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                    (paramName, param) = pnameNparam
                    if paramName == "reqId":
                        self.clntMeth2reqIdIdx[methName] = idx

                setattr(TestClient, methName, self.countReqId(methName, meth))

                # print("TestClient.clntMeth2reqIdIdx", self.clntMeth2reqIdIdx)


# ! [ewrapperimpl]
class TestWrapper(wrapper.EWrapper):
    # ! [ewrapperimpl]
    def __init__(self):
        wrapper.EWrapper.__init__(self)

        self.wrapMeth2callCount = collections.defaultdict(int)
        self.wrapMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nAns = collections.defaultdict(int)
        self.setupDetectWrapperReqId()

    # TODO: see how to factor this out !!

    def countWrapReqId(self, methName, fn):
        def countWrapReqId_(*args, **kwargs):
            self.wrapMeth2callCount[methName] += 1
            idx = self.wrapMeth2reqIdIdx[methName]
            if idx >= 0:
                self.reqId2nAns[args[idx]] += 1
            return fn(*args, **kwargs)

        return countWrapReqId_

    def setupDetectWrapperReqId(self):

        methods = inspect.getmembers(wrapper.EWrapper, inspect.isfunction)
        for (methName, meth) in methods:
            self.wrapMeth2callCount[methName] = 0
            # logging.debug("meth %s", name)
            sig = inspect.signature(meth)
            for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                (paramName, param) = pnameNparam
                # we want to count the errors as 'error' not 'answer'
                if 'error' not in methName and paramName == "reqId":
                    self.wrapMeth2reqIdIdx[methName] = idx

            setattr(TestWrapper, methName, self.countWrapReqId(methName, meth))

            # print("TestClient.wrapMeth2reqIdIdx", self.wrapMeth2reqIdIdx)


# this is here for documentation generation
"""
#! [ereader]
        #this code is in Client::connect() so it's automatically done, no need
        # for user to do it
        self.reader = reader.EReader(self.conn, self.msg_queue)
        self.reader.start()   # start thread

#! [ereader]
"""


# ! [socket_init]
class TestApp(TestWrapper, TestClient):
    def __init__(self, tickrSymbol):
        self.INSTRUMENT = WatchListStocks.USStockAtSmart1(tickrSymbol.upper())
        # self.INSTRUMENT = WatchListForex.EurGbpFx(tickrSymbol.upper())
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        # ! [socket_init]
        self.nKeybInt = 0
        self.started = False
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.reqId2nErr = collections.defaultdict(int)
        self.globalCancelOnly = False
        self.tickr = self.INSTRUMENT.symbol # my add,

    def dumpTestCoverageSituation(self):
        for clntMeth in sorted(self.clntMeth2callCount.keys()):
            logging.debug("ClntMeth: %-30s %6d" % (clntMeth,
                                                   self.clntMeth2callCount[clntMeth]))

        for wrapMeth in sorted(self.wrapMeth2callCount.keys()):
            logging.debug("WrapMeth: %-30s %6d" % (wrapMeth,
                                                   self.wrapMeth2callCount[wrapMeth]))

    def dumpReqAnsErrSituation(self):
        logging.debug("%s\t%s\t%s\t%s" % ("ReqId", "#Req", "#Ans", "#Err"))
        for reqId in sorted(self.reqId2nReq.keys()):
            nReq = self.reqId2nReq.get(reqId, 0)
            nAns = self.reqId2nAns.get(reqId, 0)
            nErr = self.reqId2nErr.get(reqId, 0)
            logging.debug("%d\t%d\t%s\t%d" % (reqId, nReq, nAns, nErr))

    @iswrapper
    # ! [connectack]
    def connectAck(self):
        if self.async:
            self.startApi()

    # ! [connectack]

    @iswrapper
    # ! [nextvalidid]
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)

        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        # ! [nextvalidid]

        # we can start now
        self.start()

    def start(self):
        if self.started:
            return

        self.started = True

        if self.globalCancelOnly:
            print("Executing GlobalCancel only")
            self.reqGlobalCancel()
        else:
            print("Executing requests")
            # self.reqGlobalCancel()
            # self.marketDataType_req()
            self.accountOperations_req()
            # self.tickDataOperations_req()
            # self.marketDepthOperations_req()
            self.realTimeBars_req()
            # self.historicalDataRequests_req()
            # self.optionsOperations_req()
            # self.marketScanners_req()
            # self.reutersFundamentals_req()
            # self.bulletins_req()
            # self.contractOperations_req()
            # self.contractNewsFeed_req()
            # self.miscelaneous_req()
            # self.linkingOperations()
            # self.financialAdvisorOperations()
            # self.orderOperations_req()
            print("Executing requests ... finished")

    def keyboardInterrupt(self):
        self.nKeybInt += 1
        if self.nKeybInt == 1:
            self.stop()
        else:
            print("Finishing test")
            self.done = True

    def stop(self):
        print("Executing cancels")
        # self.orderOperations_cancel()
        self.accountOperations_cancel()
        # self.tickDataOperations_cancel()
        # self.marketDepthOperations_cancel()
        self.realTimeBars_cancel()
        # self.historicalDataRequests_cancel()
        # self.optionsOperations_cancel()
        # self.marketScanners_cancel()
        # self.reutersFundamentals_cancel()
        # self.bulletins_cancel()
        print("Executing cancels ... finished")

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    @iswrapper
    # ! [error]
    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        print("Error. Id: ", reqId, " Code: ", errorCode, " Msg: ", errorString)

    # ! [error] self.reqId2nErr[reqId] += 1


    @iswrapper
    def winError(self, text: str, lastError: int):
        super().winError(text, lastError)

    @iswrapper
    # ! [openorder]
    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        super().openOrder(orderId, self.tickr, order, orderState)
        # print("OpenOrder. ID:", orderId, contract.symbol, contract.secType,
        #       "@", contract.exchange, ":", order.action, order.orderType,
        #       order.totalQuantity, orderState.status)
        # ! [openorder]
        if contract.symbol == self.tickr:
            self.openOrderId = orderId


    @iswrapper
    # ! [openorderend]
    def openOrderEnd(self):
        super().openOrderEnd()
        # print("OpenOrderEnd")
        # ! [openorderend]

        logging.debug("Received %d openOrders", len(self.permId2ord))

    @iswrapper
    # ! [orderstatus]
    def orderStatus(self, orderId: OrderId, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld)
        # print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", filled,
        #       "Remaining:", remaining, "AvgFillPrice:", avgFillPrice,
        #       "PermId:", permId, "ParentId:", parentId, "LastFillPrice:",
        #       lastFillPrice, "ClientId:", clientId, "WhyHeld:", whyHeld)

    # ! [orderstatus]


    @printWhenExecuting
    def accountOperations_req(self):
        # Requesting managed accounts***/
        # ! [reqmanagedaccts]
        # self.reqManagedAccts()
        # ! [reqmanagedaccts]
        # Requesting accounts' summary ***/

        # ! [reqaaccountsummary]
        # self.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)
        # ! [reqaaccountsummary]

        # ! [reqaaccountsummaryledger]
        # self.reqAccountSummary(9002, "All", "$LEDGER")
        # ! [reqaaccountsummaryledger]

        # ! [reqaaccountsummaryledgercurrency]
        # self.reqAccountSummary(9003, "All", "$LEDGER:EUR")
        # ! [reqaaccountsummaryledgercurrency]

        # ! [reqaaccountsummaryledgerall]
        # self.reqAccountSummary(9004, "All", "$LEDGER:ALL")
        # ! [reqaaccountsummaryledgerall]

        # Subscribing to an account's information. Only one at a time!
        # ! [reqaaccountupdates]
        # self.reqAccountUpdates(True, self.account)
        # ! [reqaaccountupdates]

        # ! [reqaaccountupdatesmulti]
        # self.reqAccountUpdatesMulti(9005, self.account, "", True)
        # ! [reqaaccountupdatesmulti]

        # Requesting all accounts' positions.
        # ! [reqpositions]
        self.reqPositions()
        # ! [reqpositions]

        # ! [reqpositionsmulti]
        # self.reqPositionsMulti(9006, self.account, "")
        # ! [reqpositionsmulti]

        # ! [reqfamilycodes]
        # self.reqFamilyCodes()
        # ! [reqfamilycodes]

    @printWhenExecuting
    def accountOperations_cancel(self):
        # ! [cancelaaccountsummary]
        self.cancelAccountSummary(9001)
        self.cancelAccountSummary(9002)
        self.cancelAccountSummary(9003)
        self.cancelAccountSummary(9004)
        # ! [cancelaaccountsummary]

        # ! [cancelaaccountupdates]
        self.reqAccountUpdates(False, self.account)
        # ! [cancelaaccountupdates]

        # ! [cancelaaccountupdatesmulti]
        self.cancelAccountUpdatesMulti(9005)
        # ! [cancelaaccountupdatesmulti]

        # ! [cancelpositions]
        self.cancelPositions()
        # ! [cancelpositions]

        # ! [cancelpositionsmulti]
        self.cancelPositionsMulti(9006)
        # ! [cancelpositionsmulti]

    @iswrapper
    # ! [managedaccounts]
    def managedAccounts(self, accountsList: str):
        super().managedAccounts(accountsList)
        print("Account list: ", accountsList)
        # ! [managedaccounts]

        self.account = accountsList.split(",")[0]





    @iswrapper
    # ! [updateaccounttime]
    def updateAccountTime(self, timeStamp: str):
        super().updateAccountTime(timeStamp)
        print("UpdateAccountTime. Time:", timeStamp)

    # ! [updateaccounttime]


    @iswrapper
    # ! [accountdownloadend]
    def accountDownloadEnd(self, accountName: str):
        super().accountDownloadEnd(accountName)
        print("Account download finished:", accountName)

    # ! [accountdownloadend]


    @iswrapper
    # ! [position]
    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        super().position(account, contract, position, avgCost)
        # print("Position.", account, "Symbol:", contract.symbol, "SecType:",
        #       contract.secType, "Currency:", contract.currency,
        #       "Position:", position, "Avg cost:", avgCost)
        if contract.symbol == self.tickr:
            self.positionExist = position
            self.avgcost = avgCost
        # self.cost = round(avgCost, 5)

    # ! [position]


    @iswrapper
    # ! [positionend]
    def positionEnd(self):
        super().positionEnd()
        print("PositionEnd")

    # ! [positionend]




    @printWhenExecuting
    def realTimeBars_req(self):
        # Requesting real time bars
        # ! [reqrealtimebars]
        # self.reqRealTimeBars(3101, ContractSamples.USStockAtSmart(), 5, "MIDPOINT", True, [])
        print (self.reqRealTimeBars(3001, self.INSTRUMENT, 5, "MIDPOINT", True, []))
        # ! [reqrealtimebars]


    @printWhenExecuting
    def realTimeBars_cancel(self):
        # Canceling real time bars
        # ! [cancelrealtimebars]
        self.cancelRealTimeBars(3101)
        self.cancelRealTimeBars(3001)
        # ! [cancelrealtimebars]



    @iswrapper
    # ! [headTimestamp]
    def headTimestamp(self, reqId:int, headTimestamp:str):
        print("HeadTimestamp: ", reqId, " ", headTimestamp)
    # ! [headTimestamp]

    @iswrapper
    # ! [securityDefinitionOptionParameter]
    def securityDefinitionOptionParameter(self, reqId: int, exchange: str,
                                          underlyingConId: int, tradingClass: str, multiplier: str,
                                          expirations: SetOfString, strikes: SetOfFloat):
        super().securityDefinitionOptionParameter(reqId, exchange,
                                                  underlyingConId, tradingClass, multiplier, expirations, strikes)
        print("Security Definition Option Parameter. ReqId:%d Exchange:%s "
              "Underlying conId: %d TradingClass:%s Multiplier:%s Exp:%s Strikes:%s",
              reqId, exchange, underlyingConId, tradingClass, multiplier,
              ",".join(expirations), ",".join(str(strikes)))

    # ! [securityDefinitionOptionParameter]


    @iswrapper
    # ! [securityDefinitionOptionParameterEnd]
    def securityDefinitionOptionParameterEnd(self, reqId: int):
        super().securityDefinitionOptionParameterEnd(reqId)
        print("Security Definition Option Parameter End. Request: ", reqId)

    # ! [securityDefinitionOptionParameterEnd]


    @iswrapper
    # ! [smartcomponents]
    def smartComponents(self, reqId:int, map:SmartComponentMap):
        super().smartComponents(reqId, map)
        print("smartComponents: ")
        for exch in map:
            print(exch.bitNumber, ", Exchange Name: ", exch.exchange, ", Letter: ", exch.exchangeLetter)
    # ! [smartcomponents]

    @printWhenExecuting
    def miscelaneous_req(self):
        # Request TWS' current time ***/
        self.reqCurrentTime()
        # Setting TWS logging level  ***/
        self.setServerLogLevel(1)

    @printWhenExecuting
    def linkingOperations(self):
        self.verifyRequest("a name", "9.71")
        self.verifyMessage("apiData")
        self.verifyAndAuthMessage("apiData", "xyz")
        self.verifyAndAuthRequest("a name", "9.71", "key")

        # ! [querydisplaygroups]
        self.queryDisplayGroups(19001)
        # ! [querydisplaygroups]

        # ! [subscribetogroupevents]
        self.subscribeToGroupEvents(19002, 1)
        # ! [subscribetogroupevents]

        # ! [updatedisplaygroup]
        self.updateDisplayGroup(19002, "8314@SMART")
        # ! [updatedisplaygroup]

        # ! [subscribefromgroupevents]
        self.unsubscribeFromGroupEvents(19002)
        # ! [subscribefromgroupevents]

    @iswrapper
    # ! [displaygrouplist]
    def displayGroupList(self, reqId: int, groups: str):
        super().displayGroupList(reqId, groups)
        print("DisplayGroupList. Request: ", reqId, "Groups", groups)

    # ! [displaygrouplist]


    @iswrapper
    # ! [displaygroupupdated]
    def displayGroupUpdated(self, reqId: int, contractInfo: str):
        super().displayGroupUpdated(reqId, contractInfo)
        print("displayGroupUpdated. Request:", reqId, "ContractInfo:", contractInfo)

    # ! [displaygroupupdated]


    @printWhenExecuting
    def orderOperations_req(self):
        pass

        # Placing/modifying an order - remember to ALWAYS increment the
        # nextValidId after placing an order so it can be used for the next one!
        # Note if there are multiple clients connected to an account, the
        # order ID must also be greater than all order IDs returned for orders
        # to orderStatus and openOrder to this client.
        #

    @iswrapper
    # ! [realtimebar]
    # using realtimebar instead of order operations since it updatese every 5 seconds
    def realtimeBar(self, reqId: TickerId, time: int, open: float, high: float,
                    low: float, close: float, volume: int, wap: float,
                    count: int):
        start = timeit.default_timer()
        # Requesting the next valid id ***/
        # ! [reqids]
        # The parameter is always ignored.
        self.reqIds(-1)
        # ! [reqids]

        # Requesting all open orders ***/
        # ! [reqallopenorders]
        self.reqAllOpenOrders()
        # ! [reqallopenorders]

        # Taking over orders to be submitted via TWS ***/
        # ! [reqautoopenorders]
        self.reqAutoOpenOrders(True)
        # ! [reqautoopenorders]

        # Requesting this API client's orders ***/
        # ! [reqopenorders]
        self.reqOpenOrders()
        # ! [reqopenorders]
        try:
            print (self.avgcost)
        except:
            self.avgcost = 0
        try:
            print (self.positionExist) # current number of shares
        except:
            self.positionExist = 0.0 # to fix error when position table is empty
        self.simplePlaceOid = self.nextOrderId()
        buyOrSell = realTimeDataIB.buySellRecommendation(self.tickr, self.positionExist, self.avgcost)
        if buyOrSell == [0]:
            print ("Not enough data to perform computation!!")
        else:
            print (buyOrSell)
        try:
            print (self.tickr)
        except:
            pass
        print ("Currently you have", self.positionExist, "shares in", self.tickr)

# initial order placement
        if self.positionExist == 0.0:
            if  buyOrSell[0] == "Buy":
                stopPrice = round(buyOrSell[2], 2)
                self.placeOrder(self.nextOrderId(), self.INSTRUMENT,
                                OrderSamples.MarketOrder("BUY", 500)) # market order
                self.placeOrder(self.nextOrderId(), self.INSTRUMENT,
                                OrderSamples.Stop("SELL", 500, stopPrice)) # stop order

            elif buyOrSell[0] == "Sell":
                stopPrice = round(buyOrSell[1], 2)
                self.placeOrder(self.nextOrderId(), self.INSTRUMENT,
                                OrderSamples.MarketOrder("SELL", 500))
                self.placeOrder(self.nextOrderId(), self.INSTRUMENT,
                                OrderSamples.Stop("BUY", 500, stopPrice))

#-----------------------------------------------------------------------------------------
# move stop order with market
# impliment time based exit
# implement taking out half of the shares at a fixed price
        elif self.positionExist == 500 and buyOrSell[3] == "no":
            stopPriceSell = round(buyOrSell[2], 2)
            self.placeOrder(self.openOrderId, self.INSTRUMENT,
                            OrderSamples.Stop("SELL", 500, stopPriceSell))

        elif self.positionExist == -500 and buyOrSell[3] == "no":
            stopPriceBuy = round(buyOrSell[1], 2)
            self.placeOrder(self.openOrderId, self.INSTRUMENT,
                            OrderSamples.Stop("BUY", 500, stopPriceBuy))

        #-----------------------------------------------------------------------------------------
        # move stop order with market
        # impliment time based exit
        # implement taking out half of the shares at a fixed price
        elif self.positionExist == 250 and buyOrSell[3] == "no":
            stopPriceSell = round(buyOrSell[2], 2)
            self.placeOrder(self.openOrderId, self.INSTRUMENT,
                            OrderSamples.Stop("SELL", 250, stopPriceSell))
        #
        elif self.positionExist == -250 and buyOrSell[3] == "no":
            stopPriceBuy = round(buyOrSell[1], 2)
            self.placeOrder(self.openOrderId, self.INSTRUMENT,
                                    OrderSamples.Stop("BUY", 250, stopPriceBuy))
        elif self.positionExist == 500 and buyOrSell[3]  == "sellhalf":
            stopPriceSell = round(buyOrSell[2], 2)
            self.placeOrder(self.openOrderId, self.INSTRUMENT,
                                    OrderSamples.Stop("SELL", 250, stopPriceSell))
            self.placeOrder(self.nextOrderId(), self.INSTRUMENT,
                            OrderSamples.MarketOrder("SELL", 250))
        # elif buyOrSell[3] == "sellall":
        #     self.placeOrder(self.nextOrderId(), self.INSTRUMENT,
        #                     OrderSamples.MarketOrder("SELL", self.positionExist))
        elif self.positionExist == -500 and buyOrSell[3] == "buyhalf":
            stopPriceBuy = round(buyOrSell[1], 2)
            self.placeOrder(self.openOrderId, self.INSTRUMENT,
                                    OrderSamples.Stop("BUY", 250, stopPriceBuy))
            self.placeOrder(self.nextOrderId(), self.INSTRUMENT,
                            OrderSamples.MarketOrder("BUY", 250))

        stop = timeit.default_timer()
        print ("Time elapsed:", stop - start)
#================================END==============================================
        # start = timeit.default_timer()
        # # super().realtimeBar(reqId, time, open, high, low, close, volume, wap, count)
        # # stockData = [self.tickr, time, open, high, low, close]
        # # print (stockData)
        # # interval = 5
        # # realTimeDataIB.realTimeData(self.tickr, stockData, interval)
        # self.orderOperations_req()
        # stop = timeit.default_timer()
        # print ("Time elapsed:", stop - start)
        # print (self.accountOperations_req())
        # print (self.positionExist)
        # print("RealTimeBars. ", reqId, "Time:", time, "Open:", open,
        #       "High:", high, "Low:", low, "Close:", close, "Volume:", volume,
        #       "Count:", count, "WAP:", wap)

    # ! [realtimebar]


    def orderOperations_cancel(self):
        # ! [cancelorder]
        self.cancelOrder(self.simplePlaceOid)

    # ! [cancelorder]

    @iswrapper
    # ! [execdetails]
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        super().execDetails(reqId, contract, execution)
        # print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency,
        #       execution.execId, execution.orderId, execution.shares)

    # ! [execdetails]


    @iswrapper
    # ! [execdetailsend]
    def execDetailsEnd(self, reqId: int):
        super().execDetailsEnd(reqId)
        # print("ExecDetailsEnd. ", reqId)

    # ! [execdetailsend]


    @iswrapper
    # ! [commissionreport]
    def commissionReport(self, commissionReport: CommissionReport):
        super().commissionReport(commissionReport)
        # print("CommissionReport. ", commissionReport.execId, commissionReport.commission,
        #       commissionReport.currency, commissionReport.realizedPNL)
        # ! [commissionreport]


def main():
    # SetupLogger()
    # logging.debug("now is %s", datetime.datetime.now())
    # logging.getLogger().setLevel(logging.DEBUG)

    cmdLineParser = argparse.ArgumentParser("api tests")
    # cmdLineParser.add_option("-c", action="store_True", dest="use_cache", default = False, help = "use the cache")
    # cmdLineParser.add_option("-f", action="store", type="string", dest="file", default="", help="the input file")
    cmdLineParser.add_argument("-p", "--port", action="store", type=int,
                               dest="port", default=7497, help="The TCP port to use")
    cmdLineParser.add_argument("-C", "--global-cancel", action="store_true",
                               dest="global_cancel", default=False,
                               help="whether to trigger a globalCancel req")
    cmdLineParser.add_argument('-t','--tickrSymbol', help='forex tickr',required=True)
    cmdLineParser.add_argument('-i','--clientid', help='unique client id',required=True)


    args = cmdLineParser.parse_args()
    tickrSymbol = args.tickrSymbol
    client_id = args.clientid
    print("Using args", args)
    logging.debug("Using args %s", args)
    # print(args)


    # enable logging when member vars are assigned
    from ibapi import utils
    from ibapi.order import Order
    Order.__setattr__ = utils.setattr_log
    from ibapi.contract import Contract, UnderComp
    Contract.__setattr__ = utils.setattr_log
    UnderComp.__setattr__ = utils.setattr_log
    from ibapi.tag_value import TagValue
    TagValue.__setattr__ = utils.setattr_log
    TimeCondition.__setattr__ = utils.setattr_log
    ExecutionCondition.__setattr__ = utils.setattr_log
    MarginCondition.__setattr__ = utils.setattr_log
    PriceCondition.__setattr__ = utils.setattr_log
    PercentChangeCondition.__setattr__ = utils.setattr_log
    VolumeCondition.__setattr__ = utils.setattr_log

    # from inspect import signature as sig
    # import code code.interact(local=dict(globals(), **locals()))
    # sys.exit(1)

    # tc = TestClient(None)
    # tc.reqMktData(1101, ContractSamples.USStockAtSmart(), "", False, None)
    # print(tc.reqId2nReq)
    # sys.exit(1)

    try:
        app = TestApp(tickrSymbol)
        if args.global_cancel:
            app.globalCancelOnly = True
        # ! [connect]
        app.connect("127.0.0.1", args.port, clientId=client_id)
        print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),
                                                      app.twsConnectionTime()))
        # ! [connect]
        app.run()
    except:
        raise
    finally:
        app.dumpTestCoverageSituation()
        app.dumpReqAnsErrSituation()


if __name__ == "__main__":

    main()
