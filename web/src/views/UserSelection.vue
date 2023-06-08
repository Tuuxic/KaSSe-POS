<template>
    <div id="user-selection">
        <b-navbar toggleable="md" variant="dark" type="dark" :sticky="true" class="shadow">
                <b-navbar-brand href="#" class="logo gradient-text ml-2">Ka$$e</b-navbar-brand>
                <b-navbar-toggle target="nav-collapse">
                    <template #default="{ expanded }">
                        <b-icon v-if="expanded" icon="chevron-bar-up" font-scale="1.75" variant="light"></b-icon>
                        <b-icon v-else icon="chevron-bar-down" font-scale="1.75" variant="light"></b-icon>
                    </template>
                </b-navbar-toggle>
                <b-collapse id="nav-collapse" is-nav>
                    <hr color="white">
                    <b-navbar-nav class="ml-auto">
                        <b-button size="md" variant="outline-secondary" class="text-white shadow m-1"
                                  @click="$router.push('/transaction-list')">
                            Transactions
                        </b-button>
                        
                        <b-button size="md" variant="outline-secondary" class="text-white shadow m-1"
                                  @click="showPayment">
                            Add payment
                        </b-button>

                        <b-button size="md" variant="outline-secondary" class="text-white shadow m-1"
                                  @click="key = (key+1) % sorting_keys.length">
                            Sort by: {{sorting_keys[key]}}
                        </b-button>
                        <div class="navitems-padding"></div>
                    </b-navbar-nav>
                </b-collapse>
        </b-navbar>

        <b-row class="mx-1 my-3">
            <b-col class="d-flex flex-column">
                <b-row class="justify-content-center flex-grow-1">
                    <b-col v-for="user in sortedActiveUsers" :key="'active-' + user.id" md="4"
                           class="user-card mb-3 px-3 text-muted w-100">
                        <b-card no-body class="shadow w-100 " @click="selectUser(user)">
                            <b-card-body class="p-2 d-flex flex-column">
                                <h1 class="room-number"><b>{{user.room}}</b></h1>
                                <div class="user-foreground text-left pl-2">
                                    <h2 class="selection-name-field">{{user.name}}</h2>
                                    <h3 :style="{color: balanceColor(user.balance)}" class="selection-price-field">
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
                <b-row>
                    <b-col class="text-muted">
                        <b-card no-body class="d-flex shadow" @click="$bvModal.show('more-users')">
                            <b-card-body class="d-flex justify-content-center align-items-center">
                                <h2 >More users</h2>
                            </b-card-body>
                        </b-card>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        

        <b-modal v-if="!this.$parent.auth" id="auth" size="xl" hide-header hide-footer no-close-on-backdrop centered>
                <h1 class="header-large text-center text-muted">Authentification</h1>
                <!--
                <div class="text-center">
                    <b-button-group size="sm" class="mb-3 d-flex flex-row shadow">
                        <b-button variant="outline-secondary" v-for="number in 10" :key="'number-'+number"
                                  @click="auth_code += number-1 ; if(auth_code.length > 10) {auth_code = auth_code.substring(0, 20)}">
                            <h3>{{number - 1}}</h3>
                        </b-button>
                        <b-button variant="outline-secondary" @click="auth_code = auth_code.slice(0, -1)">
                            <font-awesome-icon :icon="['fas','backspace']"/>
                        </b-button>
                    </b-button-group>
                </div>
            -->
                <b-form-input id="`type-number`" type="number" class="my-4 d-flex flex-row shadow text-center" 
                    placeholder="Please enter a Code"
                    v-model="auth_code"
                ></b-form-input>
                
                <b-button @click="authenticate" class="shadow" block size="lg" variant="success"
                          :disabled="(auth_code !== auth_number)"><h1>Confirm</h1>
                </b-button>
        </b-modal>



        
            <b-modal id="payment" hide-header hide-footer centered>
                
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
                
                <div class="text-center">
                    <!--
                    <h2 class="text-center text-muted">Admin Code</h2>
                    <b-button-group size="sm" class="mb-3 d-flex flex-row shadow">
                        <b-button variant="outline-secondary" v-for="number in 10" :key="'number-'+number"
                                  @click="payment_code += number-1">
                            <h3>{{number - 1}}</h3>
                        </b-button>
                        <b-button variant="outline-secondary" @click="payment_code = payment_code.slice(0, -1)">
                            <font-awesome-icon :icon="['fas','backspace']"/>
                        </b-button>
                    </b-button-group>
                    -->
                    <b-form-input id="`type-number`" type="number" class="my-3 d-flex flex-row shadow text-center" v-model="payment_code" placeholder="Admin Code"></b-form-input>
                </div>
                <b-button @click="pay" class="shadow" block size="lg" variant="success"
                          :disabled="(payment_user == null || payment_code !== this.$parent.admin_code)"><h1>Confirm payment</h1>
                </b-button>
              
            </b-modal>
        
    </div>
</template>

<script>
    import axios from "axios";

    //const interpolate = require('color-interpolate')

    export default {
        name: 'user-selection',
        created() {
            this.getUsers()
        },
        mounted() {

            if (this.$cookies.isKey("userIsSignedIn")) {
                this.authenticate();
                return
            }

            if(!this.$parent.auth) {
                this.$bvModal.show('auth')
            }
            
        },
        data() {
            return {
                active_users: [],
                inactive_users: [],
                sorting_keys: ['Room', 'Balance'],
                key: 0,
                payment_user: null,
                payment_amount: 30,
                payment_code: '',
                auth_code: '',
                auth_number: "31342069"
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
                console.log(this.$parent.auth)
                if(!this.$parent.auth) {
                    this.$router.go()
                    return;
                }
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
                    this.$bvModal.hide('payment')
                }).catch((error) => {
                    console.log(error)
                    this.$bvModal.hide('payment')
                })
            },
            authenticate() {
                this.$parent.auth = true
                this.$cookies.set("userIsSignedIn","")
                this.$bvModal.hide("auth")
            }
        }
    }
</script>

<style scoped>

    .logo {
        font-size: 40px;
    }


    .gradient-text {
        background: -webkit-linear-gradient(45deg, #2537AF, #70E5CB);
        -webkit-background-clip: text;
        background-clip: text;
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
    .header-large {
        font-size: 45pt; 
        margin-bottom: 5px
    }

    /* Small size user icons*/
    @media (max-width: 500px) {
        .header-large {
            font-size: 25pt; 
            margin-bottom: 5px
        }
        .room-number {
            position: absolute;
            font-size: 40pt;
            right: 10px;
            top: 5px;
            z-index: 0;
            color: gray;
        }
        .selection-name-field {
            font-size: 15pt;
        }

        .selection-price-field {
            font-size: 15pt;
        }

    }

    /* Padding when navbar collapses */
    @media (max-width: 768px) {
        .navitems-padding {
            margin-bottom: 15px;
        }
    }

    /* Medium size user selection items*/
    @media (max-width: 1000px) and (min-width: 768px) {
        
        .room-number {
            position: absolute;
            font-size: 30pt;
            right: 10px;
            top: 45px;
            z-index: 0;
            color: gray;
        }

        .user-card {
            min-width: 210px;
            flex-grow: 1;
            flex-direction: row;
        }

    }

    
</style>