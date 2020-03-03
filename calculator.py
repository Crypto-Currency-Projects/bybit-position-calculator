from colorama import Fore, Style
from exchange.bybit import Bybit
from exchange.bitmex import Bitmex


class Calculator:
    def __init__(self, balance, symbol, side, riskPercent, orderRange, stopLoss, numOfOrders):
        """
        # Calculator
        
        `balance: num` `symbol: str` `side: str` `riskPercent: num`
        `orderRange: [num, num]` `stopLoss: num` `numOfOrders: int`
        """
        
        # Check input
        errors = []
        
        if balance <= 0:
            errors.append("Balance must be greater than zero")
        if side == "LONG" or side == "SHORT":  
            pass
        else: 
            errors.append("`{}` is not a valid entry for side".format(side))
        if riskPercent < 0: 
            errors.append("You cannot risk less than zero percent of your total account")
        if orderRange[0] > orderRange[1]:
            orderRange[0], orderRange[1] = orderRange[1], orderRange[0]
        if side == "LONG" and stopLoss > orderRange[0]:
            errors.append("Stop loss cannot be higher or within buying range")
        if side == "SHORT" and stopLoss < orderRange[1]:
            errors.append("Stop loss cannot be less than or within shorting range")
        if numOfOrders < 2:
            errors.append("Number of orders cannot be less than 2")
        
        if len(errors) != 0:
            print("Errors:")
            [print("  {}{}{}".format(Fore.RED, i, Style.RESET_ALL)) for i in errors]

        self.balance = balance
        self.symbol = symbol
        self.side = side
        self.riskPercent = riskPercent
        self.orderRange = orderRange
        self.stopLoss = stopLoss
        self.numOfOrders = numOfOrders
        
    
    def calculatePosition(self):
        """
        # calculatePosition
        
        does some cool stuff
        
        ## Return
        
        `dict`
        
        ```json
        {
            "ticker": ["BTC", "USD"],
            "leverage": 25,
            "maxLeverage": 55,
            "liqPrice": 6969.69,
            "orders": [{"price": 420, "qty": 420}...],
            "totalContracts": 9999,
            "averageEntryPrice": 420.69
        }
        ```
        """
        base = Bybit.getTickerBaseQuote(self.symbol)[0]
        quote = Bybit.getTickerBaseQuote(self.symbol)[1]
        
        interval = (self.orderRange[1] - self.orderRange[0]) / (self.numOfOrders - 1)
        orderPrices = [self.orderRange[0] + (interval * i) for i in range(self.numOfOrders)]
        averagePrice = sum(orderPrices) / len(orderPrices)

        riskAmount = (self.balance * self.riskPercent) / 100
        riskAmountBase = (1 / averagePrice) * riskAmount
        
        leverage = 1

        # Calculate the maximum leverage
        while True:
            liqPrice = Bybit.liqPrice(self.side, self.symbol, leverage, averagePrice)
            if self.side == "LONG" and liqPrice > self.stopLoss:
                break
            elif self.side == "SHORT" and liqPrice < self.stopLoss:
                break
            else:
                leverage += 1
        leverage -= 1
                     
        # Calculate number of contracts
        contracts = 1
        while True:
            unrealizedPL = abs(Bybit.unrealizedPL(self.side, contracts, averagePrice, self.stopLoss))
            if unrealizedPL > riskAmountBase:
                break
            else:
                contracts += 1
        contracts -= 1

        orders = [{"price":i, "qty": contracts / self.numOfOrders} for i in orderPrices]
        balanceBase = (1 / averagePrice) * self.balance
        riskPercentRC = (unrealizedPL * 100) / balanceBase 
        
        return {
            "ticker": [base, quote],
            "leverage": leverage,
            "liqPrice": liqPrice,
            "orders": orders,
            "risk": unrealizedPL,
            "riskPercent": riskPercentRC,
            "totalContracts": contracts,
            "averageEntryPrice": averagePrice
        }