from secret.local_settings import pycquant_path, df_csv_path, analysis_data_csv, min_trading_parameters_path
import sys
sys.path.insert(0, pycquant_path)
from pycquant import MP_LoopStrategies
import datahandling
import datetime as dt
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == "__main__":
    # =========================================================================================================
    # =========================================================================================================
    # =========================================================================================================
    # --- Input parameters ---
    # -- General parameters
    print()
    # Select symbol you want to do the analysis
    symbols = ['Ger40', 'HKInd', 'Usa500', 'UsaTec', 'UsaInd', 'UsaRus', 'Bra50', 'Jp225', 'Aus200']
    # Select the timeframe of the data to do the analysis
    tfs = ['M5']
    # Select the initial date from where the analysis will start
    dates = [dt.date(2024,2,14), dt.date(2024,3,1), dt.date(2024,3,15), dt.date(2024,4,1)]

    # -- Trade system minimum requirements
    min_No_trade    = 15
    max_allowed_sl  = 0.02
    success_rate    = 0.80
    no_last_trades  = 6

    # -- Specific strategies input
    # Candle time to strategies time dependent
    times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 5)]
    candles_shifts = range(96) #96

    df_parameters = datahandling.read_minimum_trading_parameters(min_trading_parameters_path)
    # =========================================================================================================
    # =========================================================================================================
    # =========================================================================================================

    initial_time = dt.datetime.now()
    print(initial_time)
    # ------
    # --- strategy check ---
    strategies = datahandling.init_strategy_results_df()
    


    strategy_p = MP_LoopStrategies.open_at_time_shift_close(df_csv_path, dates, symbols, tfs, times, candles_shifts, min_No_trade, max_allowed_sl, success_rate, no_last_trades, print_df=False, df_min_margin_volume=df_parameters)
    strategies = pd.concat([strategies, strategy_p])
    print(f'Strategy analysis time: {dt.datetime.now()-initial_time}')
    print()
    # ------

    strategies = strategies.sort_values(by=['%_System_result'], ascending=False)

    #print(strategies.to_string())
    print(f'No. of strategies: {len(strategies)}')

    datahandling.save_analysis_results(strategies, analysis_data_csv)

    final_time = dt.datetime.now()
    total_time = final_time-initial_time
    print(f'Total analysis time: {total_time}')