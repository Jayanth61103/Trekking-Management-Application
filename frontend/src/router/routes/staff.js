import StaffDashboard from "../../views/staff/StaffDashboard.vue";
import StaffTrekManagementView from "../../views/staff/StaffTrekManagementView.vue";

export default [
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
        path: "staff/treks",
        name: "StaffTrekManagement",
        component: StaffTrekManagementView,
        meta: {
            requiresAuth: true,
            role: "Staff"
        }
    }
];