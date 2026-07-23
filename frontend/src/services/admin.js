import api from "./api";

// Create Staff
export function createStaff(staffData) {
    return api.post("/admin/create-staff", staffData);
}

// Future Admin APIs
export function getAllStaff() {
    return api.get("/admin/staff");
}
export function getStaffDetails(staffUUID) {
    return api.get(`/admin/staff/${staffUUID}`);
}
export function updateStaff(staffUUID, staffData) {
    return api.put(`/admin/staff/${staffUUID}`, staffData);
}
export function deleteStaff(staffUUID) {
    return api.delete(`/admin/staff/${staffUUID}`);
}