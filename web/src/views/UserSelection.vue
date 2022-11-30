<template>
    <div id="user-selection">
        <b-row class="py-4 px-3 full-height m-0" v-if="active_users != null">
            <b-modal id="payment" hide-header hide-footer>
                <h2 class="text-center text-muted">User</h2>
                <b-form-select size="lg" class="shadow mb-3" v-model="payment_user"
                               :options="paymentUserOptions"></b-form-select>
                <h2 class="text-center text-muted">Amount in €</h2>
                <b-input-group class="shadow mb-3">
                    <b-input-group-prepend>
                        <b-button variant="outline-secondary" @click="payment_amount = Math.max(payment_amount-1, 1)">
                            <font-awesome-icon :icon="['fas','minus']"/>
                        </b-button>
                    </b-input-group-prepend>
                    <b-form-input type="number" v-model="payment_amount" class="text-center" id="payment-amount"
                                  :formatter="formatPayment" lazy-formatter size="lg"/>
                    <b-input-group-append>
                        <b-button variant="outline-secondary">
                            <font-awesome-icon :icon="['fas','plus']" @click="payment_amount++"/>
                        </b-button>
                    </b-input-group-append>
                </b-input-group>
                <h2 class="text-center text-muted">Admin code</h2>
                <div class="text-center">
                    <b-button-group size="md" class="mb-3 d-flex flex-row shadow">
                        <b-button variant="outline-secondary" v-for="number in 10" :key="'number-'+number"
                                  @click="payment_code += number-1">
                            <h3>{{number - 1}}</h3>
                        </b-button>
                        <b-button variant="outline-secondary" @click="payment_code = payment_code.slice(0, -1)">
                            <font-awesome-icon :icon="['fas','backspace']"/>
                        </b-button>
                    </b-button-group>
                </div>
                <h2 class="text-center text-muted">{{payment_code}}</h2>
                <b-button @click="pay" class="shadow" block size="lg" variant="success"
                          :disabled="payment_user == null || payment_code !== '2306'"><h1>Confirm payment</h1>
                </b-button>
            </b-modal>
            <b-col cols="3" class="d-flex flex-column px-0">
                <b-card no-body class="shadow" style="flex-grow: 1">
                    <b-card-body class="d-flex flex-column">
                        <h1 class="logo gradient-text">Kasse</h1>
                        <div class="mb-3">
                            <hr>
                        </div>
                        <b-button pill size="lg" block variant="outline-secondary" class="shadow mb-3"
                                  @click="$router.push('/transaction-list')">
                            Transactions
                        </b-button>

                        <b-button pill size="lg" block variant="outline-secondary" class="shadow mb-3"
                                  @click="key = (key+1) % sorting_keys.length">
                            Sort by: {{sorting_keys[key]}}
                        </b-button>

                        <b-button pill size="lg" block variant="outline-secondary" class="shadow mb-3"
                                  @click="showPayment">
                            Add payment
                        </b-button>

                    </b-card-body>
                </b-card>
            </b-col>
            <b-col class="d-flex flex-column">
                <b-row>
                    <b-col v-for="user in sortedActiveUsers" :key="'active-' + user.id" cols="4"
                           class="mb-3 pl-3 pr-0 text-muted">
                        <b-card no-body class="shadow" @click="selectUser(user)">
                            <b-card-body class="p-2">
                                <h1 class="room-number"><b>{{user.room}}</b></h1>
                                <div class="user-foreground text-left pl-2">
                                    <h2>{{user.name}}</h2>
                                    <h3 :style="{color: balanceColor(user.balance)}">
                                        {{formatPrice(user.balance)}}</h3>
                                </div>
                            </b-card-body>
                        </b-card>
                    </b-col>
                </b-row>
                <b-modal id="more-users" hide-header hide-footer body-class="pb-0">
                    <b-card v-for="user in inactive_users" :key="'inactive-' + user.id" class="shadow mb-3 text-muted"
                            @click="selectUser(user)">
                        <b-row>
                            <b-col>
                                <h2>{{user.name}}</h2>
                            </b-col>
                            <b-col><h2 :style="{color: balanceColor(user.balance), float: 'right'}">
                                {{formatPrice(user.balance)}}</h2>
                            </b-col>
                        </b-row>
                    </b-card>
                </b-modal>
                <b-row style="flex-grow: 1">
                    <b-col class="pr-0 text-muted" style="height: 100%">
                        <b-card no-body class="shadow" style="height: 100%" @click="$bvModal.show('more-users')">
                            <b-card-body class="p-2 d-flex flex-column">
                                <h2 class="my-auto">More users</h2>
                            </b-card-body>
                        </b-card>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import axios from "axios";

    //const interpolate = require('color-interpolate')

    export default {
        name: 'user-selection',
        created() {
            this.getUsers()
            this.$parent.CDPclock()
        },
        data() {
            return {
                active_users: [],
                inactive_users: [],
                sorting_keys: ['Room', 'Balance'],
                key: 0,
                payment_user: null,
                payment_amount: 30,
                payment_code: ''
            }
        },
        computed: {
            sortedActiveUsers() {
                return this.active_users.sort((a, b) => {
                    if (this.key === 0)
                        return a.room - b.room
                    else
                        return a.balance - b.balance
                })
            },
            paymentUserOptions() {
                let active = []
                this.active_users.forEach((user) => {
                    active.push({
                        value: user,
                        text: user.name + (user.hasOwnProperty('room') ? ' C3' + user.room : '') // eslint-disable-line
                    })
                })
                let inactive = []
                this.inactive_users.forEach((user) => {
                    inactive.push({value: user, text: user.name})
                })
                return [{label: 'Active users', options: active}, {label: 'Inactive users', options: inactive}]
            }
        },
        methods: {
            selectUser(user) {
                this.$parent.selected_user = user
                this.$parent.CDPmessage({
                    top: {center: user.name},
                    bottom: {center: (user.balance / 100).toFixed(2)}}, 2)
                this.$router.push('item-selection')
            },
            formatPrice(value) {
                return (value / 100).toFixed(2) + '€'
            },
            formatPayment(value) {
                return Math.max(value, 1)
            },
            balanceColor(balance) {
                //let map = interpolate(['green', 'orange', 'red'])
                //return map(Math.max((-balance / 100) / 30, 0))
                if (balance > 0) {return "green";}
                if (balance == 0) {return "gray"}
                if (balance < 0 && balance > -3000) {return "red"}
                if (balance <= -30) {return "maroon"}
                return "white"
            },
            getUsers() {
                axios.get(this.$parent.host + '/users').then((res) => {
                    res.data.users.forEach((user) => {
                        if (user.id in res.data.active_users) {
                            this.active_users.push(user)
                        } else {
                            this.inactive_users.push(user)
                        }
                    })

                }).catch((error) => {
                    console.error(error)
                })
            },
            showPayment() {
                this.payment_user = null
                this.payment_amount = 30
                this.payment_code = ''
                this.$bvModal.show('payment')
            },
            pay() {
                this.payment_code = ''
                let transaction = {
                    'user': this.payment_user,
                    'payment': true,
                    'impact': this.payment_amount * 100
                }
                axios.post(this.$parent.host + '/transactions/add', transaction).then(() => {
                    this.$parent.CDPmessage({top: {center: 'Payment added!'}}, 10)
                    this.$bvModal.hide('payment')
                }).catch((error) => {
                    console.log(error)
                    this.$bvModal.hide('payment')
                })
            }
        }
    }
</script>

<style scoped>
    .full-height {
        height: 100vh;
        width: 100vw;
        overflow: hidden;
    }

    .logo {
        font-size: 62px;
        margin-bottom: -6px;
    }

    .gradient-text {
        background: -webkit-linear-gradient(45deg, #2537AF, #70E5CB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .room-number {
        position: absolute;
        font-size: 80pt;
        right: 10px;
        top: -15px;
        z-index: 0;
        color: gray;
    }

    .user-foreground {
        position: relative;
        z-index: 1;
    }
</style>