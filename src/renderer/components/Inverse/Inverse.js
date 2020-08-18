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
      const orderPrices = this.$python.range(this.orders).map((x) => { return orderRange[0] + (interval * x) })
      const averagePrice = this.$python.sum(orderPrices) / orderPrices.length;
      const riskAmount = (this.balance * this.risk) / 100;
      const riskAmountBase = (1 / averagePrice) * riskAmount;

      // Calculate the maximum leverage
      var leverage = 1;
      var liqPrice;
      while (true) {
        liqPrice = this.$bybitInverse.liqPrice(this.side, this.symbol, leverage, averagePrice);
        if (this.side === 'LONG' && liqPrice > this.stop || this.side === 'SHORT' && liqPrice < this.stop) {
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

      // Calculate number of contracts
      var contracts = this.orders;
      const step = this.orders;
      var unrealizedPL;
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
      const orders = orderPrices.map((price) => { return { price, qty: contracts / this.orders }; })

      // Recalculate liqPrice and risk
      liqPrice = this.$bybitInverse.liqPrice(this.side, this.symbol, leverage, averagePrice);
      unrealizedPL = Math.abs(this.$bybitInverse.unrealizedPL(this.side, contracts, averagePrice, this.stop) * averagePrice);

      this.out = {
        averagePrice,
        leverage,
        liqPrice,
        orders,
        risk: unrealizedPL,
        riskPercent: ((100 * unrealizedPL) / this.balance),
        totalContracts: contracts
      };

      console.log(this.out);
    },
  },
};