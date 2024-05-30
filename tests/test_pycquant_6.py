from secret.local_settings import pycquant_path, df_csv_path, analysis_data_csv, min_trading_parameters_path
import sys
sys.path.insert(0, pycquant_path)
from pycquant import LoopStrategies
import datahandling
import datetime as dt
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# --- Input parameters ---

# -- General parameters

# Select symbol you want to do the analysis
symbols2 = ['Ger40', 'HKInd', 'Usa500', 'UsaTec', 'UsaInd', 'UsaRus', 'Bra50', 'Jp225', 'Aus200']

# Select the timeframe of the data to do the analysis
tfs = ['D1']

# Select the initial date from where the analysis will start
dates = [dt.date(2024, 1, 1), dt.date(2023,11,1), dt.date(2023,1,1), dt.date(2024,2,1)]

# -- Trade system minimum requirements
min_No_trade    = 15
max_allowed_sl  = 0.02
success_rate    = 0.80
no_last_trades  = 6

# -- Specific strategies input
# Candle time to strategies time dependent
times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 5)]
pct_range = [x / 10000 for x in range(0, 501, 1)]
candles_shifts = range(50)

df_parameters = datahandling.read_minimum_trading_parameters(min_trading_parameters_path)


for symbol in symbols2:
    symbols = [symbol]
    initial_time = dt.datetime.now()
    print(initial_time)
    # ------
    # --- Individual strategy check ---
    strategies = datahandling.init_strategy_results_df()
    
    strategy1 = LoopStrategies.pct_down_last_close_close(df_csv_path, dates, symbols, tfs, [-x for x in pct_range], min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False, df_min_margin_volume=df_parameters)
    strategies = pd.concat([strategies, strategy1])
    print(dt.datetime.now()-initial_time)
    
    strategy2 = LoopStrategies.pct_up_last_close_close(df_csv_path, dates, symbols, tfs, pct_range, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False, df_min_margin_volume=df_parameters)
    strategies = pd.concat([strategies, strategy2])
    print(dt.datetime.now()-initial_time)

    strategy5 = LoopStrategies.pct_down_last_open_close(df_csv_path, dates, symbols, tfs, [-x for x in pct_range], min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False, df_min_margin_volume=df_parameters)
    strategies = pd.concat([strategies, strategy5])
    print(dt.datetime.now()-initial_time)

    strategy6 = LoopStrategies.pct_up_last_open_close(df_csv_path, dates, symbols, tfs, pct_range, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False, df_min_margin_volume=df_parameters)
    strategies = pd.concat([strategies, strategy6])
    print(dt.datetime.now()-initial_time)

    strategy7 = LoopStrategies.pct_down_current_open_close(df_csv_path, dates, symbols, tfs, [-x for x in pct_range], min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False, df_min_margin_volume=df_parameters)
    strategies = pd.concat([strategies, strategy7])
    print(dt.datetime.now()-initial_time)

    strategy8 = LoopStrategies.pct_up_current_open_close(df_csv_path, dates, symbols, tfs, pct_range, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False, df_min_margin_volume=df_parameters)
    strategies = pd.concat([strategies, strategy8])
    print(dt.datetime.now()-initial_time)



    # ------

    strategies = strategies.sort_values(by=['%_System_result'], ascending=False)

    print(strategies.to_string())
    print(f'No. of strategies: {len(strategies)}')

    datahandling.save_analysis_results(strategies, analysis_data_csv)


    final_time = dt.datetime.now()
    total_time = final_time-initial_time
    print(f'Total analysis time: {total_time}')