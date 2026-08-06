import AdminDashboard from "../../views/admin/AdminDashboard.vue";
import StaffManagementView from "../../views/admin/StaffManagementView.vue";
import CreateStaffView from "../../views/admin/CreateStaffView.vue";
import TrekManagementView from "../../views/admin/TrekManagementView.vue";
import CreateTrekView from "../../views/admin/CreateTrekView.vue";
import TrekkerManagementView from "../../views/admin/TrekkerManagementView.vue";
import BookingManagementView from "../../views/admin/BookingManagementView.vue";

export default [
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
            requiresAuth: true,
            role: "Admin"
        }
    },
    {
        path: "admin/create-trek",
        name: "CreateTrek",
        component: CreateTrekView,
        meta: {
            requiresAuth: true,
            role: "Admin"
        }
    },
    {
        path: "admin/trekkers",
        name: "TrekkerManagement",
        component: TrekkerManagementView,
        meta: {
            requiresAuth: true,
            role: "Admin"
        }
    },
    {
        path: "admin/bookings",
        name: "BookingManagement",
        component: BookingManagementView,
        meta: {
            requiresAuth: true,
            role: "Admin"
        }
    }
];