export default {
  install (Vue, defaultOptions = {}) {
    Vue.prototype.$python = new Vue({
      methods: {
        range (size, startAt = 0) {
          return [...Array(size).keys()].map(i => i + startAt)
        },
        sum (x) {
          return x.reduce((a, b) => a + b, 0)
        }
      }
    })
  }
}
