<template>
    <DashboardNavbar />
    <main class="content">
        <RouterView />
    </main>
</template>

<script setup>
import DashboardNavbar from "../components/dashboard/DashboardNavbar.vue";
import { RouterView } from "vue-router";
</script>

<style scoped>
.content{
    padding:30px;
}
</style>