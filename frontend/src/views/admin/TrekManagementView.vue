<template>
    <div class="trek-container">
        <!-- Page header -->
        <div class="trek-header">
            <div>
                <h1>Trek Management</h1>
                <p>View and manage trekking activities.</p>
            </div>
            <button class="create-button" @click="goToCreateTrek">
                + Create Trek
            </button>
        </div>

        <!-- Search Treks -->
        <div class="trek-controls">
            <input
                v-model="search"
                type="text"
                placeholder="Search treks..."
            />
        </div>

        <!-- Page states -->
        <p v-if="loading" class="state-message">
            Loading treks...
        </p>

        <p v-else-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </p>

        <div v-else-if="filteredTreks.length === 0" class="empty-state">
            <h3>No Treks Found</h3>
            <p>Treks will appear here once they are created.</p>
        </div>

        <!-- Trek table -->
        <TrekTable
            v-else
            :trek-list="filteredTreks"
            @select-trek="openTrekDetails"
        />

        <!-- Trek details -->
        <TrekDetailsModal
            v-if="selectedTrekUuid"
            :trek-uuid="selectedTrekUuid"
            @close="closeTrekDetails"
            @updated="handleTrekUpdated"
        />
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import TrekTable from "../../components/admin/TrekTable.vue"
import TrekDetailsModal from "../../components/admin/TrekDetailsModal.vue"
import { getAllTreks } from "../../services/admin"

const router = useRouter()

const trekList = ref([])
const selectedTrekUuid = ref(null)
const search = ref("")
const loading = ref(true)
const errorMessage = ref("")

// Load all Treks
async function loadTreks() {
    try {
        loading.value = true
        errorMessage.value = ""

        const response = await getAllTreks()
        trekList.value = response.data.treks || []
    }
    catch (error) {
        console.error("Failed to load Treks:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load Treks."
    }
    finally {
        loading.value = false
    }
}

// Search and filter Treks
const filteredTreks = computed(() => {
    const searchValue = search.value.toLowerCase().trim()

    if (!searchValue) {
        return trekList.value
    }

    return trekList.value.filter((trek) => {
        const trekId = String(trek.trek_id ?? "").toLowerCase()
        const trekUuid = trek.trek_uuid?.toLowerCase() || ""
        const trekName = trek.trek_name?.toLowerCase() || ""
        const location = trek.location?.toLowerCase() || ""
        const difficulty = trek.difficulty?.toLowerCase() || ""
        const status = trek.status?.toLowerCase() || ""
        const guideName = trek.assigned_guide?.full_name?.toLowerCase() || ""
        const guideCode = trek.assigned_guide?.employee_code?.toLowerCase() || ""

        return (
            trekId.includes(searchValue) ||
            trekUuid.includes(searchValue) ||
            trekName.includes(searchValue) ||
            location.includes(searchValue) ||
            difficulty.includes(searchValue) ||
            status.includes(searchValue) ||
            guideName.includes(searchValue) ||
            guideCode.includes(searchValue)
        )
    })
})

// Open Create Trek page
function goToCreateTrek() {
    router.push("/admin/create-trek")
}

// Open selected Trek
function openTrekDetails(trekUuid) {
    if (!trekUuid) {
        console.error("Trek UUID is missing.")
        return
    }

    selectedTrekUuid.value = trekUuid
}

// Close Trek details
function closeTrekDetails() {
    selectedTrekUuid.value = null
}

// Refresh Treks after update
async function handleTrekUpdated() {
    await loadTreks()
    selectedTrekUuid.value = null
}

onMounted(() => {
    loadTreks()
})
</script>

<style scoped>
.trek-container {
    width: 90%;
    max-width: 1400px;
    margin: auto;
    padding: 30px;
}

/* Page header */
.trek-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}

h1 {
    color: #2E7D32;
    margin: 0 0 8px;
}

.trek-header p {
    color: #6B7280;
    margin: 0;
}

.create-button {
    padding: 12px 20px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
}

.create-button:hover {
    background: #256428;
}

/* Search */
.trek-controls {
    margin: 30px 0 20px;
}

.trek-controls input {
    width: 320px;
    max-width: 100%;
    padding: 10px 12px;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
}

.trek-controls input:focus {
    border-color: #2E7D32;
}

/* Page states */
.state-message {
    color: #6B7280;
    padding: 20px 0;
}

.error-message {
    color: #B91C1C;
    padding: 15px 0;
}

.empty-state {
    padding: 50px;
    text-align: center;
    border: 1px dashed #D1D5DB;
    border-radius: 10px;
    color: #6B7280;
}

.empty-state h3 {
    color: #374151;
}

/* Mobile layout */
@media (max-width: 700px) {
    .trek-container {
        width: 95%;
        padding: 20px 10px;
    }

    .trek-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .create-button {
        width: 100%;
    }

    .trek-controls input {
        width: 100%;
        box-sizing: border-box;
    }
}
</style>