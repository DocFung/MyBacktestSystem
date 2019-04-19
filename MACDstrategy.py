# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 17:00:26 2018

@author: 46362
"""
from StrategyTemplate import Strategy,IndicatorCal

class MACD(Strategy):
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

        self.ic=IndicatorCal()
    
    def getIndicator(self,bar):
        self.ic.updateArray(bar)
        macd,signal,hist=self.ic.macd(self.short_MACD,self.long_MACD,self.DEA_MACD)
        
        
    def calculate_signals(self,event):
        '''
        if event.type=='MARKET':
                        self.events.put(signal)
        '''
        pass
    
    
    
    
    
    
    
    
    
    
    
#-0----------------------------------------------------------------------------------    
'''
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
'''                                        
        