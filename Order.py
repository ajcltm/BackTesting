
def order(context, symbols, unitPrice, amounts) :

    for counter, symbol in enumerate(symbols):
        if isinstance(unitPrice, list) :
            context.account['withdrawal'][symbol]['unitPrice'] = unitPrice[counter]
            context.account['withdrawal'][symbol]['amounts'] = amounts[counter]
        else:
            context.account['withdrawal'][symbol]['unitPrice'] = unitPrice
            context.account['withdrawal'][symbol]['amounts'] = amounts

    for counter, symbol in enumerate(symbols):
        if isinstance(unitPrice, list) :
            context.portfolio['stock'][symbol]['amounts'] += amounts[counter]
        else:
            context.portfolio['stock'][symbol]['amounts'] += amounts

    return context

def deposit(context, dollars) :
    context.account['deposit'] = dollars
    context.portfolio['cash'] += dollars