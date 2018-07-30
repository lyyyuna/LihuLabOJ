<template>
    <div>
        <div class="block">
            <el-row :gutter="20">
                <el-col :span="6" :offset="9">
                    <el-input
                        placeholder="请输入用户名"
                        v-model="username"
                        clearable>
                    </el-input>
                    <el-input
                        type="password"
                        placeholder="请输入密码"
                        v-model="password"
                        clearable>
                    </el-input>
                    <el-button type="danger" 
                        @click="trylogin()">登录
                    </el-button>
                </el-col>
            </el-row>
        </div>
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
            this.$http.post(this.baseUrl+'/api/ojuser/login', {username : this.username, password : this.password}).then(response => {
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
                    this.$router.push({path : '/problemlist'})
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
                console.log("response")
            });
        },
    }
}
</script>


<style>
.el-input {
    margin-bottom: 20px;
}
</style>