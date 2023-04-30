from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Trade

LIMITS = {"PEARLS": 20, "BANANAS": 20, "COCONUTS": 600, "PINA COLADAS": 300}
ENTRY_LIMITS = {"PEARLS": 10, "BANANAS": 10}
SMA_CONSTANT = 2


def long_strat(product, state, NS, NL):
    result = {}
    if product in state.market_trades:
        t = state.market_trades[product]
    else:
        t = []
    market_trades: list[Trade] = t
				
    # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
    order_depth: OrderDepth = state.order_depths[product]

    # Initialize the list of Orders to be sent as an empty list
    orders: list[Order] = []

    # Define a fair value for the PEARLS.
    # We will calculate the simple moving average (SMA) of the last N prices
    # and use that as the fair value
    ss = 0
    cs = 0
    sl = 0
    cl = 0
    for trade in market_trades:
        if (state.timestamp-trade.timestamp)/100 <= NL:
            sl+=trade.price
            cl+=1
        if (state.timestamp-trade.timestamp)/100 <=NS:
            ss+=trade.price
            cs+=1
    if cs:
        smas = ss/cs
    else:
        smas = 0
                
    if cl:
        smal = sl/cl
    else:
        smal = 0
                

    prices = list(order_depth.buy_orders.keys()) + list(order_depth.sell_orders.keys())
    avg_price = sum(prices) / len(prices)
    if smas >= smal*SMA_CONSTANT:
        ls = list(order_depth.sell_orders.keys())
        ls.sort()
        for price in ls:
            sell_volume = order_depth.sell_orders[price]
            if price > avg_price:
                break
            print("BUY", str(-sell_volume) + "x", price)
            orders.append(Order(product, price, -sell_volume))

    # The below code block is similar to the one above,
    # the difference is that it find the highest bid (buy order)
    # If the price of the order is higher than the fair value
    # This is an opportunity to sell at a premium
    if smas <= smal*SMA_CONSTANT:
        ls = list(order_depth.buy_orders.keys())
        ls.sort(reverse=True)
        for price in ls:
            bid_volume = order_depth.buy_orders[price]
            if price < avg_price:
                break
            print("SELL", str(bid_volume) + "x", price)
            orders.append(Order(product, price, -bid_volume))
            
    result[product] = orders
    return result


def short_strat(product, state):
    result = {}
    # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
    order_depth: OrderDepth = state.order_depths[product]

    # Initialize the list of Orders to be sent as an empty list
    orders: list[Order] = []
    prices = list(order_depth.buy_orders.keys()) + list(order_depth.sell_orders.keys())
    acceptable_price = sum(prices) / len(prices)
    ls = list(order_depth.sell_orders.keys())
    ls.sort()
    for price in ls:
        sell_volume = order_depth.sell_orders[price]
        if price > acceptable_price:
            break
        print("BUY", str(-sell_volume) + "x", price)
        orders.append(Order(product, price, -sell_volume))
        
    ls = list(order_depth.buy_orders.keys())
    ls.sort(reverse=True)
    for price in ls:
        bid_volume = order_depth.buy_orders[price]
        if price < acceptable_price:
            break
        print("SELL", str(bid_volume) + "x", price)
        orders.append(Order(product, price, -bid_volume))
    result[product] = orders
    return result

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():
            # Check the current product and use the according strategy
            
            if product == "PEARLS":
                result = short_strat(product, state)
            elif product == "BANANAS":
                NL=144
                NS=84
                result = long_strat(product, state, NS, NL)
            elif product == "COCONUTS":
                NL=144
                NS=84
                result = long_strat(product, state, NS, NL)
            elif product == "PINA COLADAS":
                NL=144
                NS=84
                result = long_strat(product, state, NS, NL)

                
        # Return the dict of orders
        # These possibly contain buy or sell orders for products
        # Depending on the logic above
        
        return result