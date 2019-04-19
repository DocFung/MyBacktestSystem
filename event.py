# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:26:25 2018

@author: 46362
"""
import queue
events=queue.Queue()

class Event(object):
    pass

class MarketEvent(Event):
    def __init__(self):
        self.type="MARKET"
        
class SignalEvent(Event):
    def __init__(self,symbol,datetime,signal_type):
        self.type="SIGNAL"
        self.symbol=symbol
        self.datetime=datetime
        self.signal_type=signal_type

class OrderEvent(Event):
    def __init__(self,symbol,order_type,quantity,direction):
        self.type="ORDER"
        self.symbol=symbol
        self.order_type=order_type
        self.quantity=quantity
        self.direction=direction
    
    def print_order(self):
        print("Order: Symbol={0},Type={1},Quantity={2},Direction={3}".\
              format(self.symbol,self.order_type,self.quantity,self.direction))

class FillEvent(Event):
    def __init__(self,timeindex,symbol,exchange,quantity,direction,fill_cost,comission=None):
        self.type="FILL"
        self.timeindex=timeindex
        self.symbol=symbol
        self.exchange=exchange
        self.quantity=quantity
        self.direction=direction
        self.fill_cost=fill_cost
        if comission is None:
            self.comission=self.calculate_ib_comission()
        else:
            self.comission=comission
            
    def calculate_ib_comission(self):
        """
        这里似乎使用的是ibpy这个broker,以后记得回来修改
        """
        full_cost=1.3
        if self.quantity<=500:
            full_cost=max(1.3,0.013*self.quantity)
        else:
            full_cost=max(1.3,0.008*self.quantity)
        full_cost=min(full_cost,0.5/100.0*self.quantity*self.fill_cost)
        return full_cost
        
        