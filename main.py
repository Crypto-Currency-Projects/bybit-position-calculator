from position_calculator import positionCalculator
import eel

eel.init("web")

@eel.expose
def calculate(balance, symbol, side, risk, orderRange, stopLoss, numberOfOrders):
    balance = float(balance)
    risk = float(risk)
    orderRange = [float(i) for i in orderRange]
    stopLoss = float(stopLoss)
    numberOfOrders = int(numberOfOrders)
    x = positionCalculator(balance, symbol, side, risk, orderRange, stopLoss, numberOfOrders)
    return x

eel.start("index.html")
