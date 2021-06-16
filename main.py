import pandas as pd
import numpy as np
import datetime
import types
from BackTestAlgo import *


def my_init(context):
    context.security = 'NVDA'
    context.hold = False

def handle_data(context, dayData):
    if dayData[context.security] > 0 :
        context.hold = True
        context.portfolio.positions[context.security].amounts = 1
        print("long")
    if dayData[context.security] == 2000:
        context.hold = False
        print("short")

# def symbol(code):
#     if code == 'AAPL':
#         return 1000
#     elif code == 'NVDA':
#         return 1001
#     elif code == 'SPY':
#         return 1002

if __name__ == '__main__':

    tester = BackTester(initialize=my_init, tradingAlgo=handle_data)
    print(tester.context)
    price_list = np.random.randint(650, 720, 10)
    date_list = [datetime.datetime(2021, 1, i+1) for i in range(0, 10)]
    data = pd.DataFrame(data={'NVDA': price_list}, index=date_list)
    result = tester.run(data)
    print(result)