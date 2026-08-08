import api from "./api";

// Dashboard
export function getTrekkerDashboard() {
    return api.get("/trekker/dashboard");
}

// Profile
export function getTrekkerProfile() {
    return api.get("/trekker/profile");
}

// Browse Open Treks
export function browseTreks(filters = {}) {
    return api.get("/trekker/treks", { params: filters });
}

// Get One Trek (for booking)
export function getTrekForBooking(trekUuid) {
    return api.get(`/trekker/treks/${trekUuid}`);
}

// Create Booking
export function createBooking(data) {
    return api.post("/trekker/bookings", data);
}

// Get My Bookings
export function getMyBookings() {
    return api.get("/trekker/bookings");
}

// Cancel Booking
export function cancelBooking(bookingUuid) {
    return api.patch(`/trekker/bookings/${bookingUuid}/cancel`);
}

// Export Booking History (CSV via Email)
export function exportHistory() {
    return api.post("/trekker/export-history");
}