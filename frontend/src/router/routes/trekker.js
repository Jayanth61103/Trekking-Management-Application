import TrekkerDashboard from "../../views/trekker/TrekkerDashboard.vue";
import BrowseTreksView from "../../views/trekker/BrowseTreksView.vue";
import MyBookingsView from "../../views/trekker/MyBookingsView.vue";

export default [
    {
        path: "trekker/dashboard",
        name: "TrekkerDashboard",
        component: TrekkerDashboard,
        meta: {
            requiresAuth: true,
            role: "Trekker"
        }
    },
    {
        path: "trekker/browse",
        name: "BrowseTreks",
        component: BrowseTreksView,
        meta: {
            requiresAuth: true,
            role: "Trekker"
        }
    },
    {
        path: "trekker/bookings",
        name: "MyBookings",
        component: MyBookingsView,
        meta: {
            requiresAuth: true,
            role: "Trekker"
        }
    }
];