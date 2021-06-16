import pandas as pd
import types

class BackTester:
    def __init__(self, initialize, tradingAlgo):
        print('Hello backtesting')
        self.context = types.SimpleNamespace()
        initialize(self.context)

        self.portfolio = types.SimpleNamespace()
        positions = pd.DataFrame(columns=[self.context.security], index=['amounts', 'type'])
        self.portfolio.positions = positions
        self.context.portfolio = self.portfolio

        self.tradingAlgo = tradingAlgo

    def run(self, data):
        resultColumns = ['date', 'portfolio_value']
        self.result = pd.DataFrame(columns=resultColumns)
        for i in range(0, len(data)):
            dayData = data.iloc[i,:]
            s = pd.Series([dayData.name, self.context.portfolio.positions[self.context.security].amounts*dayData[self.context.security]], index=resultColumns)
            self.result = self.result.append(s, ignore_index=True)
            self.tradingAlgo(self.context, dayData)

        return self.result

    def order(self, ticker, price, quantity) :
        self.context.portfolio.positions[self.context.security].amounts += quantity
