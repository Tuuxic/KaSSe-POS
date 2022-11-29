<template>
    <div id="item-selection">
        <div v-if="items != null">
            <b-row class="item-bar flex-nowrap m-0 px-2">
                <b-card no-body v-for="item in items" :key="item.barcode" class="item-container mx-2 my-4 shadow"
                        @click="addItem(item)">
                    <b-card-body>
                        <h3>
                            <font-awesome-icon class="like-icon" @click.stop="toggleFavorite(item.barcode)"
                                               :icon="[isFavorite(item.barcode) ? 'fas' : 'far','heart']"/>
                        </h3>
                        <b-img :src="require('@/assets/images/items/'+item.image)" class="item-image"/>
                        <b-img :src="require('@/assets/images/items/'+item.image)" class="item-image middle"/>
                        <b-img :src="require('@/assets/images/items/'+item.image)" class="item-image"/>
                        <b-img :src="require('@/assets/images/bottle_shadow.png')" class="bottle-shadow"/>
                        <b-card-text class="text-left">
                            <div class="item-values">
                                <h3><b>{{formatPrice(item.price)}}</b></h3>
                                <h6 class="item-volume text-muted">{{formatVolume(item.volume)}}</h6>
                            </div>
                            <h6>{{item.name}}</h6>
                            <h5><b>{{item.variant}}</b></h5>
                        </b-card-text>
                    </b-card-body>
                </b-card>
            </b-row>
            <b-row class="m-0 flex-nowrap">
                <b-col cols="7">
                    <b-card class="shadow text-left expand">
                        <b-table :items="selected_items" :fields="fields" v-if="selected_items.length > 0">
                            <template v-slot:cell(item)="data">
                                {{data.item.name}} <b>{{data.item.variant}}</b> {{formatVolume(data.item.volume)}}
                            </template>
                            <template v-slot:cell(quantity)="data">
                                <b-input-group class="shadow quantity-selector">
                                    <b-input-group-prepend>
                                        <b-button variant="outline-secondary"
                                                  @click="removeItem(data.item)">
                                            <font-awesome-icon :icon="['fas','minus']"/>
                                        </b-button>
                                    </b-input-group-prepend>
                                    <b-form-input type="number" v-model="data.item.quantity" class="text-center"
                                                  :formatter="formatQuantity"
                                                  style="width: 10px;" size="lg"/>
                                    <b-input-group-append>
                                        <b-button variant="outline-secondary"
                                                  @click="addItem(data.item)">
                                            <font-awesome-icon :icon="['fas','plus']"/>
                                        </b-button>
                                    </b-input-group-append>
                                </b-input-group>
                            </template>
                        </b-table>
                        <div v-else class="d-flex flex-column empty-cart">
                            <h5>Your shopping cart is empty.</h5>
                            <p>Select products by picking them above or scanning their barcodes.</p>
                            <div class="gif shadow" v-bind:style="{ 'background-image': 'url(' + gif + ')' }"/>
                        </div>
                    </b-card>
                </b-col>
                <b-col class="pl-0">
                    <b-card no-body class="shadow expand">
                        <b-card-body class="d-flex flex-column">
                            <h1>Total: {{formatPrice(total())}}</h1>
                            <template v-if="$parent.selected_user != null">
                                <h4 class="text-muted my-auto">{{$parent.selected_user.name}}<br>
                                    Balance: {{formatPrice($parent.selected_user.balance)}}</h4>
                                <b-form-checkbox size="lg" v-model="guest">Mark as guest purchase
                                </b-form-checkbox>
                                <b-button size="lg" variant="success" class="mt-auto shadow"
                                          :disabled="selected_items.length === 0" @click="buy"><h1>Confirm</h1>
                                </b-button>
                            </template>
                            <h4 v-else class="text-muted my-auto">No user selected!</h4>
                            <b-button size="lg" variant="secondary" class="mt-3 shadow" @click="$router.push('/')"><h1>
                                Cancel</h1></b-button>
                        </b-card-body>
                    </b-card>
                </b-col>
            </b-row>
        </div>
    </div>
</template>

