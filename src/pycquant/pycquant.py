import pandas as pd
import datahandling
from utils import symbol_selection, init_strategy_results_df, print_progress_bar, print_symbol_df, drop_data_before_initial_date
pd.options.mode.copy_on_write = True

class QuantStrategies:

    def pct_down_last_close_close(df, date_0, symbol, tf, target_down, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        # Get initial time and drop index before the initial date
        df = drop_data_before_initial_date(df, date_0)

        # Set target column to trade result if a condition is met then
        df['pct_target'] = pd.Series(0, index = df.index).mask(df['low_pct'] < target_down, df['close_pct'] - target_down)
        df['target']     = pd.Series(0, index = df.index).mask(df['low_pct'] < target_down, df['close'] - df['close'].shift(1) * (1+target_down))

        entry_criteria = f'{round(target_down*100, 2)}% last CLOSE candle'
        exit_criteria = 'closed candle'

        if print_df:
            print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria)

        df_results = symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_last_trades, df_min_margin_volume=df_min_margin_volume)

        return df_results

    def pct_up_last_close_close(df, date_0, symbol, tf, target_up, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        # Get initial time and drop index before the initial date
        df = drop_data_before_initial_date(df, date_0)

        # Set target column to trade result if a condition is met then
        df['pct_target'] = pd.Series(0, index = df.index).mask(df['high_pct'] > target_up, target_up - df['close_pct'])
        df['target']     = pd.Series(0, index = df.index).mask(df['high_pct'] > target_up, df['close'].shift(1) * (1+target_up) - df['close'])

        entry_criteria = f'+{round(target_up*100, 2)}% last CLOSE candle'
        exit_criteria = 'closed candle'

        if print_df:
            print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria)

        df_results = symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_last_trades, df_min_margin_volume=df_min_margin_volume)

        return df_results
    
    def pct_down_last_open_close(df, date_0, symbol, tf, target_down, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        # Get initial time and drop index before the initial date
        df = drop_data_before_initial_date(df, date_0)

        # Set target column to trade result if a condition is met then
        df['pct_target'] = pd.Series(0, index = df.index).mask((df['low_pct'] < target_down) & (df['open'].shift(1) <= df['high']) & (df['open'].shift(1) >= df['low']), df['close_pct'] - target_down)
        df['target']     = pd.Series(0, index = df.index).mask((df['low_pct'] < target_down) & (df['open'].shift(1) <= df['high']) & (df['open'].shift(1) >= df['low']), df['close'] - df['open'].shift(1) * (1+target_down))

        entry_criteria = f'{round(target_down*100, 2)}% last OPEN candle'
        exit_criteria = 'closed candle'

        if print_df:
            print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria)

        df_results = symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_last_trades, df_min_margin_volume=df_min_margin_volume)

        return df_results

    def pct_up_last_open_close(df, date_0, symbol, tf, target_up, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        # Get initial time and drop index before the initial date
        df = drop_data_before_initial_date(df, date_0)

        # Set target column to trade result if a condition is met then
        df['pct_target'] = pd.Series(0, index = df.index).mask((df['high_pct'] > target_up) & (df['open'].shift(1) <= df['high']) & (df['open'].shift(1) >= df['low']), target_up - df['close_pct'])
        df['target']     = pd.Series(0, index = df.index).mask((df['high_pct'] > target_up) & (df['open'].shift(1) <= df['high']) & (df['open'].shift(1) >= df['low']), df['open'].shift(1) * (1+target_up) - df['close'])

        entry_criteria = f'+{round(target_up*100, 2)}% last OPEN candle'
        exit_criteria = 'closed candle'

        if print_df:
            print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria)

        df_results = symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_last_trades, df_min_margin_volume=df_min_margin_volume)

        return df_results
    
    def pct_down_current_open_close(df, date_0, symbol, tf, target_down, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        # Get initial time and drop index before the initial date
        df = drop_data_before_initial_date(df, date_0)

        # Set target column to trade result if a condition is met then
        df['pct_target'] = pd.Series(0, index = df.index).mask(df['low_pct'] < target_down, df['close_pct'] - target_down)
        df['target']     = pd.Series(0, index = df.index).mask(df['low_pct'] < target_down, df['close'] - df['open'] * (1+target_down))

        entry_criteria = f'{round(target_down*100, 2)}% current OPEN candle'
        exit_criteria = 'closed candle'

        if print_df:
            print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria)

        df_results = symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_last_trades, df_min_margin_volume=df_min_margin_volume)

        return df_results

    def pct_up_current_open_close(df, date_0, symbol, tf, target_up, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        # Get initial time and drop index before the initial date
        df = drop_data_before_initial_date(df, date_0)

        # Set target column to trade result if a condition is met then
        df['pct_target'] = pd.Series(0, index = df.index).mask(df['high_pct'] > target_up, target_up - df['close_pct'])
        df['target']     = pd.Series(0, index = df.index).mask(df['high_pct'] > target_up, df['open'] * (1+target_up) - df['close'])

        entry_criteria = f'+{round(target_up*100, 2)}% current OPEN candle'
        exit_criteria = 'closed candle'

        if print_df:
            print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria)

        df_results = symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_last_trades, df_min_margin_volume=df_min_margin_volume)

        return df_results

    def open_at_time_close(df, date_0, symbol, tf, time, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):
        
        # Get initial time and drop index before the initial date
        df = drop_data_before_initial_date(df, date_0)

        df = df.between_time(time, time)

        # Set target column to trade result at close - Buy at open and Sell at close strategy
        df['target'] = df['close'] - df['open']
        df['pct_target'] = (df['close'] - df['open']) / df['open']

        entry_criteria = f'Open at {time} hrs'
        exit_criteria = 'Close of current candle'

        if print_df:
            print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria)

        df_results = symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_last_trades, df_min_margin_volume=df_min_margin_volume)

        return df_results

    def open_at_time_shift_close(df, date_0, symbol, tf, time, candles_shift, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):
        # Get initial time and drop index before the initial date
        df = drop_data_before_initial_date(df, date_0)

        df['target'] = df['close'].shift(-candles_shift)
        
        df['pct_target'] = (df['target'] - df['open']) / df['open']
        df['target'] = (df['target'] - df['open'])

        df = df.between_time(time, time)

        entry_criteria = f'Open at {time} hrs'
        exit_criteria = f'Close after {candles_shift} candles'

        if print_df:
            print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria)

        df_results = symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_last_trades, df_min_margin_volume=df_min_margin_volume)

        return df_results
    
