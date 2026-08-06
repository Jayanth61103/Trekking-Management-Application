import api from "./api";

// Staff Dashboard
export function getStaffDashboard() {
    return api.get("/staff/dashboard");
}

// Staff Profile
export function getStaffProfile() {
    return api.get("/staff/profile");
}

// Get My Assigned Treks
export function getMyTreks() {
    return api.get("/staff/treks");
}

// Get One Assigned Trek (with Participants)
export function getMyTrekDetails(trekUuid) {
    return api.get(`/staff/treks/${trekUuid}`);
}

// Update Trek Available Slots
export function updateTrekSlots(trekUuid, availableSlots) {
    return api.patch(`/staff/treks/${trekUuid}/slots`, {
        available_slots: availableSlots
    });
}

// Update Trek Status
export function updateTrekStatus(trekUuid, status) {
    return api.patch(`/staff/treks/${trekUuid}/status`, { status });
}