<script>
    import axios from "axios"

    export default {
        created() {
            this.getItems()
            this.gif = "'" + require('@/assets/images/gifs/' + this.gifs[Math.floor(Math.random() * (this.gifs.length - 1))]) + "'"
        },
        data() {
            return {
                items: null,
                selected_items: [],
                fields: [
                    {key: 'item'},
                    {key: 'price', formatter: 'formatPrice'},
                    {key: 'quantity', thClass: 'text-center', tdClass: 'text-center'}
                ],
                gifs: ['crash.gif', 'dog.gif', 'drunk.gif', 'faceplant.gif', 'house.gif',
                    'knight.gif', 'loop.gif', 'mario.gif', 'moonwalk.gif', 'panda.gif',
                    'race.gif', 'run.gif', 'skate.gif', 'snow.gif', 'space.gif', 'titanic.gif',
                    'truck.gif', 'mud.gif', 'turn.gif', 'cat.gif', 'backwards.gif', 'milk.gif',
                    'flip.gif', 'car.gif', 'boy.gif', 'parking.gif', 'legs.gif'],
                gif: null,
                guest: false
            }
        },
        sockets: {
            codeScanned(barcode) {
                if (this.items == null) {
                    return
                }
                let matching_item = this.items.filter(item => {
                    return item.barcode === barcode
                })[0]
                if (matching_item === undefined) {
                    console.log('Unregistered barcode scanned: ' + barcode)
                    return
                }
                this.addItem(matching_item)
            }
        },
        methods: {
            addItem(item_to_add) {
                let matching_item = this.selected_items.filter(item => {
                    return item.barcode === item_to_add.barcode
                })[0]
                if (matching_item) {
                    this.$set(matching_item, 'quantity', Number(matching_item.quantity) + 1)
                } else {
                    item_to_add = {...item_to_add}
                    item_to_add.quantity = 1
                    this.selected_items.push(item_to_add)
                }
                this.$parent.CDPmessage({
                    top: {left: item_to_add.name},
                    bottom: {
                        left: item_to_add.variant !== null ? item_to_add.variant : '',
                        right: (item_to_add.price / 100).toFixed(2)
                    }
                }, 2)
            },
            removeItem(item_to_remove) {
                let matching_item = this.selected_items.filter(item => {
                    return item.barcode === item_to_remove.barcode
                })[0]
                if (matching_item) {
                    if (matching_item.quantity > 1) {
                        this.$set(matching_item, 'quantity', Number(matching_item.quantity) - 1)
                    } else {
                        let index = this.selected_items.indexOf(matching_item);
                        if (index !== -1) this.selected_items.splice(index, 1);
                    }
                }
            },
            formatQuantity(value) {
                return Math.max(value, 1).toString()
            },
            formatPrice(value) {
                return (value / 100).toFixed(2) + '€'
            },
            formatVolume(value) {
                return value + 'l'
            },
            total() {
                let total = 0
                this.selected_items.forEach(item => {
                    total += Number(item.price) * Number(item.quantity)
                })
                return total
            },
            buy() {
                let transaction = {
                    'user': this.$parent.selected_user,
                    'items': this.selected_items,
                    'impact': -this.total()
                }
                if (this.guest) {
                    transaction.guest = true
                }
                axios.post(this.$parent.host + '/transactions/add', transaction).then(() => {
                    this.$parent.CDPmessage({top: {center: 'Thanks for your'}, bottom: {center: 'purchase!'}}, 10)
                    this.$router.push('/')
                }).catch((error) => {
                    console.log(error)
                    this.$router.push('/')
                })
            },
            getItems() {
                axios.get(this.$parent.host + '/items').then((res) => {
                    this.items = res.data
                    this.items.sort((a) => {
                        return this.isFavorite(a.barcode) ? -1 : 1
                    })
                }).catch((error) => {
                    console.error(error)
                })
            },
            isFavorite(barcode) {
                if (!this.$parent.selected_user) return false
                if (!this.$parent.selected_user.favorites) return false
                let is_fave = false
                this.$parent.selected_user.favorites.forEach((fave) => {
                    if (barcode === fave) {
                        is_fave = true
                    }
                })
                return is_fave
            },
            toggleFavorite(barcode) {
                if (!this.$parent.selected_user) return
                if (!this.$parent.selected_user.favorites) return
                if(this.isFavorite(barcode)) {
                    let index = this.$parent.selected_user.favorites.indexOf(barcode)
                    if (index > -1) {
                        this.$parent.selected_user.favorites.splice(index, 1)
                    }
                    axios.post(this.$parent.host + '/favorites/remove', {id: this.$parent.selected_user.id, barcode: barcode}).then(() => {
                        this.$parent.CDPmessage({top: {center: 'Favorite'}, bottom: {center: 'removed!'}}, 2)
                    }).catch((error) => {
                        console.log(error)
                    })
                } else {
                    this.$parent.selected_user.favorites.push(barcode)
                    axios.post(this.$parent.host + '/favorites/add', {id: this.$parent.selected_user.id, barcode: barcode}).then(() => {
                        this.$parent.CDPmessage({top: {center: 'Favorite'}, bottom: {center: 'added!'}}, 2)
                    }).catch((error) => {
                        console.log(error)
                    })
                }
                this.getItems()
            }
        }
    }
</script>

<style scoped>
    .empty-cart {
        height: 100%;
    }

    .gif {
        flex-grow: 1;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        border-radius: 6px;
    }

    .quantity-selector {
        min-width: 135px;
    }

    .expand {
        height: calc(100vh - 340px);
        overflow: hidden;
    }

    .item-bar {
        overflow-x: scroll;
    }

    .item-container {
        min-width: 250px;
    }

    .item-image {
        height: 100px;
        margin: 1px;
        position: relative;
        z-index: 1;
    }

    .item-image.middle {
        height: 120px;
    }

    .bottle-shadow {
        width: 160px;
        max-width: 100%;
        position: relative;
        bottom: 50px;
        margin-bottom: -50px;
    }

    .item-values {
        float: right;
        margin-left: 10px;
        margin-top: -5px;
        text-align: right;
    }

    .item-volume {
        margin-top: -5px;
    }

    .like-icon {
        position: absolute;
        right: 20px;
    }

    .purple-gradient {
        background: rgb(214, 0, 255);
        background: linear-gradient(90deg, rgba(214, 0, 255, 1) 0%, rgba(255, 218, 0, 1) 100%);
    }
</style>