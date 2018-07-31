import loginpage from "./components/login/login.vue";
import problemlistpage from "./components/problemlist/problemlist.vue"
import registerpage from "./components/register/register.vue"

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
    },
    {
        path : '/register',
        component : registerpage,
    }
]

export default routers