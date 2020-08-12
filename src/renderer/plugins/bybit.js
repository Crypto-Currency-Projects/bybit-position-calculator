export default {
  install(Vue, defaultOptions = {}) {
    Vue.prototype.$bybitInverse = new Vue({
      methods: {
        unrealizedPL(side, contracts, entryPrice, closePrice) {
          if (side == 'LONG') { return contracts * ((1 / entryPrice) - (1 / closePrice)); }
          else { return contracts * ((1 / closePrice) - (1 / entryPrice)); }
        },
        maintenanceMarginRate(ticker) {
          // TODO: only base values
          return { BTCUSD: 0.005, ETHUSD: 0.01, EOSUSD: 0.01, XRPUSD: 0.01 }[ticker];
        },
        liqPrice(side, ticker, leverage, entryPrice) {
          // LONG (entryPrice * leverage) / (leverage + 1 - (maintenanceMarginRate * leverage))
          // SHORT (entryPrice * leverage) / (leverage - 1 + (maintenanceMarginRate * leverage))
          const mmr = this.maintenanceMarginRate(ticker);
          const base = (entryPrice * leverage)
          if (side == 'LONG') { return base / (leverage + 1 - (mmr * leverage)); }
          else { return base / (leverage - 1 + (mmr * leverage)); }
        }
      },
    });
  },
};
