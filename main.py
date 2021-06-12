import pandas as pd
from BackTestAlgo import *



def my_init(context):
    context['dataColumn'] = 'price'

def handle_data(dayData):
    print(dayData)
    actionDict = {'type': ''}
    if dayData == 1000:
        actionDict['type'] = 'buy'
    if dayData == 2000:
        actionDict['type'] = 'sell'

    return actionDict


if __name__ == '__main__':

    tester = BackTester(initialize=my_init, tradingAlgo=handle_data)

    data = pd.DataFrame(data={'price': [1000, 2000]})
    tester.run(data)
