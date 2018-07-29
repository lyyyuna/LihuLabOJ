<template>
    <div>
        <el-row>
            <el-menu
            mode="horizontal"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b">
            <el-menu-item index="1">
                <router-link to="/file" tag="a">
                    题目列表
                </router-link>
            </el-menu-item>
            <el-menu-item index="2">
                <router-link to="/cdtlist" tag="a">
                    排名
                </router-link>      
            </el-menu-item>
            </el-menu>
            <div>{{ baseUrl }}</div>
            <div>{{ login }}</div>
            <div>{{ userName }}</div>

        </el-row>
        <router-view></router-view>
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
    created : function() {
        this.getLoginState()
    },
    methods : {
        getLoginState() {
            this.$http.get(this.baseUrl + '/api/ojuser/profile/my').then(response => {
                var rejs = response.body
                name = rejs['data']['username']
                this.$store.commit('setUserName', name)
                this.$store.commit('login')
            }, response => {
                if (response.status == 403){
                    this.$store.commit('logout')
                    console.log("not login")
                    return
                }
                console.log(response)
            });
        }
    }
}
</script>

<style>
.el-row {
    margin-bottom: 20px;
}
</style>
