import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);


const state = {
    login : false,
    userName : '',
    baseUrl : 'http://oj.lihulab.net',
};

const mutations={
    login(state){
        state.login=true;
    },
    logout(state){
        state.login=false;
    },
    setUserName(state, name) {
        state.userName=name
    }
};

export default new Vuex.Store({
    state,
    mutations
});