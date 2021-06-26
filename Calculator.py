

def update_portfolio_current_price(context, dataquery):

    for symbol in context.symbols :
        context.portfolio['stock'][symbol]['price'] = dataquery.current_data(symbol, 'price')

def update_portfolio_withdrawal(context) :

    for symbol in context.symbols :
        context.portfolio['stock'][symbol]['amounts'] +=  context.account['withdrawal'][symbol]['amounts']
        # context의 portfolio 딕셔너리안에 있는 해당 심볼 주식의 amounts에 체결 수량을 추가(누적)하여 저장

    if context.account['balance'] >= 0 :
        context.portfolio['cash'] = context.account['balance']
    else :
        context.portfolio['cash'] = 0

def update_portfolio_deposit(context) :

    if context.account['balance'] >= 0 :
        context.portfolio['cash'] = context.account['balance']
    else :
        context.portfolio['cash'] = 0

def calculate_portfolio_value(context, dataquery, price='price') :
    # 현 시점의 포트폴리오 평가액을 계산함(price는 'price'를 기본값으로 하지만, 'open', 'high' 등 다른 index로 평가할수도 있음)
    cash_value = context.portfolio['cash']

    stock_value = 0

    price_data = dataquery.current_data(context.symbols, [price])
    exited_symbols = price_data['symbol'].unique().tolist()

    for symbol in exited_symbols:
        context.portfolio['stock'][symbol]['price'] = dataquery.current_data(symbol, price)
        stock_price = context.portfolio['stock'][symbol]['price']
        # dataquery에서 현재 가격을 조회함
        stock_amounts = context.portfolio['stock'][symbol]['amounts']
        # context의 portfolio에서 해당 심볼에 해당하는 주식의 보유 주식 수를 가지고옴
        stock_value += stock_price * stock_amounts

    portfolio_value = cash_value + stock_value
    # portfolio_value는 현금 가치와 주식 가치를 합한 값
    # portfolio_value 계산

    return portfolio_value

def calculate_return_value(context) :

    portfolio_value = calculate_portfolio_value(context)

    return_value = portfolio_value - context.capial_base

    return return_value