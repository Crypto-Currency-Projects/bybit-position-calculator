from colorama import Fore, Style

class PositionCalculator:
    POSITION_LONG = "LONG"
    POSITION_SHORT = "SHORT"
    
    def __init__(self, equityUSD, position={}):
        """
        Initializes the position

        Paramters
        ---------
            equityUSD : float
        """

        # enter values
        position = {}
        position["ticker"]
        # enter values
        position = {}
        position["ticker"] = input("Ticker (ex. \"BTCUSD\"): ")
        position["leverage"] = int(input("Leverage: "))
        position["riskPercent"] = float(input("Risk Amount (Percentage): "))
        position["riskAmount"] = round((equityUSD * position["riskPercent"]) / 100, 2)
        position["side"] = input("Position Type [long/short]: ").upper()
        position["orderRange"] = [float(input("Start Price: ")), float(input("End Price: "))]
        position["numOfOrders"] = int(input("Number of Orders: "))

        # makes sure orderRange[0] is always lower than orderRange[1]
        if position["orderRange"][0] > position["orderRange"][1]:
            x = position["orderRange"][0]
            position["orderRange"][0] = position["orderRange"][1]
            position["orderRange"][1] = x
        
        self.position = position

    
    def verifyPositionValues(self):
        """
        Check for errors within position
        """

        position = self.position

        # detect errors
        errors = []
        if position["side"] == Position.POSITION_LONG or position["side"] == Position.POSITION_SHORT:
            pass
        else:
            errors.append("\"{}\" is not a valid position type".format(position["side"]))
        if not position["leverage"] in range(1, 100):
            errors.append("Leverage cannot be higher than 100 and nor lower than 1")
        if position["numOfOrders"] <= 1:
            errors.append("Your number of orders cannot be below or equal to 1")
        if len(errors) != 0:
            print("Errors:")
            [print("  {}{}{}".format(Fore.RED, i, Style.RESET_ALL)) for i in errors]
            exit()

        # detect warnings
        warnings = []
        if position["riskPercent"] > 2:
            warnings.append("It is not recommended to risk more than 2% of your account")
        if len(warnings) != 0:
            print("Warnings:")
            [print("  {}{}{}".format(Fore.YELLOW, i, Style.RESET_ALL)) for i in warnings]
            input("Press [enter] to acknowledge...")

        return True

    def generateOrders(self):
        """Generates orders to be placed"""

        position = self.position

        # orderPrice = position["orderRange"][0]
        # orderInterval = (position["orderRange"][1] - position["orderRange"][0]) / (position["numOfOrders"] - 1)
        # position["orders"] = []
        # position["orders"].append({"price": orderPrice, "contracts": None})
        # for _ in range(position["numOfOrders"] - 1):
        #     orderPrice += orderInterval

        orderRange = position["orderRange"]
        orderInterval = (orderRange[1] - orderRange[0]) / (position["numOfOrders"] - 1)

        orderPrices = [orderRange[0] + (orderInterval * i) for i in range(position["numOfOrders"])]

        # calculate contracts per order
        contractsPerOrder = round(position["riskAmount"]  / position["numOfOrders"])

        self.position["orders"] = []
        for i in orderPrices:
            self.position["orders"].append({"price": i, "amountUSD": contractsPerOrder})

        return self.position