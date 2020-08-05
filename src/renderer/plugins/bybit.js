export default {
  install(Vue, defaultOptions = {}) {
    Vue.prototype.$bybitInverse = new Vue({
      methods: {
        unrealizedPL(side, contracts, entryPrice, closePrice) {
          if (side == 'LONG') {
            return contracts * ((1 / entryPrice) - (1 / closePrice));
          }
          return contracts * ((1 / closePrice) - (1 / entryPrice));
        },
        maintenanceMarginRate(ticker) {
          return {
            BTCUSD: 0.005,
            ETHUSD: 0.01,
            EOSUSD: 0.01,
            XRPUSD: 0.01,
          }[ticker];
        },
        liqPrice(side, ticker, leverage, averagePrice) {
          const mmr = this.maintenanceMarginRate(ticker);
          if (side == 'LONG') {
            return (averagePrice * leverage) / (leverage + 1 - (mmr * leverage));
          } else {
            return (averagePrice * leverage) / (leverage - 1 + (mmr * leverage));
          }
        },
      },
    });
  },
};
