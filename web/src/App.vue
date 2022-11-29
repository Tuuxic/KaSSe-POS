<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script>
    import axios from "axios"

    const moment = require('moment');

    export default {
        created() {
            this.preventContextMenu()
            this.CDPclock()
            this.clockID = setInterval(this.CDPclock, 60 * 1000)
        },
        data() {
            return {
                host: 'http://localhost:5000',
                selected_user: null,
                clockID: null,
                show_clock: true
            }
        },
        methods: {
            preventContextMenu() {
                document.addEventListener("contextmenu", function (e) {
                    e.preventDefault()
                }, false)
            },
            CDPclock() {
                if (this.show_clock === true) {
                    moment.locale('de')
                    this.CDPset({
                        top: moment().format("HH:mm"),
                        bottom: moment().format("Do MMM YYYY")
                    })
                }
            },
            CDPmessage(data, timeout) {
                this.show_clock = false
                this.CDPset(data)
                setTimeout(() => {
                    this.show_clock = true
                }, timeout * 1000);
            },
            CDPset(data) {
                axios.post(this.host + '/cdp', data).catch((error) => {
                    console.log(error)
                })
            }
        }
    }

</script>

<style>
    @import "./assets/sass/fonts.scss";

    #app {
        font-family: "Helvetica Neue", Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    ::-webkit-scrollbar {
        display: none;
    }

    * {
        scrollbar-width: none;
        -webkit-user-select: none; /* Chrome all / Safari all */
        -moz-user-select: none; /* Firefox all */
        -ms-user-select: none; /* IE 10+ */
        user-select: none; /* Likely future */
        touch-action: manipulation;
    }

    input[type=number]::-webkit-outer-spin-button,
    input[type=number]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    input[type=number] {
        -moz-appearance: textfield;
    }
</style>
