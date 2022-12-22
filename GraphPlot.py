## this runs, returns thr backtrader plot, starting and final account valuse, and plots each buy and sell point
from datetime import datetime

import alpaca_backtrader_api
import backtrader

ALPACA_API_KEY = "KEY"
ALPACA_SECRET_KEY = "KEY"
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
    2020, 7, 27), timeframe=backtrader.TimeFrame.Minutes)

cerebro.adddata(data0)

##########################################################################################

class OrderPlSMA(backtrader.Strategy):

    #cerebro.addsizer(backtrader.sizers.FixedSize, stake=700)
    def __init__(self):
        sma1 = backtrader.ind.SMA(period=3)  # fast moving average
        sma2 =  backtrader.ind.SMA(period=1)    # slow moving average
        #sma3 = backtrader.ind.SMA(data0)
        self.crossover = backtrader.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy(size=1000)  # enter long

        #elif self.position > sma3:
        elif self.crossover < 0:  # in the market & cross to the downside
            self.close(size=1000)  # close long position

cerebro.addstrategy(OrderPlSMA)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()

