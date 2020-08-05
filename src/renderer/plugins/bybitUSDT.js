export default {
  install(Vue, defaultOptions = {}) {
    Vue.prototype.$bybitUSDT = new Vue({
      data: {
        tieredMargin: {
          tier: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
          contractValue: [1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000],
          maintenanceMarginRate: [0.0050, 0.0100, 0.0150, 0.0200, 0.0250, 0.0300, 0.0350, 0.0400, 0.0450, 0.0500],
          initialMarginRate: [0.0100, 0.0150, 0.0200, 0.0250, 0.0300, 0.0350, 0.0400, 0.0450, 0.0500, 0.0550],
          maxLeverage: [100.00, 66.67, 50.00, 40.00, 33.33, 28.57, 25.00, 22.22, 20.00, 18.18],
        },
      },
      methods: {
        unrealizedPL(side, contracts, entryPrice, closePrice) {
          if (side === 'LONG') {
            return contracts * (closePrice - entryPrice);
          }
          return contracts * (entryPrice - closePrice);
        },
        initialMargin(contractSize, entryPrice, leverage) {
          return (contractSize * entryPrice) / leverage;
        },
        initialMarginRate(contracts, averagePrice) {
          var contractValue = contracts * averagePrice;
          for (var x of this.$python.range(10)) {
            if (contractValue < this.tieredMargin.contractValue[0]) {
              return this.tieredMargin.initialMarginRate[0];
            } else if (this.tieredMargin.contractValue[x] > contractValue) {
              return this.tieredMargin.initialMarginRate[x - 1]
            }
          }
        },
        maintenanceMarginRate(contracts, averagePrice) {
          var contractValue = contracts * averagePrice;
          for (var x of this.$python.range(10)) {
            if (contractValue < this.tieredMargin.contractValue[0]) {
              return this.tieredMargin.maintenanceMarginRate[0];
            } else if (this.tieredMargin.contractValue[x] > contractValue) {
              return this.tieredMargin.maintenanceMarginRate[x - 1]
            }
          }
        },
        liqPrice(side, entryPrice, contracts) {
          if (side == 'LONG') {
            return entryPrice * (1 - this.initialMarginRate(contracts, entryPrice) + this.maintenanceMarginRate(contracts, entryPrice)); // - extraMarginAdded / contractSize
          } else {
            return entryPrice * (1 + this.initialMarginRate(contracts, entryPrice) - this.maintenanceMarginRate(contracts, entryPrice)); // + extraMarginAdded / contractSize
          }
        },
      },
    });
  },
};
