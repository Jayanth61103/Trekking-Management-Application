<template>
    <div class="dashboard-container">
        <h1>Admin Dashboard</h1>
        <p class="welcome-message">
            Welcome to the Trekking Management System Admin Portal.
        </p>
        <DashboardStats
            :stats="dashboardStats"/>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

import { getDashboard } from "../../services/admin"

import DashboardStats from "../../components/dashboard/DashboardStats.vue"
import QuickActions from "../../components/dashboard/QuickActions.vue"
import RecentActivity from "../../components/dashboard/RecentActivity.vue"

const dashboardStats = ref({
    totalStaff: 0,
    totalTrekkers: 0,
    totalTreks: 0,
    totalBookings: 0,
    totalRevenue: 0,
    upcomingTreks: 0
})
const recentActivities = ref([])

onMounted(async () => {
    try {
        const response = await getDashboard()
        dashboardStats.value = response.data.statistics
        recentActivities.value = response.data.activities
    }
    catch (error) {
        console.error("Failed to load dashboard:", error)
    }
})
</script>

<style scoped>
.dashboard-container{
    width:90%;
    margin:auto;
    padding:30px;
}
h1{
    color:#2E7D32;
    margin-bottom:10px;
}
.welcome-message{
    color:#6B7280;
    margin-bottom:30px;
    font-size:16px;
}
</style>