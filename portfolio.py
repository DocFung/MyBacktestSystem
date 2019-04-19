# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 14:24:16 2018

@author: 46362
"""

import pandas as pd
import numpy as np
import datetime
import queue
from performance import create_sharpe_ratio,create_drawdowns
import time
from abc import ABCMeta,abstractmethod
from math import floor

from event import FillEvent,OrderEvent

import matplotlib.pyplot as plt

class Portfolio(metaclass=ABCMeta):
    @abstractmethod
    def update_signal(self,event):
        raise NotImplementedError("should implement update_signal()")
    
    @abstractmethod
    def update_fill(self,event):
        """
        更新资产目前的仓位和持有
        """
        raise NotImplementedError("should implement update_fill()")

class NaivePortfolio(Portfolio):
    """
    一个简单的例子，有很多不现实的假设：
    1.发生固定的买卖数量给经纪商
    2.不考虑现金持有
    
    先调用update_timeindex 更新timeindex，将上一个index的数据复制进来
    再根据update_fill来更新数据，在复制来的上一个index的数据上加减
    """        
    def __init__(self,bars,events,start_date,initial_captial=100000.0):
        self.bars=bars
        self.events=events
        self.tradeType=self.bars.tradeType
        self.start_date=start_date
        self.initial_captial=initial_captial
        
        self.tradeRecord={'datetime':[],'volume':[]}
        self.account={'datetime':[self.start_date],'cash':[self.initial_captial],
                      'comission':[0],'total':[self.initial_captial]}

    def update_timeindex(self):

        bars[s]=self.bars.get_latest_bars()[0]
        

        
    
    def updateVolume(self,fill):
        fill_dir=0
        if fill.direction=='BUY':
            fill_dir=1
        if fill.direction=='SELL':
            fill_dir=-1
        self.tradeRecord['volume'].append(fill_dir*fill.quantity)
    
    def updateAccount(self,fill):
        fill_dir=0
        if fill.direction=='BUY':
            fill_dir=1
        if fill.direction=='SELL':
            fill_dir=-1
        
        fill_cost=self.bars.get_latest_bars()[0].close
        cost=fill_dir*fill_cost*fill.quantity
        newComission=self.account['comission'][-1]+
        self.account['comission'].append(fill.comission)
        self.account['cash'].append(-(cost+fill.comission))
        self.account['total'].append(-(cost+fill.comission))
        
    def update_fill(self,event):
        if event.type=='FILL':
            self.updateVolume(event)
            self.updateAccount(event)
            print("portfolio.py update fill")
            
    def generate_naive_order(self,signal):
        order=None
        direction=signal.signal_type
        #strength=signal.strength
        
        mkt_quantity=1
        cur_quantity=sum(self.tradeRecord['volume'])
        order_type='MKT'
        
        if direction=='LONG': #and cur_quantity==0:
            order=OrderEvent(order_type,mkt_quantity,'BUY')
        if direction=='SHORT': #and cur_quantity==0:
            order=OrderEvent(order_type,mkt_quantity,'SELL')
        """
        退出信号 exit 全部卖掉
        """
        if direction=='EXIT' and cur_quantity>0:
            order=OrderEvent(order_type,abs(cur_quantity),'SELL')
        if direction=='EXIT' and cur_quantity<0:
            order=OrderEvent(order_type,abs(cur_quantity),'BUY')
        return order
    
    def update_signal(self,event):
        if event.type=='SIGNAL':
            order_event=self.generate_naive_order(event)
            print("portfolio.py put ORDER!")
            self.events.put(order_event)
    
    def create_equity_curve_dataframe(self):
        curve=pd.DataFrame(self.all_holdings)
        curve.set_index('datetime',inplace=True)
        curve['returns']=curve['total'].pct_change()
        curve['equity_curve']=(1.0+curve['returns']).cumprod()
        self.equity_curve=curve
    
    def output_summary_stats(self):
        total_return=self.equity_curve['equity_curve'][-1]
        returns=self.equity_curve['returns']
        pnl=self.equity_curve['equity_curve']
        
        sharpe_ratio=create_sharpe_ratio(returns)
        max_dd,dd_duration=create_drawdowns(pnl)
        
        stats=[("total return","%0.2f%%"%((total_return-1.0)*100.0)),
               ("sharpe ratio","%0.2f"%sharpe_ratio),
               ("Max Drawdown","%0.2f%%"%(max_dd*100)),
               ("Drawdown duration","%d"%dd_duration)]
        return stats
    
    def output_total(self):
        data=self.equity_curve['total']
        plt.plot(data)
        plt.title("total assets")
        plt.ylabel("dollar")
        left=min(data.index.year)
        right=max(data.index.year)
        tick=[str(x) for x in list(range(left,right+1))]
        plt.xticks(tick)
