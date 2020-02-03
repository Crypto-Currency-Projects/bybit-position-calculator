from calculator import calculatePosition
from colorama import Fore, Style
import json
import os

# Allows for color support in cmd.exe
os.system("color 0")

print("\n{}Bybit Position Calculator{}\n".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))

# config.json doesn't have much of a purpose yet, if it fails to load
# you can manually enter your account balance manually.
def loadConfig():
    """Load ...\\position-calculator\\config.json\\"""
    try:
        x = open("{}\\config.json".format(os.getcwd()))
        x = json.load(x)
    except Exception as e:
        print("{}Failed to load config.json\n{}{}".format(Fore.RED, e, Style.RESET_ALL))
        x = {"balanceUSD": float(input("Enter your account equity manually: "))}
    return x

config = loadConfig()
balanceUSD = config["balanceUSD"]

ticker = input("Ticker: ").upper()
side = input("Side (long/short): ").upper()
leverage = int(input("Leverage: "))
riskPercent = float(input("Percentage of account to risk: "))
orderRange = [float(input("Start Price: ")), float(input("End Price: "))]
stopLoss = float(input("Stop-Loss Price: "))
numOfOrders = int(input("Total number of orders to generate: "))

position = calculatePosition(balanceUSD, ticker, side, leverage, riskPercent, orderRange, stopLoss, numOfOrders)

print("\n-----------------------------")

print("\n{}Risk{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
print("Risk: {} {}".format(position["risk"], position["ticker"][0]))
print("Risk: {} USD".format(position["risk"] * position["averageEntryPrice"]))

print("\n{}Leverage{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
print("Current Leverage: {}".format(leverage))
print("Max Leverage: {}".format(position["maxLeverage"]))

print("\n{}Stop{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
print("Stop Price: {}".format(stopLoss))
print("Distance to Stop: {} / {:.2f}%".format(abs(position["averageEntryPrice"] - stopLoss), abs((position["averageEntryPrice"] - stopLoss) / stopLoss)))

print("\n{}Position{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
print("Average Entry Price: {}".format(position["averageEntryPrice"]))
print("Total Contracts: {}".format(position["totalContracts"]))
print("Liq Price: {}".format(position["liqPrice"]))

print("\n{}Orders{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
[print("Price: {} Qty: {}".format(i["price"], i["qty"])) for i in position["orders"]]
exit()