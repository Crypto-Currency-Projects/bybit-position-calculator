<template>
  <v-container>
    <v-card>
      <v-card-title>Position Calculator</v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <v-text-field
              label="Account Balance (USD)"
              v-model.number="balance"
              type="number"
              prefix="$"
              outlined
              dense
            ></v-text-field>
            <v-row>
              <v-col>
                <v-select
                  label="Ticker"
                  :items="tickers"
                  v-model="ticker"
                  outlined
                  dense
                ></v-select>
              </v-col>
              <v-col>
                <v-text-field
                  label="Risk (%)"
                  v-model.number="risk"
                  hint="The percentage of your account expected to be lost if stop is hit"
                  type="number"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  label="Number of Orders"
                  v-model.number="orders"
                  type="number"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-text-field
              label="Start Price"
              v-model.number="start"
              hint="Specify the range to long/short, start and end prices are interchnageable"
              type="number"
              outlined
              dense
            ></v-text-field>
            <v-text-field
              label="End Price"
              v-model.number="end"
              hint="Specify the range to long/short, start and end prices are interchnageable"
              type="number"
              outlined
              dense
            ></v-text-field>
            <v-text-field
              label="Stop Loss"
              v-model.number="stop"
              type="number"
              outlined
              dense
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row
          align="center"
          justify="space-around"
        >
          <v-btn
            color="green"
            v-on:click="calculate('LONG')"
          >LONG</v-btn>
          <v-btn
            color="red"
            v-on:click="calculate('SHORT')"
          >SHORT</v-btn>
        </v-row>
        <v-row>
          <v-col>
            <v-simple-table dense>
              <thead>
                <tr>
                  <th
                    class="text-left"
                    colspan="2"
                  >Position Information</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Leverage</td>
                  <td>{{ output.leverage }}x</td>
                </tr>
                <tr>
                  <td>Risk</td>
                  <td>{{ output.risk }} USD</td>
                </tr>
                <tr>
                  <td>Average Entry Price</td>
                  <td>{{ output.averagePrice }}</td>
                </tr>
                <tr>
                  <td>Total Contracts</td>
                  <td>{{ output.contracts }}</td>
                </tr>
                <tr>
                  <td>Estimated Liq Price</td>
                  <td>{{ output.liqPrice }}</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-col>
          <v-col>
            <v-simple-table dense>
              <thead>
                <tr>
                  <th class="text-left">
                    Price
                  </th>
                  <th class="text-left">
                    Qty
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="x in output.orders"
                  :key="x.price"
                >
                  <td>{{ x.price }}</td>
                  <td>{{ x.qty }}</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'position-calculator',
  data () {
    return {
      balance: 420.69,
      ticker: 'BTCUSDT',
      tickers: ['BTCUSD', 'ETHUSD', 'XRPUSD', 'EOSUSD', 'BTCUSDT'],
      risk: 1,
      side: '',
      start: 0,
      end: 0,
      stop: 0,
      orders: 5,
      output: {
        averagePrice: 0,
        contracts: 0,
        leverage: 0,
        liqPrice: 0,
        orders: [],
        risk: 0,
        table: {
          headers: [
            { text: 'Price', align: 'start', value: 'price' },
            { text: 'Qty', value: 'qty' }
          ]
        }
      }
    }
  },
  methods: {
    calculate (side) {
      // Error messages
      var message = ''
      if (this.balance <= 0) { message = 'Your account must have money in it!' }
      if (this.ticker === '') { message = 'No ticker selected' }
      if (side === 'LONG' && this.stop >= Math.min(this.start, this.end)) { message = 'Stop cannot be greater than or equal to the range mininum.' }
      if (side === 'SHORT' && this.stop <= Math.max(this.start, this.end)) { message = 'Stop cannot be less than or equal to the range maximum.' }
      if (this.orders < 2) { message = 'Number of Orders cannot be less than 2' }
      if (message !== '') {
        this.$notify({
          group: 'main',
          type: 'error',
          title: 'Error',
          text: message
        })
        return
      }

      if (this.risk > 2) {
        this.$notify({
          group: 'main',
          type: 'info',
          title: 'Risk warning',
          text: 'It is not recommended to risk more than 2% of your account on a single trade.'
        })
      }
      if (this.ticker === 'BTCUSDT') {
        this.positionUSDT(side)
      } else {
        this.positionInverse(side)
      }
    },
    positionInverse (side) {
      const orderRange = (this.start < this.end) ? [this.start, this.end] : [this.end, this.start]
      const interval = (orderRange[1] - orderRange[0]) / (this.orders - 1)
      const orderPrices = this.$python.range(this.orders).map((x) => { return orderRange[0] + (interval * x) })
      const averagePrice = this.$python.sum(orderPrices) / orderPrices.length
      const riskAmount = (this.balance * this.risk) / 100
      const riskAmountBase = (1 / averagePrice) * riskAmount

      // Calculate maximum leverage
      var leverage = 1
      var liqPrice
      var maxLeverage = (this.ticker === 'BTCUSD') ? 100 : 50
      while (true) {
        liqPrice = this.$bybitInverse.liqPrice(side, this.ticker, leverage, averagePrice)
        if (side === 'LONG' && liqPrice > this.stop) {
          leverage -= 3
          break
        } else if (side === 'SHORT' && liqPrice < this.stop) {
          leverage -= 3
          break
        } else {
          leverage += 1
          if (leverage > maxLeverage) {
            leverage = maxLeverage
            break
          }
        }
      }

      // Calculate number of contracts
      var contracts = this.orders
      const step = this.orders
      var unrealizedPL
      while (true) {
        unrealizedPL = Math.abs(this.$bybitInverse.unrealizedPL(side, contracts, averagePrice, this.stop))
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
      liqPrice = this.$bybitInverse.liqPrice(side, this.ticker, leverage, averagePrice)
      unrealizedPL = Math.abs(this.$bybitInverse.unrealizedPL(side, contracts, averagePrice, this.stop) * averagePrice)

      this.output = {
        averagePrice,
        leverage,
        liqPrice,
        orders,
        risk: unrealizedPL,
        riskPercent: ((100 * unrealizedPL) / this.balance),
        contracts: contracts
      }

      console.log(this.output)
    },
    positionUSDT (side) {
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
        unrealizedPL = Math.abs(this.$bybitUSDT.unrealizedPL(side, contracts, averagePrice, this.stop))
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
      let maxLeverage = 100
      while (true) {
        liqPrice = this.$bybitUSDT.liqPrice(side, averagePrice, leverage)
        if (side === 'LONG' && liqPrice > this.stop) {
          leverage -= 3
          break
        } else if (side === 'SHORT' && liqPrice < this.stop) {
          leverage -= 3
          break
        } else {
          leverage += 1
          if (leverage > maxLeverage) {
            leverage = maxLeverage
            break
          }
        }
      }

      // Generate Orders
      const orders = orderPrices.map((price) => { return { price, qty: contracts / this.orders } })

      // Recalculate liqPrice and risk
      liqPrice = this.$bybitUSDT.liqPrice(side, averagePrice, leverage)
      unrealizedPL = Math.abs(this.$bybitUSDT.unrealizedPL(side, contracts, averagePrice, this.stop))

      this.output = {
        averagePrice: averagePrice,
        leverage: leverage,
        liqPrice: liqPrice,
        orders: orders,
        risk: unrealizedPL,
        riskPercent: ((100 * unrealizedPL) / this.balance),
        contracts: contracts
      }

      console.log(this.output)
    }
  }
}
</script>

<style lang="scss"></style>