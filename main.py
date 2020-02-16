from calculator import Calculator
from exchange.bybit import Bybit
from colorama import Fore, Style
import json
import os

# Allows for color support in cmd.exe
os.system("color 0")

# TODO: fix this entire thing, its pretty much pointless
# put your bybit account balance here
config = {
    # eventual support for multiple exchanges... Kappa
    "Profile": {
        "Bybit": {
            "balanceUSD": 208
        }
    }
}


# TODO: does colour really matter, get a web interface already...
print("{}========================={}".format(Fore.LIGHTBLACK_EX, Style.RESET_ALL))
print("Bybit Position Calculator".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
print("{}========================={}\n".format(Fore.LIGHTBLACK_EX, Style.RESET_ALL))


def enterValues():
        # TODO: whats better, a class or a dictionary? idk
    class Input:
        ticker = input("Ticker: ").upper()
        side = input("Side (long/short): ").upper()
        leverage = int(input("Leverage: "))
        riskPercent = float(input("Percentage of account to risk: "))
        orderRange = [float(input("Start Price: ")), float(input("End Price: "))]
        stopLoss = float(input("Stop-Loss Price: "))
        numOfOrders = int(input("Total number of orders to generate: "))
    return Input


while True:
    try: 
        Input = enterValues()
        break
    except Exception as e:
        print("{}{}{}".format(Fore.RED, e, Style.RESET_ALL))
    
calculator = Calculator(config["Profile"]["Bybit"]["balanceUSD"],
                        Input.ticker, Input.side, Input.leverage, Input.riskPercent, Input.orderRange,
                        Input.stopLoss, Input.numOfOrders)
position = calculator.calculatePosition()


print("\n-----------------------------\n")
print("Symbol: {}".format(Input.ticker))
print()
print("Total Contracts: {}".format(position["totalContracts"]))
print("Average Entry Price: {}".format(position["averageEntryPrice"]))
print("Maximum Leverage: {}".format(position["maxLeverage"]))
print()
[print("Price: {} Qty: {}".format(i["price"], i["qty"])) for i in position["orders"]]
print()
print("Risk: {} {}".format(position["risk"], position["ticker"][0]))
print("Risk: {} USD".format(position["risk"] * position["averageEntryPrice"]))
print("Account Risk: {:.2f}%".format(position["riskPercent"]))
print()
print("Stop: {}".format(Input.stopLoss))
print("Distance to stop: {} / {:.2f}%".format(abs(position["averageEntryPrice"] - Input.stopLoss), 100 * (abs(position["averageEntryPrice"] - Input.stopLoss) / Input.stopLoss)))
print("Liquidation Price: {}".format(position["liqPrice"]))
exit()