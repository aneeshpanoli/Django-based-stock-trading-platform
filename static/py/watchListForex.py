"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable.
"""

import sys

from ibapi.contract import *


class WatchListForex:

    """ Usually, the easiest way to define a Stock/CASH contract is through
    these four attributes.  """

    @staticmethod
    def EurGbpFx(tickr):
        #! [cashcontract]
        contract = Contract()
        contract.symbol = tickr
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        #! [cashcontract]
        return contract
