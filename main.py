import pandas as pd
import numpy as np
import datetime
import types
from BackTestAlgo import *
import Order
from DataQuery import *

def my_init(context):
    context.symbols = ['APPL', 'NVDA']
    context.price = 'price'

    context.hold = False
    context.i = 0

def handle_data(context, data):
    context.i += 1
    if data.current_data('NVDA', 'price') > 0 :
    # if context.i < 6 :
        context.hold = True
        #context.portfolio.positions[context.security].amounts = 1
        Order.deposit(context, 500)
        Order.order(context, ['APPL', 'NVDA'], [20, 10], [20, 10])
        print('account: {0}'.format(context.account))
        print('portfolio: {0}'.format(context.portfolio))

    # if dayData[dayData['symbol'] == 'NVDA'].price.values[0] == 2000:
    if data.current_data('NVDA', 'price') == 0 :
        Order.order(context, ['APPL', 'NVDA'], [5, 10], [-5, -10])
        print('account: {0}'.format(context.account))
        print('portfolio: {0}'.format(context.portfolio))
        context.hold = False
        print("short")

if __name__ == '__main__':

    # price_list = np.random.randint(650, 720, 10)
    price_list = [10 for i in range(0, 10)]
    date_list = [datetime.datetime(2021, 1, i + 1) for i in range(0, 10)]
    data = pd.DataFrame(data={'NVDA': price_list, 'APPL': price_list}, index=date_list)
    data = data.unstack()
    data = data.reset_index()
    data.columns = ['symbol', 'date', 'price']
    data = data[['date', 'symbol', 'price']]

    tester = BackTester(initialize=my_init, tradingAlgo=handle_data)

    result = tester.run(data)

    print(result)