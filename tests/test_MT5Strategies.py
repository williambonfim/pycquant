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

checkorder = True

# Startegies list
strategies = []
strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=1, last_close=True, check_order=checkorder))
strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=-1, buy=False, last_close=True, check_order=checkorder))
strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=1, last_open=True, check_order=checkorder))
strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=-1, buy=False, last_open=True, check_order=checkorder))
strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=1, current_open=True, check_order=checkorder))
strategies.append(PctStrategies('Ger40', 'D1', 0.25, pct=-1, buy=False, current_open=True, check_order=checkorder))

# Place orders
for strategy in strategies:
    strategy.place_order()

strategies = []

h = 11
m = 34
s = 0

entry = dt.time(h,m,s)
out = dt.time(h,m,s+30)

strategies.append(OpenCloseAtTimeStrategies(entry, out, 'Ger40', 0.25, buy=True, check_order=checkorder))

    
while True:
    
    for strategy in strategies:
        strategy.place_order()
        strategy.close_opened_order()