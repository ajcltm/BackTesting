import pandas as pd
import numpy as np
import datetime
import types
from BackTestAlgo import *
from Order import *
from DataQuery import *
from Record import *
from AlphaBeta import *

def my_init(context):
    context.symbols = ['APPL', 'NVDA']
    # universe를 symbols로 정의(반드시 지정해야함)

    set_benchmark(context, data, type='price')
    # data는 칼럼이 [benchmark, price] 이나 [benchmark, return] 형식으로 넣어줘야함
    # type은 'price' or 'return'으로 지정해줘야함. 지정 안하면 기본값으로 'price'로 진행

    context.benchmark = ['SNP500']
    # 벤치마크 대상을 benchmark로 정의(지정하지 않아도 됨)
    context.price = 'price'
    # price로 사용할 칼럼 인덱스 이름을 알려줘야함(open, high, close 등의 인덱스를 price로 활용 가능함)
    # 여기서 지정한 인덱스는 포트폴리오를 평가할 때 기본적으로 사용하는 지표임
    context.capital_base = 5000
    # 투자원금을 설정함. 지정하지 않으면 기본값을 사용함

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