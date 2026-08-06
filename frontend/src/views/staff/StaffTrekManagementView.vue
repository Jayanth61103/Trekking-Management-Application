<template>
    <div class="trek-container">
        <div class="trek-header">
            <div>
                <h1>My Treks</h1>
                <p>View and manage your assigned treks.</p>
            </div>
        </div>

        <p v-if="loading" class="state-message">Loading your treks...</p>
        <p v-else-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div v-else-if="treks.length === 0" class="empty-state">
            <h3>No Treks Assigned</h3>
            <p>Treks assigned to you by the Admin will appear here.</p>
        </div>

        <StaffTrekTable
            v-else
            :trek-list="treks"
            @select-trek="openTrekDetails"/>

        <StaffTrekDetailsModal
            v-if="selectedTrekUuid"
            :trek-uuid="selectedTrekUuid"
            @close="closeTrekDetails"
            @updated="handleTrekUpdated"/>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import StaffTrekTable from "../../components/staff/StaffTrekTable.vue"
import StaffTrekDetailsModal from "../../components/staff/StaffTrekDetailsModal.vue"
import { getMyTreks } from "../../services/staff"

const treks = ref([])
const selectedTrekUuid = ref(null)
const loading = ref(true)
const errorMessage = ref("")

async function loadTreks() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getMyTreks()
        treks.value = response.data.treks || []
    }
    catch (error) {
        console.error("Failed to load treks:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load your treks."
    }
    finally {
        loading.value = false
    }
}

function openTrekDetails(trekUuid) {
    selectedTrekUuid.value = trekUuid
}

function closeTrekDetails() {
    selectedTrekUuid.value = null
}

async function handleTrekUpdated() {
    await loadTreks()
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
.trek-header h1 {
    color: #2E7D32;
    margin: 0 0 8px;
}
.trek-header p {
    color: #6B7280;
    margin: 0 0 20px;
}
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
</style>