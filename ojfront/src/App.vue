<template>
  <div>
    <navigation></navigation>

    <el-input
      placeholder="请输入用户名"
      v-model="username"
      clearable>
    </el-input>
    <el-input
      placeholder="请输入密码"
      v-model="password"
      clearable>
    </el-input>
    <el-button type="danger" 
          @click="trylogin()">登陆</el-button>
  </div>
</template>

<script type="text/ecmascript-6">
  import navigation from "./components/navigation/navigation.vue";
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
    components: {
      navigation,
    },
    methods : {
      trylogin() {
        this.$http.post(this.baseUrl+'/api/ojuser/login', {username : this.username, password : this.password}).then(response => {
          var res = response.body
          console.log(res)

        this.$http.get(this.baseUrl + '/api/ojuser/profile/my').then(response => {
                var res = response.body
                this.$store.commit('login')
            }, response => {
              if (response.status == 403){
                this.$store.commit('logout')
                console.log("not login")
                return
              }
                console.log(response)
            });


        }, response => {
          console.log("error")
        });


      },

    }
  };
</script>

<style>
.el-row {
    margin-bottom: 20px;
}
</style>
