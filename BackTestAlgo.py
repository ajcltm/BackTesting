import pandas as pd
import numpy as np
import types
from DataQuery import *
from Calculator import *
from AlphaBeta import *

class BackTester:
    def __init__(self, initialize, tradingAlgo):
        print('\nHello backtesting')

        self.context = types.SimpleNamespace()
        # context 네임스페이스 객체 생성

        self.context.capital_base = 0
        # 투자원금의 기본값을 설정함 (initialize 밑에서 설정하면, initialize에서 투자원금에 특정값을 부여해도 기본값을 다시 부여해버림)

        initialize(self.context)
        # initialize 함수로 context에 symbols와 price 상태 저장(symbols와 price에 해당하는 이름을 반드시 정의해줘야 함)
        # 그 밖에 사용하고자 하는 사용자 정의 key : value 지정할 수 있음 ( ex : context.hold = True )

        self.context.current_time = 0
        # context에 current_time 정보 저장하기

        withdrawal = {}
        for symbol in self.context.symbols:
            withdrawal[symbol] = {'unitPrice': 0, 'amounts': 0}
        account = {'deposit': 0, 'withdrawal': withdrawal, 'balance': self.context.capital_base}
        self.context.account = account
        # context에 account 상태 공간 만들기( {'deposit': %%, 'withdrawal' : {'symbol':{'unitPrice':%%, 'amounts':%%}}} 형태)

        stock = {}
        for symbol in self.context.symbols:
            stock[symbol] = {'price': 0, 'amounts': 0}
        portfolio = {'cash': self.context.capital_base, 'stock': stock}
        portfolio = portfolio
        self.context.portfolio = portfolio
        # context에 portfolio 상태 공간 만들기( {'cash': %%, 'stock' : {'symbol':{'price':%%, 'amounts':%%}}} 형태)

        benchmark = {'benchmark_symbols' : 0, 'benchmark_df' : 0, 'benchmark_class' : 0}
        self.context.benchmark = benchmark

        self.context.record = {}
        self.context.record_on = False
        # context에 record 상태 공간 만들기, 녹화 스위치(record_on)는 껴놓은 상태로 저장

        self.tradingAlgo = tradingAlgo

    def run(self, data, benchmark_data):
        # data는 'data', 'symbol', 'price_factor' 형태로 줘야함

        data['price'] = data[self.context.price]
        # data에 price 정보에 해당하는 열을 지정해줌

        benchmark = AlphaBeta(self.context, benchmark_data, type='price')

        self.context.benchmark['benchmark_class'] = benchmark

        benchmark_symbols = self.context.benchmark['benchmark_symbols']

        resultColumns = ['date', 'total_profit', 'rate_of_return', 'starting_cash', 'ending_cash',
                         'starting_stock_value', 'ending_stock_value',
                         'starting_portfolio_value', 'ending_portfolio_value', 'portfolio_return', 'capital_base',
                         'alpha', 'beta']

        self.result = pd.DataFrame(columns=resultColumns)
        # result 공간 dataframe 만들기 (열만 정의된 빈 dataframe)

        date_univers = data.drop_duplicates(['date'])['date']
        # date_univers 정의 (데이터에 있는 일자를 중복제거 해서 event를 일으킬 일자 정의)

        ending_portfolio_value = self.context.portfolio['cash']
        # 기초평가액은 전날의 기말평가액임(첫날 이전의 기말평가액은 존재 하지 않으므로 초기 셋팅을 첫날 기초현금가로 셋팅해야함)

        for i in range(0, len(date_univers)):
            current_time = date_univers.iloc[i]
            # 현재 일자 정의

            self.context.current_time = current_time
            # context에 현재시간 저장

            dataquery = DataQuery(data, self.context)
            # DataQuery의 class 객체 생성(run 함수에 넣은 data 인자와 현재 시간을 인수로 넣어줌)

            starting_cash=self.context.portfolio['cash']
            starting_portfolio_value = ending_portfolio_value
            starting_stock_value = starting_portfolio_value - starting_cash
            # tradingAlgo를 실행 하기 전에 '기초 현금, 기초 평가액, 기초 주식 가치'를 기록해놓음
            starting_capital_base = self.context.capital_base
            # tradingAlgo 전후의 deposit을 비교하기 위해 기록해둠

            self.tradingAlgo(self.context, dataquery)
            # tradingAlgo 실행 (tradingAlgo에 context 정보와 데이터를 조회할 수 있는 dataquery 객체를 인자로 넣어줌)
            ending_capital_base = self.context.capital_base
            if starting_capital_base < ending_capital_base :
                starting_cash += self.context.account['deposit']
                starting_portfolio_value += self.context.account['deposit']
            # tradingAlgo 안에서 deposit()이 호출될 경우, starting_cash가 늘어나야하고, 그로인해 starting 평가액도 늘어야함
            # deposit이 증가하면 투자원금이 증가하는데, starting 금액에 편입안되면 그 금액만큼 수익으로 인식되어 수익률이 과대평가됨
            # tradingAlgo 안에서 deposit()이 호출된 사실을 인식하려면, starting_capital_base과 ending_capital_base를 비교해야함
            # (self.context.portfolio['cash']는 tradingAlgo에 order()가 호출될경우 인출이 발생하기 때문에 이미 왜곡되어 활용할수 없음)

            ending_cash=self.context.portfolio['cash']
            ending_portfolio_value = calculate_portfolio_value(self.context, dataquery)
            ending_stock_value = ending_portfolio_value - ending_cash
            # tradingAlgo를 실행 하기 후에 '기초 현금, 기초 평가액, 기초 주식 가치'를 기록함

            capital_base = self.context.capital_base
            # 투자원금은 deposit()이 생길때마다 누적하여 계산되어 있음

            total_profit = ending_portfolio_value - capital_base
            rate_of_return = (ending_portfolio_value - capital_base) / capital_base

            portfolio_return = (ending_portfolio_value - starting_portfolio_value) / starting_portfolio_value


            y = np.append(self.result['portfolio_return'].values, [portfolio_return]).reshape(-1, 1)
            print('y : \n{0}'.format(y))
            y = np.delete(y, 0, 0)
            print('x drop : \n{0}'.format(y))
            benchmark_history = benchmark.benchmark_history(self.context, benchmark_symbols, 'return', i+1)
            print('benchmark_history : \n{0}'.format(benchmark_history))
            if i == 0:
                alpha, beta = 0, 0
            else :
                alpha, beta = benchmark.get_alpha_beta(y)


            s = pd.Series([current_time, total_profit, rate_of_return, starting_cash, ending_cash,
                           starting_stock_value, ending_stock_value, starting_portfolio_value, ending_portfolio_value,
                           portfolio_return, capital_base, alpha, beta], index=resultColumns)
            self.result = self.result.append(s, ignore_index=True)
            # result 데이터프레임 공간에 결과값 저장


        if bool(self.context.record):
        # record된 것이 있다면
            self.result = pd.merge(self.result, self.context.record_df, how='outer', left_on='date', right_on='date')
            # date 칼럼을 기준으로 result 데이터프레임과 record 데이터프레임 병합(없는 값은 nan 처리)

        return self.result


