<template>
    <section class="dashboard-stats">
        <StatCard
            title="Total Staff"
            :value="stats.totalStaff"
            route="/admin/staff"/>
        <StatCard
            title="Total Trekkers"
            :value="stats.totalTrekkers"
            route="/admin/trekkers"/>
        <StatCard
            title="Total Treks"
            :value="stats.totalTreks"
            route="/admin/treks"/>
        <StatCard
            title="Total Bookings"
            :value="stats.totalBookings"
            route="/admin/bookings"/>
        <StatCard
            title="Revenue"
            :value="'₹' + stats.totalRevenue"
            route="/admin/bookings"/>
        <StatCard
            title="Upcoming Treks"
            :value="stats.upcomingTreks"
            route="/admin/treks?status=upcoming"/>
    </section>
</template>

<script setup>
import StatCard from "./StatCard.vue"

// Receive statistics from AdminDashboard.vue
defineProps({
    stats: {
        type: Object,
        required: true
    }
})
</script>

<style scoped>
.dashboard-stats {
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-top: 30px;
}
</style>