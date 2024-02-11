from pycquant import QuantStrategies
import datahandling
import datetime as dt
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# --- Input parameters ---

# -- General parameters
csv_original_path = '/Volumes/NASpi/data/MT5'
# Select symbol you want to do the analysis
tickers = ['Ger40', 'UsaTec']

# Select the timeframe of the data to do the analysis
tfs = ['D1', 'M5']

# Select the initial date from where the analysis will start
dates = [dt.date(2024, 1, 1)]

# -- Trade system minimum requirements
min_No_trade = 1
max_allowed_sl = 0.03
success_rate = 0.8


# ------
# --- Individual strategy check ---
strategies = datahandling.init_strategy_results_df()

df = datahandling.compile_data(csv_original_path, tickers[0], tfs[0], calc_pct = True)

strategy1 = QuantStrategies.pct_down_last_close_close(df, dates[0], tickers[0], tfs[0], -0.01)      #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy1])

strategy2 = QuantStrategies.pct_up_last_close_close(df, dates[0], tickers[0], tfs[0], 0.01)         #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy2])


df = datahandling.compile_data(csv_original_path, tickers[0], tfs[1], calc_pct = False)

strategy3 = QuantStrategies.open_at_time_close(df, dates[0], tickers[0], tfs[1], '14:10')           #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy3])

strategy4 = QuantStrategies.open_at_time_shift_close(df, dates[0], tickers[0], tfs[1], '18:50', 1)  #, min_No_trade, max_allowed_sl, success_rate, print_df=False)
strategies = pd.concat([strategies, strategy4])

# -- Strategies dataframe with trade systems validated with minimum requirements


print()
print()
print(strategies.to_string())