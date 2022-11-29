import Vue from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import {BootstrapVue} from "bootstrap-vue"

import VueSocketIOExt from 'vue-socket.io-extended';
import io from 'socket.io-client';

import {library} from '@fortawesome/fontawesome-svg-core'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faPlus, faMinus, faChevronLeft, faTimes, faCheck, faHandHoldingUsd, faUser, faBackspace, faHeart} from '@fortawesome/free-solid-svg-icons'
import {faHeart as farHeart} from '@fortawesome/free-regular-svg-icons'
library.add(faPlus, faMinus, faChevronLeft, faTimes, faCheck, faHandHoldingUsd, faUser, faBackspace, faHeart, farHeart)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

Vue.use(BootstrapVue)

const socket = io('http://localhost:5000')
Vue.use(VueSocketIOExt, socket)

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
