"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable.
"""

import sys

from ibapi.contract import *


class WatchListStocks:

    """ Usually, the easiest way to define a Stock/CASH contract is through
    these four attributes.  """

    @staticmethod
    def USStockAtSmart1(tickr):
        contract = Contract()
        contract.symbol = tickr
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USStockAtSmart2(tickr):
        contract = Contract()
        contract.symbol = tickr
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USStockAtSmart3(tickr):
        contract = Contract()
        contract.symbol = tickr
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USStockAtSmart4(tickr):
        contract = Contract()
        contract.symbol = tickr
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    @staticmethod
    def USStockAtSmart5(tickr):
        contract = Contract()
        contract.symbol = tickr
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract
