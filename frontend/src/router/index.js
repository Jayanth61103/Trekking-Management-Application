import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import HomeView from "../views/HomeView.vue";
import ProfileView from "../views/ProfileView.vue";
import AdminDashboard from "../views/admin/AdminDashboard.vue"
import StaffDashboard from "../views/staff/StaffDashboard.vue"
import TrekkerDashboard from "../views/trekker/TrekkerDashboard.vue"

const routes = [
    {
        path: "/login",
        name: "Login",
        component: LoginView
    },
    {
        path: "/register",
        name: "Register",
        component: RegisterView
    },
    {
        path: "/",
        name: "Home",
        component: HomeView
    },
    {
        path: "/profile",
        name: "Profile",
        component: ProfileView
    },
    {
        path: "/admin/dashboard",
        component: AdminDashboard
    },
    {
        path: "/staff/dashboard",
        component: StaffDashboard
    },
    {
        path: "/trekker/dashboard",
        component: TrekkerDashboard
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;