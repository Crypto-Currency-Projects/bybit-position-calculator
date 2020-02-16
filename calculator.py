from colorama import Fore, Style
from exchange.bybit import Bybit
from exchange.bitmex import Bitmex


class Calculator:
    def __init__(self, balance, symbol, side, leverage, riskPercent, orderRange, stopLoss, numOfOrders):
        """
        # Calculator
        
        it does some cool things
        
        ## Parameters
        
        ```txt
        balance         num
        symbol          str
        side            str
        leverage        int
        riskPercent     num
        orderRange      [num, num]
        stopLoss        num
        numOfOrders     int
        ```
        """
        
        # Check input
        # TODO: this is ugly
        errors = []
        if balance <= 0:
            errors.append("Balance must be greater than zero")
        if side == "LONG" or side == "SHORT":  
            pass
        else: 
            errors.append("{} is not a valid entry for side".format(side))
        if leverage < 1: 
            errors.append("Leverage cannot be less than 1")
        if riskPercent < 0: 
            errors.append("You cannot risk less than zero percent of your total account")
        if orderRange[0] > orderRange[1]:
            orderRange[0], orderRange[1] = orderRange[1], orderRange[0]
        if side == "LONG" and stopLoss > orderRange[0]:
            errors.append("Stop loss cannot be higher or within buying range")
        if side == "SHORT" and stopLoss < orderRange[1]:
            errors.append("Stop loss cannot be less than or within shorting range")
        if numOfOrders < 3:
            errors("Cannot generate less than 3 orders")
        
        if len(errors) != 0:
            print("Errors:")
            [print("  {}{}{}".format(Fore.RED, i, Style.RESET_ALL)) for i in errors]

        self.balance = balance
        self.symbol = symbol
        self.side = side
        self.leverage = leverage
        self.riskPercent = riskPercent
        self.orderRange = orderRange
        self.stopLoss = stopLoss
        self.numOfOrders = numOfOrders
        
    
    def calculatePosition(self):
        """
        # calculatePosition
        
        calculates your position!
        
        ## Example Return
        
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
        riskAmountBase = (1 / averagePrice) * ((self.riskPercent * self.balance) / 100)
        
        # Liquidation Price
        #   Verify liqPrice is not beyond stop price
        liqPrice = Bybit.liqPrice(self.side, self.symbol, self.leverage, averagePrice)
        if self.side == "LONG" and self.stopLoss < liqPrice:
            raise Exception("Stop price cannot be lower than liquidation price.\nLiq Price: {}\nStop: {}".format(liqPrice, self.stopLoss))
        if self.side == "SHORT" and self.stopLoss > liqPrice:
            raise Exception("Stop price cannot be higher than liquidation price.\nLiq Price: {}\nStop: {}".format(liqPrice, self.stopLoss))

        # Calculate the maximum leverage possible
        #   The maximum amount of leverage able to be taken on a position until
        #   the liquidation price goes beyond stop price.
        maxLeverage = self.leverage
        while True:
            if self.side == "LONG":
                liqPriceMaxLeverage = Bybit.liqPrice(self.side, self.symbol, maxLeverage, averagePrice)
                if liqPriceMaxLeverage < self.stopLoss:
                    maxLeverage += 1
                else: break
            if self.side == "SHORT":
                liqPriceMaxLeverage = Bybit.liqPrice(self.side, self.symbol, maxLeverage, averagePrice)
                if liqPriceMaxLeverage > self.stopLoss:
                    maxLeverage += 1
                else: break
        
        # Calculate number of contracts
        #   The number of contracts will keeping adding until the position's
        #   unrealized profit/loss is equal or less than the amount of account 
        #   willing to be risked or if the amount of contracts exceeds your 
        #   account's balance.
        contracts = 1
        while True:
            unrealizedPL = abs(Bybit.unrealizedPL(self.side, contracts, averagePrice, self.stopLoss))
            if (1 / averagePrice) * contracts > riskAmountBase:
                break
            if unrealizedPL < riskAmountBase:
                contracts += 1
            else: break

        orders = [{"price":i, "qty": contracts / self.numOfOrders} for i in orderPrices]
        
        return {
            "ticker": [base, quote],
            "leverage": self.leverage,
            "maxLeverage": maxLeverage,
            "liqPrice": liqPrice,
            "orders": orders,
            "risk": unrealizedPL,
            "riskPercent": 100 * ((100 * unrealizedPL) / ((1 / averagePrice) * self.balance)),
            "totalContracts": contracts,
            "averageEntryPrice": averagePrice
        }