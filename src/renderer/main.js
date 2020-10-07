import Vue from 'vue'
import axios from 'axios'

import App from './App'

import bybit from './plugins/bybit'
import bybitUSDT from './plugins/bybitUSDT'
import python from './plugins/python'

Vue.use(bybit)
Vue.use(bybitUSDT)
Vue.use(python)

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  components: { App },
  template: '<App/>'
}).$mount('#app')
