import loginpage from "./components/login/login.vue";
import problemlistpage from "./components/problemlist/problemlist.vue"

const routers = [
    {
        path : '/',
        redirect : '/problemlist',
    },
    {
        path : '/login',
        component : loginpage,
    },
    {
        path : '/problemlist',
        component : problemlistpage,
    }
]

export default routers