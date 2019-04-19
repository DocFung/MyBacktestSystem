# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 11:06:28 2018

@author: 46362
"""

import datetime
import os,os.path
import pandas as pd

from abc import ABCMeta,abstractmethod
from event import MarketEvent

class DataHandler(metaclass=ABCMeta):
    
    @abstractmethod
    def get_latest_bars(self,symbol,N=1):
        """
        从latest_symbol list中返回N个bar
        """
        raise NotImplementedError("Should Implement get_latest_bars()")
    
    @abstractmethod
    def update_bars(self):
        """
        将最新的bar push进latest_symbol list
        """
        raise NotImplementedError("should Implement update_bars()")
class btBarData(object):
    """names=['datetime','open','low','high','close','volume','oi']"""
    def __inti__(self):
        self.symbol=None
        self.datetime=None
        self.open=0
        self.low=0
        self.high=0
        self.close=0
        self.volume=0
        self.oi=0
       
class HistoricCSVDataHandler(DataHandler):
    """
    初始化：
    continue_backtest=true
    _open_convert_csv_files打开本地数据，赋予symbol_data每一个symbol一个iterable对象
    并且将latest_symbol_data置空[]
    
    update_bars 调用 _get_new_bar从symbol中next一个bar出来，将其push入 latest_symbol_data
    put一个marketevent
    
    get_latest_bars 从 latest_symbol_data中获取最新的bar
    
    很多策略需要计算指标，这个回测系统将data yield new bar的操作形容为滴水，是为了防止look ahead bias
    但是以窗口来计算指标会造成大量计算冗余，所以在data.py里计算指标
    
    以MACD为例子，首先建立一个list来存放emd数据，每一次drip出新bar，就在这个list中添加新的数据
    strategy.MACDStrategy 通过调用来进行信号生成
    """
    def __init__(self,events,csv_dir,tradeType):
        """
        假设所有文件名为symbol.csv
        存在csv_dir文档之下
        """
        self.events=events
        self.csv_dir=csv_dir
        self.tradeType=tradeType
        '''
        symbol_data dict类型 以symbol为key value为pandas.df.iterrows()生产的 generator
        latest_symbol_data dict类型 以symbol为key value是一个元组构成的list，每一个元组是genertor next方法得到的新bar
        '''
        self.continue_backtest=True
        
        self._open_convert_csv_files()
        
    def _open_convert_csv_files(self):
        """
        最后调用iterrows()将逐行遍历DF
        使得symol_data的每一个value值都是一个iterable对象
        pad method向后填充
        """

        self.tradeData=pd.read_csv(self.csv_dir,header=0,index_col=0,
                                   names=['datetime','open','low','high','close','volume']).iterrows()
        self.latestData=[]
            
        
            
    def _get_new_bar(self):
        """
        pandas.Df.iterrows()返回iterable对象
        遍历时，每一次遍历yield返回的是一个tuple(row_index,Series(column_index,value))
        names=['datetime','open','low','high','close','volume','oi']
        """
        for t in self.tradeType:
            bar=btBarData()
            bar.datetime=datetime.datetime.strptime(t[0],'%Y-%m-%d')
            bar.open=t[1][0]
            bar.low=t[1][1]
            bar.high=t[1][2]
            bar.close=t[1][3]
            bar.volume=t[1][4]
            yield bar
#-------------------------------------------------------------------------------
    #override absmethod
    def get_latest_bars(self,N=1):
        try:
            bars_list=self.latestData
        except KeyError:
            print("there is no data")
        else:
            return bars_list[-N:]
    #override absmethod
    def update_bars(self):
        """
        更新latest_symbol_data dict类型
        push 最新的bar进入latest_symbol_data中
        """

        try:
            bar=next(self._get_new_bar())
        except StopIteration:
            self.continue_backtest=False
        else:
            if bar is not None:
                self.latestData.append(bar)
        print("data.py update_bars put MARKET!")
        self.events.put(MarketEvent())
    

        
        