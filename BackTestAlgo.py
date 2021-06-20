import pandas as pd
import types
from DataQuery import *
from Calculator import *

class BackTester:
    def __init__(self, initialize, tradingAlgo):
        print('Hello backtesting')

        self.context = types.SimpleNamespace()
        # context 네임스페이스 객체 생성

        self.context.capital_base = 0

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

        self.context.record = {}
        self.context.record_on = False
        # context에 record 상태 공간 만들기, 녹화 스위치(record_on)는 껴놓은 상태로 저장

        self.tradingAlgo = tradingAlgo

    def run(self, data):
        # data는 'data', 'symbol', 'price_factor' 형태로 줘야함

        data['price'] = data[self.context.price]
        # data에 price 정보에 해당하는 열을 지정해줌

        resultColumns = ['date', 'return_value' , 'return_rate', 'starting_cash', 'ending_cash', 'ending_stock_value',
                         'portfolio_value', 'capital_base']
        self.result = pd.DataFrame(columns=resultColumns)
        # result 공간 dataframe 만들기 (열만 정의된 빈 dataframe)

        date_univers = data.drop_duplicates(['date'])['date']
        # date_univers 정의 (데이터에 있는 일자를 중복제거 해서 event를 일으킬 일자 정의)
        for i in range(0, len(date_univers)):
            current_time = date_univers.iloc[i]
            # 현재 일자 정의

            self.context.current_time = current_time
            # context에 현재시간 저장

            dataquery = DataQuery(data, self.context)
            # DataQuery의 class 객체 생성(run 함수에 넣은 data 인자와 현재 시간을 인수로 넣어줌)

            starting_cash=self.context.portfolio['cash']

            update_portfolio_current_price(self.context, dataquery)
            # portfolio의 가격 정보를 업데이트 함

            self.tradingAlgo(self.context, dataquery)
            # tradingAlgo 실행 (tradingAlgo에 context 정보와 데이터를 조회할 수 있는 dataquery 객체를 인자로 넣어줌)

            ending_cash=self.context.portfolio['cash']

            portfolio_value = calculate_portfolio_value(self.context)

            ending_stock_value = portfolio_value - ending_cash

            capital_base = self.context.capital_base

            return_value = portfolio_value - capital_base

            return_rate = (portfolio_value - capital_base) / capital_base

            s = pd.Series([current_time, return_value, return_rate, starting_cash, ending_cash, ending_stock_value,
                           portfolio_value, capital_base], index=resultColumns)
            self.result = self.result.append(s, ignore_index=True)
            # result 데이터프레임 공간에 결과값 저장


        if bool(self.context.record):
        # record된 것이 있다면
            self.result = pd.merge(self.result, self.context.record_df, how='outer', left_on='date', right_on='date')
            # date 칼럼을 기준으로 result 데이터프레임과 record 데이터프레임 병합(없는 값은 nan 처리)

        return self.result


