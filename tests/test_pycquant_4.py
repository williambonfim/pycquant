from secret.local_settings import pycquant_path, df_csv_path, analysis_data_csv, all_symbols_path
import sys
sys.path.insert(0, pycquant_path)
from pycquant import LoopStrategies
import datahandling
import datetime as dt
import pandas as pd
import warnings
import csv

warnings.simplefilter(action='ignore', category=FutureWarning)

# --- Input parameters ---

# -- General parameters

# Select symbol you want to do the analysis

with open(all_symbols_path, newline='') as f:
    reader = csv.reader(f)
    symbols = list(reader)
symbols = symbols[0]


# Select the timeframe of the data to do the analysis
tfs = ['D1']

# Select the initial date from where the analysis will start
dates = [dt.date(2024, 1, 1), dt.date(2023,11,1), dt.date(2023,1,1)]
dates = [dt.date(2023,11,1)]
# -- Trade system minimum requirements
min_No_trade    = 10
max_allowed_sl  = 0.02
success_rate    = 0.80
no_last_trades  = 6

# -- Specific strategies input
# Candle time to strategies time dependent
times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 5)]
pct_range = [x / 10000 for x in range(0, 501, 1)]
candles_shifts = range(50)

datahandling.update_D1_data(df_csv_path, symbols)

initial_time = dt.datetime.now()
# ------
# --- Individual strategy check ---
strategies = datahandling.init_strategy_results_df()

strategy1 = LoopStrategies.pct_down_last_close_close(df_csv_path, dates, symbols, tfs, [-x for x in pct_range], min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False)
strategies = pd.concat([strategies, strategy1])

strategy2 = LoopStrategies.pct_up_last_close_close(df_csv_path, dates, symbols, tfs, pct_range, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False)
strategies = pd.concat([strategies, strategy2])

tfs = ['M5']

strategy3 = LoopStrategies.open_at_time_close(df_csv_path, dates, symbols, tfs, times, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False)
strategies = pd.concat([strategies, strategy3])

strategy4 = LoopStrategies.open_at_time_shift_close(df_csv_path, dates, symbols, tfs, times, candles_shifts, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False)
strategies = pd.concat([strategies, strategy4])

# ------

strategies = strategies.sort_values(by=['%_System_result'], ascending=False)

print(strategies.to_string())
print(f'No. of strategies: {len(strategies)}')

datahandling.save_analysis_results(strategies, analysis_data_csv)


final_time = dt.datetime.now()
total_time = final_time-initial_time
print(f'Total analysis time: {total_time}')