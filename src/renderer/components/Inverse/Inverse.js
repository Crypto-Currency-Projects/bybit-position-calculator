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
      orders: 5,
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
      var orderPrices = [];
      for (var i of this.$python.range(this.orders)) { orderPrices.push(orderRange[0] + (interval * i)); }
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