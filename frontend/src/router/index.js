import { createRouter, createWebHistory } from "vue-router";

// Layouts
import AuthLayout from "../layouts/AuthLayout.vue";
import MainLayout from "../layouts/MainLayout.vue";

// Public Views
import HomeView from "../views/common/HomeView.vue";
import LoginView from "../views/auth/LoginView.vue";
import RegisterView from "../views/auth/RegisterView.vue";

// Shared Views
import ProfileView from "../views/common/ProfileView.vue";

// Admin Views
import AdminDashboard from "../views/admin/AdminDashboard.vue";
import StaffManagementView from "../views/admin/StaffManagementView.vue";
import CreateStaffView from "../views/admin/CreateStaffView.vue";
import TrekManagementView from "../views/admin/TrekManagementView.vue";
import CreateTrekView from "../views/admin/CreateTrekView.vue";

// Staff Views
import StaffDashboard from "../views/staff/StaffDashboard.vue";

// Trekker Views
import TrekkerDashboard from "../views/trekker/TrekkerDashboard.vue";

// Authentication Helpers
import { isLoggedIn, getRole } from "../services/auth";

const routes = [
    // PUBLIC ROUTES
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

    // PROTECTED ROUTES
    {
        path: "/",
        component: MainLayout,

        children: [

            // Profile
            {
                path: "profile",
                name: "Profile",
                component: ProfileView,
                meta: {
                    requiresAuth: true
                }
            },

            // ADMIN
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
                path: "admin/staff",
                name: "StaffManagement",
                component: StaffManagementView,
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
                path: "admin/treks",
                name: "TrekManagement",
                component: TrekManagementView,
                meta: {
                    requiresAuth: true, role: "Admin"}
            },

            {
                path: "admin/create-trek",
                name: "CreateTrek",
                component: CreateTrekView,
                meta: {
                    requiresAuth: true, role: "Admin"}

            },

            // STAFF
            {
                path: "staff/dashboard",
                name: "StaffDashboard",
                component: StaffDashboard,
                meta: {
                    requiresAuth: true,
                    role: "Staff"
                }
            },

            // TREKKER
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
const router = createRouter({
    history: createWebHistory(),
    routes
});

// NAVIGATION GUARD
router.beforeEach((to) => {
    // Protected route without login
    if (to.meta.requiresAuth && !isLoggedIn()) {
        return "/login";
    }
    // Role protected route
    if (to.meta.role && getRole() !== to.meta.role) {
        const role = getRole();
        if (role === "Admin") {
            return "/admin/dashboard";
        }
        if (role === "Staff") {
            return "/staff/dashboard";
        }
        if (role === "Trekker") {
            return "/trekker/dashboard";
        }
        return "/login";
    }
    // Allow navigation
    return true;
});
export default router;