import MetaTrader5 as mt5
import datetime as dt
import pandas as pd
from MT5utils import MT5




# ==============================================================

class PctStrategies:

    def __init__(self, symbol, timeframe, volume, pct, buy=True, last_close=False, last_open=False, current_open=False, check_order=False):

        self.symbol = symbol
        self.timeframe = timeframe
        self.pct = pct/100
        self.lot = volume
        self.buy = buy
        self.last_close = last_close
        self.last_open = last_open
        self.current_open = current_open
        self.check_order = check_order
        self.comment = PctStrategies.comment_strategy(pct, last_close, last_open, current_open)

        PctStrategies.check_reference(self)

    def comment_strategy(pct, last_close, last_open, current_open):

        if last_close:
            return f'PyS-LC {pct}'
        if last_open:
            return f'PyS-LO {pct}'
        if current_open:
            return f'PyS-CO {pct}'
        else:
            return 'PyS'

    def check_reference(abc) -> None:
        
        check_candle_reference = abc.last_close + abc.last_open + abc.current_open

        if check_candle_reference != 1:
            print()
            print('Invalid candle reference. Define a correct candle reference (last_close or last_open or current_open)!')
            print()
            quit()

    def pending_order(abc, entry_price):

        if abc.check_order:
            if abc.buy:
                print('BUY:')
                order = MT5.check_buy_pending(abc.symbol, abc.lot, entry_price, comment=abc.comment)
                MT5.print_request(order)
                print()

            else:
                print('SELL:')
                order = MT5.check_sell_pending(abc.symbol, abc.lot, entry_price, comment=abc.comment)
                MT5.print_request(order)
                print()
    
        else:
            if abc.buy:
                print('BUY:')
                order = MT5.buy_pending(abc.symbol, abc.lot, entry_price, comment=abc.comment)
                MT5.print_request(order)
                print()

            else:
                print('SELL:')
                order = MT5.sell_pending(abc.symbol, abc.lot, entry_price, comment=abc.comment)
                MT5.print_request(order)
                print()

    def place_order(abc):

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
        
        tf = dict[abc.timeframe]

        if (abc.last_close):

            last_close = MT5.get_rates(abc.symbol, number_of_candles=2, timeframe=tf).close[-2]
            entry_price = round(last_close * (1 + abc.pct), 2)
            print(f'Last close: {last_close} / entry_price {entry_price}')
            
            PctStrategies.pending_order(abc, entry_price)

        elif (abc.last_open):

            last_open = MT5.get_rates(abc.symbol, number_of_candles=2, timeframe=tf).open[-2]
            entry_price = round(last_open * (1 + abc.pct), 2)
            print(f'Last open: {last_open} / entry_price {entry_price}')

            PctStrategies.pending_order(abc, entry_price)

        elif (abc.current_open):

            current_open = MT5.get_rates(abc.symbol, number_of_candles=2, timeframe=tf).open[-1]
            entry_price = round(current_open * (1 + abc.pct), 2)
            print(f'Current open: {current_open} / entry_price {entry_price}')

            PctStrategies.pending_order(abc, entry_price)

# ==============================================================
class OpenCloseAtTimeStrategies():
    #def __init__(self, symbol, timeframe, lot, pct, buy=True, last_close=False, last_open=False, current_open=False, check_order=False):

    def __init__(self, open_order_at_time, close_order_at_time, symbol, volume, buy=True, check_order=False):
        self.open_order_at_time = open_order_at_time
        self.close_order_at_time = close_order_at_time
        self.symbol = symbol
        self.volume = volume
        self.comment = OpenCloseAtTimeStrategies.comment_strategy(open_order_at_time, close_order_at_time)
        self.buy = buy
        self.check_order = check_order
        self.magic = 10001
        self.checker = 0
        self.order = []
        self.close_order = []

    def comment_strategy(open_order_at_time, close_order_at_time):

        return f'PyS-AtT: {open_order_at_time}/{close_order_at_time}'

    # Open the buy or sell order
    def place_order(abc):
        time0 = dt.datetime.now().time().replace(microsecond=0)
        if time0 == abc.open_order_at_time:

            if abc.checker == 0:
                
                if abc.buy == True:
                    
                    if abc.check_order:

                        abc.order = MT5.check_buy_market(abc.symbol, abc.volume, comment = abc.comment, magic = abc.magic)
                        abc.checker = 1
                        print()
                        MT5.print_request(abc.order)
                        print()
                    
                    else:

                        abc.order = MT5.buy_market(abc.symbol, abc.volume, comment = abc.comment, magic = abc.magic)
                        abc.checker = 1
                        print()
                        MT5.print_request(abc.order)
                        print()
                
                else:

                    if abc.check_order:

                        abc.order = MT5.check_sell_market(abc.symbol, abc.volume, comment = abc.comment, magic = abc.magic)
                        abc.checker = 1
                        print()
                        MT5.print_request(abc.order)
                        print()

                    else:

                        abc.order = MT5.sell_market(abc.symbol, abc.volume, comment = abc.comment, magic = abc.magic)
                        abc.checker = 1
                        print()
                        MT5.print_request(abc.order)
                        print()

            else:
                pass
            
        else:
            pass

    # Close the opened order
    def close_opened_order(abc):
        time0 = dt.datetime.now().time().replace(microsecond=0)

        if time0 == abc.close_order_at_time:

            if abc.checker == 1:

                if abc.buy == True:

                    if abc.check_order:
                        print('Time to close opened buy...')
                        abc.checker = 2

                    else:

                        abc.close_order = MT5.close_open_buy(abc.order)
                        abc.checker = 2
                        print()
                        MT5.print_request(abc.close_order)
                        print()
                
                else:

                    if abc.check_order:
                        print('Time to close opened sell...')
                        abc.checker = 2

                    else:

                        abc.close_order = MT5.close_open_sell(abc.order)
                        abc.checker = 2
                        print()
                        MT5.print_request(abc.close_order)
                        print()


