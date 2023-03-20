from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Trade
import math

LIMITS = {"PEARLS": 20, "BANANAS": 20}
ENTRY_LIMITS = {"PEARLS": 10, "BANANAS": 10}


class Trader:

    

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            N=0
            if product == "PEARLS":
            	N=45
            elif product == "BANANAS":
                N=45
            if N:
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
                s = 0
                c = 0
                for trade in market_trades:
                    if (state.timestamp-trade.timestamp)/100 <= N:
                        s+=trade.price
                        c+=1
                if c:
                    sma = s/c
                else:
                    sma = 0
                
                # if len(prices) < N:
                #     # If there are not enough prices to calculate the SMA, use a default value of 1
                #     sma = sum(prices) / len(prices)
                #     acceptable_price = sma
                # else:
                #     sma = sum(prices[-N:]) / N
                #     acceptable_price = sma

                # If statement checks if there are any SELL orders in the PEARLS market
                prices = list(order_depth.buy_orders.keys()) + list(order_depth.sell_orders.keys())
                avg_price = sum(prices) / len(prices)
                if avg_price >= sma*5:
                    pos = 0
                    if product in state.position:
                        pos = state.position[product]
                    buy_quantity = min(LIMITS[product]- pos, ENTRY_LIMITS[product])
                    print("BUY", str(buy_quantity) + "x", avg_price)
                    orders.append(Order(product, math.floor(avg_price), buy_quantity))

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if avg_price <= sma*5:
                    pos = 0
                    if product in state.position:
                        pos = state.position[product]
                    sell_quantity = max(-LIMITS[product]- pos, -ENTRY_LIMITS[product])
                    print("SELL", str(sell_quantity) + "x", avg_price)
                    orders.append(Order(product, math.ceil(avg_price), sell_quantity))
                
                

                # Add all the above the orders to the result dict
                result[product] = orders

        # Return the dict of orders
        # These possibly contain buy or sell orders for PEARLS
        # Depending on the logic above
        return result
