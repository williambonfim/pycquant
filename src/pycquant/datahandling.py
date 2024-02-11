import pandas as pd
from utils import init_strategy_results_df
import datetime as dt
import os

def compile_data(csv_original_path, symbol, tf = 'M5', calc_pct = False, save_to_csv_path = ''):

    # Read .csv file from a local path based on the ticker name and timeframe name
    df = pd.read_csv('{}/{}_{}.csv'.format(csv_original_path, tf, symbol))
    
    # Adjust time column to Pandas datetime and set it as index of the df
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # Drop columns that will not be used
    df.drop(['spread', 'real_volume', 'tick_volume'], axis=1, inplace=True)

    # Calculate percentage change based on the last close value
    if calc_pct:
        df['high_pct']  = (df['high']  - df['close'].shift(1)) / df['close'].shift(1)
        df['low_pct']   = (df['low']   - df['close'].shift(1)) / df['close'].shift(1)
        df['close_pct'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)
    
    # Create a target column with only 0
    df['target'] = 0
    df['pct_target'] = 0

    # Save the df into a .csv file
    if save_to_csv_path != '':
        df.to_csv(f'{save_to_csv_path}/{symbol}_{tf}.csv')

    print(f'{symbol}_{tf} compiled')

    # Return the dataframe
    return df

def save_analysis_results(df, csv_file_path):
    
    current_dt = dt.datetime.now()
    file_name = csv_file_path + f'/analysis_{current_dt}.csv'
    df.to_csv(file_name)

def read_analysis_csv_data(csv_file_path, last_analysis_No):

    files_list = [item for item in os.listdir(csv_file_path) if not item.startswith('.')]
    file = files_list[last_analysis_No-1]
    df = pd.read_csv(f'{csv_file_path}/{file}')

    print()
    print('=========================================')
    print(df.to_string())
    print(f'No. of strategies: {len(df)}')
    print('=========================================')



# ========== TO UPDATE BELOW ==============
def read_data(symbol, tf):

    # Read the .csv file saved from compile_data
    df = pd.read_csv(f'/Volumes/PiNAS/market/1_Statistic_Method/Statistic Data/{symbol}_{tf}.csv')

    # Adjust the time column to Pandas datetime and set it as index of the df
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    print(f'{symbol}_{tf}')

    # Return the dataframe
    return df


