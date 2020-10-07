<template>
  <div class="panel" id="inverse">
    <div class="header">Inverse Contract</div>
    <div class="body">
      <table>
        <tr>
          <td>Ticker / Side</td>
          <td>
            <span>
              <select v-model="symbol">
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
            <input type="button" @click="calculatePosition()" value="Submit">
          </td>
        </tr>
      </table>
      <table class="bordered">
        <tr><th class="title" colspan="2">Position Information</th></tr>
        <tr>
          <td colspan="2">
            <table class="bordered">
              <tr class="underline">
                <th>#</th>
                <th class="number">Price</th>
                <th class="number">Qty</th>
              </tr>
              <tr v-for="(order, num) in out.orders">
                <td>{{ num + 1 }}</td>
                <td class="number">{{ order.price }}</td>
                <td class="number">{{ order.qty }}</td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td>Recommended Leverage</td>
          <td class="number">{{ out.leverage }}x</td>
        </tr>
        <tr>
          <td>Risk</td>
          <td class="number">USD {{ out.risk }} ({{ Math.round(out.riskPercent * 100) / 100 }}%)</td>
        </tr>
        <tr>
          <td>Total Contracts</td>
          <td class="number">{{ out.totalContracts }}</td>
        </tr>
        <tr>
          <td>Average Entry Price</td>
          <td class="number">{{ out.averagePrice }}</td>
        </tr>
        <tr>
          <td>Estimated Liq Price</td>
          <td class="number">{{ out.liqPrice }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'inverse',
  data () {
    return {
      symbol: '',
      side: '',
      balance: 0,
      risk: 0,
      start: 0,
      end: 0,
      stop: 0,
      orders: 5,
      out: {
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
    calculatePosition () {
      const orderRange = (this.start < this.end) ? [this.start, this.end] : [this.end, this.start]
      const interval = (orderRange[1] - orderRange[0]) / (this.orders - 1)
      const orderPrices = this.$python.range(this.orders).map((x) => { return orderRange[0] + (interval * x) })
      const averagePrice = this.$python.sum(orderPrices) / orderPrices.length
      const riskAmount = (this.balance * this.risk) / 100
      const riskAmountBase = (1 / averagePrice) * riskAmount

      // Calculate the maximum leverage
      var leverage = 1
      var liqPrice
      while (true) {
        liqPrice = this.$bybitInverse.liqPrice(this.side, this.symbol, leverage, averagePrice)
        if (this.side === 'LONG' && liqPrice > this.stop) {
          leverage -= 3
          break
        } else if (this.side === 'SHORT' && liqPrice < this.stop) {
          leverage -= 3
          break
        } else {
          leverage += 1
          if (leverage > 100) {
            leverage = 100
            break
          }
        }
      }

      // Calculate number of contracts
      var contracts = this.orders
      const step = this.orders
      var unrealizedPL
      while (true) {
        unrealizedPL = Math.abs(this.$bybitInverse.unrealizedPL(this.side, contracts, averagePrice, this.stop))
        if (unrealizedPL > riskAmountBase) {
          contracts -= step
          break
        } else {
          contracts += step
        }
      }

      // Generate Orders
      const orders = orderPrices.map((price) => { return { price, qty: contracts / this.orders } })

      // Recalculate liqPrice and risk
      liqPrice = this.$bybitInverse.liqPrice(this.side, this.symbol, leverage, averagePrice)
      unrealizedPL = Math.abs(this.$bybitInverse.unrealizedPL(this.side, contracts, averagePrice, this.stop) * averagePrice)

      this.out = {
        averagePrice,
        leverage,
        liqPrice,
        orders,
        risk: unrealizedPL,
        riskPercent: ((100 * unrealizedPL) / this.balance),
        totalContracts: contracts
      }

      console.log(this.out)
    }
  }
}
</script>

<style>

</style>
