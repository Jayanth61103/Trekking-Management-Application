import api from "./api";

export function getTrekkerProfile() {
    return api.get("/trekker/profile");
}

export function getTrekkerDashboard() {
    return api.get("/trekker/dashboard");
}