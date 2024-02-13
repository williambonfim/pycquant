import MT5datahandling as mt5


csv_file_path= '\\\\192.168.0.4\\NASpi\\data\MT5\\symbol_data\\activtrades_symbols.csv'
symbols = mt5.datahandling.save_all_symbols(csv_file_path , print_symbols=False)


min_trading_parameters_path = '\\\\192.168.0.4\\NASpi\\data\MT5\\trading_parameters_data'
print(mt5.datahandling.save_minimum_trading_parameters('Ger40'))
mt5.datahandling.save_multiple_minimum_trading_parameters(symbols, min_trading_parameters_path)

