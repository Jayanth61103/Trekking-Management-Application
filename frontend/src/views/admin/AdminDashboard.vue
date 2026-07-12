<template>
    <div class="dashboard-container">
        <h1>Admin Dashboard</h1>
        <p>
            Welcome to the Trekking Management System Admin Portal.
        </p>
        <div class="dashboard-actions">
            <button @click="goToCreateStaff">
                Create Staff
            </button>
            <button @click="goToProfile">
                My Profile
            </button>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from "vue-router"

const router = useRouter()
function goToCreateStaff() {
    router.push("/admin/create-staff")
}
function goToProfile() {
    router.push("/profile")
}
</script>

<style scoped>
.dashboard-container{
    width:80%;
    margin:auto;
    padding:40px;
}
h1{
    color:#2E7D32;
}
.dashboard-actions{
    margin-top:30px;
    display:flex;
    gap:20px;
}
button{
    padding:12px 25px;
    background:#2E7D32;
    color:white;
    border:none;
    border-radius:6px;
    cursor:pointer;
    font-size:16px;
}
button:hover{
    background:#256428;
}
</style>