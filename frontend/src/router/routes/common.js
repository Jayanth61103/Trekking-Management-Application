import ProfileView from "../../views/common/ProfileView.vue";

export default [
    {
        path: "profile",
        name: "Profile",
        component: ProfileView,
        meta: {
            requiresAuth: true
        }
    }
];