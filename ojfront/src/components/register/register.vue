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
                        placeholder="邀请码"
                        v-model="ackey"
                        clearable>
                    </el-input>
                    <el-input
                        type="password"
                        placeholder="请输入密码，密码不能过于简单"
                        v-model="password1"
                        clearable>
                    </el-input>
                    <el-input
                        type="password"
                        placeholder="再次输入密码"
                        v-model="password2"
                        clearable>
                    </el-input>
                    <el-button type="danger" 
                        @click="tryRegister()">点击注册
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
            password1 : '',
            password2 : '',
            ackey : '',

        }
    },
    methods : {
        tryRegister() {
            // cannot be blank
            if (this.username == '' || this.password1 == '' || this.ackey == '') {
                this.$message({
                showClose: true,
                message: '用户名、密码或者邀请码不能为空',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            // username length should <30
            var usernameLen = this.username.length
            if (usernameLen>30) {
                this.$message({
                showClose: true,
                message: '用户名长度不能大于30',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            // password length should be 8-20
            var passLen = this.password1.length
            if (passLen > 20 || passLen < 8) {
                this.$message({
                showClose: true,
                message: '密码长度应在 8～20 之间',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            // two password should be same
            if (this.password1 != this.password2) {
                this.$message({
                showClose: true,
                message: '两次密码不一致',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            // call api
            var csrftoken = Cookies.get('csrftoken');
            this.$http.post(this.baseUrl + '/api/ojuser/register', 
                {username : this.username, password : this.password1, activiation_code : this.ackey},
                {headers: {"X-CSRFToken":csrftoken }}
            ).then(response => {
                console.log(response)
                var rejs = response.body
                var code = rejs['code']
                var data = rejs['data']
                if (code == 0) {
                    this.$message({
                    showClose: true,
                    message: '注册成功，请登录',
                    type: 'success',
                    duration:2000
                    });
                    this.$router.push({path : '/login'})
                    return
                }
                if (code == 1) {
                    if (data == 'username already exists') {
                        this.$message({
                        showClose: true,
                        message: '用户名已存在，请换一个',
                        type: 'warning',
                        duration:2000
                        });    
                        return                    
                    }
                    if (data == 'wrong ac key') {
                        this.$message({
                        showClose: true,
                        message: '邀请码不对',
                        type: 'warning',
                        duration:2000
                        });    
                        return                    
                    }
                    if (data == 'input invalid') {
                        this.$message({
                        showClose: true,
                        message: '输入不符合要求，请使用字母与数字的组合',
                        type: 'warning',
                        duration:2000
                        });    
                        return                    
                    }
                }

            },
            response => {
                console.log(response)
            });

        }
    }
}
</script>


<style>
.el-input {
    margin-bottom: 20px;
}
</style>