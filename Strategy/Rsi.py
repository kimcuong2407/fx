from backtesting import Backtest, Strategy

import talib

class RsiOscillator(Strategy):
    def init(self):
        self.rsi = self.I(talib.RSI)