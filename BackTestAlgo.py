import pandas as pd
import types
from DataQuery import *

class BackTester:
    def __init__(self, initialize, tradingAlgo):
        print('Hello backtesting')

        self.context = types.SimpleNamespace()
        # context 네임스페이스 객체 생성

        initialize(self.context)
        # initialize 함수로 context에 symbols와 price 상태 저장(symbols와 price에 해당하는 이름을 반드시 정의해줘야 함)
        # 그 밖에 사용하고자 하는 사용자 정의 key : value 지정할 수 있음 ( ex : context.hold = True )

        withdrawal = {}
        for symbol in self.context.symbols:
            withdrawal[symbol] = {'unitPrice': 0, 'amounts': 0}
        account = {'deposit': 0, 'withdrawal': withdrawal}
        self.context.account = account
        # context에 account 상태 공간 만들기( {'deposit': %%, 'withdrawal' : {'symbol':{'unitPrice':%%, 'amounts':%%}}} 형태)

        stock = {}
        for symbol in self.context.symbols:
            stock[symbol] = {'price': 0, 'amounts': 0}
        portfolio = {'cash': 0, 'stock': stock}
        portfolio = portfolio
        self.context.portfolio = portfolio
        # context에 portfolio 상태 공간 만들기( {'cash': %%, 'stock' : {'symbol':{'price':%%, 'amounts':%%}}} 형태)

        self.tradingAlgo = tradingAlgo

    def run(self, data):
        # data는 'data', 'symbol', 'price_factor' 형태로 줘야함

        data['price'] = data[self.context.price]
        # data에 price 정보에 해당하는 열을 지정해줌

        resultColumns = ['date', 'portfolio_value']
        self.result = pd.DataFrame(columns=resultColumns)
        # result 공간 dataframe 만들기 (열만 정의된 빈 dataframe)

        date_univers = data.drop_duplicates(['date'])['date']
        # date_univers 정의 (데이터에 있는 일자를 중복제거 해서 event를 일으킬 일자 정의)
        for i in range(0, len(date_univers)):
            current_time = date_univers.iloc[i]
            # 현재 일자 정의

            dataquery = DataQuery(data, current_time)
            # DataQuery의 class 객체 생성(run 함수에 넣은 data 인자와 현재 시간을 인수로 넣어줌)

            self.tradingAlgo(self.context, dataquery)
            # tradingAlgo 실행 (tradingAlgo에 context 정보와 데이터를 조회할 수 있는 dataquery 객체를 인자로 넣어줌)

            cash_value = self.context.portfolio['cash']
            print('cash_value : {0}'.format(cash_value))
            stock_value = 0
            for symbol in self.context.symbols :
                stock_price = dataquery.current_data(symbol, 'price')
                # dataquery에서 현재 가격을 조회함
                stock_amounts = self.context.portfolio['stock'][symbol]['amounts']
                # context의 portfolio에서 해당 심볼에 해당하는 주식의 보유 주식 수를 가지고옴
                stock_value += stock_price*stock_amounts
                print('{0} : price   = {1}'.format(symbol, stock_price))
                print('{0} : amounts = {1}'.format(symbol, stock_amounts))
                print('{0} : sum     = {1}'.format(symbol, stock_value))
            portfolio_value = cash_value + stock_value
            # portfolio_value는 현금 가치와 주식 가치를 합한 값
            print('portfolio_value : {0}'.format(portfolio_value))
            # portfolio_value 계산

            s = pd.Series([current_time, portfolio_value], index=resultColumns)
            self.result = self.result.append(s, ignore_index=True)
            # result 공간에 결과값 저장

        return self.result


