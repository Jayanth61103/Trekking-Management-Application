<template>
    <section class="quick-actions">
        <h2>Quick Actions</h2>
        <div class="action-grid">
            <button @click="goToCreateStaff">
                Create Staff
            </button>
            <button @click="goToStaffList">
                View Staff
            </button>
            <button @click="goToCreateTrek">
                Create Trek
            </button>
            <button @click="goToTrekList">
                View Treks
            </button>
        </div>
    </section>
</template>

<script setup>
import { useRouter } from "vue-router"
const router = useRouter()
function goToCreateStaff(){
    router.push("/admin/create-staff")
}
function goToStaffList(){
    router.push("/admin/staff")
}
function goToCreateTrek(){
    router.push("/admin/create-trek")
}
function goToTrekList(){
    router.push("/admin/treks")
}
</script>

<style scoped>
.quick-actions{
    margin-top:40px;
}
.quick-actions h2{
    margin-bottom:20px;
    color:#2E7D32;
}
.action-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:20px;
}
button{
    padding:18px;
    border:none;
    border-radius:12px;
    background:#2E7D32;
    color:white;
    font-size:16px;
    font-weight:600;
    cursor:pointer;
    transition:0.25s;
}
button:hover{
    background:#256428;
    transform:translateY(-2px);
}
</style>