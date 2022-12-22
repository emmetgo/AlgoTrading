## this was copied of graphplot.py for a simple strat to test the limit order, then put into strat.py when it works
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

cerebro = backtrader.Cerebro()

if not ALPACA_PAPER:
  broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
  cerebro.setbroker(broker)

DataFactory = store.getdata  # or use alpaca_backtrader_api.AlpacaData
data0 = DataFactory(dataname='F', historical=True, fromdate=datetime(
    2021, 7, 12), timeframe=backtrader.TimeFrame.Minutes)   # year, month, day

cerebro.adddata(data0)


############______________________________________________________________--__-_-__-__########################
##stratagy below runs trading


class limitSMA(backtrader.Strategy):

    #cerebro.addsizer(backtrader.sizers.FixedSize, stake=700)
    def __init__(self):
        sma1 = backtrader.ind.SMA(period=9)  # fast moving average
        sma2 = backtrader.ind.SMA(period=1)    # slow moving average
        #sma3 = backtrader.ind.SMA(period=3)
        self.crossover = backtrader.ind.CrossOver(sma2, sma1)  # crossover signal #can switch 1&2
        #self.crossover2 = backtrader.ind.CrossOver(sma3, sma2)



    def next(self):
        if not self.position:  # not in the market
            if self.crossover < 0:  # if fast crosses slow to the upside
            #if self.data[0] > self.crossover:  #FIX TO GET BUY POINT AT THE CROSS OR THE LOW INTEAD OF ONLY BUIY IF HIGHER THAN LAST, SELL, MIGHGHT NEED TO FIX TIN THE SEL ARREAS
                #price = self.crossover == -1 # self.data.close -10, both return the same value
                                     # sma grewater thna adata clsoe
                #price = self.p
                #self.buy(exectype=backtrader.Order.Limit, price=price, size=1000)  # enter long
                self.buy(size=100)
            #self.buyprice = order.executed.price

                print(self.position.price), print(self.position.size)

        elif self.crossover > -1:       # in the market & cross to the downside
            #if not self.data[-1] < self.data[0]:
          ##      #if data0[0] < data0[-1]:
            if self.position.price < self.data0:
                price = self.position.price + 1.50
                self.close(price=price, size=10000)  # close long position


### now tie in the short play, for seperate strat for f,pcg,ge, others:
cerebro.addstrategy(limitSMA)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()



#4### wont run with currtent pip, needs new envirmment, from thbe 3.8 settings (update made 5am on

#### on 12/16 at 5 am
