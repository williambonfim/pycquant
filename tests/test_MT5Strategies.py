from secret.local_settings import pycquant_path_1
import sys
sys.path.insert(0, pycquant_path_1)

from MT5Strategies import PctStrategies, OpenCloseAtTimeStrategies
import warnings
from MT5utils import MT5
import datetime as dt
import MetaTrader5 as mt5

warnings.simplefilter(action='ignore', category=FutureWarning)

# Initialize MetaTrader terminal
MT5.initialize()

checkorder = False
MT5.remove_all_pending_orders()
MT5.close_all_orders()
# Startegies list
daily = True
if daily:
    strategies = []
    strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=0.77, buy=True, current_open=True, check_order=checkorder))
    strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=0.76, buy=True, current_open=True, check_order=checkorder))
    strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=0.75, buy=True, current_open=True, check_order=checkorder))
    strategies.append(PctStrategies('UsaTec', 'D1', 0.2, pct=-0.81, buy=True, last_open=True, check_order=checkorder))
    strategies.append(PctStrategies('UsaTec', 'D1', 0.2, pct=-0.79, buy=True, last_open=True, check_order=checkorder))
    strategies.append(PctStrategies('UsaTec', 'D1', 0.2, pct=-0.8, buy=True, last_open=True, check_order=checkorder))

    # Place orders
    for strategy in strategies:
        strategy.place_order()

at_time = False
if at_time:
    strategies = []

    h = 19
    m = 52
    s = 10

    entry = dt.time(h,m,s)
    out = dt.time(h,m,s+20)

    entry2 = dt.time(h,m+1,s)
    out2 = dt.time(h,m+1,s+20)

    strategies.append(OpenCloseAtTimeStrategies(dt.time(7,39,59), dt.time(7,45,0), 'Ger40', 0.25, buy=True, check_order=checkorder))
    strategies.append(OpenCloseAtTimeStrategies(dt.time(7,39,59), dt.time(7,45,0), 'Ger40', 0.25, buy=True, check_order=checkorder))
    strategies.append(OpenCloseAtTimeStrategies(dt.time(8,59,59), dt.time(9,5,0), 'Ger40', 0.25, buy=True, check_order=checkorder))
    strategies.append(OpenCloseAtTimeStrategies(dt.time(8,54,59), dt.time(9,5,0), 'Ger40', 0.25, buy=True, check_order=checkorder))
    strategies.append(OpenCloseAtTimeStrategies(dt.time(8,59,59), dt.time(9,10,0), 'Ger40', 0.25, buy=True, check_order=checkorder))
    strategies.append(OpenCloseAtTimeStrategies(dt.time(2,29,59), dt.time(2,35,0), 'HKInd', 0.05, buy=True, check_order=checkorder))
    strategies.append(OpenCloseAtTimeStrategies(dt.time(13,54,59), dt.time(14,0,0), 'UsaTec', 0.2, buy=False, check_order=checkorder))
    

        
    while True:
        
        for strategy in strategies:
            strategy.place_order()
            strategy.close_opened_order()