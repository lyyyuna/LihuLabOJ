<template>
    <div>
        <div class="block">
            <el-row :gutter="20">
                <el-col :span="6" :offset="9">
                    <el-input
                        class="lyyinput"
                        type="password"
                        placeholder="请输入新密码"
                        v-model="password1"
                        clearable>
                    </el-input>
                    <el-input
                        class="lyyinput"
                        type="password"
                        placeholder="再次输入密码"
                        v-model="password2"
                        clearable>
                    </el-input>
                    <el-button 
                        class="lyyinput"
                        type="danger" 
                        @click="tryChangePassword()">点击修改密码
                    </el-button>
                    <el-input
                        class="lyyinput"
                        type="textarea"
                        :rows="2"
                        placeholder="请输入新签名"
                        v-model="signature"
                        clearable>
                    </el-input>
                    <el-button 
                        class="lyyinput"
                        type="danger" 
                        @click="tryChangeSignature()">点击修改签名
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
            password1 : '',
            password2 : '',
            signature : '',

        }
    },
    methods : {
        tryChangePassword() {
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
            this.$http.post(this.baseUrl + '/api/ojuser/profile/my/password', 
                {password : this.password1},
                {headers: {"X-CSRFToken":csrftoken }}
            ).then(response => {
                console.log(response)
                var rejs = response.body
                var code = rejs['code']
                var data = rejs['data']
                if (code == 0) {
                    this.$message({
                    showClose: true,
                    message: '密码修改成功，请重新登录',
                    type: 'success',
                    duration:3000
                    });
                    // update global state
                    this.$store.commit('logout')
                    this.$store.commit('setUserName', '')
                    // redirect to login page
                    this.$router.push({path : '/login'})
                    return
                }
                if (code == 1) {
                    this.$message({
                    showClose: true,
                    message: '密码修改失败，不符合规范',
                    type: 'warning',
                    duration:2000
                    });
                    return
                }
            }, response => {
                console.log(response)
            })
        },
        tryChangeSignature() {
            var signaLen = this.signature.length
            if (signaLen > 20) {
                this.$message({
                showClose: true,
                message: '签名长度应小于20',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            // call api
            var csrftoken = Cookies.get('csrftoken');
            this.$http.post(this.baseUrl + '/api/ojuser/profile/my/update', 
                {signature : this.signature},
                {headers: {"X-CSRFToken":csrftoken }}
            ).then(response => {
                console.log(response)
                var rejs = response.body
                var code = rejs['code']
                var data = rejs['data']
                if (code == 0) {
                    this.$message({
                    showClose: true,
                    message: '签名修改成功',
                    type: 'success',
                    duration:2000
                    });
                    return
                }
                if (code == 1) {
                    this.$message({
                    showClose: true,
                    message: '签名修改失败，不符合规范',
                    type: 'warning',
                    duration:2000
                    });
                    return
                }
            }, response => {
                console.log(response)
            })
        }
    }
}
</script>


<style>
.lyyinput {
    margin-top: 20px;
}
</style>