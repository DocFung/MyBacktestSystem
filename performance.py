# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:41:19 2018

@author: 46362
"""

import numpy as np
import pandas as pd

def create_sharpe_ratio(returns,period=252):
    """
    period是交易周期，252是美国交易日
    return是pandas series对象
    """
    return (np.sqrt(period)*np.mean(returns))/np.std(returns)

def create_drawdowns(equity_curve):
    hwm=[0]
    eq_idx=equity_curve.index
    drawdown=pd.Series(index=eq_idx)
    duration=pd.Series(index=eq_idx)
    
    for t in range(1,len(eq_idx)):
        cur_hwm=max(hwm[t-1],equity_curve[t])
        hwm.append(cur_hwm)
        drawdown[t]=hwm[t]-equity_curve[t]
        duration[t]=0 if drawdown[t]==0 else duration[t-1]+1
    return drawdown.max(),duration.max()

