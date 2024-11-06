# Author: Michael Daniels
# Agent Name: finalagentMPD
#
# The author of this code hereby permits it to be included as a part of the ABIDES distribution, 
# and for it to be released under any open source license the ABIDES authors choose to release ABIDES under.



from agent.TradingAgent import TradingAgent
import pandas as pd
import numpy as np
import os
from contributed_traders.util import get_file


class mdaniels33_finalagentMPD(TradingAgent):
    """
    Enhanced Trading Agent that uses an RSI for high-frequency trading decisions,
    in addition to comparing past mid-price observations with exponential moving averages.
    """

    def __init__(self, id, name, type, symbol, starting_cash,
                 min_size, max_size, wake_up_freq='60s',
                 log_orders=False, random_state=None):
        
        super().__init__(id, name, type, starting_cash=starting_cash, log_orders=log_orders, random_state=random_state)
        self.symbol = symbol
        self.size = 20
        self.wake_up_freq = wake_up_freq
        self.mid_list, self.avg_win1_list, self.avg_win2_list = [], [], []
        self.high_list, self.low_list, self.close_list = [], [], []  # Lists for Stochastic Oscillator
        self.gains, self.losses, self.rsi_values = [], [], []  # Lists for RSI calculation
        self.rsi_period = 6  # Look-back period for RSI
        self.log_orders = log_orders
        self.state = "AWAITING_WAKEUP"
        self.trade_counter = 0  # Initialize trade counter
        self.cash_balance = starting_cash
        self.last_purchase_price = None
        self.last_trade_type = None 
        



    def kernelStarting(self, startTime):
        super().kernelStarting(startTime)
        with open(get_file('mdaniels33_finalagentMPD/finalagentMPD.cfg'), 'r') as f:
            self.window1, self.window2 = [int(w) for w in f.readline().split()]

    def wakeup(self, currentTime):
        can_trade = super().wakeup(currentTime)
        if not can_trade: return
        self.getCurrentSpread(self.symbol)
        self.state = 'AWAITING_SPREAD'

    def dump_shares(self):
    # get rid of any outstanding shares we have
        if self.symbol in self.holdings and len(self.orders) == 0:
            order_size = self.holdings[self.symbol]
            bid, _, ask, _ = self.getKnownBidAsk(self.symbol)

            # Check that both bid and ask are valid (not None and greater than 0)
            if bid is not None and ask is not None and bid > 0 and ask > 0:
                if order_size > 0:
                    # If holding positive shares, sell at bid price
                    self.placeLimitOrder(self.symbol, quantity=order_size, is_buy_order=False, limit_price=bid)
                    self.trade_counter += 1
                elif order_size < 0:
                    # If holding a short position, buy back at ask price to cover
                    self.placeLimitOrder(self.symbol, quantity=-order_size, is_buy_order=True, limit_price=ask)
                    self.trade_counter += 1


    def receiveMessage(self, currentTime, msg):
        super().receiveMessage(currentTime, msg)
        if self.state == 'AWAITING_SPREAD' and msg.body['msg'] == 'QUERY_SPREAD':
            dt = (self.mkt_close - currentTime) / np.timedelta64(1, 'm')
            if dt < 30:
                self.dump_shares()  # Make sure to cover all short positions before the end of the day
            else:
                bid, _, ask, _ = self.getKnownBidAsk(self.symbol)
                if bid and ask:
                    mid_price = (bid + ask) / 2
                    self.close_list.append(mid_price)  # Assuming mid_price as a proxy for close price for RSI calculation

                    if len(self.close_list) > 1:
                        change = self.close_list[-1] - self.close_list[-2]
                        self.gains.append(max(change, 0))
                        self.losses.append(max(-change, 0))
                        self.gains = self.gains[-self.rsi_period:]
                        self.losses = self.losses[-self.rsi_period:]

                        if len(self.gains) == self.rsi_period:
                            avg_gain = sum(self.gains) / self.rsi_period
                            avg_loss = sum(self.losses) / self.rsi_period if sum(self.losses) != 0 else 1
                            rs = avg_gain / avg_loss
                            rsi = 100 - (100 / (1 + rs))
                            if self.last_purchase_price is not None: 
                                
                                if self.last_trade_type == "buy" and mid_price < self.last_purchase_price*.9:
                                    order_size = self.size
                                    self.placeLimitOrder(self.symbol, quantity = order_size, is_buy_order = False, limit_price = bid)
                                    self.last_purchase_price = ask
                                    self.last_trade_type = None
                                    self.trade_counter += 1
                                
                                elif self.last_trade_type == "sell" and mid_price > self.last_purchase_price*1.1:
                                    order_size = self.size
                                    self.placeLimitOrder(self.symbol, quantity=order_size, is_buy_order=True, limit_price=ask)
                                    self.last_purchase_price = bid
                                    self.last_trade_type = None
                                    self.trade_counter += 1
                                
                                elif rsi < 20 and self.holdings['CASH'] >= (self.size * ask):
                                    # Oversold condition, initiate a buy and cover a short sell
                                    order_size = self.size
                                    self.placeLimitOrder(self.symbol, quantity=2*order_size, is_buy_order=True, limit_price=ask)
                                    self.last_purchase_price = bid
                                    self.last_trade_type = "buy"
                                    self.trade_counter += 1
                                elif rsi > 80:
                                    # Overbought condition, initiate a short sell
                                    order_size = self.size
                                    self.placeLimitOrder(self.symbol, quantity = 2*order_size, is_buy_order = False, limit_price = bid)
                                    self.last_purchase_price = ask
                                    self.last_trade_type = "sell"
                                    self.trade_counter += 1
                            else: 
                                if rsi < 20:
                                    # Oversold condition, initiate a buy or cover a short sell
                                    order_size = self.size
                                    self.placeLimitOrder(self.symbol, quantity=order_size, is_buy_order=True, limit_price=ask)
                                    self.last_purchase_price = bid
                                    self.last_trade_type = "buy"
                                    self.trade_counter += 1
                                elif rsi > 80:
                                # Overbought condition, initiate a short sell
                                    order_size = self.size
                                    self.placeLimitOrder(self.symbol, quantity = order_size, is_buy_order = False, limit_price = bid)
                                    self.last_purchase_price = ask
                                    self.last_trade_type = "sell"
                                    self.trade_counter += 1
                          
            self.setWakeup(currentTime + self.getWakeFrequency())
            self.state = 'AWAITING_WAKEUP'

    def getWakeFrequency(self):
        return pd.Timedelta(self.wake_up_freq)

    def number_of_counting(self):
        """
        Returns the number of trades executed by the agent.
        """
        return self.trade_counter

    def author(self): 
        return "mdaniels33"
        
    def agentname(self):
        return "mdaniels33_finalagentMPD"



