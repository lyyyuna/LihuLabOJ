<template>
    <div>
        <div>{{ baseUrl }}</div>
        <div>{{ login }}</div>
        <div>{{ userName }}</div>
    </div>
</template>

<script>
export default {
    computed : {
        baseUrl() {
            return this.$store.state.baseUrl;
        },
        login() {
            return this.$store.state.login;
        },
        userName() {
            return this.$store.state.userName;
        }
    },
    data() {
        return {

        }
    }
}
</script>


<style>
.el-input {
    margin-bottom: 20px;
}
</style>