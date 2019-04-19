# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:23:19 2018

@author: 46362
"""

import datetime
import queue
import time
from abc import ABCMeta,abstractmethod
from event import FillEvent,OrderEvent

class ExecutionHandler(metaclass=ABCMeta):
    @abstractmethod
    def execute_order(self,event):
        raise NotImplementedError("should implement Execution()")

class SimulatedExecutionHandler(ExecutionHandler):
    
    def __init__(self,events):
        """
        events queue
        """
        self.events=events
    
    def execute_order(self,event):
        """
        简单地将order转换为fill
        没有考虑任何其他因素，滑点，以及交易费用
        timeindex,symbol,exchange,quantity,direction,fill_cost,comission=None
        """
        if event.type=="ORDER":
            fill_event=FillEvent(datetime.datetime.utcnow(),event.symbol,'ARCA',
                                 event.quantity,event.direction,0,0)
            print("execution.py put FILL")
            self.events.put(fill_event)
    