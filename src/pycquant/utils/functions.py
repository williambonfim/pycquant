import pandas as pd
import os
import sys

def print_progress_bar(index, total, label):
    n_bar = 50  # Progress bar width
    progress = index / total
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {label}")
    sys.stdout.flush()

def full_path(relative_path):
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), relative_path)

    return full_path

def print_symbol_df(df, symbol, tf, entry_criteria, exit_criteria):
    print()
    print(f'========= Dataframe - {symbol} - {tf} =========')
    print(f'Entry: {entry_criteria}')
    print(f'Exit: {exit_criteria}')
    print(df.to_string())
    print('================================================')

def init_strategy_results_df():
    
    df = pd.DataFrame(columns = ['symbol', 'timeframe', 'entry_criteria', 'exit_criteria', 'date_0', 'Total_No_candles', 'No_Trades', 'No_tp', '%_tp', 'No_sl', '%_sl', 'Max_tp', 'Max_%_tp', 'Max_sl', 'Max_%_sl', 'Average_result', '%_Average_result', 'System_result', '%_System_result', 'last_5_trades'])
    
    return df

def get_last_x_trades(df, No_Trades=5, profit_per_price_unit=0, profits=False):

    index_list = df[df['pct_target'] != 0].index.tolist()[-No_Trades:]
  
    if profits:

        last_x_trades = df.loc[index_list, ['target']]
        last_x_trades = [(round(x*profit_per_price_unit, 2)) for x in last_x_trades['target']]

    else:
        
        last_x_trades = df.loc[index_list, ['pct_target']]
        last_x_trades = [1 if target > 0 else (-1 if target <0 else 'X') for target in last_x_trades['pct_target']]  

    return last_x_trades

def drop_data_before_initial_date(df, date):

    date = pd.to_datetime(date)
    df = df[~(df.index < date)]

    return df


def symbol_selection(df, symbol, tf, entry_criteria, exit_criteria, date_0, min_No_trade, max_allowed_sl, success_rate, no_trades=5, df_min_margin_volume=pd.DataFrame()):

    df_results = init_strategy_results_df()
   
    # Total No of candles analysed
    Total_No_candles = df.shape[0]
    # Count the number of profit trades
    count_tp = df[df['pct_target'] > 0].count()['pct_target']

    # Count the total number of trades
    total_No_trades = df.astype(bool).sum(axis=0)['pct_target']

    if total_No_trades < min_No_trade:
        return df_results

    # Count the number of loser trades
    count_sl = total_No_trades - count_tp

    # Calculate pct tp
    if total_No_trades == 0:
        pct_tp = 0
        pct_sl = 0
    else: 
        pct_tp = count_tp/total_No_trades
        pct_sl = count_sl/total_No_trades

    if (pct_tp > (round(1-success_rate,4)) and pct_tp < success_rate):
        return df_results    

    # Calculate total system result in the time period
    pct_system_result = df.sum()['pct_target']
    system_result = df.sum()['target']

    # Calculate maximum profit trade
    pct_max_tp = df.max()['pct_target']
    max_tp = df.max()['target']

    # Calculate maximum loss trade
    pct_max_sl = df.min()['pct_target']

    if (pct_max_sl < -max_allowed_sl and pct_tp >= success_rate):
        return df_results
    
    if (pct_max_sl > max_allowed_sl and pct_tp <= success_rate):
        return df_results

    max_sl = df.min()['target']

    # Calculate average result in the time period
    if pct_system_result == 0 or total_No_trades == 0:
        pct_average_result = 0
        average_result = 0
    else:
        pct_average_result = pct_system_result / total_No_trades
        average_result = system_result / total_No_trades
    
    last_x_trades = get_last_x_trades(df, No_Trades = no_trades)

    # Create a list with the data and the column header
    data = [[   symbol, \
                tf, \
                entry_criteria, \
                exit_criteria, \
                date_0, \
                Total_No_candles, \
                total_No_trades, \
                count_tp, \
                round(pct_tp, 4), \
                count_sl, \
                round(pct_sl, 4), \
                round(max_tp, 2), \
                round(pct_max_tp, 4), \
                round(max_sl, 2), \
                round(pct_max_sl, 4), \
                round(average_result, 2), \
                round(pct_average_result, 4), \
                round(system_result, 2), \
                round(pct_system_result, 4), \
                last_x_trades   ]]
    
    data = pd.DataFrame(data, columns=df_results.columns)
    data = data.dropna(axis=1, how='all')

    df_results = pd.concat([df_results, data])
    
    # Drop results with less trades than minimum amount
    #df_results.drop(df_results.index[df_results['No_Trades'] < min_No_trade], inplace=True)

    # Drop results with success_rate between minimum success_rate
    #index_drop = df_results[(df_results['%_tp'] > (round(1-success_rate,4))) & (df_results['%_tp'] < success_rate)].index
    #df_results.drop(index_drop, inplace=True)

    # Drop results with sl above the maximum allowed
    #index_drop = df_results[(df_results['Max_%_sl'] < -max_allowed_sl) & (df_results['%_tp'] >= success_rate)].index
    #df_results.drop(index_drop, inplace=True)

    #index_drop = df_results[(df_results['Max_%_tp'] > max_allowed_sl) & (df_results['%_tp'] <= (1-success_rate))].index
    #df_results.drop(index_drop, inplace=True)

    if not df_min_margin_volume.empty and not df_results.empty:

        df_min_margin_volume = df_min_margin_volume.loc[[symbol],:]

        min_margin = df_min_margin_volume.loc[symbol, 'min_margin']
        min_volume = df_min_margin_volume.loc[symbol, 'min_volume']
        point = df_min_margin_volume.loc[symbol, 'point']
        profit_per_10000points = df_min_margin_volume.loc[symbol, 'profit_per_10000points']

        profit_per_price_unit = profit_per_10000points / 10000 / point

        df_results['min_volume'] = min_volume
        df_results['min_margin'] = min_margin
        df_results['£_Max_tp'] = round(profit_per_price_unit * df_results.loc[0, 'Max_tp'], 2)
        df_results['£_Max_sl'] = round(profit_per_price_unit * df_results.loc[0, 'Max_sl'], 2)
        df_results['£_Average_result'] = round(profit_per_price_unit * df_results.loc[0, 'Average_result'], 2)
        df_results['£_System_result'] = round(profit_per_price_unit * df_results.loc[0, 'System_result'], 2)
        last_x_trades = [get_last_x_trades(df, No_Trades = no_trades, profit_per_price_unit=profit_per_price_unit, profits=True)]
        df_results['£_last_x_trades'] = last_x_trades

    return df_results

