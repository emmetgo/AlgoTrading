# this runs a closing time at each minuet an dplots the symbol over the time set
#copy of patd -> strats
import alpaca_backtrader_api
import backtrader
from datetime import datetime


ALPACA_API_KEY = "PKWIUE7UEL1VRYZ5V9F6"
ALPACA_SECRET_KEY = "Q3i7QXbQG2098nIutKqmQaof2oVLiqwLIk93mcOY"
ALPACA_PAPER = True
cerebro = backtrader.Cerebro()


#Logs each minuet and price at the time,
class Description(backtrader.SignalStrategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        #Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))
            self.bar_executed = len(self)

        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])


#cerebro = backtrader.Cerebro() # this is also in line 8?
cerebro.addstrategy(Description)

store = alpaca_backtrader_api.AlpacaStore(
    key_id = ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER
)

if not ALPACA_PAPER:
  broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
  cerebro.setbroker(broker)

DataFactory = store.getdata  # or use alpaca_backtrader_api.AlpacaData
data0 = DataFactory(dataname='F', historical=True, fromdate=datetime(
    2020, 11, 4), timeframe=backtrader.TimeFrame.Minutes)

cerebro.adddata(data0)
#cerebro.addsizer(bt.sizers.FixedSize, stake=100000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()
