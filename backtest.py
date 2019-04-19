# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 19:21:47 2018

@author: 46362
"""
import queue
import portfolio
import data
import execution

class BackTest(object):
    
    def __init__(self,csvPath,symbolList,startTime,tradeType='000001'):
        self.events=queue.Queue()
        self.feed=data.HistoricCSVDataHandler(self.events,csvPath,symbolList)
        self.port=portfolio.NaivePortfolio(self.feed,self.events,startTime)
        self.broker=execution.SimulatedExecutionHandler(self.events)
        #暂时性的
        #为了能够调用后面的get_latest_bar
        #之后的修改需要考虑symbol_list的修改
        self.tradeType=tradeType
        
    def initStrategy(self,StrategyClass):
        self.strategy=StrategyClass(self.feed,self.events)
        self.strategy.name=str(StrategyClass)
        
    def run(self):
        get_event=0
        bars_update=0
        market=0
        signal=0
        order=0
        fill=0
        while 1:
            if self.feed.continue_backtest==True:
                print("get bar",bars_update)
                self.feed.update_bars()
                bar=self.feed.get_latest_bars(self.tradeType)[0]
                '''
                每一次update bar，更新indicator
                '''
                bars_update+=1
                self.strategy.getIndicator(bar)
            else:
                print("output result")
                self.port.create_equity_curve_dataframe()
                print(self.port.output_summary_stats())
                self.port.output_total()
                break
        
            while 1:
                try:
                    event=self.events.get(False)
                    #print("get_event ",get_event," type ",event.type)
                    get_event+=1
                except queue.Empty:
                    print("queue Empty!")
                    break
                else:
                    if event is not None:
                        print("event is not None-------------------------------------")
                        if event.type == "MARKET":       
                            market+=1
                            self.strategy.calculate_signals(event)
                        if event.type == "SIGNAL":
                            signal+=1
                            self.port.update_signal(event)
                        if event.type == "ORDER":
                            order+=1
                            self.broker.execute_order(event)
                        if event.type == "FILL":
                            fill+=1
                            self.port.update_fill(event)
                        print("market:",market,"signal:",signal,"order:",order,"fill:",fill)
                        print("------------------------------------------------------")
                        print("\n")
                        #time.sleep(10)