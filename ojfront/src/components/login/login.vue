<template>
    <div>
        <div class="block">
            <el-row :gutter="20">
                <el-col :span="6" :offset="9">
                    <el-input
                        class="lyyinput"
                        placeholder="请输入用户名"
                        v-model="username"
                        clearable>
                    </el-input>
                    <el-input
                        class="lyyinput"
                        type="password"
                        placeholder="请输入密码"
                        v-model="password"
                        clearable>
                    </el-input>
                    <el-button 
                        class="lyyinput"
                        type="danger" 
                        @click="trylogin()">登录
                    </el-button>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
import Cookies from 'js-cookie';

export default {
    computed : {
        baseUrl() {
            return this.$store.state.baseUrl;
        },
        login() {
            return this.$store.state.login;
        }
    },
    data() {
        return {
            username : '',
            password : ''
        }
    },
    methods : {
        trylogin() {
            // cannot be blank
            if (this.username == '' || this.password == '') {
                this.$message({
                showClose: true,
                message: '用户名或者密码不能为空',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            // username length should <15
            var usernameLen = this.username.length
            if (usernameLen>15) {
                this.$message({
                showClose: true,
                message: '用户名长度不能大于15',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            // password length should be 8-20
            var passLen = this.password.length
            if (passLen > 20 || passLen < 8) {
                this.$message({
                showClose: true,
                message: '密码长度应在 8～20 之间',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            // call api
            var csrftoken = Cookies.get('csrftoken');
            this.$http.post(this.baseUrl+'/api/ojuser/login', 
                {username : this.username, password : this.password},
                {headers: {"X-CSRFToken":csrftoken }}
            ).then(response => {
                var rejs = response.body
                var code = rejs['code']
                var data = rejs['data']
                // login success
                if (code == 0 && data == 'login success') {
                    this.$message({
                    showClose: true,
                    message: '登录成功',
                    type: 'success',
                    duration:2000
                    });
                    // update global state
                    this.$store.commit('login')
                    console.log('login')
                    // go to problemlist page
                    this.$router.push({path : '/problemlist'})
                    // update my profile global state
                    this.$http.get(this.baseUrl + '/api/ojuser/profile/my').then(response => {
                        var rejs = response.body
                        var name = rejs['data']['username']
                        this.$store.commit('setUserName', name)
                    }, response => {
                        if (response.status == 403){
                            this.$store.commit('logout')
                            console.log("not login")
                            return
                        }
                        console.log(response)
                    });
                }
                if (code == 1) {
                    this.$message({
                    showClose: true,
                    message: '用户名或者密码错误',
                    type: 'warning',
                    duration:2000
                    });                                
                }
            }, response => {
                console.log(response)
            });
        },
    }
}
</script>


<style>
.lyyinput {
    margin-top: 20px;
}
</style>