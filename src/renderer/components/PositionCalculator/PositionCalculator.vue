<template>
  <div class="container">
    <table>
      <tr><th class="title" colspan="2">Inverse Contract</th></tr>
      <tr>
        <td>Ticker / Side</td>
        <td>
          <span>
            <select v-model="symbol" >
              <option value="" disabled hidden>Select Ticker</option>
              <option>BTCUSD</option>
              <option>ETHUSD</option>
              <option>XRPUSD</option>
              <option>EOSUSD</option>
            </select>
          </span>
          <span>
            <select v-model="side">
              <option value="" disabled hidden>Side</option>
              <option>LONG</option>
              <option>SHORT</option>
            </select>
          </span>
        </td>
      </tr>
      <tr>
        <td>Account Balance (USD)</td>
        <td><input class="number" type="number" v-model.number="balance"></td>
      </tr>
      <tr>
        <td>Risk (%)</td>
        <td><input class="number" type="number" v-model.number="risk"></td>
      </tr>
      <tr>
        <td>Start Price</td>
        <td><input class="number" type="number" v-model.number="start"></td>
      </tr>
      <tr>
        <td>End Price</td>
        <td><input class="number" type="number" v-model.number="end"></td>
      </tr>
      <tr>
        <td>Stop Loss Price</td>
        <td><input class="number" type="number" v-model.number="stop"></td>
      </tr>
      <tr>
        <td>Number of Orders</td>
        <td><input class="number" type="number" v-model.number="orders"></td>
      </tr>
      <tr>
        <td></td>
        <td>
          <button v-on:click="calculatePosition()">Submit</button>
        </td>
      </tr>
    </table>
    <table>
      <tr><th class="title" colspan="2">Position Information</th></tr>
      <tr>
        <td colspan="2">
          <table>
            <tr><th class="title" colspan="3">Invidual Orders</th></tr>
            <tr><td colspan="3">These orders are to be placed in bybit; dont forget about your stop loss!</td></tr>
            <tr v-for="(order, num) in pc['orders']">
              <td>{{num + 1}}</td>
              <td>Price: {{order.price}}</td>
              <td>Qty: {{order.qty}}</td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td>Leverage</td>
        <td class="number">{{pc["leverage"]}}x</td>
      </tr>
      <tr>
        <td>Total Contracts</td>
        <td class="number">{{pc["totalContracts"]}}</td>
      </tr>
      <tr>
        <td>Average Entry Price</td>
        <td class="number">{{pc["averagePrice"]}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      symbol: '',
      side: '',
      balance: 0,
      risk: 0,
      start: 0,
      end: 0,
      stop: 0,
      orders: 0,
      pc: {
        leverage: 0,
        liqPrice: 0,
        orders: [],
        risk: 0,
        totalContracts: 0,
        averagePrice: 0
      }
    }
  },
  methods: {
    range: function (size, startAt = 0) {
      return [...Array(size).keys()].map(i => i + startAt)
    },
    sum: function (x) {
      var y = 0
      for (var i of x) { y += i }
      return y
    },
    unrealizedPL: function (side, contracts, averagePrice, closePrice) {
      if (side === 'LONG') {
        return contracts * ((1 / averagePrice) - (1 / closePrice))
      } else {
        return contracts * ((1 / closePrice) - (1 / averagePrice))
      }
    },
    maintenanceMarginRate: function (ticker) {
      var rate = { 'BTCUSD': 0.005, 'ETHUSD': 0.01, 'EOSUSD': 0.01, 'XRPUSD': 0.01 }
      return rate[ticker]
    },
    liqPrice: function (side, ticker, leverage, averagePrice) {
      var marginRate = this.maintenanceMarginRate(ticker)
      if (side === 'LONG') {
        return (averagePrice * leverage) / (leverage + 1 - (marginRate * leverage))
      } else {
        return (averagePrice * leverage) / (leverage - 1 + (marginRate * leverage))
      }
    },
    calculatePosition: function () {
      var orderRange = (this.start < this.end) ? [this.start, this.end] : [this.end, this.start]
      var interval = (orderRange[1] - orderRange[0]) / (this.orders - 1)
      var orderPrices = []
      for (var i in this.range(this.orders)) {
        orderPrices.push(orderRange[0] + (interval * i))
      }
      var averagePrice = this.sum(orderPrices) / orderPrices.length

      var riskAmount = (this.balance * this.risk) / 100
      var riskAmountBase = (1 / averagePrice) * riskAmount

      // Calculate the maximum leverage
      var leverage = 1
      var liqPrice
      while (true) {
        liqPrice = this.liqPrice(this.side, this.symbol, leverage, averagePrice)
        if (this.side === 'LONG' && liqPrice > this.stop) {
          break
        } else if (this.side === 'SHORT' && liqPrice < this.stop) {
          break
        } else {
          leverage += 1
          if (leverage > 100) {
            break
          }
        }
      }
      leverage -= 2

      /* Calculate number of contracts
      Number of contracts will keep adding from one until unrealized P/L
      between average entry and stop price match your account risk
      percentage. */
      var contracts = this.orders
      var step = this.orders
      while (true) {
        var unrealizedPL = Math.abs(this.unrealizedPL(this.side, contracts, averagePrice, this.stop))
        if (unrealizedPL > riskAmountBase) {
          contracts -= step
          break
        } else {
          contracts += step
        }
      }

      // Generate Orders
      var orders = []
      for (var price of orderPrices) {
        orders.push({'price': price, 'qty': contracts / this.orders})
      }

      this.pc = {
        active: true,
        leverage: leverage,
        liqPrice: liqPrice,
        orders: orders,
        risk: unrealizedPL,
        totalContracts: contracts,
        averagePrice: averagePrice
      }

      console.log(this.pc)
    }
  }
}
</script>
<style>
.container {
  display: inline-flex;
}
</style>