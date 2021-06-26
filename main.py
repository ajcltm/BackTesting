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
from setting import *

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

    start_date_n = datetime.datetime(2021, 1, 1)
    start_date_a = datetime.datetime(2021, 4, 9)
    end_date = datetime.datetime(2021, 6, 25)

    NVDA = web.DataReader('NVDA', 'yahoo', start_date_n, end_date)
    ARVL = web.DataReader('ARVL', 'yahoo', start_date_a, end_date)

    NVDA['date'] = NVDA.index
    NVDA = NVDA.reset_index(drop=True)
    NVDA['symbol'] = 'NVDA'
    NVDA['price'] = NVDA['Adj Close']
    NVDA = NVDA[['date', 'symbol', 'price']]
    ARVL['date'] = ARVL.index
    ARVL = ARVL.reset_index(drop=True)
    ARVL['symbol'] = 'ARVL'
    ARVL['price'] = ARVL['Adj Close']
    ARVL = ARVL[['date', 'symbol', 'price']]
    data = pd.concat([NVDA, ARVL])

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

    result = tester.run(data)

    # print('\nresult :\n{0} '.format(result['beta_SP500']))

    result.to_csv('C:/Users/ajcltm/Desktop/backtesting/result.csv')
