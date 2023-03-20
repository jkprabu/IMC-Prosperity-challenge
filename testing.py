from datamodel import Listing, OrderDepth, Trade, TradingState
from cgptexbot import Trader
timestamp = 1000

listings = {
	"PRODUCT1": Listing(
		symbol="PRODUCT1", 
		product="PRODUCT1", 
		denomination="SEASHELLS"
	),
	"PRODUCT2": Listing(
		symbol="PRODUCT2", 
		product="PRODUCT2", 
		denomination="SEASHELLS"
	),
}
p1 = OrderDepth()
p1.buy_orders = {10: 7, 9: 5}
p1.sell_orders = {11: -4, 12: -8}
p2 = OrderDepth()
p2.buy_orders = {142: 3, 141: 5}
p2.sell_orders = {144: -5, 145: -8}


order_depths = {
	"PRODUCT1": p1,
	"PRODUCT2": p2,	
}

own_trades = {
	"PRODUCT1": [],
	"PRODUCT2": []
}

market_trades = {
	"PRODUCT1": [
		Trade(
			symbol="PRODUCT1",
			price=11,
			quantity=4,
			buyer="",
			seller=""
		)
	],
	"PRODUCT2": []
}

position = {
	"PRODUCT1": 3,
	"PRODUCT2": -5
}

observations = {}

state = TradingState(
	timestamp=timestamp,
  	listings=listings,
	order_depths=order_depths,
	own_trades=own_trades,
	market_trades=market_trades,
    position=position,
    observations=observations
)
t = Trader()
t.run(state)
print("good shit jim")