class LoopStrategies:

    def pct_down_last_close_close(df_csv_path, dates, symbols, tfs, pct_down_range, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        df_results = init_strategy_results_df()
        for symbol in symbols:
            for tf in tfs:

                df = datahandling.compile_data(df_csv_path, symbol, tf, calc_pct_last_close = True)

                for date in dates:
                    for pct_down in pct_down_range:

                        print_progress_bar(pct_down_range.index(pct_down), len(pct_down_range), f'Pct down last close and close - {date}')
                        df_results = pd.concat([df_results, QuantStrategies.pct_down_last_close_close(df, date, symbol, tf, pct_down, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df, df_min_margin_volume)])
                    
                    print_progress_bar(1 , 1, f'Pct down last CLOSE and close - {date}')
                    print()

        return df_results

    def pct_up_last_close_close(df_csv_path, dates, symbols, tfs, pct_up_range, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        df_results = init_strategy_results_df()
        for symbol in symbols:
            for tf in tfs:

                df = datahandling.compile_data(df_csv_path, symbol, tf, calc_pct_last_close = True)

                for date in dates:
                    for pct_up in pct_up_range:

                        print_progress_bar(pct_up_range.index(pct_up), len(pct_up_range), f'Pct up last close and close - {date}')
                        df_results = pd.concat([df_results, QuantStrategies.pct_up_last_close_close(df, date, symbol, tf, pct_up, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df, df_min_margin_volume)])
                    
                    print_progress_bar(1 , 1, f'Pct up last CLOSE and close - {date}')
                    print()

        return df_results
    
    def pct_down_last_open_close(df_csv_path, dates, symbols, tfs, pct_down_range, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        df_results = init_strategy_results_df()
        for symbol in symbols:
            for tf in tfs:

                df = datahandling.compile_data(df_csv_path, symbol, tf, calc_pct_last_open = True)

                for date in dates:
                    for pct_down in pct_down_range:

                        print_progress_bar(pct_down_range.index(pct_down), len(pct_down_range), f'Pct down last close and close - {date}')
                        df_results = pd.concat([df_results, QuantStrategies.pct_down_last_open_close(df, date, symbol, tf, pct_down, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df, df_min_margin_volume)])
                    
                    print_progress_bar(1 , 1, f'Pct down last OPEN and close - {date}')
                    print()

        return df_results

    def pct_up_last_open_close(df_csv_path, dates, symbols, tfs, pct_up_range, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        df_results = init_strategy_results_df()
        for symbol in symbols:
            for tf in tfs:

                df = datahandling.compile_data(df_csv_path, symbol, tf, calc_pct_last_open = True)

                for date in dates:
                    for pct_up in pct_up_range:

                        print_progress_bar(pct_up_range.index(pct_up), len(pct_up_range), f'Pct up last close and close - {date}')
                        df_results = pd.concat([df_results, QuantStrategies.pct_up_last_open_close(df, date, symbol, tf, pct_up, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df, df_min_margin_volume)])
                    
                    print_progress_bar(1 , 1, f'Pct up last OPEN and close - {date}')
                    print()

        return df_results
    
    def pct_down_current_open_close(df_csv_path, dates, symbols, tfs, pct_down_range, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        df_results = init_strategy_results_df()
        for symbol in symbols:
            for tf in tfs:

                df = datahandling.compile_data(df_csv_path, symbol, tf, calc_pct_current_open = True)

                for date in dates:
                    for pct_down in pct_down_range:

                        print_progress_bar(pct_down_range.index(pct_down), len(pct_down_range), f'Pct down last close and close - {date}')
                        df_results = pd.concat([df_results, QuantStrategies.pct_down_current_open_close(df, date, symbol, tf, pct_down, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df, df_min_margin_volume)])
                    
                    print_progress_bar(1 , 1, f'Pct down current OPEN and close - {date}')
                    print()

        return df_results

    def pct_up_current_open_close(df_csv_path, dates, symbols, tfs, pct_up_range, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        df_results = init_strategy_results_df()
        for symbol in symbols:
            for tf in tfs:

                df = datahandling.compile_data(df_csv_path, symbol, tf, calc_pct_current_open = True)

                for date in dates:
                    for pct_up in pct_up_range:

                        print_progress_bar(pct_up_range.index(pct_up), len(pct_up_range), f'Pct up last close and close - {date}')
                        df_results = pd.concat([df_results, QuantStrategies.pct_up_current_open_close(df, date, symbol, tf, pct_up, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df, df_min_margin_volume)])
                    
                    print_progress_bar(1 , 1, f'Pct up current OPEN and close - {date}')
                    print()

        return df_results

    def open_at_time_close(df_csv_path, dates, symbols, tfs, times, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        df_results = init_strategy_results_df()
        for symbol in symbols:
            for tf in tfs:

                df = datahandling.compile_data(df_csv_path, symbol, tf)

                for date in dates:
                    for time in times:

                        print_progress_bar(times.index(time), len(times), f'Open at time and close - {date}')
                        df_results = pd.concat([df_results, QuantStrategies.open_at_time_close(df, date, symbol, tf, time, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df, df_min_margin_volume)])
                    
                    print_progress_bar(1, 1, f'Open at time and close - {date}')
                    print()

        return df_results
    
    def open_at_time_shift_close(df_csv_path, dates, symbols, tfs, times, candles_shifts, min_No_trade=1, max_allowed_sl=1, success_rate=0.4, no_last_trades=5, print_df=False, df_min_margin_volume=pd.DataFrame()):

        df_results = init_strategy_results_df()
        for symbol in symbols:
            for tf in tfs:

                df = datahandling.compile_data(df_csv_path, symbol, tf)

                for date in dates:
                    for time in times:

                        print_progress_bar(times.index(time), len(times), f'Open at time and shift close - {date}')

                        for candles_shift in candles_shifts:

                            df_results = pd.concat([df_results, QuantStrategies.open_at_time_shift_close(df, date, symbol, tf, time, candles_shift, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df, df_min_margin_volume)])
                    
                    print_progress_bar(1 , 1, f'Open at time and shift close - {date}')
                    print()
        return df_results
