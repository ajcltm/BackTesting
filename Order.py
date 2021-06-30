from Calculator import *


def order(context, symbols, unitPrice, amounts) :
    # symbols, unitPrice, amounts는 스칼라 문자열 또는 리스트로 넣을 수 있음
    # 단, unitPrice, amounts는 동일한 형태이어야함(symbols과는 다른 형태이어도 괜찮음)

    if isinstance(symbols, list):
        for counter, symbol in enumerate(symbols):
            if isinstance(unitPrice, list) :
            # symbols와 unitPrice 모두 리스트 형태로 넣어준 것이라면

                context.account['withdrawal'][symbol]['unitPrice'] = unitPrice[counter]
                # context의 account 딕셔너리안에 있는 해당 심볼 주식의 unitPrice에 체결 단가를 저장
                context.account['withdrawal'][symbol]['amounts'] = amounts[counter]
                # context의 account 딕셔너리안에 있는 해당 심볼 주식의 amounts에 체결 수량을 저장

            else:
            # symbols는 리스트, unitPrice는 스칼라 문자형태로 넣어준 것이라면
                context.account['withdrawal'][symbol]['unitPrice'] = unitPrice
                # context의 account 딕셔너리안에 있는 해당 심볼 주식의 unitPrice에 체결 단가를 저장
                context.account['withdrawal'][symbol]['amounts'] = amounts
                # context의 account 딕셔너리안에 있는 해당 심볼 주식의 amounts에 체결 수량을 저장


    else :
        if isinstance(unitPrice, list):
        # symbols는 스칼라 문자형태, unitPrice는 리스트 형태로 넣어준 것이라면
            context.account['withdrawal'][symbols]['unitPrice'] = unitPrice[0]
            # context의 account 딕셔너리안에 있는 해당 심볼 주식의 unitPrice에 체결 단가를 저장
            context.account['withdrawal'][symbols]['amounts'] = amounts[0]
            # context의 account 딕셔너리안에 있는 해당 심볼 주식의 amounts에 체결 수량을 저장

        else:
            context.account['withdrawal'][symbols]['unitPrice'] = unitPrice
            # context의 account 딕셔너리안에 있는 해당 심볼 주식의 unitPrice에 체결 단가를 저장
            context.account['withdrawal'][symbols]['amounts'] = amounts
            # context의 account 딕셔너리안에 있는 해당 심볼 주식의 amounts에 체결 수량을 저장

    for symbol in symbols :
        withdrawal = context.account['withdrawal'][symbol]['unitPrice'] * context.account['withdrawal'][symbol]['amounts']
        print('withrawal : {}'.format(withdrawal))
        context.account['balance'] -= withdrawal
        print('balance by withrawal: {}'.format(context.account['balance']))

    update_portfolio_withdrawal(context, symbols)
    # context의 portfolio 딕셔너리안에 있는 해당 심볼 주식의 amounts에 체결 수량을 추가(누적)하여 저장

    return context
    # 주문한 정보들을 담은 context 반환

def deposit(context, dollars) :
    context.account['deposit'] = dollars
    # dollar 만큼을 입금하여 계좌(account) 정보에 저장
    context.account['balance'] += context.account['deposit']
    print('balance by deposit : {}'.format(context.account['balance']))

    context.capital_base += context.account['deposit']

    update_portfolio_deposit(context)
