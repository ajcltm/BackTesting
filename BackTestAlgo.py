class BackTester:
    def __init__(self, initialize, tradingAlgo):
        print('Hello backtesting')
        self.context = {'dataColumn': ''}
        initialize(self.context)

        self.tradingAlgo = tradingAlgo

    def run(self, data):
        dataColumn = self.context['dataColumn']
        for dayData in data[dataColumn]:
            actionDict = self.tradingAlgo(dayData)
            if actionDict['type'] == 'sell':
                # 판다
                print('sell')
            elif actionDict['type'] == 'buy':
                # 산다
                print('buy')
