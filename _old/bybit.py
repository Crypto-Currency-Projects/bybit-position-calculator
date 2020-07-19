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


class BybitINVERSE:
    """
    `INVERSE CONTRACT`
    Basic calculations for various stuff. More info available
    at https://help.bybit.com/

    These do not get data from Bybit API and therefore must be updated manually
    """

    SIDE_LONG = "LONG"
    SIDE_SHORT = "SHORT"

    @staticmethod
    def initialMargin(contracts, averagePrice, leverage):
        """
        ## Initial Margin
        `contracts / (averagePrice * leverage)`

        Return `float`
        """
        return contracts / (averagePrice * leverage)

    @staticmethod
    def maintenanceMarginRate(ticker):
        """
        ## Mainteanance Margin Rate
        ```json
        { "BTCUSD": 0.005, "ETHUSD": 0.01, "EOSUSD": 0.01, "XRPUSD": 0.01 }
        ```
        Return `float`
        """
        rate = { "BTCUSD": 0.005, "ETHUSD": 0.01, "EOSUSD": 0.01, "XRPUSD": 0.01 }
        try: return rate[ticker]
        except: raise Exception("`{}` is not a valid ticker".format(ticker))

    @staticmethod
    def maintenanceMargin(ticker, contracts, averagePrice):
        """
        ## Maintenance Margin
        `(contracts / averagePrice) * maintenancemarginRate`

        Return `float`
        """
        return (contracts / averagePrice) * BybitINVERSE.maintenanceMarginRate(ticker)

    @staticmethod
    def liqPrice(side, ticker, leverage, averagePrice):
        """
        ## Liquidation Price
        LONGS: `(averagePrice * leverage) / (leverage + 1 - (marginRate * leverage))`

        SHORTS: `(averagePrice * leverage) / (leverage - 1 + (marginRate * leverage))`

        Return `float`
        """
        marginRate = BybitINVERSE.maintenanceMarginRate(ticker)
        if side == BybitINVERSE.SIDE_LONG:
            return (averagePrice * leverage) / (leverage + 1 - (marginRate * leverage))
        elif side == BybitINVERSE.SIDE_SHORT:
            return (averagePrice * leverage) / (leverage - 1 + (marginRate * leverage))
        else:
            raise Exception("param [side] not valid")

    @staticmethod
    def unrealizedPL(side, contracts, averagePrice, closePrice):
        """
        ## Unrealized Profit / Loss
        LONGS: `contracts * ((1 / averagePrice) - (1 / closePrice))`

        SHORTS: `contracts * ((1 / closePrice) - (1 / averagePrice))`

        Return `float`
        """
        if side == BybitINVERSE.SIDE_LONG:
            return contracts * ((1 / averagePrice) - (1 / closePrice))
        elif side == BybitINVERSE.SIDE_SHORT:
            return contracts * ((1 / closePrice) - (1 / averagePrice))
        else:
            raise Exception("param [side] not valid")
