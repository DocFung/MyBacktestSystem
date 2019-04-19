# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:45:54 2018

@author: 46362
"""

import pandas as pd
import datetime
import numpy as np
import queue

from abc import ABCMeta,abstractmethod
from event import SignalEvent

class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def calculate_signals(self):
        raise NotImplementedError("should implement calculate_signals()")
        
class IndicatorCal(object):
    """
    用于计算指标
    """
    def __init__(self,size=100):
        self.size=size
        self.closeArray=np.zeros(size)
        self.highArray=np.zeros(size)
        self.lowArray=np.zeros(size)
        self.openArray=np.zeros(size)
        self.volumeArray=np.zeros(size)
    
    def updateBar(self,bar):
        size=self.size
        self.openArray[0:size-1]=self.openArray[1:size]
        self.closeArray[0:size-1]=self.closeArray[1:size]
        self.highArray[0:size-1]=self.highArray[1:size]
        self.lowArray[0:size-1]=self.lowArray[1:size]
        self.volumeArray[0:size-1]=self.volumeArray[1:size]
        
        self.openArray[-1]=bar.open
        self.closeArray[-1]=bar.close
        self.highArray[-1]=bar.high
        self.lowArray[-1]=bar.low
        self.volumeArray[-1]=bar.volume
        
    """这可能是一种减少代码量的方法"""
    @property
    def open(self):
        return self.openArray
    @property
    def close(self):
        return self.closeArray
    @property
    def high(self):
        return self.highArray
    @property
    def low(self):
        return self.lowArray
    @property
    def volume(self):
        return self.volumeArray
    #-------------------------------------
    def macd(self):
        return

class BuyAndHoldStrategy(Strategy):
    """
    只是一个例子
    其中bars是一个DataHandler类或者子类
    """
    def __init__(self,bars,events):
        self.bars=bars
        self.events=events
        self.symbol_list=self.bars.symbol_list
        self.bought=self._calculate_initial_bought()
    
    def _calculate_initial_bought(self):
        bought={}
        for s in self.symbol_list:
            bought[s]=False
        return bought
    
    def calculate_signals(self,event):
        if event.type=='MARKET':
            for s in self.symbol_list:
                bars=self.bars.get_latest_bars(s,N=1)
                if bars is not None and bars != []:
                    if self.bought[s]==False:
                        #signalevent: symbol,datetime,signal_type
                        #bar:symbol,['datetime','open','low','high','close','volume','oi']
                        signal=SignalEvent(bars[0][0],bars[0][1],signal_type='LONG')
                        print("strategy.py put SIGNAL!")
                        self.events.put(signal)
                        self.bought[s]=True
                        
class MACDStrategy(Strategy):
    """
    只是一个例子
    其中bars是一个DataHandler类或者子类
    """
    def __init__(self,bars,events,long_MACD=26,short_MACD=12,DEA_MACD=9):
        self.bars=bars
        self.events=events
        self.symbol_list=self.bars.symbol_list
        self.long_MACD=long_MACD
        self.short_MACD=short_MACD
        self.DEA_MACD=DEA_MACD
        self.indicator={"EMAshort":[0],"EMAlong":[0],"DIFF":[0],"DEA":[0],"MACD":[0]}
        self.symbol_indicator={s:self.indicator for s in self.symbol_list}
    
    def calculate_indicator(self):
        for s in self.symbol_list:
            feed=self.bars.get_latest_bars(s)[0]
            self.symbol_indicator[s]["EMAshort"].append(
                    feed[5]*(2/(self.short_MACD+1))+self.symbol_indicator[s]["EMAshort"][-1]*((self.short_MACD-1)/(self.short_MACD+1)))
            self.symbol_indicator[s]["EMAlong"].append(
                    feed[5]*(2/(self.long_MACD+1))+self.symbol_indicator[s]["EMAlong"][-1]*((self.long_MACD-1)/(self.long_MACD+1)))
            self.symbol_indicator[s]["DIFF"].append(
                    self.symbol_indicator[s]["EMAshort"][-1]-self.symbol_indicator[s]["EMAlong"][-1])
            self.symbol_indicator[s]["DEA"].append(
                    self.symbol_indicator[s]["DIFF"][-1]*(2/(self.DEA_MACD+1))+self.symbol_indicator[s]["DEA"][-1]*((self.DEA_MACD-1)/(self.DEA_MACD+1)))
            self.symbol_indicator[s]["MACD"].append(
                    2*(self.symbol_indicator[s]["DIFF"][-1]-self.symbol_indicator[s]["DEA"][-1]))
    
    def calculate_signals(self,event):
        if event.type=='MARKET':
            
            if len(self.symbol_indicator[self.symbol_list[0]]['MACD'])>5:
                for s in self.symbol_list:
                    feed=self.bars.get_latest_bars(s)[0]
                    
                    BUYsignal=(self.symbol_indicator[s]["DIFF"][-1]>self.symbol_indicator[s]["MACD"][-1]) \
                    &(self.symbol_indicator[s]["DIFF"][-2]>self.symbol_indicator[s]["MACD"][-2]) \
                    &(self.symbol_indicator[s]["DIFF"][-3]>self.symbol_indicator[s]["MACD"][-3]) \
                    &(self.symbol_indicator[s]["DIFF"][-4]<self.symbol_indicator[s]["MACD"][-4]) \
                    &(self.symbol_indicator[s]["DIFF"][-5]<self.symbol_indicator[s]["MACD"][-5])
                    
                    SELLsignal=(self.symbol_indicator[s]["DIFF"][-1]<self.symbol_indicator[s]["MACD"][-1]) \
                    &(self.symbol_indicator[s]["DIFF"][-2]<self.symbol_indicator[s]["MACD"][-2]) \
                    &(self.symbol_indicator[s]["DIFF"][-3]<self.symbol_indicator[s]["MACD"][-3]) \
                    &(self.symbol_indicator[s]["DIFF"][-4]>self.symbol_indicator[s]["MACD"][-4]) \
                    &(self.symbol_indicator[s]["DIFF"][-5]>self.symbol_indicator[s]["MACD"][-5])
                
                    if BUYsignal == True:
                        signal=SignalEvent(feed[0],feed[1],signal_type="LONG")
                        self.events.put(signal)
                    elif SELLsignal == True:
                        signal=SignalEvent(feed[0],feed[1],signal_type="SHORT")
                        self.events.put(signal)

                    
                        
        