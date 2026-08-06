<template>
    <div class="dashboard-container">
        <h1>Trekker Dashboard</h1>
        <p class="welcome-message">
            Welcome back, {{ dashboardData.full_name }}.
        </p>

        <div v-if="loading" class="state-message">Loading dashboard...</div>
        <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <section v-else class="stats-grid">
            <div class="stat-card">
                <span>Total Bookings</span>
                <strong>{{ dashboardData.total_bookings }}</strong>
            </div>
            <div class="stat-card">
                <span>Active Bookings</span>
                <strong>{{ dashboardData.active_bookings }}</strong>
            </div>
            <div class="stat-card">
                <span>Completed Treks</span>
                <strong>{{ dashboardData.completed_treks }}</strong>
            </div>
        </section>

        <div class="action-buttons">
            <button class="primary-button" @click="goToBrowse">
                Browse Treks
            </button>
            <button class="secondary-button" @click="goToBookings">
                My Bookings
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { getTrekkerDashboard } from "../../services/trekker"

const router = useRouter()

const dashboardData = ref({
    full_name: "",
    total_bookings: 0,
    active_bookings: 0,
    completed_treks: 0
})

const loading = ref(true)
const errorMessage = ref("")

async function loadDashboard() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getTrekkerDashboard()
        dashboardData.value = response.data
    }
    catch (error) {
        console.error("Failed to load dashboard:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load dashboard."
    }
    finally {
        loading.value = false
    }
}

function goToBrowse() {
    router.push("/trekker/browse")
}

function goToBookings() {
    router.push("/trekker/bookings")
}

onMounted(() => {
    loadDashboard()
})
</script>

<style scoped>
.dashboard-container {
    width: 90%;
    max-width: 1200px;
    margin: auto;
    padding: 30px;
}
h1 { color: #2E7D32; margin-bottom: 10px; }
.welcome-message { color: #6B7280; margin-bottom: 30px; font-size: 16px; }
.state-message { color: #6B7280; padding: 20px 0; }
.error-message { color: #B91C1C; padding: 15px 0; }
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}
.stat-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.stat-card span { color: #6B7280; font-size: 14px; }
.stat-card strong { font-size: 28px; color: #1F2937; }
.action-buttons { display: flex; gap: 15px; }
.primary-button, .secondary-button {
    padding: 12px 22px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    border: none;
}
.primary-button { background: #2E7D32; color: white; }
.primary-button:hover { background: #256428; }
.secondary-button { background: white; color: #2E7D32; border: 1px solid #2E7D32; }
.secondary-button:hover { background: #F0FDF4; }
</style>