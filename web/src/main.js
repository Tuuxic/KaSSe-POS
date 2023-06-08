import Vue from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import {BootstrapVue, BootstrapVueIcons} from "bootstrap-vue"
import VueCookies from 'vue-cookies'

import {library} from '@fortawesome/fontawesome-svg-core'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faPlus, faMinus, faChevronLeft, faTimes, faCheck, faHandHoldingUsd, faUser, faBackspace, faHeart} from '@fortawesome/free-solid-svg-icons'
import {faHeart as farHeart} from '@fortawesome/free-regular-svg-icons'
library.add(faPlus, faMinus, faChevronLeft, faTimes, faCheck, faHandHoldingUsd, faUser, faBackspace, faHeart, farHeart)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VueCookies, { expires: '30d', secure: true})

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
