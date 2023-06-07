<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script>

    export default {
        created() {
            this.preventContextMenu()
        },
        data() {
            return {
                host: 'https://getraenke.c3flur.de:5000',
                //host: "http://localhost:5000", 
                selected_user: null,
                auth: false,
                admin_code: "1337230601"
            }
        },
        methods: {
            preventContextMenu() {
                document.addEventListener("contextmenu", function (e) {
                    e.preventDefault()
                }, false)
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
        appearance: textfield;
    }
</style>
