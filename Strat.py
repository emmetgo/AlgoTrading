#this was coppied from 'Nov.py' as the ont ont that ran to build the latest strat
## this runs, returns thr backtrader plot, starting and final account valuse, and plots each buy and sell point

from datetime import datetime

import alpaca_backtrader_api
import backtrader

ALPACA_API_KEY = "key"
ALPACA_SECRET_KEY = "key"
ALPACA_PAPER = True

store = alpaca_backtrader_api.AlpacaStore(
    key_id = ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER
)

cerebro = backtrader.Cerebro()  #also0 lkower may commenbt again

if not ALPACA_PAPER:
  broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
  cerebro.setbroker(broker)

DataFactory = store.getdata  # or use alpaca_backtrader_api.AlpacaData
data0 = DataFactory(dataname='F', historical=True, fromdate=datetime(
    2021, 7, 2), timeframe=backtrader.TimeFrame.Minutes)      #calender in YYYY, MM, DD format

#cerebro.adddata(data0)

##########################################################################################

class Strat(backtrader.SignalStrategy):
    # Logs each minuet and price at the time,
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        #Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        sma1 = backtrader.ind.SMA(period=1)
        sma2 = backtrader.ind.SMA(period=3)
        self.sma1 = backtrader.ind.SMA(period=1)  # fast moving average, #this and next 3 lines normally below
        self.sma2 = backtrader.ind.SMA(period=3)  # slow moving average
        # sma3 = backtrader.ind.SMA(data0)
        self.crossover = backtrader.ind.CrossOver(sma1, sma2)  # crossover signal
        self.crossover2 = backtrader.ind.CrossOver(sma2, sma1)  # crossover signal

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

            # Write down: no pending order
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

    ### all below this is the strat, but calls on whats in the def to start
##___________________________________________________________________________________

        if not self.position:  # not in the market
            if self.crossover > self.crossover2:  # if fast crosses slow to the upside only line really changes buy as of now
                #if self.sma1 > self.sma2:
            #if self.crossover2 < self.crossover: #\
                    #and self.sma2 < self.sma1:
                #keep all, only edid the order size
                        # BUY, BUY, BUY!!! (with default parameters)
                self.log('BUY CREATE, %.2f' %self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy(size=1000)

        elif self.crossover < self.crossover2:             #self.crossover < 0:   # if in the market & cross to the downside
            #if (self.bar_executed + .50) > self.dataclose[0]:                                          #self.buy < self.crossover:
            #if self.bar_executed > self.dataclose[0]:                                            #if     %.2f' %self.dataclose[0]:
            #if self.bar_executed > self.buyprice:
                #return  # this make it so only one buy is in, keep until fix buy location

                #keep all, only edit the order size
                #self.close(size=1000)  # close long position
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' %self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=1000)


if __name__ == '__main__':
    cerebro.adddata(data0)
    cerebro.addstrategy(Strat)
    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.000)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()



### write new strat, for a comapany that is above a dollar but below 5,
## buy 10,000 shares, after 1 cents, sell for 100
## other companies be able to change to 5 cents to sell for 500, but then
# hold off buyinh again for contions of multiple closes in a row are down
