import Vue from 'vue'
import VueRouter from 'vue-router'
import UserSelection from '../views/UserSelection.vue'
import ItemSelection from "../views/ItemSelection";
import TransactionList from "../views/TransactionList";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'user-selection',
        component: UserSelection
    },
    {
        path: '/item-selection',
        name: 'item-selection',
        component: ItemSelection
    },
    {
        path: '/transaction-list',
        name: 'transaction-list',
        component: TransactionList
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
