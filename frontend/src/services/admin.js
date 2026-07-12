import api from "./api";

export function getStaffProfile() {
    return api.get("/staff/profile");
}

export function getStaffDashboard() {
    return api.get("/staff/dashboard");
}
export function createStaff(data) {
    return api.post("/admin/create-staff", data);
}