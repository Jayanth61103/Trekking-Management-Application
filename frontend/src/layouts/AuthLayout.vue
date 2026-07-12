<template>
    <Navbar />
    <main class="content">
        <RouterView />
    </main>
</template>

<script setup>
import Navbar from "../components/common/Navbar.vue";
import { RouterView } from "vue-router";
</script>

<style scoped>
.content{
    padding:30px;
}
</style>