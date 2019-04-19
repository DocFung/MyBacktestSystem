# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:16:35 2018

@author: 46362
"""
from MACDstrategy import MACD
import backtest


path=r"C:\Users\46362\Desktop\OnePy_Old-master"
symbol_list=['000001','000002']

engine=backtest.BackTest(path,symbol_list,None)
engine.initStrategy(MACD)
engine.run()