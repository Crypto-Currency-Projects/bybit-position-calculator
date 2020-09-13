export default {
  install (Vue, defaultOptions = {}) {
    Vue.prototype.$bybitUSDT = new Vue({
      data: {
        // TODO: finish this!!
        /* tieredMargin: {
          tier: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
          contractValue: [1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000],
          maintenanceMarginRate: [0.0050, 0.0100, 0.0150, 0.0200, 0.0250, 0.0300, 0.0350, 0.0400, 0.0450, 0.0500],
          initialMarginRate: [0.0100, 0.0150, 0.0200, 0.0250, 0.0300, 0.0350, 0.0400, 0.0450, 0.0500, 0.0550],
          maxLeverage: [100.00, 66.67, 50.00, 40.00, 33.33, 28.57, 25.00, 22.22, 20.00, 18.18],
        }, */
      },
      methods: {
        unrealizedPL (side, contracts, entryPrice, closePrice) {
          if (side === 'LONG') { return contracts * (closePrice - entryPrice) } else { return contracts * (entryPrice - closePrice) }
        },
        initialMargin (contractSize, entryPrice, leverage) {
          return (contractSize * entryPrice) / leverage
        },
        initialMarginRate (leverage) {
          return 1 / leverage
        },
        maintenanceMarginRate (/* contracts, averagePrice */) {
          // TODO: does not support tiered margin
          return 0.005
        },
        liqPrice (side, entryPrice, leverage) {
          const imr = this.initialMarginRate(leverage)
          const mmr = this.maintenanceMarginRate()
          if (side === 'LONG') { return entryPrice * (1 - imr + mmr) } else { return entryPrice * (1 + imr - mmr) }
        }
      }
    })
  }
}
