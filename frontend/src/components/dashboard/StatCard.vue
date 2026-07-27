<template>
    <div
        class="stat-card"
        @click="openPage">
        <div>
            <h3 class="stat-title">
                {{ title }}
            </h3>
            <h1 class="stat-value">
                {{ value }}
            </h1>
        </div>
        <p class="view-details">
            View Details →
        </p>
    </div>
</template>

<script setup>
import { useRouter } from "vue-router"

// Receive data from parent component
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    value: {
        type: [String, Number],
        required: true
    },
    route: {
        type: String,
        required: true
    }
})

// Access Vue Router
const router = useRouter()

// Navigate when card is clicked
function openPage() {
    router.push(props.route)
}
</script>

<style scoped>
.stat-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: 0.25s ease;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 130px;
}
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.12);
}
.stat-title {
    font-size: 16px;
    color: #6B7280;
    margin-bottom: 12px;
    font-weight: 600;
}
.stat-value {
    font-size: 36px;
    color: #2E7D32;
    font-weight: 700;
    margin: 0;
}
.view-details {
    color: #2E7D32;
    font-size: 13px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 0;
}
</style>