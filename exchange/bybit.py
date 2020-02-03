

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
        https://help.bybit.com/hc/en-us/articles/360007133254-Initial-Margin
        """
        return contracts / (averagePrice * leverage)
    
    @staticmethod
    def maintenanceMarginRate(ticker):
        """
        Maintenance Margin Rate
        -----------------------
        https://help.bybit.com/hc/en-us/articles/360007133274-Maintenance-Margin

        Return
        ------
            float
        """
        return Bybit.exchangeInfo[ticker]["maintenanceMarginRate"]

    @staticmethod
    def maintenanceMargin(ticker, contracts, averagePrice):
        """
        Maintenance Margin
        ------------------
        https://help.bybit.com/hc/en-us/articles/360007133274-Maintenance-Margin

        Calculation
        -----------
            maintenanceMargin = (contracts / averagePrice) * maintenanceMarginRate
        
        Return
        ------
            float
        """
        return (contracts / averagePrice) * Bybit.maintenanceMarginRate(ticker)

    @staticmethod
    def liqPrice(side, ticker, leverage, averagePrice):
        """
        Liquidation Price
        -----------------
        https://help.bybit.com/hc/en-us/articles/360007206554-Liquidation

        Calculation
        -----------
            POSITION LONG: LP = (averagePrice * leverage) / (leverage + 1 - (maintenanceMarginRate * leverage))
            POSITION SHORT: LP = (averagePrice * leverage) / (leverage - 1 + (maintenanceMarginRate * leverage))

        Return
        ------
            float
        """
        marginRate = Bybit.maintenanceMarginRate(ticker)
        if side == Bybit.SIDE_LONG:
            lp = (averagePrice * leverage) / (leverage + 1 - (marginRate * leverage))
        elif side == Bybit.SIDE_SHORT:
            lp = (averagePrice * leverage) / (leverage - 1 + (marginRate * leverage))
        else: raise Exception("param [side] not valid")
        return lp

    @staticmethod
    def unrealizedPL(side, contracts, averagePrice, lastPrice):
        """
        Unrealized Profit/Loss
        ----------------------
        https://help.bybit.com/hc/en-us/articles/360013263213-Calculation-of-Unrealized-Profit-Loss

        Calculation
        -----------
            POSITION LONG: PL = contracts * ((1 / averagePrice) - (1 / lastPrice))
            POSITION SHORT: PL = contracts * ((1 / lastPrice) - (1 / averagePrice))

        Return
        ------
            float
        """
        if side == Bybit.SIDE_LONG:
            pl = contracts * ((1 / averagePrice) - (1 / lastPrice))
        elif side == Bybit.SIDE_SHORT:
            pl = contracts * ((1 / lastPrice) - (1 / averagePrice))
        else:
            raise Exception("param [side] not valid")

        return pl

    @staticmethod
    def getTickerBaseQuote(ticker):
        """
        Gets the base and quote currency of ticker

        Return
        ------
            list
        """
        return [Bybit.exchangeInfo[ticker]["base"], Bybit.exchangeInfo[ticker]["quote"]]

        