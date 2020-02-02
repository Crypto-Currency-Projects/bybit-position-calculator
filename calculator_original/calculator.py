from colorama import Fore, Style


def calculatePosition(
    accountEquityUSD, ticker, positionType, riskPercent, orderRange, stopLoss, numOfOrders
    ):
    """
    Calculates Position

    Parameters
    ----------
        accountEquityUSD : float
        ticker : str.upper()
        positionType : str.upper()
        riskPercent : float
        orderRange : list
        stopLoss : float
        numberOfOrders : int

    Returns
    -------
        {...}
    """

    def verify():
        # makes sure orderRange[0] is less than orderRange[1]
        errors = []

        if orderRange[0] > orderRange[1]:
            x = orderRange[1]
            orderRange[1] = orderRange[0]
            orderRange[0] = x
        elif orderRange[0] == orderRange[1]:
            errors.append("Buying / Selling range cannot be the same number")
        # check positionType
        if positionType == "LONG" or positionType == "SHORT":
            pass
        else:
            errors.append("Position Type must be either \"LONG\" or \"SHORT\"")
        # riskPercent
        if riskPercent < 0:
            errors.append("You cannot risk less than 0% of your account")
        if numOfOrders < 2:
            errors.append("Your total number of orders cannot be less than 2")
        if positionType == "LONG":
            if stopLoss > orderRange[0]:
                errors.append("SL cannot be higher or within buying range")
        elif positionType == "SHORT":
            if stopLoss < orderRange[1]:
                errors.append("SL cannot be lower or within shorting range")

        if len(errors) != 0:
            print("\nErrors:")
            [print("  {}{}{}".format(Fore.RED, i, Style.RESET_ALL)) for i in errors]
            exit()
        else:
            return True
            
    verify()

    # Generate orders within range
    riskAmountUSD = round((riskPercent * accountEquityUSD) / 100, 2)
    riskAmountUSDPerOrder = round(riskAmountUSD / numOfOrders)
    interval = (orderRange[1] - orderRange[0]) / (numOfOrders - 1)
    orderPrices = [orderRange[0] + (interval * i) for i in range(numOfOrders)]
    averageEntryPrice = sum(orderPrices) / len(orderPrices)

    # Bybit Maintenance Margin: https://help.bybit.com/hc/en-us/articles/360007133274-Maintenance-Margin
    maintenanceMarginRate = 0.005 if ticker == "BTCUSD" else .01

    # Calculates maximum leverage
    maxLeverage = 1
    while True:
        # initialMargin = riskAmountUSD / ((averageEntryPrice) * maxLeverage)
        # No Suport for Cross Margin
        # Bybit Liquidation: https://help.bybit.com/hc/en-us/articles/360007206554-Liquidation
        if positionType == "LONG":
            liqPrice = (averageEntryPrice * maxLeverage) / (maxLeverage + 1 - (maintenanceMarginRate * maxLeverage))
            if liqPrice < stopLoss:
                maxLeverage += 1
            else: break
        elif positionType == "SHORT":
            liqPrice = (averageEntryPrice * maxLeverage) / (maxLeverage - 1 + (maintenanceMarginRate * maxLeverage))
            if liqPrice > stopLoss:
                maxLeverage += 1
            else: break

    orders = [{"price": i, "qty": riskAmountUSDPerOrder} for i in orderPrices]
    
    return {
        "maxLeverage": maxLeverage,
        "orders": orders,
        "qty": riskAmountUSD,
        "liqPrice": liqPrice,
        "averageEntryPrice": averageEntryPrice
    }