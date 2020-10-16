import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

const opts = {
  theme: {
    dark: {
      primary: '#18191F',
      secondary: '#FFB11A',
      accent: '#303036'
    }
  }
}

export default new Vuetify(opts)
