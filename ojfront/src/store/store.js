import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);


const state = {
    login : 0,
    userName : '',
    baseUrl : 'http://127.0.0.1:8000',
};

const mutations={
    login(state){
        state.login=1;
    },
    logout(state){
        state.login=0;
    },
    setUserName(state, name) {
        state.userName=name
    }
};

export default new Vuex.Store({
    state,
    mutations
});