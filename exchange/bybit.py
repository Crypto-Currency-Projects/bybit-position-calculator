

class Bybit:
    """
    Bybit
    -----
    Info can be found at https://help.bybit.com/
    """
    TICKER_BTCUSD = "BTCUSD"
    TICKER_ETHUSD = "ETHUSD"
    TICKER_XRPUSD = "XRPUSD"
    TICKER_EOSUSD = "EOSUSD"

    SIDE_SHORT = "SHORT"
    SIDE_LONG = "LONG"

    exchangeInfo = {
        "tickers": ["BTCUSD", "ETHUSD", "XRPUSD", "EOSUSD"],
        "BTCUSD": {
            "base": "BTC",
            "quote": "USD",
            "maintenanceMarginRate": 0.005
        },
        "ETHUSD": {
            "base": "ETH",
            "quote": "USD",
            "maintenanceMarginRate": 0.01
        },
        "XRPUSD": {
            "base": "XRP",
            "quote": "USD",
            "maintenanceMarginRate": 0.01
        },
        "EOSUSD": {
            "base": "EOS",
            "quote": "USD",
            "maintenanceMarginRate": 0.01
        }
    }
    @staticmethod
    def initialMargin(contracts, averagePrice, leverage):
        """
        # Initial Margin
        
        `Initial Margin = Contracts / (AveragePrice * Leverage)`
        
        https://help.bybit.com/hc/en-us/articles/360007133254-Initial-Margin
        
        ## Parameters
        
        `contracts: int` `averagePrice: num` `leverage: int`
        
        ## Return
        
        `float`
        """
        return contracts / (averagePrice * leverage)
    
    @staticmethod
    def maintenanceMarginRate(ticker):
        """
        # Maintenance Margin Rate
        
        Returns the maintenance margin rate for the selected ticker
        
        https://help.bybit.com/hc/en-us/articles/360007133274-Maintenance-Margin

        ## Parameters
        
        `ticker: str`
        
        ## Return
        
        `float`
        """
        return Bybit.exchangeInfo[ticker]["maintenanceMarginRate"]

    @staticmethod
    def maintenanceMargin(ticker, contracts, averagePrice):
        """
        # Maintenance Margin
        
        `Maintenance Margin = (Contracts / Order Price) * Maintenance Margin Rate`
        
        https://help.bybit.com/hc/en-us/articles/360007133274-Maintenance-Margin
        
        ## Paramters
        
        `ticker: str` `contracts: int` `averagePrice: num`
        
        ## Return
        
        `float`
        """
        return (contracts / averagePrice) * Bybit.maintenanceMarginRate(ticker)

    @staticmethod
    def liqPrice(side, ticker, leverage, averagePrice):
        """
        # Liquidation Price
        
        Long Position: `LP = (averagePrice * leverage) / (leverage + 1 - (maintenanceMarginRate * leverage))`
        
        Short Position: `LP = (averagePrice * leverage) / (leverage - 1 + (maintenanceMarginRate * leverage))`
        
        https://help.bybit.com/hc/en-us/articles/360007206554-Liquidation

        ## Parameters
        
        `side: str` `ticker: str` `leverage: int` `averagePrice: num`
        
        ## Return
        
        `float`
        """
        marginRate = Bybit.maintenanceMarginRate(ticker)
        if side == Bybit.SIDE_LONG:
            lp = (averagePrice * leverage) / (leverage + 1 - (marginRate * leverage))
        elif side == Bybit.SIDE_SHORT:
            lp = (averagePrice * leverage) / (leverage - 1 + (marginRate * leverage))
        else: raise Exception("param [side] not valid")
        return lp

    @staticmethod
    def unrealizedPL(side, contracts, averagePrice, closePrice):
        """
        # Unrealized Profit/Loss
        
        Long Position: `UPL = contracts * ((1 / averagePrice) - (1 / closePrice))`
        
        Short Position: `UPL = contracts * ((1 / closePrice) - (1 / averagePrice))`

        https://help.bybit.com/hc/en-us/articles/360013263213-Calculation-of-Unrealized-Profit-Loss

        ## Paramters
        
        `side: str` `contracts: int` `averagePrice: num` `closePrice: num`
        
        ## Return
        
        `float`
        """
        if side == Bybit.SIDE_LONG:
            pl = contracts * ((1 / averagePrice) - (1 / closePrice))
        elif side == Bybit.SIDE_SHORT:
            pl = contracts * ((1 / closePrice) - (1 / averagePrice))
        else:
            raise Exception("param [side] not valid")
        return pl

    @staticmethod
    def getTickerBaseQuote(ticker):
        """
        Gets the base and quote currency of ticker

        Return: `[str, str]`
        """
        return [Bybit.exchangeInfo[ticker]["base"], Bybit.exchangeInfo[ticker]["quote"]]

        