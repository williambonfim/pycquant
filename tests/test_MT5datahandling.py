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
symbols = mt5.datahandling.save_all_symbols(symbols_file_path , print_symbols=False)

# =========================================================================================================
# =========================================================================================================

# -------------------
# Save symbols candle data from MT5

tfs = ['D1']
number_of_candles = 15 #15 for 1D - 2000 for 5 days M5 - 300 for 1 day M5

mt5.datahandling.save_multiple_candle_data_to_csv(symbols, tfs, candle_file_path, number_of_candles)

update_D1_data(candle_file_path, symbols)

# =========================================================================================================
# =========================================================================================================
# -------------------
# Save minimum trading parameters for all symbols
mt5.datahandling.save_multiple_minimum_trading_parameters(symbols, min_trading_parameters_path_1)
quit()
symbols = ['Ger40', 'HKInd', 'Usa500', 'UsaTec', 'UsaInd', 'UsaRus', 'Bra50', 'Jp225', 'Aus200']
tfs = ['M5']
number_of_candles = 300 * 15
mt5.datahandling.save_multiple_candle_data_to_csv(symbols, tfs, candle_file_path, number_of_candles)

# =========================================================================================================
# =========================================================================================================

#mt5.datahandling.save_candle_data_to_csv('Ger40', 'M5', candle_file_path, number_of_candles = 150000)
