import MetaTrader5 as mt5
from MT5utils import MT5
from utils import print_progress_bar
import csv
import os
import pandas as pd


class datahandling: 

    @staticmethod
    def save_all_symbols(path_to_save_csv, groups = '', print_symbols=False, initialize=True):

        if initialize: MT5.initialize()

        if groups == '':
            all_symbols_info = mt5.symbols_get()
            all_symbols = []

            for i in all_symbols_info:
                all_symbols.append(i.name)
        
        else:
            all_symbols_info = mt5.symbols_get(group=groups)
            all_symbols = []

            for i in all_symbols_info:
                all_symbols.append(i.name)

        print(f'Total symbols available: {len(all_symbols)}')
        if print_symbols:
            print()
            for symbol in all_symbols: print(symbol)
            print()

        with open(f"{path_to_save_csv}", 'w') as f:
            writer = csv.writer(f)
            writer.writerow(all_symbols)
            f.close()

        print(f'CSV files saved in {path_to_save_csv}.csv')

        if initialize: MT5.shutdown()

        return all_symbols

    @staticmethod
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
        file_name = f'{csv_file_path}{tf}_{symbol}.csv'
        file_path = os.path.join(csv_file_path, file_name)

        if os.path.exists(file_path):

            df_existing = pd.read_csv(file_path, index_col=0)
            last_index = df_existing.index[-1]
            df_existing.drop(last_index, inplace=True)

            last_index = df_existing.index[-1]

            rates = MT5.get_rates(symbol, number_of_candles, tf_mt5)
            date = pd.to_datetime(last_index)

            rates = rates[~(rates.index <= date)]

            df_existing = pd.concat([df_existing, rates])

            df_existing.to_csv(file_name)

            return 'Existing data updated.'


        else:

            rates = MT5.get_rates(symbol, number_of_candles, tf_mt5)
            rates.to_csv(file_name)
            print(f'New data added to {symbol}')

            return 'New data added.'

    @staticmethod
    def save_multiple_candle_data_to_csv(symbols, tfs, csv_file_path, number_of_candles=15000, initialize=True):
        
        if initialize: MT5.initialize()

        t = len(symbols) * len(tfs)
        i=0
        str_saved = ''
        for symbol in symbols:
            for tf in tfs:
                print_progress_bar(i, t, f'Saving {i}/{t} symbols... {symbol} {tf}: {str_saved}')
                i = i+1
                str_saved = datahandling.save_candle_data_to_csv(symbol, tf, csv_file_path, number_of_candles, initialize=False)

        print_progress_bar(1, 1, f'All symbols saved to csv.')
        print()
            
        if initialize: MT5.shutdown()

    @staticmethod
    def get_minimum_trading_parameters(symbol, initialize=True, print_symbol_info=False):
        
        if initialize: MT5.initialize()
        
        symbol_info = mt5.symbol_info(symbol)
        if print_symbol_info: print(symbol_info)

        min_volume = symbol_info.volume_min
        price = MT5.get_rates(symbol, number_of_candles = 1).iloc[0, 3]
        point = symbol_info.point
        min_margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, min_volume, price)

        profit_per_10000points = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY, symbol, min_volume, price, price + point*10000)

        trading_parameters = [[ symbol, \
                                min_volume, \
                                min_margin, \
                                point, \
                                profit_per_10000points ]]

        return trading_parameters

    @staticmethod
    def save_multiple_minimum_trading_parameters(symbols, csv_file_path, initialize=True):
        
        if initialize: MT5.initialize()

        import pandas as pd
        df = pd.DataFrame(columns = ['symbol', 'min_volume', 'min_margin', 'point', 'profit_per_10000points'])

        i=0
        t = len(symbols)
        for symbol in symbols:
            i = i+1
            print_progress_bar(i, t, f'Saving {i}/{t} symbols...')
            trading_parameters = datahandling.get_minimum_trading_parameters(symbol, initialize=False)
            df = pd.concat([df, pd.DataFrame(trading_parameters, columns=df.columns)])
        
        print_progress_bar(1, 1, f'Symbols remaining: 0')
        df = df.sort_values(by='symbol')
        df = df.reset_index()
        df = df.drop('index', axis=1)
        df.to_csv(f'{csv_file_path}/minimum_trading_parameters.csv', index=False)
        print()
        print()
        print(f'All trading parameters saved. {csv_file_path}')
        print()

        return df


