import pandas as pd
import types

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
            current_day = date_univers.iloc[i]
            # 현재 일자 정의
            current_data = data[data['date'] == current_day]
            # 현재 일자에 해당하는 dataframe 필터
            print('\ncurrent_data : {0}'.format(current_data))

            self.tradingAlgo(self.context, current_data)
            # tradingAlgo 실행 (tradingAlgo에 현재 일자로 필터된 dataframe을 인자로 넣어줌)

            cash_value = self.context.portfolio['cash']
            print('cash_value : {0}'.format(cash_value))
            stock_value = 0
            for symbol in self.context.symbols :
                stock_price = current_data[current_data['symbol'] == symbol].price.values[0]
                stock_amounts = self.context.portfolio['stock'][symbol]['amounts']
                stock_value += stock_price*stock_amounts
                print('{0} : price   = {1}'.format(symbol, stock_price))
                print('{0} : amounts = {1}'.format(symbol, stock_amounts))
                print('{0} : sum     = {1}'.format(symbol, stock_value))
            portfolio_value = cash_value + stock_value
            print('portfolio_value : {0}'.format(portfolio_value))
            # portfolio_value 계산

            s = pd.Series([current_day, portfolio_value], index=resultColumns)
            self.result = self.result.append(s, ignore_index=True)

        return self.result


