import MetaTrader5 as mt5
import pandas as pd
import datetime as dt

# ===============================================================================================
# ===============================================================================================
# ===============================================================================================
#                   --- MAIN MT5 TRADING FUNCTIONS ---
# ===============================================================================================
# ===============================================================================================
# ===============================================================================================
class MT5:

    def initialize() -> None:
        # establish connection to the MetaTrader 5 terminal 
        mt5.initialize()

        if not mt5.initialize(): 
            print("initialize() failed, error code =", mt5.last_error()) 
            quit() 

        account_info=mt5.account_info()
        print()
        #print(account_info)
        print('====================================')
        print('CONNECTION SUCCESSFULLY')
        print(f'ACCOUNT NUMBER: {account_info.login}')
        print(f'LEVERAGE: {account_info.leverage}')
        print(f'BALANCE: {account_info.balance}')
        print(f'CURRENCY: {account_info.currency}')
        print(f'FREE MARGIN: {account_info.margin_free}')
        print(f'NAME: {account_info.name}')
        print(f'SERVER: {account_info.server}')
        print('====================================')

    def shutdown() -> None:
        mt5.shutdown()
        print('====================================')
        print('MT5 TERMINAL SHUTDOWN')
        print('====================================')

    # Function to get rates given the Symbol, No. Candles and Timeframe
    def get_rates(symbol, number_of_candles = 100, timeframe = mt5.TIMEFRAME_M1):
        from_date = dt.datetime.now()
        rates = mt5.copy_rates_from(symbol, timeframe, from_date, number_of_candles)
        df_rates = pd.DataFrame(rates)
        df_rates['time'] = pd.to_datetime(df_rates['time'], unit='s')
        df_rates = df_rates.set_index('time')
        #print(df_rates.tail())
        return df_rates

    def find_filling_mode(symbol, deviation):
        for i in range(2):
            request = {
                "action":       mt5.TRADE_ACTION_DEAL,
                "symbol":       symbol,
                "volume":       mt5.symbol_info(symbol).volume_min,
                "type":         mt5.ORDER_TYPE_BUY,
                "price":        mt5.symbol_info_tick(symbol).ask,
                "deviation":    deviation,
                "type_filling": i,
                "type_time":    mt5.ORDER_TIME_GTC
            }

            result = mt5.order_check(request)
            if result.comment == "Done":
                break
        
        #filling_type = find_filling_mode(symbol)
        #filling_type = mt5.symbol_info(symbol).filling_mode

        return i

    def check_buy_market_order(symbol, lot, sl, tp, deviation=10, comment='python script'):
        point = mt5.symbol_info(symbol).point

        filling_type = MT5.find_filling_mode(symbol, deviation)

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       symbol,
            "volume":       lot,
            "type":         mt5.ORDER_TYPE_BUY,
            "price":        mt5.symbol_info_tick(symbol).ask,
            "sl":           mt5.symbol_info_tick(symbol).ask - sl*point,
            "tp":           mt5.symbol_info_tick(symbol).ask + tp*point,
            "deviation":    deviation,
            "comment":      comment,
            "type_filling": filling_type,
            "type_time":    mt5.ORDER_TIME_GTC
        }
        check = mt5.order_check(request)
        reply = check.comment
        return reply, check

    def buy_market_order(symbol, lot, sl, tp, deviation=10, comment='python script', magic=0):
        point = mt5.symbol_info(symbol).point
        filling_type = MT5.find_filling_mode(symbol, deviation)

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       symbol,
            "volume":       lot,
            "type":         mt5.ORDER_TYPE_BUY,
            "price":        mt5.symbol_info_tick(symbol).ask,
            "sl":           mt5.symbol_info_tick(symbol).ask - sl*point,
            "tp":           mt5.symbol_info_tick(symbol).ask + tp*point,
            "deviation":    deviation,
            "magic":        magic, 
            "comment":      comment,
            "type_filling": filling_type,
            "type_time":    mt5.ORDER_TIME_GTC
        }
        
        order = mt5.order_send(request)
        
        return order

    def buy_market_order_sl(symbol, lot, sl, deviation=10, comment='python script', magic=0):
        point = mt5.symbol_info(symbol).point
        filling_type = MT5.find_filling_mode(symbol, deviation)

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       symbol,
            "volume":       lot,
            "type":         mt5.ORDER_TYPE_BUY,
            "price":        mt5.symbol_info_tick(symbol).ask,
            "sl":           mt5.symbol_info_tick(symbol).ask - sl*point,
            "deviation":    deviation,
            "magic":        magic,
            "comment":      comment,
            "type_filling": filling_type,
            "type_time":    mt5.ORDER_TIME_GTC
        }
        
        order = mt5.order_send(request)
        
        return order

    def buy_market(symbol, lot, deviation=10, comment='python script', magic=0):

        filling_type = MT5.find_filling_mode(symbol, deviation)

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       symbol,
            "volume":       lot,
            "type":         mt5.ORDER_TYPE_BUY,
            "price":        mt5.symbol_info_tick(symbol).ask,
            "deviation":    deviation,
            "magic":        magic,
            "comment":      comment,
            "type_filling": filling_type,
            "type_time":    mt5.ORDER_TIME_GTC
        }
        
        order = mt5.order_send(request)
        
        return order

    def close_open_buy(order, deviation = 10):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": order.request.symbol,
            "position": order.order,
            "volume": order.volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(order.request.symbol).bid,
            "deviation": deviation,
            "type_filling": order.request.type_filling,
            "type_time": mt5.ORDER_TIME_GTC
        }

        close_order = mt5.order_send(request)
        return close_order

    def check_sell_market_order(symbol, lot, sl, tp, deviation=10, comment='python script'):
        point = mt5.symbol_info(symbol).point

        filling_type = MT5.find_filling_mode(symbol, deviation)

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       symbol,
            "volume":       lot,
            "type":         mt5.ORDER_TYPE_SELL,
            "price":        mt5.symbol_info_tick(symbol).bid,
            "sl":           mt5.symbol_info_tick(symbol).bid + sl*point,
            "tp":           mt5.symbol_info_tick(symbol).bid - tp*point,
            "deviation":    deviation,
            "comment":      comment,
            "type_filling": filling_type,
            "type_time":    mt5.ORDER_TIME_GTC
        }
        check = mt5.order_check(request)
        reply = check.comment
        return reply, check

    def sell_market_order(symbol, lot, sl, tp, deviation=10, comment='python script', magic=0):
        
        point = mt5.symbol_info(symbol).point
        filling_type = MT5.find_filling_mode(symbol, deviation)

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       symbol,
            "volume":       lot,
            "type":         mt5.ORDER_TYPE_SELL,
            "price":        mt5.symbol_info_tick(symbol).bid,
            "sl":           mt5.symbol_info_tick(symbol).bid + sl*point,
            "tp":           mt5.symbol_info_tick(symbol).bid - tp*point,
            "deviation":    deviation,
            "magic":        magic,
            "comment":      comment,
            "type_filling": filling_type,
            "type_time":    mt5.ORDER_TIME_GTC
        }
        
        order = mt5.order_send(request)
        
        return order
    
    def sell_market_order_sl(symbol, lot, sl, deviation=10, comment='python script', magic=0):
        
        point = mt5.symbol_info(symbol).point
        filling_type = MT5.find_filling_mode(symbol, deviation)

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       symbol,
            "volume":       lot,
            "type":         mt5.ORDER_TYPE_SELL,
            "price":        mt5.symbol_info_tick(symbol).bid,
            "sl":           mt5.symbol_info_tick(symbol).bid + sl*point,
            "deviation":    deviation,
            "magic":        magic,
            "comment":      comment,
            "type_filling": filling_type,
            "type_time":    mt5.ORDER_TIME_GTC
        }
        
        order = mt5.order_send(request)
        
        return order

    def sell_market(symbol, lot, deviation=10, comment='python script', magic=0):

        filling_type = MT5.find_filling_mode(symbol, deviation)

        request = {
            "action":       mt5.TRADE_ACTION_DEAL,
            "symbol":       symbol,
            "volume":       lot,
            "type":         mt5.ORDER_TYPE_SELL,
            "price":        mt5.symbol_info_tick(symbol).bid,
            "deviation":    deviation,
            "magic":        magic,
            "comment":      comment,
            "type_filling": filling_type,
            "type_time":    mt5.ORDER_TIME_GTC
        }

        order = mt5.order_send(request)

        return order

    def close_open_sell(order, deviation = 10):
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": order.request.symbol,
            "position": order.order,
            "volume": order.volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(order.request.symbol).ask,
            "deviation": deviation,
            "type_filling": order.request.type_filling,
            "type_time": mt5.ORDER_TIME_GTC
        }

        close_order = mt5.order_send(request)
        return close_order

    def close_by(open_order, order_close_by):
        request = {
            "action": mt5.TRADE_ACTION_CLOSE_BY,
            "symbol": open_order.request.symbol,
            "position": open_order.order,
            "position_by": order_close_by.order,
            "type_time": mt5.ORDER_TIME_GTC
        }

        close_by_order = mt5.order_send(request)
        return close_by_order

    def change_sl(order, new_sl) -> None:
        point = mt5.symbol_info(order.request.symbol).point

        request = {
            "action": mt5.TRADE_ACTION_MODIFY,
            "symbol": order.request.symbol,
            "position": order.order,
            "sl": order.price + new_sl*point,
            "type_filling": order.request.type_filling,
            "type_time": mt5.ORDER_TIME_GTC
        }

    def check_orders(symbol):

        orders = mt5.orders_get(symbol = symbol) 

        if len(orders) == 0:
            print(f'No orders on {symbol}')
            return 0, None
        else:
            for order in orders:
                print(order)
            return len(orders), orders

    def check_positions(symbol):

        positions = mt5.positions_get(symbol = symbol) 

        if len(positions) == 0:
            print(f'No orders on {symbol}')
            return 0, None
        else:
            for order in positions:
                print(order)
            return len(positions), positions

    def delta_from_open(symbol, timeframe = mt5.TIMEFRAME_M15):

        open = MT5.get_rates(symbol, number_of_candles = 1, timeframe = timeframe)['open'].iat[-1]
        current_price = mt5.symbol_info_tick(symbol).bid
        point = mt5.symbol_info(symbol).point

        delta_open_point = (current_price - open)/point
        
        return delta_open_point

    def check_time_shutdown(time_close_all) -> None:
        if time_close_all <= dt.datetime.now().time().replace(microsecond=0):
            MT5.shutdown()
            quit()