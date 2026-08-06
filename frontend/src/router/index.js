import { createRouter, createWebHistory } from "vue-router";

// Layouts
import MainLayout from "../layouts/MainLayout.vue";

// Route Groups
import publicRoutes from "./routes/public";
import commonRoutes from "./routes/common";
import adminRoutes from "./routes/admin";
import staffRoutes from "./routes/staff";
import trekkerRoutes from "./routes/trekker";

// Authentication Helpers
import { isLoggedIn, getRole } from "../services/auth";

const routes = [
    // PUBLIC ROUTES
    publicRoutes,

    // PROTECTED ROUTES
    {
        path: "/",
        component: MainLayout,
        children: [
            ...commonRoutes,
            ...adminRoutes,
            ...staffRoutes,
            ...trekkerRoutes
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