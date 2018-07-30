import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);


const state = {
    login : false,
    userName : '',
    baseUrl : 'http://127.0.0.1:8000',
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