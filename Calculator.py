
def update_portfolio_withdrawal(context, symbols) :

    for symbol in symbols :
        context.portfolio['stock'][symbol]['amounts'] +=  context.account['withdrawal'][symbol]['amounts']
        # context의 portfolio 딕셔너리안에 있는 해당 심볼 주식의 amounts에 체결 수량을 추가(누적)하여 저장

    if context.account['balance'] >= 0 :
        context.portfolio['cash'] = context.account['balance']
        # balance(잔액)이 0보다 크면, 현금은 balance 와 동일함
    else :
        context.portfolio['cash'] = 0
        # balance가 마이너스이면, 현금은 0 임

def update_portfolio_deposit(context) :

    if context.account['balance'] >= 0 :
        context.portfolio['cash'] = context.account['balance']
        # balance(잔액)이 0보다 크면, 현금은 balance 와 동일함
    else :
        context.portfolio['cash'] = 0
        # balance가 마이너스이면, 현금은 0 임

def calculate_portfolio_value(context, dataquery, price='price') :
    # 현 시점의 포트폴리오 평가액을 계산함(price는 'price'를 기본값으로 하지만, 'open', 'high' 등 다른 index로 평가할수도 있음)
    cash_value = context.portfolio['cash']
    # 현금가치는 현재 보유하고 있는 현금의 양과 동일함
    stock_value = 0
    # 밑에 있는 for loop를 돌면서 주식가치를 누적합계하기 위해 초기값을 0으로 설정
    price_data = dataquery.current_data(context.symbols, [price])
    # current_data함수를 이용하여 현재 가격을 호출함(symbols와 price를 리스트 형태로 설정하면, symbol과 price의 열을 가진 df가 반환됨
    exited_symbols = price_data['symbol'].unique().tolist()
    # 현재 시간에 가격데이터가 존재하는 symbol에 대해서만 portfolio value를 업데이트하기 위해 고유한 synbol값을 지정

    for symbol in exited_symbols:
    # 현재 시간을 기준으로 가격데이터가 존재하는 symbol에 대해 for loop를 돌림
        context.portfolio['stock'][symbol]['price'] = dataquery.current_data(symbol, price)
        # 각 심볼에 대해 현재 가격을 반환하여 context portfolio price에 저장(current_data 함수에 symbol과 price를 스칼라 값으로 넣으면 스칼라 값이 반환됨)
        stock_price = context.portfolio['stock'][symbol]['price']
        # dataquery에서 현재 가격을 조회함
        stock_amounts = context.portfolio['stock'][symbol]['amounts']
        # context의 portfolio에서 해당 심볼에 해당하는 주식의 보유 주식 수를 가지고옴
        stock_value += stock_price * stock_amounts
        # for loop를 돌면서 계산한 주식가치를 누적하여 합산

    portfolio_value = cash_value + stock_value
    # portfolio_value는 현금 가치와 주식 가치를 합한 값
    # portfolio_value 계산

    return portfolio_value