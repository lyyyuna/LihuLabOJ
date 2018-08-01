import loginpage from "./components/login/login.vue";
import problemlistpage from "./components/problemlist/problemlist.vue"
import registerpage from "./components/register/register.vue"
import profilepage from "./components/profile/profile.vue"
import editprofilepage from "./components/profile/editprofile.vue"

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
    },
    {
        path : '/profile',
        component : profilepage,
    },
    {
        path : '/editprofile',
        component : editprofilepage,
    }
]

export default routers