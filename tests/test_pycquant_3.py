from secret.local_settings import pycquant_path, df_csv_path, analysis_data_csv, min_trading_parameters_path
import sys
sys.path.insert(0, pycquant_path)
from pycquant import QuantStrategies
import datahandling
import datetime as dt
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# --- Input parameters ---

# -- General parameters

# Select symbol you want to do the analysis
tickers = ['UsaTec']

# Select the timeframe of the data to do the analysis
tfs = ['D1']

# Select the initial date from where the analysis will start
dates = [dt.date(2023, 11, 1)]

# -- Trade system minimum requirements
min_No_trade = 1
max_allowed_sl = 0.03
success_rate = 0.8

pct = [x/10000 for x in range(96, 145)]

print(pct)
# ------
# --- Individual strategy check ---
strategies = datahandling.init_strategy_results_df()

df = datahandling.compile_data(df_csv_path, tickers[0], tfs[0], calc_pct_last_close = True)
for i in pct:
    '''
    strategy1 = QuantStrategies.pct_down_last_close_close(df, dates[0], tickers[0], tfs[0], -0.01)      #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
    strategies = pd.concat([strategies, strategy1])
    '''
    strategy2 = QuantStrategies.pct_up_last_close_close(df, dates[0], tickers[0], tfs[0], i, print_df=False)         #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
    strategies = pd.concat([strategies, strategy2])


df = datahandling.compile_data(df_csv_path, tickers[0], tfs[1])

strategy3 = QuantStrategies.open_at_time_close(df, dates[0], tickers[0], tfs[1], '14:10')           #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy3])

strategy4 = QuantStrategies.open_at_time_shift_close(df, dates[0], tickers[0], tfs[1], '18:50', 1)  #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy4])

df = datahandling.compile_data(df_csv_path, tickers[0], tfs[0], calc_pct_last_open=True)

strategy5 = QuantStrategies.pct_down_last_open_close(df, dates[0], tickers[0], tfs[0], -0.01)      #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy5])

strategy6 = QuantStrategies.pct_up_last_open_close(df, dates[0], tickers[0], tfs[0], 0.01)         #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy6])

df = datahandling.compile_data(df_csv_path, tickers[0], tfs[0], calc_pct_current_open=True)

strategy7 = QuantStrategies.pct_down_current_open_close(df, dates[0], tickers[0], tfs[0], -0.01)      #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy7])

strategy8 = QuantStrategies.pct_up_current_open_close(df, dates[0], tickers[0], tfs[0], 0.01)         #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy8])

# -- Strategies dataframe with trade systems validated with minimum requirements


print()
print()
print(strategies.to_string())