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

        # bench1_return = context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][0], 'return', 1).values[0]
        # bench2_return = context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][0], 'return', 1).values[0]
        # print('bench_price :{0} '.format(bench_return))
        # record(context, bench1_return=bench1_return,bench2_return=bench2_return, appl_price=appl_price, appl_amounts=appl_amounts,
        #        nvda_price=nvda_price, nvda_amounts=nvda_amounts, action=context.action)

    else :
        order(context, ['APPL', 'NVDA'], [10, 10], [-20, -10])
        context.action = 'short'
        context.hold = False
        sum = data.history('NVDA', 'price', 3).sum()
        sum_alpha = data.history('NVDA', 'price', 3).sum()+5
        appl_price = data.current_data('APPL', 'price')
        appl_amounts = context.account['withdrawal']['APPL']['amounts']
        nvda_price = data.current_data('NVDA', 'price')
        nvda_amounts = context.account['withdrawal']['NVDA']['amounts']
        # bench1_return = context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][0], 'return', 1).values[0]
        # bench2_return = context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][0], 'return', 1).values[0]
        # print('bench_price :{0} '.format(bench_return))
        # record(context, bench1_return=bench1_return,bench2_return=bench2_return, appl_price=appl_price, appl_amounts=appl_amounts,
        #        nvda_price=nvda_price, nvda_amounts=nvda_amounts, action=context.action)
if __name__ == '__main__':

    price_list = [i for i in range(20, 30)]
    date_list = [datetime.datetime(2021, 1, i + 1) for i in range(0, 10)]
    data = pd.DataFrame(data={'NVDA': price_list, 'APPL': price_list}, index=date_list)
    data = data.unstack()
    data = data.reset_index()
    data.columns = ['symbol', 'date', 'price']
    data = data[['date', 'symbol', 'price']]

    bench_price_list = [i for i in range(20, 30)]
    benchmark = pd.DataFrame(data={'SNP500': bench_price_list, 'kospi': bench_price_list}, index=date_list)
    # benchmark = pd.DataFrame(data={'SNP500': bench_price_list}, index=date_list)
    benchmark = benchmark.unstack()
    benchmark = benchmark.reset_index()
    benchmark.columns = ['benchmark', 'date', 'price']
    benchmark = benchmark[['date', 'benchmark', 'price']]
    print('benchmark :\n{0} '.format(benchmark))


    tester = BackTester(initialize=my_init, tradingAlgo=handle_data)

    result = tester.run(data, benchmark)

    print('\nresult :\n{0} '.format(result['portfolio_return']))

    result.to_csv('C:/Users/ajcltm/Desktop/backtesting/result.csv')