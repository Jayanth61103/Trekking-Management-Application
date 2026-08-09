<template>
    <nav class="navbar">

        <!-- Logo -->
        <div class="logo">
            <RouterLink to="/">
            Trekmate
            </RouterLink>
        </div>

        <!-- Navigation Links -->
        <div class="nav-links">
            <RouterLink to="/">Home</RouterLink>
        </div>

        <!-- Right Side Authentication -->
        <div class="auth-links">
            <template v-if="!isLoggedIn">
                <RouterLink to="/login">
                    Login
                </RouterLink>
                <RouterLink to="/register">
                    Register
                </RouterLink>
            </template>
            <template v-else>
                <RouterLink to="/profile">
                    Profile
                </RouterLink>
                <button
                   class="logout-btn"
                   @click="handleLogout"
                >
                    Logout
                </button>
            </template>
        </div>
    </nav>
</template>

<script setup>
import { computed } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { logout } from "../../services/auth";

const router = useRouter();

const isLoggedIn = computed(() => {
    return !!localStorage.getItem("access_token");
});

async function handleLogout() {

    await logout();

    router.push("/login");

}
</script>

<style scoped>

.navbar{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 40px;
    background-color: white;
    border-bottom: 1px solid #dddddd;
}

/* Logo */
.logo a{
    text-decoration: none;
    font-size: 24px;
    font-weight: bold;
    color: #2E7D32;
}

/* Middle Links */
.nav-links{
    display: flex;
    gap: 30px;
}
.nav-links a{
    text-decoration: none;
    color: black;
    font-weight: 500;
}
.nav-links a:hover{
    color: #2E7D32;
}

/* Right Links */
.auth-links{
    display: flex;
    gap: 20px;
}
.auth-links a{
    text-decoration: none;
    color: #2E7D32;
    font-weight: bold;
}
.auth-links a:hover{
    color: #1B5E20;
}
.logout-btn{
    border:none;
    background:#2E7D32;
    color:white;
    padding:8px 18px;
    border-radius:6px;
    cursor:pointer;
    font-weight:bold;
}
.logout-btn:hover{
    background:#1B5E20;
}
</style>