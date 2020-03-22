import requests


class Bybit:
    baseUrl = "https://api.bybit.com"
        
    @staticmethod
    def request(method, url, params="", retries=5):
        """Base request"""
        while retries > 0:
            try:
                response = requests.request(method, url, params=params)
                responseJson = response.json()
                return responseJson
            except:
                retries -= 1
    
    @staticmethod
    def symbols():
        """
        `[GET]` `/v2/public/symbols`
        
        Get symbol info.
        
        return `dict`
        """
        return Bybit.request("GET", Bybit.baseUrl + "/v2/public/symbols")
    
    @staticmethod
    def tickers(params=""):
        """
        `[GET]` `/v2/public/tickers`
        
        Get the latest information for symbol.
        
        return `dict`
        """
        return Bybit.request("GET", Bybit.baseUrl + "/v2/public/tickers", params)
    
    
class BybitCalculator:
    """
    Basic calculations for various stuff. More info available 
    at https://help.bybit.com/

    These do not get data from Bybit API and therefore must be updated manually
    """
    
    SIDE_LONG = "LONG"
    SIDE_SHORT = "SHORT"
    
    @staticmethod
    def initialMargin(contracts, averagePrice, leverage):
        """Initial Margin"""
        return contracts / (averagePrice * leverage)

    @staticmethod
    def maintenanceMarginRate(ticker):
        """Mainteanance Margin Rate"""
        if ticker == "BTCUSD": return 0.005
        else: return 0.01

    @staticmethod
    def maintenanceMargin(ticker, contracts, averagePrice):
        """Maintenance Margin"""
        return (contracts / averagePrice) * BybitCalculator.maintenanceMarginRate(ticker)

    @staticmethod
    def liqPrice(side, ticker, leverage, averagePrice):
        """Liquidation Price"""
        marginRate = BybitCalculator.maintenanceMarginRate(ticker)
        if side == BybitCalculator.SIDE_LONG:
            lp = (averagePrice * leverage) / (leverage + 1 - (marginRate * leverage))
        elif side == BybitCalculator.SIDE_SHORT:
            lp = (averagePrice * leverage) / (leverage - 1 + (marginRate * leverage))
        else: raise Exception("param [side] not valid")
        return lp

    @staticmethod
    def unrealizedPL(side, contracts, averagePrice, closePrice):
        """Unrealized Profit / Loss"""
        if side == BybitCalculator.SIDE_LONG:
            pl = contracts * ((1 / averagePrice) - (1 / closePrice))
        elif side == BybitCalculator.SIDE_SHORT:
            pl = contracts * ((1 / closePrice) - (1 / averagePrice))
        else:
            raise Exception("param [side] not valid")
        return pl
