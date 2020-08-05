<template>
  <div class="container">
    <table>
      <tr><th class="title" colspan="2">Inverse Contract</th></tr>
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
            <tr v-for="(order, num) in out['orders']">
              <td>{{ num + 1 }}</td>
              <td>Price: {{ order.price }}</td>
              <td>Qty: {{ order.qty }}</td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td>Leverage</td>
        <td class="number">{{ out["leverage"] }}x</td>
      </tr>
      <tr>
        <td>Total Contracts</td>
        <td class="number">{{ out["totalContracts"] }}</td>
      </tr>
      <tr>
        <td>Average Entry Price</td>
        <td class="number">{{ out["averagePrice"] }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  name: 'calculator-inverse',
  data() {
    return {
      symbol: '',
      side: '',
      balance: 0,
      risk: 0,
      start: 0,
      end: 0,
      stop: 0,
      orders: 0,
      out: {
        leverage: 0,
        liqPrice: 0,
        orders: [],
        risk: 0,
        totalContracts: 0,
        averagePrice: 0,
      },
    };
  },
  methods: {
    calculatePosition() {
      const orderRange = (this.start < this.end) ? [this.start, this.end] : [this.end, this.start];
      const interval = (orderRange[1] - orderRange[0]) / (this.orders - 1);
      const orderPrices = [];
      for (const i in this.$python.range(this.orders)) {
        orderPrices.push(orderRange[0] + (interval * i));
      }
      const averagePrice = this.$python.sum(orderPrices) / orderPrices.length;

      const riskAmount = (this.balance * this.risk) / 100;
      const riskAmountBase = (1 / averagePrice) * riskAmount;

      // Calculate the maximum leverage
      let leverage = 1;
      let liqPrice;
      while (true) {
        liqPrice = this.$bybitInverse.liqPrice(this.side, this.symbol, leverage, averagePrice);
        if (this.side === 'LONG' && liqPrice > this.stop) {
          leverage -= 2;
          break;
        } else if (this.side === 'SHORT' && liqPrice < this.stop) {
          leverage -= 2;
          break;
        } else {
          leverage += 1;
          if (leverage > 100) {
            leverage = 100;
            break;
          }
        }
      }
      if (leverage > 100) {
        leverage = 100;
      } else {
        leverage -= 2;
      }

      /* Calculate number of contracts
      Number of contracts will keep adding from one until unrealized P/L
      between average entry and stop price match your account risk
      percentage. */
      let contracts = this.orders;
      const step = this.orders;
      let unrealizedPL;
      while (true) {
        unrealizedPL = Math.abs(this.$bybitInverse.unrealizedPL(this.side, contracts, averagePrice, this.stop));
        if (unrealizedPL > riskAmountBase) {
          contracts -= step;
          break;
        } else {
          contracts += step;
        }
      }

      // Generate Orders
      const orders = [];
      for (const price of orderPrices) {
        orders.push({ price, qty: contracts / this.orders });
      }

      this.out = {
        leverage,
        liqPrice,
        orders,
        risk: unrealizedPL,
        totalContracts: contracts,
        averagePrice,
      };

      console.log(this.out);
    },
  },
};
</script>
<style>
.container {
  display: inline-flex;
}
</style>