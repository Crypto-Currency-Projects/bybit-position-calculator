<template>
  <div class="container">
    <table>
      <tr>
        <th>Ticker</th>
        <th>
          <select v-model="symbol">
            <option selected>BTCUSD</option>
            <option>ETHUSD</option>
            <option>XRPUSD</option>
            <option>EOSUSD</option>
          </select>
        </th>
      </tr>
      <tr>
        <th>Long / Short</th>
        <th>
          <select v-model="side">
            <option selected>LONG</option>
            <option>SHORT</option>
          </select>
        </th>
      </tr>
      <tr>
        <th>Account Balance</th>
        <th><input class="number" type="number" v-model.number="balance"></th>
      </tr>
      <tr>
        <th>Risk (%)</th>
        <th><input class="number" type="number" v-model.number="risk"></th>
      </tr>
      <tr>
        <th>Start Price</th>
        <th><input class="number" type="number" v-model.number="start"></th>
      </tr>
      <tr>
        <th>End Price</th>
        <th><input class="number" type="number" v-model.number="end"></th>
      </tr>
      <tr>
        <th>Stop Loss Price</th>
        <th><input class="number" type="number" v-model.number="stop"></th>
      </tr>
      <tr>
        <th>Number of Orders</th>
        <th><input class="number" type="number" v-model.number="orders"></th>
      </tr>
      <tr>
        <th></th>
        <th>
          <button v-on:click="calculatePosition()">Submit</button>
        </th>
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
      orders: 0
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

      var ret = {
        leverage: leverage,
        liqPrice: liqPrice,
        orders: orders,
        risk: unrealizedPL,
        totalContracts: contracts,
        averagePrice: averagePrice
      }
      console.log(ret)
    }
  }
}
</script>
<style>

</style>