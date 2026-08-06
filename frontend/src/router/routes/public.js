import AuthLayout from "../../layouts/AuthLayout.vue";
import HomeView from "../../views/common/HomeView.vue";
import LoginView from "../../views/auth/LoginView.vue";
import RegisterView from "../../views/auth/RegisterView.vue";

export default {
    path: "/",
    component: AuthLayout,
    children: [
        {
            path: "",
            name: "Home",
            component: HomeView
        },
        {
            path: "login",
            name: "Login",
            component: LoginView
        },
        {
            path: "register",
            name: "Register",
            component: RegisterView
        }
    ]
};