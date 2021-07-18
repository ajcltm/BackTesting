import types

from numpy import nan as NA

from AlphaBeta import *
from Calculator import *
from DataQuery import *


class BackTester:
    def __init__(self, initialize, tradingAlgo):
        print('\nHello backtesting')

        self.context = types.SimpleNamespace()
        # context 네임스페이스 객체 생성

        self.context.capital_base = 0
        # 투자원금의 기본값을 설정함 (initialize 밑에서 설정하면, initialize에서 투자원금에 특정값을 부여해도 기본값을 다시 부여해버림)

        self.context.market_benchmark = {}
        # initialize()에서 지정하면 win_rate 계산 시에 비교, 지정 안하면 절대수익(0%와 비교)으로 계산

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

    def run(self, data, benchmark_data=None, free_risk_data=None):
        # data는 'data', 'symbol', 'price_factor' 형태로 줘야함
        # benchmark_data 디폴트값은 none이며, data를 넣어줄때는 columns = [date, benchmark, price] 또는 [date, benchmark, return] 형식으로 줘야함
        # free_risk_data는 데이터프레임 형태로 넣어줄수 있음 (return 값으로 넣어야함, price아님)

        data['price'] = data[self.context.price]
        # data에 price 정보에 해당하는 열을 지정해줌

        if isinstance(benchmark_data, pd.DataFrame):
        # benchmark_data가 입력되었는지 확인함
            benchmark = AlphaBeta(self.context, benchmark_data)
            # benchmark_data가 있으면 AlphaBeta 클래스 생성
            self.context.benchmark['benchmark_class'] = benchmark
            # 클래스 객체를 context에 저장(main 등에서 클래스 객처를 별도로 만들지 않고 데이터 조회등에 활용할 수 있음)
            benchmark_symbols = self.context.benchmark['benchmark_symbols']
            # AlphaBeta 클래스 생성 시 init에서 benchmark_data에 있는 benchmakrk symbol를 정리하여 context에 저장해 놓은 것을 꺼내어 씀
            beta_list = ['beta_{0}'.format(i) for i in benchmark_data['benchmark'].unique().tolist()]
            # benchmark 데이터의 symbol 개수 만큼 beta 변수를 만들고 list 형태로 지정함
        else :
            beta_list = ['beta']
            # benchmakrk data가 없으면 beta 변수를 하나만 만듬

        resultColumns = ['date', 'capital_base', 'starting_cash', 'ending_cash',
                         'starting_stock_value', 'ending_stock_value', 'starting_portfolio_value', 'ending_portfolio_value',
                         'portfolio_return','annualized_return', 'roll_annualized_return', 'volatility', 'roll_volatility',
                         'sharp_ratio', 'roll_sharp_ratio',
                         'cumulative_return', 'drawdown_ratio', 'MDD', 'underwater_period',
                         'win_rate', 'roll_win_rate', 'total_profit', 'alpha'] + beta_list
        # result의 컬럼을 미리 만듬(beta_list안에 개수는 가변적임)
        self.result = pd.DataFrame(columns=resultColumns)
        # result 공간 dataframe 만들기 (열만 정의된 빈 dataframe)

        date_univers = data.drop_duplicates(['date'])['date']
        # date_univers 정의 (데이터에 있는 일자를 중복제거 해서 event를 일으킬 일자 정의)

        self.context.date_univers = date_univers
        # date_univers를 context에 저장함(DataQuery와 AlphaBeta에서 history 함수 호출할때 사용)

        ending_portfolio_value = self.context.portfolio['cash']
        # 기초평가액은 전날의 기말평가액임(첫날 이전의 기말평가액은 존재 하지 않으므로 초기 셋팅을 첫날 기초현금가로 셋팅해야함)

        drawdown = {'current_value':1, 'current_date':0 ,'max_value' : 0, 'max_value_date': 0, 'MDD':0, 'underwater_period':datetime.timedelta(days=0)}

        winrate = {'win' : 0, 'not_win' : 0}
        roll_winrate = {'win': 0, 'not_win': 0}

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
            if starting_capital_base != ending_capital_base :
                starting_cash += ending_capital_base - starting_capital_base
                starting_portfolio_value += ending_capital_base - starting_capital_base
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
            cumulative_return = (ending_portfolio_value - capital_base) / capital_base

            portfolio_return = (ending_portfolio_value - starting_portfolio_value) / starting_portfolio_value
            if np.isnan(portfolio_return) :
                portfolio_return=0
            y = np.append(self.result['portfolio_return'].values, [portfolio_return]).reshape(-1, 1)

            if  i > 250 :
            # 252개가 채워지면 rolling 시작 ( 0~251 이 252개가 되는 시점이고, 그때 i는 251임)
                roll_y = np.append(self.result['portfolio_return'].iloc[i-251:i].values, [portfolio_return]).reshape(-1,1)
                print(i-251, i)
                print(roll_y)
                # i가 251일때, result에는 0~250까지만 있을 것이므로 iloc[i-251:i] 로 조회하면 0:251 이므로 0~250까지 조회됨(251개). 이후 하나더 추가하여 252개를 만듬
            else :
                roll_y = y
                print(0, i)

            # 전날 result의 portfolio_return에 오늘 portfolio_return 값을 추가하고, 시리즈를 2차원 배열로 변환함
            annualized_return = np.prod(y+1)**(252/(i+1))-1
            print(np.prod(y+1)**((i+1))-1)
            if  i > 250 :
                roll_annualized_return = np.prod(roll_y + 1) ** (252 / 252) - 1
                print(np.prod(y + 1) ** ((i + 1)) - 1)
            else :
                roll_annualized_return = annualized_return
                print(np.prod(y + 1) ** ((i + 1)) - 1)

            annualized_return_y = np.append(self.result['annualized_return'].values, [annualized_return]).reshape(-1, 1)

            if i > 250:
                # 252개가 채워지면 rolling 시작 ( 0~251 이 252개가 되는 시점이고, 그때 i는 251임)
                roll_annualized_return_y = np.append(self.result['annualized_return'].iloc[i - 251:i].values, [annualized_return]).reshape(-1, 1)
                print(i - 251, i)
                print(roll_annualized_return_y)
                # i가 251일때, result에는 0~250까지만 있을 것이므로 iloc[i-251:i] 로 조회하면 0:251 이므로 0~250까지 조회됨(251개). 이후 하나더 추가하여 252개를 만듬
            else:
                roll_annualized_return_y = annualized_return_y
                print(0, i)

            std_y = np.std(annualized_return_y)
            roll_std_y = np.std(roll_annualized_return_y)

            sharp_ratio = annualized_return / std_y
            roll_sharp_ratio = roll_annualized_return / roll_std_y

            drawdown['current_value'] *= (1+portfolio_return)
            drawdown['current_date'] = current_time
            if drawdown['current_value'] > drawdown['max_value'] :
                drawdown['max_value'] = drawdown['current_value']
                drawdown['max_value_date'] = drawdown['current_date']
            drawdown_ratio = (drawdown['current_value'] - drawdown['max_value']) / drawdown['max_value']
            drawdown_period = drawdown['current_date'] - drawdown['max_value_date']
            if drawdown_ratio < drawdown['MDD'] :
                drawdown['MDD'] = drawdown_ratio
            if drawdown_period > drawdown['underwater_period'] :
                drawdown['underwater_period'] = drawdown_period
            MDD = drawdown['MDD']
            underwater_period = drawdown['underwater_period']

            if bool(self.context.market_benchmark):
                if i == 0 :
                    benchmark_return = 0
                else :
                    benchmark_return = benchmark.benchmark_history(self.context, self.context.market_benchmark, 'return', 1).values[-1]

                if portfolio_return > benchmark_return :
                    # 벤치마크 수익과 비교
                    winrate['win'] += 1
                else :
                    winrate['not_win'] += 1
                win_rate = winrate['win'] / (winrate['win'] + winrate['not_win'])
                if i > 251:
                    # 처음것을 빼고 다시 정리하는 개념이라서 i=252부터 시작함 -> 253개에서 1개 빼고 252개의 승률을 계산함
                    if self.result['portfolio_return'].iloc[i - 252] > benchmark_return:
                        # 1년전 그날 승리 여부 확인
                        roll_winrate['win'] -= 1
                        # 1년전 그날 승리했으면 승리한 기록 하나 삭제
                        if portfolio_return > 0:
                            # 오늘 결과 확인하고 반영(1년전 기록 하나는 삭제하고 오늘 기록 하나는 넣는 방식) -> 252개가 유지됨(이하내용 동일)
                            roll_winrate['win'] += 1
                        else:
                            roll_winrate['not_win'] += 1
                    else:
                        roll_winrate['not_win'] -= 1
                        if portfolio_return > 0:
                            roll_winrate['win'] += 1
                        else:
                            roll_winrate['not_win'] += 1
                else:
                    # 252개가 안되면 rolling 방식으로 계산 하지 않음
                    roll_winrate['win'] = winrate['win']
                    roll_winrate['not_win'] = winrate['not_win']
                roll_win_rate = roll_winrate['win'] / (roll_winrate['win'] + roll_winrate['not_win'])
            else :
                if portfolio_return > 0 :
                    # 절대수익 비교
                    winrate['win'] += 1
                else :
                    winrate['not_win'] += 1
                win_rate = winrate['win'] / (winrate['win'] + winrate['not_win'])
                if i > 251 :
                # 처음것을 빼고 다시 정리하는 개념이라서 i=252부터 시작함 -> 253개에서 1개 빼고 252개의 승률을 계산함
                    if self.result['portfolio_return'].iloc[i-252] > 0 :
                       # 1년전 그날 승리 여부 확인
                        roll_winrate['win'] -= 1
                       # 1년전 그날 승리했으면 승리한 기록 하나 삭제
                        if portfolio_return > 0:
                            # 오늘 결과 확인하고 반영(1년전 기록 하나는 삭제하고 오늘 기록 하나는 넣는 방식) -> 252개가 유지됨(이하내용 동일)
                            roll_winrate['win'] +=1
                        else:
                            roll_winrate['not_win'] += 1
                    else :
                        roll_winrate['not_win'] -= 1
                        if portfolio_return > 0:
                            roll_winrate['win'] += 1
                        else:
                            roll_winrate['not_win'] += 1
                else :
                    #252개가 안되면 rolling 방식으로 계산 하지 않음
                    roll_winrate['win'] = winrate['win']
                    roll_winrate['not_win'] = winrate['not_win']
                roll_win_rate = roll_winrate['win'] / (roll_winrate['win'] + roll_winrate['not_win'])

            if isinstance(benchmark_data, pd.DataFrame):
                # y = np.append(self.result['portfolio_return'].values, [portfolio_return]).reshape(-1, 1)
                # 전날 result의 portfolio_return에 오늘 portfolio_return 값을 추가하고, 시리즈를 2차원 배열로 변환함

                if isinstance(free_risk_data, pd.DataFrame):
                    y = y - free_risk_data.iloc[:i+1]['return'].values.reshape(-1, 1)
                    # print('y : \n{0}'.format(y))
                y = np.delete(y, 0, 0)
                # 첫날의 데이터는 삭제해줌(benchmark 수익률은 두번째날 부터 존재하기 때문에 result 데이터도 갯수를 맞추기 위함)
                # print('y drop : \n{0}'.format(y))
                benchmark_history = benchmark.benchmark_history(self.context, benchmark_symbols, 'return', i+1)
                # print('benchmark_history : \n{0}'.format(benchmark_history))
                if i == 0:
                    alpha, beta_list = NA, [NA for i in range(0 , len(benchmark_data['benchmark'].unique().tolist()))]
                    # 첫날은 alpha, beta를 모두 NA 값으로 만듬(beta는 benchmark 갯수 만큼 NA 만듬)
                else :
                    alpha, beta_list = benchmark.get_alpha_beta(y)
                    # 첫날이 아니면 result의 portfolio return을 benchmark 객체의 get_alpha_beta 메서드의 인자로 넣어서 alpha, beta 값을 계산함
            else :
                alpha, beta_list = NA, [NA]
                # benchmarkt data가 없으면 alpha, beta 모두 NA로 설정함(beta는 리스트 형태로 넣어줌)

            s = pd.Series([current_time, capital_base, starting_cash, ending_cash,
                           starting_stock_value, ending_stock_value, starting_portfolio_value, ending_portfolio_value,
                           portfolio_return, annualized_return, roll_annualized_return, std_y, roll_std_y, sharp_ratio, roll_sharp_ratio,
                           cumulative_return, drawdown_ratio, MDD, underwater_period,
                           win_rate, roll_win_rate, total_profit, alpha] + beta_list, index=resultColumns)
            self.result = self.result.append(s, ignore_index=True)
            # result 데이터프레임 공간에 결과값 저장

            for symbol in self.context.symbols:
                self.context.account['withdrawal'][symbol] = {'unitPrice': 0, 'amounts': 0}
            self.context.account['deposit'] = 0
            # 하루가 끝나면 account의 withdrawal과 deposit을 0으로 초기화함

        if bool(self.context.record):
        # record된 것이 있다면
            self.result = pd.merge(self.result, self.context.record_df, how='outer', left_on='date', right_on='date')
            # date 칼럼을 기준으로 result 데이터프레임과 record 데이터프레임 병합(없는 값은 nan 처리)

        return self.result