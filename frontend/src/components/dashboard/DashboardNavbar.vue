<template>
    <nav class="dashboard-navbar">
        <!-- Logo -->
        <div class="brand" @click="goToDashboard">
            Trekmate
        </div>
        <!-- Navigation -->
        <div class="nav-links">
            <button
                class="nav-link"
                @click="goToDashboard"
            >
                Dashboard
            </button>
            <button
                class="nav-link"
                @click="goToProfile"
            >
                Profile
            </button>
            <button
                class="logout-button"
                @click="handleLogout"
            >
                Logout
            </button>
        </div>
    </nav>
</template>

<script setup>
import { useRouter } from "vue-router"
import { logout } from "../../services/auth"

const router = useRouter()

// Dashboard Navigation
function goToDashboard() {

    const role = localStorage.getItem("role")
    if (role === "Admin") {
        router.push("/admin/dashboard")
    }
    else if (role === "Staff") {
        router.push("/staff/dashboard")
    }
    else if (role === "Trekker") {
        router.push("/trekker/dashboard")
    }
}
// Profile Navigation
function goToProfile() {
    router.push("/profile")
}

// Logout
async function handleLogout() {
    try {
        await logout()
    }
    catch (error) {
        console.error("Logout error:", error)
    }
    finally {
        localStorage.clear()
        router.push("/login")
    }
}
</script>

<style scoped>
.dashboard-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 30px;
    border-bottom: 1px solid #E5E7EB;
}
.brand {
    color: #2E7D32;
    font-size: 32px;
    font-weight: bold;
    cursor: pointer;
}
.nav-links {
    display: flex;
    align-items: center;
    gap: 20px;
}
.nav-link {
    background: none;
    border: none;
    color: #2E7D32;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
}
.nav-link:hover {
    text-decoration: underline;
}
.logout-button {
    padding: 10px 20px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}
.logout-button:hover {
    background: #256428;
}
</style>