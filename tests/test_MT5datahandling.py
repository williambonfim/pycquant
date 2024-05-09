from secret.local_settings import pycquant_path_1, symbols_file_path, candle_file_path, min_trading_parameters_path_1
import sys
sys.path.insert(0, pycquant_path_1)

import MT5datahandling as mt5
import datetime as dt
from datahandling import update_D1_data

# =========================================================================================================
# =========================================================================================================

# -------------------
# Save a list of all available symbols in the current MT5 account

group = '*,!*.*, !*Jan*, !*Feb*, !*Mar*, !*Apr*, !*May*, !*Jun*, !*Jul*, !*Aug*,, !*Sep*,, !*Oct*, !*Nov*, !*Dec*'
symbols = mt5.datahandling.save_all_symbols(symbols_file_path, groups=group, print_symbols=False)
# =========================================================================================================
# =========================================================================================================

# -------------------
# Save symbols candle data from MT5

tfs = ['D1']
number_of_candles = 5 #15 for 1D - 2000 for 5 days M5 - 300 for 1 day M5

start_time = dt.datetime.now()

mt5.datahandling.save_multiple_candle_data_to_csv(symbols, tfs, candle_file_path, number_of_candles)
mt5.datahandling.save_multiple_candle_data_to_csv(symbols, tfs, candle_file_path, number_of_candles)

print(f'5min time: {dt.datetime.now()-start_time}')
print()

update_D1_data(candle_file_path, symbols)

# =========================================================================================================
# =========================================================================================================
# -------------------
# Save minimum trading parameters for all symbols
mt5.datahandling.save_multiple_minimum_trading_parameters(symbols, min_trading_parameters_path_1)

#symbols = ['Ger40', 'HKInd', 'Usa500', 'UsaTec', 'UsaInd', 'UsaRus', 'Bra50', 'Jp225', 'Aus200']
tfs = ['M5']
number_of_candles = 300 * 3

start_time = dt.datetime.now()
mt5.datahandling.save_multiple_candle_data_to_csv(symbols, tfs, candle_file_path, number_of_candles)
print(f'5min time: {dt.datetime.now()-start_time}')
print()

# =========================================================================================================
# =========================================================================================================

#mt5.datahandling.save_candle_data_to_csv('Ger40', 'M5', candle_file_path, number_of_candles = 150000)
