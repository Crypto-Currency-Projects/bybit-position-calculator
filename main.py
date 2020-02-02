from calculator import calculatePosition
from colorama import Fore, Style
import json
import os

# Allows for color support in cmd.exe
os.system("color 0")

print("\n{}Bybit Position Calculator{}\n".format(Fore.LIGHTBLUE_EX, Style.RESET_ALL))

# config.json doesn't have much of a purpose yet, if it fails to load
# you can manually enter your account equity.
try:
    config = open("{}\\config.json".format(os.getcwd()))
    config = json.load(config)
    equityUSD = config["equityUSD"]
except Exception as e:
    print("{}Failed to load config.json\n{}{}".format(Fore.RED, e, Style.RESET_ALL))
    equityUSD = float(input("Enter account equity manually: "))

equityUSD = config["equityUSD"]
ticker = input("Ticker: ").upper()
side = input("Side (long/short): ").upper()
leverage = int(input("Leverage: "))
riskPercent = float(input("Percentage of account to risk: "))
orderRange = [float(input("Start Price: ")), float(input("End Price: "))]
stopLoss = float(input("Stop-Loss Price: "))
numOfOrders = int(input("Total number of orders to generate: "))

# FOR TESTING PURPOSES
# equityUSD = config["equityUSD"]
# ticker = "BTCUSD"
# side = "short".upper()
# leverage = 25
# riskPercent = 2
# orderRange = [9562.5, 9602.5]
# stopLoss = 9625
# numOfOrders = 3

position = calculatePosition(equityUSD, ticker, side, leverage, riskPercent, orderRange, stopLoss, numOfOrders)

print()
print("{}Position Details{}".format(Fore.LIGHTBLUE_EX, Style.RESET_ALL))
print("You are risking {}% of your account".format(riskPercent))
print("You will risk {}BTC / {}USD if stop gets hit".format(position["risk"], position["risk"] * position["averageEntryPrice"]))
print("Total contracts to be placed: {}".format(position["totalContracts"]))
print("Max Leverage: {}".format(position["maxLeverage"]))
print("Orders:")
[print("  Price: {} Qty: {}".format(i["price"], i["qty"])) for i in position["orders"]]
exit()