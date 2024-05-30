from secret.local_settings import pycquant_path_1, symbols_file_path, min_trading_parameters_path
import sys
sys.path.insert(0, pycquant_path_1)

import MT5datahandling as mt5


symbols = mt5.datahandling.save_all_symbols(symbols_file_path , print_symbols=False)


print(mt5.datahandling.save_minimum_trading_parameters('Ger40'))
mt5.datahandling.save_multiple_minimum_trading_parameters(symbols, min_trading_parameters_path)

