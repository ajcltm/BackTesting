import pandas as pd
import numpy as np
import datetime
import types
import pandas_datareader as web
from BackTestAlgo import *
from Order import *
from DataQuery import *
from Record import *
from AlphaBeta import *

def my_init(context):
    context.symbols = ['NVDA', 'ARVL']
    # universe를 symbols로 정의(반드시 지정해야함)

    context.price = 'price'
    # price로 사용할 칼럼 인덱스 이름을 알려줘야함(open, high, close 등의 인덱스를 price로 활용 가능함)
    # 여기서 지정한 인덱스는 포트폴리오를 평가할 때 기본적으로 사용하는 지표임

    context.capital_base = 5000
    # 투자원금을 설정함. 지정하지 않으면 기본값을 사용함

    context.i = 0

def handle_data(context, data):
    context.i += 1
    print('\n')
    print(data.current_time)

    nvda_price = data.current_data('NVDA', 'price')

    if context.i ==1 :
        order(context, ['NVDA'], [nvda_price], [int(context.capital_base/nvda_price)])

    if data.current_time > datetime.datetime(2021, 4, 9) :
        arvl_price = data.current_data('ARVL', 'price')
        if data.current_time == datetime.datetime(2021, 6, 21) :
            order(context, ['ARVL'], [arvl_price], [int(context.portfolio['cash']/arvl_price)])
        arvl_amounts = context.account['withdrawal']['ARVL']['amounts']
    else :
        arvl_price = NA
        arvl_amounts = context.account['withdrawal']['ARVL']['amounts']
    nvda_amounts = context.account['withdrawal']['NVDA']['amounts']

    # bench1_return = context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][0], 'return', 1).values[0]
    # bench2_return = \
    # context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][1], 'return',
    #                                                        1).values[0]

    mean_price = data.history(context, 'NVDA', 'price', 5).mean()

    # print('bench_price :{0} '.format(bench1_return))
    # record(context, bench1_return=bench1_return,bench2_return=bench2_return, nvda_price=nvda_price, nvda_amounts=nvda_amounts, mena_price=mena_price)
    record(context, nvda_price=nvda_price, nvda_amounts=nvda_amounts, arvl_price=arvl_price, arvl_amounts = arvl_amounts, mean_price=mean_price)