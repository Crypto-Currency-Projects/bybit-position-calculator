export default {
  name: 'calculator-usdt',
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
      for (var i in this.$python.range(this.orders)) {
        orderPrices.push(orderRange[0] + (interval * i));
      }
      const averagePrice = this.$python.sum(orderPrices) / orderPrices.length;

      const riskAmount = (this.balance * this.risk) / 100;

      /* Calculate number of contracts
      Number of contracts will keep adding from one until unrealized P/L
      between average entry and stop price match your account risk
      percentage. */
      let contracts = this.orders * 0.001;
      const step = this.orders * 0.001;
      let unrealizedPL;
      while (true) {
        unrealizedPL = Math.abs(this.$bybitUSDT.unrealizedPL(this.side, contracts, averagePrice, this.stop));
        if (unrealizedPL > riskAmount) {
          contracts -= step;
          break;
        } else {
          contracts += step;
        }
      }

      // Calculate maximum leverage
      let leverage = 1;
      let liqPrice;
      while (true) {
        liqPrice = this.$bybitUSDT.liqPrice(this.side, averagePrice, leverage);
        if (this.side === 'LONG' && liqPrice > this.stop || this.side === 'SHORT' && liqPrice < this.stop) {
          leverage -= 1;
          break;
        } else {
          leverage += 1;
          if (leverage > 100) {
            leverage = 100;
            break;
          }
        }
      }

      // Generate Orders
      let orders = [];
      for (const price of orderPrices) {
        orders.push({ price, qty: contracts / this.orders });
      }

      this.out = {
        leverage: leverage,
        liqPrice: liqPrice,
        orders: orders,
        risk: unrealizedPL,
        totalContracts: contracts,
        averagePrice: averagePrice,
      };

      console.log(this.out);
    },
  },
};