<template>
    <div>
        <el-row>
            <el-menu
            :default-active='activeIndex'
            @select="handleSelect"
            mode="horizontal"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b">
            <el-submenu index="1">
                <template slot="title">个人中心</template>
                <el-menu-item index="1-1" v-show="login">
                    <router-link to="/profile" tag="div">答题情况</router-link>
                </el-menu-item>
                <el-menu-item index="1-2" v-show="!login">
                    <router-link to="/login" tag="div">登录</router-link>
                </el-menu-item>
                <el-menu-item index="1-5" v-show="login">
                    <router-link to="/editprofile" tag="div">修改个人资料</router-link>
                </el-menu-item>
                <el-menu-item 
                    index="1-3" 
                    v-show="login">
                    注销
                </el-menu-item>
                <el-menu-item index="1-4" v-show="!login">
                    <router-link to="/register" tag="div">注册</router-link>
                </el-menu-item>
            </el-submenu>
            <el-menu-item index="2">
                <router-link to="/problemlist" tag="div">
                    题目列表
                </router-link>
            </el-menu-item>
            <el-menu-item index="3">
                <router-link to="/ranks" tag="div">
                    排名
                </router-link>      
            </el-menu-item>
            </el-menu>

        </el-row>
    </div>
</template>

<script>
import Cookies from 'js-cookie';
export default {
    data() {
        return {
            activeIndex : '2'
        }
    },
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
                var name = rejs['data']['username']
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
        },
        handleSelect(key, keyPath) {
            if (key == '1-3') {
                this.tryLogout()
            }
        },
        tryLogout() {
            var csrftoken = Cookies.get('csrftoken');
            this.$http.post(this.baseUrl + '/api/ojuser/logout', '', {headers: {"X-CSRFToken":csrftoken }}).then(response => {
                var rejs = response.body
                console.log(rejs)
                var code = rejs['code']
                var data = rejs['data']
                if (code == 0 && data == 'logout success') {
                    this.$message({
                    showClose: true,
                    message: '注销成功',
                    type: 'success',
                    duration: 2000
                    });
                    // update global state
                    this.$store.commit('logout')
                    this.$store.commit('setUserName', '')
                    // go to problemlist page
                    this.$router.push({path : '/problemlist'})
                    console.log('logout')
                }
                // code == 1
            }, response => {
                console.log(response)
            })
        }
    }
}
</script>

<style>

</style>
