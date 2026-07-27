import api from "./api";

// Dashboard
export function getDashboard() {
    return api.get("/admin/dashboard");
}

// Staff Managements
// Get All Staff
export function getAllStaff() {
    return api.get("/admin/staff");
}

// Create Staff
export function createStaff(staffData) {
    return api.post("/admin/create-staff", staffData);
}

// Get One Staff
export function getStaffDetails(staffUUID) {
    return api.get(`/admin/staff/${staffUUID}`);
}

// Update Staff Status
export function updateStaffStatus(staffUUID, status) {
    return api.patch(`/admin/staff/${staffUUID}/status`,{status: status});
}

// Trek Managements 
// Get All Treks
export function getAllTreks() {
    return api.get("/admin/treks");
}

// Get One Trek
export function getTrekDetails(trekUuid) {
    return api.get(`/admin/treks/${trekUuid}`);
}

// Get Eligible Guides
export function getEligibleGuides() {
    return api.get("/admin/eligible-guides")
}

// Create Trek
export function createTrek(data) {
    return api.post("/admin/create-trek", data)
}

// Update Trek
export function updateTrek(trekUuid, data) {
    return api.patch(
        `/admin/treks/${trekUuid}`,
        data);
}