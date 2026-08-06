<template>
    <div class="browse-container">
        <div class="browse-header">
            <h1>Browse Treks</h1>
            <p>Find and book your next trekking adventure.</p>
        </div>

        <!-- Filters -->
        <div class="filters">
            <select v-model="filters.difficulty" @change="loadTreks">
                <option value="">All Difficulties</option>
                <option value="EASY">Easy</option>
                <option value="MODERATE">Moderate</option>
                <option value="DIFFICULT">Difficult</option>
                <option value="EXTREME">Extreme</option>
            </select>

            <input
                v-model="filters.location"
                type="text"
                placeholder="Filter by location..."
                @input="debouncedLoad"/>

            <input
                v-model.number="filters.max_duration"
                type="number"
                min="1"
                placeholder="Max duration (days)"
                @change="loadTreks"/>
        </div>

        <p v-if="loading" class="state-message">Loading treks...</p>
        <p v-else-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div v-else-if="treks.length === 0" class="empty-state">
            <h3>No Treks Found</h3>
            <p>Try adjusting your filters, or check back later for new treks.</p>
        </div>

        <div v-else class="trek-grid">
            <div v-for="trek in treks" :key="trek.trek_uuid" class="trek-card">
                <h3>{{ trek.trek_name }}</h3>
                <p class="location">{{ trek.location }}</p>
                <div class="trek-meta">
                    <span>{{ trek.difficulty }}</span>
                    <span>{{ trek.duration_days }} Days</span>
                    <span>{{ trek.available_slots }} slots left</span>
                </div>
                <p class="price">₹{{ trek.price }}</p>
                <p class="dates">{{ trek.start_date }} → {{ trek.end_date }}</p>
                <button class="book-button" @click="openBooking(trek.trek_uuid)">
                    View & Book
                </button>
            </div>
        </div>

        <TrekBookingModal
            v-if="selectedTrekUuid"
            :trek-uuid="selectedTrekUuid"
            @close="closeBooking"
            @booked="handleBooked"/>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import TrekBookingModal from "../../components/trekker/TrekBookingModal.vue"
import { browseTreks } from "../../services/trekker"

const treks = ref([])
const selectedTrekUuid = ref(null)
const loading = ref(true)
const errorMessage = ref("")

const filters = reactive({
    difficulty: "",
    location: "",
    max_duration: null
})

let debounceTimer = null
function debouncedLoad() {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(loadTreks, 400)
}

async function loadTreks() {
    try {
        loading.value = true
        errorMessage.value = ""

        const params = {}
        if (filters.difficulty) params.difficulty = filters.difficulty
        if (filters.location) params.location = filters.location
        if (filters.max_duration) params.max_duration = filters.max_duration

        const response = await browseTreks(params)
        treks.value = response.data.treks || []
    }
    catch (error) {
        console.error("Failed to load treks:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load treks."
    }
    finally {
        loading.value = false
    }
}

function openBooking(trekUuid) {
    selectedTrekUuid.value = trekUuid
}

function closeBooking() {
    selectedTrekUuid.value = null
}

async function handleBooked() {
    selectedTrekUuid.value = null
    await loadTreks()
}

onMounted(() => {
    loadTreks()
})
</script>

<style scoped>
.browse-container {
    width: 90%;
    max-width: 1400px;
    margin: auto;
    padding: 30px;
}
.browse-header h1 { color: #2E7D32; margin: 0 0 8px; }
.browse-header p { color: #6B7280; margin: 0 0 20px; }
.filters {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    margin-bottom: 25px;
}
.filters select,
.filters input {
    padding: 10px 12px;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    font-size: 14px;
}
.state-message { color: #6B7280; padding: 20px 0; }
.error-message { color: #B91C1C; padding: 15px 0; }
.empty-state {
    padding: 50px;
    text-align: center;
    border: 1px dashed #D1D5DB;
    border-radius: 10px;
    color: #6B7280;
}
.trek-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
}
.trek-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 20px;
}
.trek-card h3 { margin: 0 0 5px; color: #1F2937; }
.location { color: #6B7280; margin: 0 0 12px; font-size: 14px; }
.trek-meta {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.trek-meta span {
    background: #F0FDF4;
    color: #166534;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.price { font-size: 20px; font-weight: 700; color: #2E7D32; margin: 0 0 5px; }
.dates { color: #6B7280; font-size: 13px; margin: 0 0 15px; }
.book-button {
    width: 100%;
    padding: 10px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}
.book-button:hover { background: #256428; }
</style>