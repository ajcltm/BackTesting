import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import types
import pandas_datareader as pdr
from BackTestAlgo import *
from Order import *
from DataQuery import *
from Record import *
from AlphaBeta import *
from Preprocessing import *

def my_init(context):
    # context.symbols = ['MRNA', 'NVDA', 'AMZN', 'ARVL']
    context.symbols = ['MRNA']
    # universe를 symbols로 정의(반드시 지정해야함)

    context.price = 'Adj Close'
    # price로 사용할 칼럼 인덱스 이름을 알려줘야함(open, high, close 등의 인덱스를 price로 활용 가능함)
    # 여기서 지정한 인덱스는 포트폴리오를 평가할 때 기본적으로 사용하는 지표임

    context.capital_base = 186
    # 투자원금을 설정함. 지정하지 않으면 기본값을 사용함

    # context.market_benchmark = 'SP500'
    # 지정하면 win_rate 계산 시에 비교, 지정 안하면 절대수익(0%와 비교)으로 계산

    context.i = 0

def handle_data(context, data):
    context.i += 1
    print('\n')
    print(data.current_time)

    # order_schedule = pd.read_csv("C:/Users/ajcltm/Desktop/ordr_schedule.csv")
    # order_schedule['date'] = pd.to_datetime(order_schedule['date'], format='%Y-%m-%d')
    # order_schedule = order_schedule[['date', 'symbol', 'price', 'amounts']]
    #
    # for i in range(0, len(order_schedule)) :
    #     if data.current_time == order_schedule.loc[i, 'date']:
    #         symbol = order_schedule.loc[i, 'symbol']
    #         price = order_schedule.loc[i, 'price']
    #         amounts = order_schedule.loc[i, 'amounts']
    #         # if amounts > 0:
    #         deposit(context, price*amounts)
    #         order(context, [symbol], [price], [amounts])
    if context.i == 1 :
        order(context, ['MRNA'], [18.6], [10])


    balance = context.account['balance']
    mrna_price = data.current_data('MRNA', 'price')
    mrna_amounts = context.portfolio['stock']['MRNA']['amounts']
    # nvda_price = data.current_data('NVDA', 'price')
    # nvda_amounts = context.portfolio['stock']['NVDA']['amounts']
    # amzn_price = data.current_data('AMZN', 'price')
    # amzn_amounts = context.portfolio['stock']['AMZN']['amounts']
    # arvl_price = data.current_data('ARVL', 'price')
    # arvl_amounts = context.portfolio['stock']['ARVL']['amounts']

    # bench1_return = context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'], 'return', 1).values[0]
    # bench2_return = \
    # context.benchmark['benchmark_class'].benchmark_history(context, context.benchmark['benchmark_symbols'][1], 'return',1).values[0]

    # record(context, balance=balance, bench1_return=bench1_return, mrna_price=mrna_price, mrna_amounts=mrna_amounts, nvda_price=nvda_price, nvda_amounts=nvda_amounts, amzn_price=amzn_price, amzn_amounts = amzn_amounts, arvl_price=arvl_price, arvl_amounts = arvl_amounts)
    record(context, mrna_price=mrna_price, mrna_amounts=mrna_amounts)

if __name__ == '__main__':

    s_date = datetime.datetime(2020, 9, 2)
    e_date = datetime.datetime(2021, 6, 28)

    data = pd.read_csv("C:/Users/ajcltm/Desktop/MRNA.csv")
    data['symbol'] = 'MRNA'
    data['date'] = pd.to_datetime(data['Date'])

    # mrna = pdr.DataReader('MRNA', 'yahoo', s_date, e_date)
    # nvda = pdr.DataReader('NVDA', 'yahoo', s_date, e_date)
    # amzn = pdr.DataReader('AMZN', 'yahoo', s_date, e_date)
    # arvl = pdr.DataReader('ARVL', 'yahoo', s_date, e_date)
    #
    # mrna['date'] = mrna.index
    # mrna = mrna.reset_index(drop=True)
    # mrna['symbol'] = 'MRNA'
    # mrna = mrna[['date', 'symbol', 'Adj Close']]
    #
    # nvda['date'] = nvda.index
    # nvda = nvda.reset_index(drop=True)
    # nvda['symbol'] = 'NVDA'
    # nvda = nvda[['date', 'symbol', 'Adj Close']]
    #
    # amzn['date'] = amzn.index
    # amzn = amzn.reset_index(drop=True)
    # amzn['symbol'] = 'AMZN'
    # amzn = amzn[['date', 'symbol', 'Adj Close']]
    #
    # arvl['date'] = arvl.index
    # arvl = arvl.reset_index(drop=True)
    # arvl['symbol'] = 'ARVL'
    # arvl = arvl[['date', 'symbol', 'Adj Close']]
    #
    # data = pd.concat([mrna, nvda, amzn, arvl])


    # start_date = datetime.datetime(2020, 9, 2)
    # end_date = datetime.datetime(2021, 6, 28)
    # benchmark = pdr.DataReader('^GSPC', 'yahoo', start_date, end_date)
    # benchmark['date'] = benchmark.index
    # benchmark = benchmark.reset_index(drop=True)
    # benchmark['price'] = benchmark['Adj Close']
    # benchmark['benchmark'] = 'SP500'
    # benchmark = benchmark[['date', 'benchmark', 'price']]

    # checking_data_contidion(my_init, data, benchmark)


    tester = BackTester(initialize=my_init, tradingAlgo=handle_data)

    result = tester.run(data)

    pd.set_option('display.max.columns', 50)
    pd.set_option('display.max_rows', 1000)
    print(result)

    result.to_csv('C:/Users/ajcltm/Desktop/backtesting/result.csv')