from colorama import Fore, Style
from exchange.bybit import Bybit


def calculatePosition(balanceUSD, ticker, side, leverage, riskPercent, orderRange, stopLoss, numOfOrders):
    """
    Parameters
    ----------
        balanceUSD : float
        ticker : str.upper()
        side : str.upper()
        leverage : int
        riskPercent : float
        orderRange : [float, float]
        numOfOrders : int

    Return
    ------
        {
            "ticker": [str, str],
            "leverage": int,
            "maxLeverage": int,
            "liqPrice": float,
            "orders": [{"price": float, "qty": float}...],
            "totalContracts": int,
            "averageEntryPrice": float
        }
    """

    # TODO: move verify() to main.py or somewhere not in calculatePosition()

    def verify():
        errors = []

        # Makes sure orderRange[0] is always less than orderRange[1]
        if orderRange[0] > orderRange[1]:
            x = orderRange[1]
            orderRange[1] = orderRange[0]
            orderRange[0] = x
        elif orderRange[0] == orderRange[1]:
            errors.append("Buying / Selling range cannot be the same number")

        # Check side
        if side == "LONG" or side == "SHORT":
            pass
        else:
            errors.append("Position type must be either \"LONG\" or \"SHORT\"")

        # riskPercent
        if riskPercent < 0:
            errors.append("You cannot risk less than 0% of your account")

        # numOfOrders
        if numOfOrders < 2:
            errors.append("Your total number of orders cannot be less than 2")

        # Check stop loss price
        if side == "LONG":
            if stopLoss > orderRange[0]:
                errors.append("SL cannot be higher or within buying range")
        elif side == "SHORT":
            if stopLoss < orderRange[1]:
                errors.append("SL cannot be lower or within shorting range")

        if len(errors) != 0:
            print("\nErrors:")
            [print("  {}{}{}".format(Fore.RED, i, Style.RESET_ALL)) for i in errors]
            exit()
        else:
            return True
            
    verify()

    base = Bybit.getTickerBaseQuote(ticker)[0]
    quote = Bybit.getTickerBaseQuote(ticker)[1]

    # General info
    interval = (orderRange[1] - orderRange[0]) / (numOfOrders - 1)
    orderPrices = [orderRange[0] + (interval * i) for i in range(numOfOrders)]
    averagePrice = sum(orderPrices) / len(orderPrices)
    riskAmountBase = (1 / averagePrice) * ((riskPercent * balanceUSD) / 100)
    
    # Verify liquidation price is not beyond stop price
    liqPrice = Bybit.liqPrice(side, ticker, leverage, averagePrice)
    if side == "LONG":
        if stopLoss < liqPrice:
            print("{}Stop price cannot be lower than liquidation price".format(Fore.RED))
            exit()
    if side == "SHORT":
        if stopLoss > liqPrice:
            print("{}Stop price cannot be lower than liquidation price".format(Fore.RED))
            exit()

    # Calculate the maximum leverage possible
    #   The maximum amount of leverage able to be taken on a position until
    #   the liquidation price goes beyond stop price.
    maxLeverage = leverage
    while True:
        if side == "LONG":
            liqPriceMaxLeverage = Bybit.liqPrice(side, ticker, maxLeverage, averagePrice)
            if liqPriceMaxLeverage < stopLoss:
                maxLeverage += 1
            else: break
        if side == "SHORT":
            liqPriceMaxLeverage = Bybit.liqPrice(side, ticker, maxLeverage, averagePrice)
            if liqPriceMaxLeverage > stopLoss:
                maxLeverage += 1
            else: break
    
    # Calculate number of contracts
    #   Contracts will keeping adding until the positions unrealized 
    #   profit/loss is equal or less than the amount of account willing to 
    #   be risked or if the amount of contracts exceeds your account balance.
    contracts = 1
    while True:
        unrealizedPL = abs(Bybit.unrealizedPL(side, contracts, averagePrice, stopLoss))
        if (1 / averagePrice) * contracts > riskAmountBase:
            break
        if unrealizedPL < riskAmountBase:
            contracts += 1
        else: break

    # Generate orders to be placed
    orders = [{"price":i, "qty": contracts / numOfOrders} for i in orderPrices]
    
    return {
        "ticker": [base, quote],
        "leverage": leverage,
        "maxLeverage": maxLeverage,
        "liqPrice": liqPrice,
        "orders": orders,
        "risk": unrealizedPL,
        "totalContracts": contracts,
        "averageEntryPrice": averagePrice
    }