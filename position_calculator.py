from exchange.bybit import Bybit, BybitCalculator


def positionCalculator(accountBalanceUSD, symbol, side, riskPercent, orderRange, stopLoss, numOfOrders):
    """
    Generates your position. yay!

    Parameters: `accountBalanceUSD: num` `symbol: str` `side: str`
    `riskPercent: num` `orderRange: [num, num]` `stopLoss: num`
    `numOfOrders: int`

    Return `dict`

    Example Return
    ```json
    {
        "symbol": ["BTC", "USD"],
        "leverage": 72,
        "liqPrice": 5120.7068,
        "orders": [{"price": 5153.5, "qty": 24}...],
        "risk": 0.00021387,
        "riskPercent": 0.56215287,
        "totalContracts": 124,
        "averageEntryPrice": 5156.25
    }
    ```
    """

    # Verify if the ticker entered is a valid ticker
    symbolInfo = Bybit.symbols()["result"]
    for i in symbolInfo:
        if i["name"] == symbol:
            symbolInfo = i
            break
        else: return {"message": "Ticker not valid"}

    symbolList = [symbolInfo["base_currency"], symbolInfo["quote_currency"]]

    interval = (orderRange[1] - orderRange[0]) / (numOfOrders - 1)
    orderPrices = [orderRange[0] + (interval * i) for i in range(numOfOrders)]
    averagePrice = sum(orderPrices) / len(orderPrices)

    riskAmount = (accountBalanceUSD * riskPercent) / 100
    riskAmountBase = (1 / averagePrice) * riskAmount

    leverage = 1
    # Calculate the maximum leverage
    while True:
        liqPrice = BybitCalculator.liqPrice(side, symbol, leverage, averagePrice)
        if side == "LONG" and liqPrice > stopLoss:
            break
        elif side == "SHORT" and liqPrice < stopLoss:
            break
        else:
            leverage += 1
            if leverage > 100:
                return {"message": "Unable to find suitable leverage"}
    leverage -= 2  # provides a bit of leeway in case

    # Calculate number of contracts
    #   Number of contracts will keep adding from one until unrealized P/L
    #   between average entry and stop price match your account risk
    #   percentage.
    contracts = 1
    while True:
        unrealizedPL = abs(BybitCalculator.unrealizedPL(side, contracts, averagePrice, stopLoss))
        if unrealizedPL > riskAmountBase:
            contracts -= 1
            break
        else:
            contracts += 1

    # Generates orders
    #   Ensures equal distribution of contracts per orders.
    while contracts % numOfOrders > 0:
        contracts -= 1
        if contracts < numOfOrders:
            return {"message": "Unable to distribute contracts evenly"}
    orders = [{"price": i, "qty": contracts / numOfOrders} for i in orderPrices]

    # Recalculates your account risk
    liqPrice = BybitCalculator.liqPrice(side, symbol, leverage, averagePrice)
    unrealizedPL = abs(BybitCalculator.unrealizedPL(side, contracts, averagePrice, stopLoss))
    balanceBase = (1 / averagePrice) * accountBalanceUSD
    riskPercentRC = (unrealizedPL * 100) / balanceBase

    return {
        "message": "OK",
        "data": {
            "symbol": [symbolList[0], symbolList[1]],
            "leverage": leverage,
            "liqPrice": liqPrice,
            "orders": orders,
            "risk": unrealizedPL,
            "riskPercent": riskPercentRC,
            "totalContracts": contracts,
            "averageEntryPrice": averagePrice
        }
    }
