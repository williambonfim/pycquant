import MetaTrader5 as mt5
from MT5utils import MT5
from utils import print_progress_bar
import csv


class datahandling: 

    def save_all_symbols(path_to_save_csv, print_symbols=False):

        MT5.initialize()

        all_symbols_info = mt5.symbols_get()
        all_symbols = []

        for i in all_symbols_info:
            all_symbols.append(i.name)
        print(f'Total symbols available: {len(all_symbols)}')
        if print_symbols:
            print()
            for symbol in all_symbols: print(symbol)
            print()

        with open(f"{path_to_save_csv}.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerow(all_symbols)
            f.close()

        print(f'CSV files saved in {path_to_save_csv}.csv')

        MT5.shutdown()

        return all_symbols

    def save_candle_data_to_csv(symbol, tf, csv_file_path, number_of_candles=150000, initialize=True):

        if initialize: MT5.initialize()

        dict = {
            'M1': mt5.TIMEFRAME_M1,
            'M3': mt5.TIMEFRAME_M3,
            'M5': mt5.TIMEFRAME_M5,
            'M10': mt5.TIMEFRAME_M10,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'H12': mt5.TIMEFRAME_H12,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
        }

        tf_mt5 = dict[tf]

        rates = MT5.get_rates(symbol, number_of_candles, tf_mt5)
        rates.to_csv(f'{csv_file_path}{tf}_{symbol}.csv')

    def save_multiple_candle_data_to_csv(symbols, tfs, csv_file_path, number_of_candles=150000):
        
        MT5.initialize()

        t = len(symbols) * len(tfs)
        i=0

        for symbol in symbols:
            for tf in tfs:
                i = i+1
                print_progress_bar(i, t, f'Saving {i}/{t} symbols...')
                datahandling.save_candle_data_to_csv(symbol, tf, csv_file_path, number_of_candles, initialize=False)

        print_progress_bar(1, 1, f'Symbols remaining: 0')
        print()
            
        MT5.shutdown()

