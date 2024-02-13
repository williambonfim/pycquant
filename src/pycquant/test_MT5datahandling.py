import MT5datahandling as mt5


# -------------------
# Save a list of all available symbols in the current MT5 account
csv_file_path= '\\\\192.168.0.4\\NASpi\\data\MT5\\symbol_data\\activtrades_symbols.csv'
symbols = mt5.datahandling.save_all_symbols(csv_file_path , print_symbols=False)

# -------------------
# Save symbols candle data from MT5
#symbols = ['Ger40', 'HKInd', 'Usa500', 'UsaTec', 'UsaInd', 'UsaRus', 'Bra50', 'Jp225', 'Aus200']
tfs = ['D1']
csv_file_path = '\\\\192.168.0.4\\NASpi\\data\\MT5\\candle_data\\'
number_of_candles = 3000#50000

#mt5.datahandling.save_candle_data_to_csv(symbols[0], tfs[0], csv_file_path, number_of_candles)
mt5.datahandling.save_multiple_candle_data_to_csv(symbols, tfs, csv_file_path, number_of_candles)

# -------------------
# Save minimum trading parameters for all symbols
min_trading_parameters_path = '\\\\192.168.0.4\\NASpi\\data\MT5\\trading_parameters_data'
mt5.datahandling.save_multiple_minimum_trading_parameters(symbols, min_trading_parameters_path)