import pandas as pd
from utils import init_strategy_results_df
import datetime as dt
import os


def update_D1_data(csv_original_path, symbols) -> None:
    tf = 'D1'
    for symbol in symbols:
        print(symbol)
        df = pd.read_csv('{}/{}_{}.csv'.format(csv_original_path, tf, symbol))
        df['time'] = pd.to_datetime(df['time'], format='mixed')
        df['time'] = df['time'].dt.strftime('%Y-%m-%d')
        df.set_index('time', inplace=True)
        df.to_csv(f'{csv_original_path}/{tf}_{symbol}.csv')

def compile_data(csv_original_path, symbol, tf = 'M5', calc_pct_last_close=False, calc_pct_last_open=False, calc_pct_current_open=False, save_to_csv_path = ''):

    # Read .csv file from a local path based on the ticker name and timeframe name
    df = pd.read_csv('{}/{}_{}.csv'.format(csv_original_path, tf, symbol))
    
    # Adjust time column to Pandas datetime and set it as index of the df
    if tf == 'D1':
        #pd.to_datetime(df['time'], format='mixed', dayfirst=True)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
    else:
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

    # Drop columns that will not be used
    df.drop(['spread', 'real_volume', 'tick_volume'], axis=1, inplace=True)

    # Calculate percentage change based on the last close value
    if calc_pct_last_close:
        df['high_pct']  = (df['high']  - df['close'].shift(1)) / df['close'].shift(1)
        df['low_pct']   = (df['low']   - df['close'].shift(1)) / df['close'].shift(1)
        df['close_pct'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)
    
    if calc_pct_last_open:
        df['high_pct']  = (df['high']  - df['open'].shift(1)) / df['open'].shift(1)
        df['low_pct']   = (df['low']   - df['open'].shift(1)) / df['open'].shift(1)
        df['close_pct'] = (df['close'] - df['open'].shift(1)) / df['open'].shift(1)
    
    if calc_pct_current_open:
        df['high_pct']  = (df['high']  - df['open']) / df['open']
        df['low_pct']   = (df['low']   - df['open']) / df['open']
        df['close_pct'] = (df['close'] - df['open']) / df['open']

    # Create a target column with only 0
    df['target'] = 0
    df['pct_target'] = 0

    # Save the df into a .csv file
    if save_to_csv_path != '':
        df.to_csv(f'{save_to_csv_path}/{symbol}_{tf}.csv')

    print(f'{symbol}_{tf} compiled')

    # Return the dataframe
    return df

def save_analysis_results(df, csv_file_path) -> None:
    
    current_dt = dt.datetime.now()
    file_name = csv_file_path + f'/analysis_{current_dt}.csv'
    df.to_csv(file_name, index=False)

def read_analysis_csv_data(csv_file_path, last_analysis_No):

    files_list = [item for item in os.listdir(csv_file_path) if not item.startswith('.')]
    files_list.sort()
    file = files_list[-last_analysis_No]
    df = pd.read_csv(f'{csv_file_path}/{file}')

    print()
    print('=========================================')
    print(f'{file}')
    print(df.to_string())
    print(f'No. of strategies: {len(df)}')
    print('=========================================')

    return df

def read_minimum_trading_parameters(csv_file_path):

    df = pd.read_csv(csv_file_path, index_col=0)

    return df


