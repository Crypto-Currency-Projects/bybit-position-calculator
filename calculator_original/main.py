from colorama import Fore, Style
from calculator import calculatePosition
import json
import os

# allows for color when launched through cmd.exe
os.system("color 0")

print("\n{}Bybit Position Calculator{}\n".format(Fore.LIGHTBLUE_EX, Style.RESET_ALL))

try:
    config = open("{}\\config.json".format(os.getcwd()))
    config = json.load(config)
except Exception as e:
    raise Exception("{}Failed to load config.json\n{}".format(Fore.RED, e))

# print("Accounts:")
# [print("  {}: {}".format(i, config["Accounts"][i]["accountEquity"])) for i in config["Accounts"]]
# print()
# 
# if len(config["Accounts"]) > 1:
#     profile = input("Select profile: ").lower().capitalize()
# else:
#     profile = config["Accounts"][iter(config["Accounts"])]
# print("Selected Profile: {}".format(profile))

print("{}Enter Position Values{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
ticker = input("Ticker (ex. BTCUSD): ").upper()
side = input("Position Type (Long/Short): ").upper()
riskPercent = float(input("Percentage of account to risk: "))
orderRange = [float(input("Start Price: ")), float(input("End Price: "))]
stopLoss = float(input("Stop-Loss Price: "))
numOfOrders = int(input("Total number of orders to generate: "))


position = calculatePosition(config["accountEquityUSD"], ticker, side, riskPercent, orderRange, stopLoss, numOfOrders)

print("\n")
print("{}Position{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
print("  Max Leverage: {}x".format(position["maxLeverage"]))
print("  Average Entry Price: {}".format(position["averageEntryPrice"]))
print("  Distance to Stop: {}, {:.2f}%".format(abs(position["averageEntryPrice"] - stopLoss), abs(position["averageEntryPrice"] - stopLoss) / stopLoss))
print("  Total Qty: {}".format(position["qty"]))
print("  Estimated Liq Price: {}".format(position["liqPrice"]))
print("  {}Orders{}".format(Fore.LIGHTCYAN_EX, Style.RESET_ALL))
[print("    Price: {} Qty: {}".format(i["price"], i["qty"])) for i in position["orders"]]
exit()
