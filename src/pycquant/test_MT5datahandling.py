import MT5datahandling as mt5


csv_file_path= '\\\\192.168.0.4\\NASpi\\data\MT5\\symbol_data\\activtrades_symbols'

symbols = mt5.datahandling.save_all_symbols(csv_file_path , print_symbols=True)

#symbols = ['Ger40', 'HKInd', 'Usa500', 'UsaTec', 'UsaInd', 'UsaRus', 'Bra50', 'Jp225', 'Aus200']
tfs = ['D1']
csv_file_path = '\\\\192.168.0.4\\NASpi\\data\\MT5\\candle_data\\'
number_of_candles = 3000#50000


#mt5.datahandling.save_candle_data_to_csv(symbols[0], tfs[0], csv_file_path, number_of_candles)
mt5.datahandling.save_multiple_candle_data_to_csv(symbols, tfs, csv_file_path, number_of_candles)
