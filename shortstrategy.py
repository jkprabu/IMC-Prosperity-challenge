from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

LIMITS = {"PEARLS": 20, "BANANAS": 20}

class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            N=0
            if product == "PEARLS":
            	N=34
            elif product == "BANANAS":
                N=5
            if N:

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # We will calculate the simple moving average (SMA) of the last N prices
                # and use that as the fair value
                prices = list(order_depth.buy_orders.keys()) + list(order_depth.sell_orders.keys())
                acceptable_price = sum(prices) / len(prices)
                # if len(prices) < N:
                #     # If there are not enough prices to calculate the SMA, use a default value of 1
                #     sma = sum(prices) / len(prices)
                #     acceptable_price = sma
                # else:
                #     sma = sum(prices[-N:]) / N
                #     acceptable_price = sma
                ls = list(order_depth.sell_orders.keys())
                ls.sort()
                for price in ls:
                    sell_volume = order_depth.sell_orders[price]
                    if price > acceptable_price:
                        break
                    print("BUY", str(-sell_volume) + "x", price)
                    orders.append(Order(product, price, -sell_volume))

                # If statement checks if there are any SELL orders in the PEARLS market

                    
                
                # if len(order_depth.sell_orders) > 0:

                #     # Sort all the available sell orders by their price,
                #     # and select only the sell order with the lowest price
                #     best_ask = min(order_depth.sell_orders.keys())
                #     best_ask_volume = order_depth.sell_orders[best_ask]

                #     # Check if the lowest ask (sell order) is lower than the above defined fair value
                #     if best_ask < acceptable_price:

                #         # In case the lowest ask is lower than our fair value,
                #         # This presents an opportunity for us to buy cheaply
                #         # The code below therefore sends a BUY order at the price level of the ask,
                #         # with the same quantity
                #         # We expect this order to trade with the sell order
                #         print("BUY", str(-best_ask_volume) + "x", best_ask)
                #         orders.append(Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                ls = list(order_depth.buy_orders.keys())
                ls.sort(reverse=True)
                for price in ls:
                    bid_volume = order_depth.buy_orders[price]
                    if price < acceptable_price:
                        break
                    print("SELL", str(bid_volume) + "x", price)
                    orders.append(Order(product, price, -bid_volume))

                # Add all the above the orders to the result dict
                result[product] = orders

        # Return the dict of orders
        # These possibly contain buy or sell orders for PEARLS
        # Depending on the logic above
        
        return result