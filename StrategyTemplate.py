# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:45:54 2018

@author: 46362
"""

import pandas as pd
import datetime
import numpy as np
import queue
import talib

from abc import ABCMeta,abstractmethod
from event import SignalEvent

class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def calculate_signals(self):
        raise NotImplementedError("should implement calculate_signals()")
    
    def getIndicator(self):
        pass
    
        
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
    
    def updateArray(self,bar):
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
    def macd(self,fastPeriod, slowPeriod, signalPeriod, array=True):
        macd,signal,hist = talib.MACD(self.close,fastPeriod,slowPeriod,signalPeriod)
        if array:
            return macd, signal, hist
        return macd[-1], signal[-1], hist[-1]

