import pandas as pd
import numpy as np
import datetime
import types
from BackTestAlgo import *
from Order import *
from DataQuery import *
from Record import *

def my_init(context):
    context.symbols = ['APPL', 'NVDA']
    context.price = 'price'
    context.capital_base = 5000

    context.hold = False
    context.i = 0
    context.action = 0

def handle_data(context, data):
    context.i += 1
    print('\n')
    print(data.current_time)

    if context.i < 6 :
        context.hold = True
        deposit(context,100)
        order(context, ['APPL', 'NVDA'], [10, 10], [20, 10])
        # deposit(context, 10)
        context.action = 'long'
        sum = data.history('NVDA', 'price', 3).sum()
        sum_alpha = data.history('NVDA', 'price', 3).sum()+5
        appl_price = data.current_data('APPL', 'price')
        appl_amounts = context.account['withdrawal']['APPL']['amounts']
        nvda_price = data.current_data('NVDA', 'price')
        nvda_amounts = context.account['withdrawal']['NVDA']['amounts']

        record(context, appl_price=appl_price, appl_amounts=appl_amounts,
               nvda_price=nvda_price, nvda_amounts=nvda_amounts, action=context.action)
        print('account: {0}'.format(context.account))
        print('portfolio: {0}'.format(context.portfolio))
        print('record: {0}'.format(context.record))

    else :
        order(context, ['APPL', 'NVDA'], [10, 10], [-20, -10])
        context.action = 'short'
        print('account: {0}'.format(context.account))
        print('portfolio: {0}'.format(context.portfolio))
        context.hold = False
        sum = data.history('NVDA', 'price', 3).sum()
        sum_alpha = data.history('NVDA', 'price', 3).sum()+5
        appl_price = data.current_data('APPL', 'price')
        appl_amounts = context.account['withdrawal']['APPL']['amounts']
        nvda_price = data.current_data('NVDA', 'price')
        nvda_amounts = context.account['withdrawal']['NVDA']['amounts']
        record(context, appl_price=appl_price, appl_amounts=appl_amounts,
               nvda_price=nvda_price, nvda_amounts=nvda_amounts, action=context.action)

if __name__ == '__main__':

    # price_list = np.random.randint(650, 720, 10)
    price_list = [i for i in range(20, 30)]
    date_list = [datetime.datetime(2021, 1, i + 1) for i in range(0, 10)]
    data = pd.DataFrame(data={'NVDA': price_list, 'APPL': price_list}, index=date_list)
    data = data.unstack()
    data = data.reset_index()
    data.columns = ['symbol', 'date', 'price']
    data = data[['date', 'symbol', 'price']]

    tester = BackTester(initialize=my_init, tradingAlgo=handle_data)

    result = tester.run(data)

    print(result)

    result.to_csv('C:/Users/ajcltm/Desktop/backtesting/result.csv')