from calculator import Calculator
from exchange.bybit import Bybit
from colorama import Fore, Style
import json
import os

# Allows for color support in cmd.exe
os.system("color 0")

# put your bybit account balance here
# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓
balanceUSD = 350
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑


print()
print("{}Bybit Position Calculator{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
print()


def enterValues():
    values = {
        "symbol": input("Symbol: ").upper(),
        "side": input("Side (long/short): ").upper(),
        "riskPercent": float(input("Risk Percentage: ")),
        "orderRange": [float(input("Start Price: ")), float(input("Stop Price: "))],
        "stopLoss": float(input("Stop Loss: ")),
        "numOfOrders": int(input("Number of Orders: "))
    }
    return values


while True:
    try: 
        values = enterValues()

        calculator = Calculator(balanceUSD, values["symbol"], values["side"], 
                                values["riskPercent"], values["orderRange"], 
                                values["stopLoss"], values["numOfOrders"])
                               
        position = calculator.calculatePosition()
        break
    except Exception as e:
        print("{}{}{}".format(Fore.RED, e, Style.RESET_ALL))


print("\n-----------------------------\n")
print("Symbol: {}".format(values["symbol"]))
print()
print("Total Contracts: {}".format(position["totalContracts"]))
print("Average Entry Price: {}".format(position["averageEntryPrice"]))
print("Leverage: {}x".format(position["leverage"]))
print()
[print("Price: {} Qty: {}".format(i["price"], i["qty"])) for i in position["orders"]]
print()
print("Risk: {} {}".format(position["risk"], position["ticker"][0]))
print("Risk: {} USD".format(position["risk"] * position["averageEntryPrice"]))
print("Account Risk: {:.2f}%".format(position["riskPercent"]))
print()
print("Stop: {}".format(values["stopLoss"]))
print("Distance to stop: {} / {:.2f}%".format(abs(position["averageEntryPrice"] - values["stopLoss"]), 100 * (abs(position["averageEntryPrice"] - values["stopLoss"]) / values["stopLoss"])))
print("Liquidation Price: {}".format(position["liqPrice"]))
exit()