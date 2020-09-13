<template>
  <div class="panel" id="usdt">
    <div class="header">USDT Contract</div>
    <div class="body">
      <table>
        <tr>
          <td>Ticker / Side</td>
          <td>
            <span>
              <select v-model="symbol">
                <option value="" disabled hidden>Select Ticker</option>
                <option>BTCUSDT</option>
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
          <td>Account Balance (USDT)</td>
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
  name: 'usdt',
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

      // Calculate number of contracts
      let contracts = this.orders * 0.001
      const step = this.orders * 0.001
      let unrealizedPL
      while (true) {
        unrealizedPL = Math.abs(this.$bybitUSDT.unrealizedPL(this.side, contracts, averagePrice, this.stop))
        if (unrealizedPL > riskAmount) {
          contracts -= step
          break
        } else {
          contracts += step
        }
      }

      // Calculate maximum leverage
      let leverage = 1
      let liqPrice
      while (true) {
        liqPrice = this.$bybitUSDT.liqPrice(this.side, averagePrice, leverage)
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

      // Generate Orders
      const orders = orderPrices.map((price) => { return { price, qty: contracts / this.orders } })

      // Recalculate liqPrice and risk
      liqPrice = this.$bybitUSDT.liqPrice(this.side, averagePrice, leverage)
      unrealizedPL = Math.abs(this.$bybitUSDT.unrealizedPL(this.side, contracts, averagePrice, this.stop))

      this.out = {
        averagePrice: averagePrice,
        leverage: leverage,
        liqPrice: liqPrice,
        orders: orders,
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