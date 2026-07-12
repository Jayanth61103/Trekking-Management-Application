<template>
    <nav class="dashboard-navbar">

        <div class="logo">
            <RouterLink to="/">
                Trekmate
            </RouterLink>
        </div>

        <div class="dashboard-links">
            <RouterLink to="/profile">
                Profile
            </RouterLink>

            <button
                class="logout-btn"
                @click="handleLogout"
            >
                Logout
            </button>
        </div>
    </nav>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import { logout } from "../../services/auth";

const router = useRouter();

async function handleLogout() {
    await logout();
    router.push("/login");
}
</script>

<style scoped>
.dashboard-navbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:15px 40px;
    background:white;
    border-bottom:1px solid #ddd;
}
.logo a{
    text-decoration:none;
    font-size:24px;
    color:#2E7D32;
    font-weight:bold;
}
.dashboard-links{
    display:flex;
    align-items:center;
    gap:20px;
}
.dashboard-links a{
    text-decoration:none;
    color:#2E7D32;
    font-weight:bold;
}
.logout-btn{
    border:none;
    background:#2E7D32;
    color:white;
    padding:8px 18px;
    border-radius:6px;
    cursor:pointer;
}
.logout-btn:hover{
    background:#1B5E20;
}
</style>