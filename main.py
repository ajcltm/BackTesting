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
    context.symbols = ['NVDA']
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

    nvda_amounts = context.account['withdrawal']['NVDA']['amounts']

    bench1_return = context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][0], 'return', 1).values[0]
    bench2_return = \
    context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][1], 'return',
                                                           1).values[0]

    mena_price = data.history(context, 'NVDA', 'price', 5).mean()

    print('bench_price :{0} '.format(bench1_return))
    record(context, bench1_return=bench1_return,bench2_return=bench2_return, nvda_price=nvda_price, nvda_amounts=nvda_amounts, mena_price=mena_price)


if __name__ == '__main__':

    # price_list = [i for i in range(20, 30)]
    # date_list = [datetime.datetime(2021, 1, i + 1) for i in range(0, 10)]
    # data = pd.DataFrame(data={'NVDA': price_list, 'APPL': price_list}, index=date_list)
    # data = data.unstack()
    # data = data.reset_index()
    # data.columns = ['symbol', 'date', 'price']
    # data = data[['date', 'symbol', 'price']]
    #
    # bench_price_list = [i for i in range(20, 30)]
    # benchmark = pd.DataFrame(data={'SNP500': bench_price_list, 'kospi': bench_price_list}, index=date_list)
    # # benchmark = pd.DataFrame(data={'SNP500': bench_price_list}, index=date_list)
    # benchmark = benchmark.unstack()
    # benchmark = benchmark.reset_index()
    # benchmark.columns = ['benchmark', 'date', 'price']
    # benchmark = benchmark[['date', 'benchmark', 'price']]
    # print('benchmark :\n{0} '.format(benchmark))



    start_date = datetime.datetime(2021, 1, 5)
    end_date = datetime.datetime(2021, 6, 25)

    data = web.DataReader('NVDA', 'yahoo', start_date, end_date)
    data['date'] = data.index
    data = data.reset_index(drop=True)
    data['price'] = data['Adj Close']
    data['symbol'] = 'NVDA'
    data = data[['date', 'symbol', 'price']]

    benchmark_1 = web.DataReader('^GSPC', 'yahoo', start_date, end_date)
    benchmark_1['date'] = benchmark_1.index
    benchmark_1 = benchmark_1.reset_index(drop=True)
    benchmark_1['price'] = benchmark_1['Adj Close']
    benchmark_1['benchmark'] = 'SP500'
    benchmark_1 = benchmark_1[['date', 'benchmark', 'price']]

    benchmark_2 = web.DataReader('^DJI', 'yahoo', start_date, end_date)
    benchmark_2['date'] = benchmark_2.index
    benchmark_2 = benchmark_2.reset_index(drop=True)
    benchmark_2['price'] = benchmark_2['Adj Close']
    benchmark_2['benchmark'] = 'KOSPI'
    benchmark_2 = benchmark_2[['date', 'benchmark', 'price']]

    benchmark = pd.concat([benchmark_1, benchmark_2])

    tester = BackTester(initialize=my_init, tradingAlgo=handle_data)

    result = tester.run(data, benchmark)

    print('\nresult :\n{0} '.format(result['beta_SP500']))

    result.to_csv('C:/Users/ajcltm/Desktop/backtesting/result.csv')
