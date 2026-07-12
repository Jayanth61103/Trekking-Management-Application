import api from "./api";

// Login
export async function login(credentials) {

    const response = await api.post("/login", credentials);

    const user = response.data.user;

    // Store Session
    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("user", JSON.stringify(user));
    localStorage.setItem("role", user.role);
    localStorage.setItem("user_id", user.id);
    localStorage.setItem("username", user.username);
    return response;
}

// Register
export function register(userData) {
    return api.post("/register", userData);
}

// Logout
export async function logout() {

    try {
        await api.post("/logout");
    } catch (error) {
        console.log("Logout API Error:", error);
    }
    // Clear complete session
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    localStorage.removeItem("role");
    localStorage.removeItem("user_id");
    localStorage.removeItem("username");

}

// Profile
export function getProfile() {
    return api.get("/profile");
}

// Session Helpers
export function isLoggedIn() {
    return !!localStorage.getItem("access_token");
}
export function getRole() {
    return localStorage.getItem("role");
}
export function getUser() {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
}