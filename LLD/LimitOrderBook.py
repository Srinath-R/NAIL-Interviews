import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DSA.DLL import DLL
from uuid import uuid4
from enum import Enum
from collections import defaultdict

class Side(Enum):
    buy = "BUY"
    sell = "SELL"

class Order:
    def __init__(self, side: Side, price: float, quantity: int):
        self.prev = None
        self.next = None
        self.order_id = uuid4()
        self.side = side
        self.price = price
        self.quantity = quantity

class PriceLevel(DLL):
    def match_order(self, quantity: int) -> int:
        total_trade_quantity = 0
        while quantity > 0 and self.head:
            order = self.head
            trade_quantity = min(quantity, order.quantity)
            total_trade_quantity += trade_quantity
            quantity -= trade_quantity
            if order.quantity == trade_quantity:
                print(f"Order {order.order_id}: {order.side} has been executed @ {order.price}.")
                self.pop_left()
            else:
                order.quantity -= trade_quantity 
        return total_trade_quantity

class OrderBook:
    def __init__(self, price_min: float, price_max: float, tick_size: float):
        self.price_min = price_min
        self.price_max = price_max
        self.tick_size = tick_size
        self.size = int((price_max - price_min) / tick_size) + 1
        self.bids = [PriceLevel() for _ in range(self.size)]
        self.asks = [PriceLevel() for _ in range(self.size)]
        self.best_bid = None
        self.best_ask = None
        self.volumes = defaultdict(int)
        self.orders = {}
    
    def price_to_index(self, price: float) -> int:
        return int((price - self.price_min) / self.tick_size)
    
    def index_to_price(self, index: int) -> float:
        return self.price_min + index * self.tick_size
    
    def update_best_price(self, side:Side):
        if side == Side.buy:
            for i in reversed(range(self.size)):
                if not self.bids[i].is_empty():
                    self.best_bid = i
                    return
            self.best_bid = None
        else:
            for i in range(self.size):
                if not self.asks[i].is_empty():
                    self.best_ask = i
                    return
            self.best_ask = None

    def place_order(self, price: float, quantity: int, side: Side):
        if price < self.price_min or price > self.price_max:
            raise ValueError(f"Price {price} is out of range. Must be between {self.price_min} and {self.price_max}.")
        
        index = self.price_to_index(price)
        initial_quantity = quantity
        self.volumes[(side, price)] += quantity
        if side == Side.buy:
            while self.best_ask is not None and self.best_ask <= index and quantity > 0:
                best_sell = self.asks[self.best_ask]
                matched = best_sell.match_order(quantity)
                quantity -= matched
                if best_sell.is_empty():
                    self.update_best_price(side)

            if quantity:
                order = Order(side, price, quantity)
                self.orders[order.order_id] = (order, index)
                self.bids[index].append(order)
                if self.best_bid is None or index > self.best_bid:
                    self.best_bid = index
        else:
            while self.best_bid is not None and self.best_bid >= index and quantity > 0:
                best_buy = self.bids[self.best_bid]
                matched = best_buy.match_order(quantity)
                quantity -= matched
                if best_buy.is_empty():
                    self.update_best_price(side)

            if quantity:
                order = Order(side, price, quantity)
                self.orders[order.order_id] = (order, index)
                self.asks[index].append(order)
                if self.best_ask is None or index > self.best_ask:
                    self.best_ask = index
        if quantity == 0:
            print(f"{side} has been executed @ {price} for {initial_quantity} shares.")
        elif initial_quantity == quantity:
            return order.order_id
        return None

    def cancel_order(self, order_id):
        if order_id not in self.orders:
            print(f"Order {order_id} not found!")
            return
        
        order, index = self.orders.pop(order_id)
        book = self.bids if order.side == Side.buy else self.asks
        book[index].remove(order)
        self.volumes[(order.side, order.price)] -= order.quantity

        if (order.side == Side.buy and index == self.best_bid) or (order.side == Side.sell and index == self.best_ask):
            self.update_best_price(order.side)
        print(f"Order {order_id} has been cancelled.")

    def get_volume_at_price(self, price: float, side: Side) -> int:
        return self.volumes.get((side, price), 0)

# Example Usage
ob = OrderBook(price_min=100.0, price_max=110.0, tick_size=0.5)

ob.place_order(101.0, 10, Side.buy)
order = ob.place_order(101.0, 5, Side.buy)
ob.place_order(103.0, 15, Side.sell)
ob.place_order(100.5, 8, Side.sell)

ob.cancel_order(order)

print("\nVolume at 101.0 (buy):", ob.get_volume_at_price(101.0, Side.buy))
print("Best Bid Index:", ob.best_bid)
print("Best Ask Index:", ob.best_ask)
