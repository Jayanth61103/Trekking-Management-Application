import { createRouter, createWebHistory } from "vue-router";

// Layouts
import AuthLayout from "../layouts/AuthLayout.vue";
import MainLayout from "../layouts/MainLayout.vue";

// Public Views
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";

// Shared Views
import ProfileView from "../views/ProfileView.vue";

// Admin Views
import AdminDashboard from "../views/admin/AdminDashboard.vue";
import CreateStaffView from "../views/admin/CreateStaffView.vue";

// Staff Views
import StaffDashboard from "../views/staff/StaffDashboard.vue";

// Trekker Views
import TrekkerDashboard from "../views/trekker/TrekkerDashboard.vue";

// Authentication Helpers
import { isLoggedIn, getRole } from "../services/auth";

// Routes
const routes = [

    // Public Layout
    {
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
    },

    // Protected Layout
    {
        path: "/",
        component: MainLayout,

        children: [

            {
                path: "profile",
                name: "Profile",
                component: ProfileView,
                meta: {
                    requiresAuth: true
                }
            },
            {
                path: "admin/dashboard",
                name: "AdminDashboard",
                component: AdminDashboard,
                meta: {
                    requiresAuth: true,
                    role: "Admin"
                }
            },
            {
                path: "admin/create-staff",
                name: "CreateStaff",
                component: CreateStaffView,
                meta: {
                    requiresAuth: true,
                    role: "Admin"
                }
            },
            {
                path: "staff/dashboard",
                name: "StaffDashboard",
                component: StaffDashboard,
                meta: {
                    requiresAuth: true,
                    role: "Staff"
                }
            },
            {
                path: "trekker/dashboard",
                name: "TrekkerDashboard",
                component: TrekkerDashboard,
                meta: {
                    requiresAuth: true,
                    role: "Trekker"
                }
            }
        ]
    }
];

// Create Router
const router = createRouter({
    history: createWebHistory(),
    routes
});

// Navigation Guard
router.beforeEach((to, from, next) => {

    // User not logged in
    if (to.meta.requiresAuth && !isLoggedIn()) {
        return next("/login");
    }

    // Wrong Role
    if (to.meta.role && getRole() !== to.meta.role) {
        return next("/login");
    }
    next();
});

// Export
export default router;