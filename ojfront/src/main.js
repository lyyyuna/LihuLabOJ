import Vue from 'vue';
import ElementUI from 'element-ui';
import VueRouter from 'vue-router';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import routers from './router';
import VueResource from 'vue-resource'
import Vuex from 'vuex';
import store from './store/store';
import VueHighlightJS from 'vue-highlightjs'

Vue.use(VueHighlightJS)
Vue.use(VueResource)
Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(Vuex);

Vue.http.interceptors.push((request, next) => {
  request.credentials = true
  next()
})

const router = new VueRouter({
  mode : 'history',
  routes : routers
})

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});