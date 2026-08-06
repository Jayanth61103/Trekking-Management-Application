<template>
    <div class="trekker-container">

        <!-- Page Header -->
        <div class="trekker-header">
            <div>
                <h1>Trekker Management</h1>
                <p>View and manage trekker accounts.</p>
            </div>
        </div>

        <!-- Search -->
        <div class="trekker-controls">
            <input
                v-model="search"
                type="text"
                placeholder="Search by name, username, email or phone..."/>
        </div>

        <!-- Loading -->
        <p v-if="loading" class="state-message">
            Loading trekkers...
        </p>

        <!-- Error -->
        <p v-else-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </p>

        <!-- Empty State -->
        <div v-else-if="filteredTrekkers.length === 0" class="empty-state">
            <h3>No Trekkers Found</h3>
            <p v-if="search">No trekkers match your search.</p>
            <p v-else>Trekkers will appear here once they register.</p>
        </div>

        <!-- Trekker Table -->
        <TrekkerTable
            v-else
            :trekker-list="filteredTrekkers"
            @select-trekker="openTrekkerDetails"/>

        <!-- Trekker Details Modal -->
        <TrekkerDetailsModal
            v-if="selectedTrekkerUUID"
            :trekker-uuid="selectedTrekkerUUID"
            @close="closeTrekkerDetails"
            @updated="handleTrekkerUpdated"/>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"

import TrekkerTable from "../../components/admin/TrekkerTable.vue"
import TrekkerDetailsModal from "../../components/admin/TrekkerDetailsModal.vue"

import { getAllTrekkers } from "../../services/admin"

const trekkerList = ref([])
const selectedTrekkerUUID = ref(null)
const search = ref("")

const loading = ref(true)
const errorMessage = ref("")

async function loadTrekkers() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getAllTrekkers()
        trekkerList.value = response.data.trekkers || []
    }
    catch (error) {
        console.error("Failed to load trekkers:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load trekkers."
    }
    finally {
        loading.value = false
    }
}

const filteredTrekkers = computed(() => {
    const searchValue = search.value.toLowerCase().trim()

    if (!searchValue) {
        return trekkerList.value
    }

    return trekkerList.value.filter((trekker) => {
        const fullName = trekker.full_name?.toLowerCase() || ""
        const username = trekker.username?.toLowerCase() || ""
        const email = trekker.email?.toLowerCase() || ""
        const phone = trekker.phone?.toLowerCase() || ""
        const status = trekker.status?.toLowerCase() || ""

        return (
            fullName.includes(searchValue) ||
            username.includes(searchValue) ||
            email.includes(searchValue) ||
            phone.includes(searchValue) ||
            status.includes(searchValue)
        )
    })
})

function openTrekkerDetails(trekkerUUID) {
    selectedTrekkerUUID.value = trekkerUUID
}

function closeTrekkerDetails() {
    selectedTrekkerUUID.value = null
}

async function handleTrekkerUpdated() {
    await loadTrekkers()
}

onMounted(() => {
    loadTrekkers()
})
</script>

<style scoped>
.trekker-container {
    width: 90%;
    max-width: 1400px;
    margin: auto;
    padding: 30px;
}
.trekker-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}
h1 {
    color: #2E7D32;
    margin: 0 0 8px;
}
.trekker-header p {
    color: #6B7280;
    margin: 0;
}
.trekker-controls {
    margin: 30px 0 20px;
}
.trekker-controls input {
    width: 420px;
    max-width: 100%;
    padding: 11px 13px;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
    box-sizing: border-box;
}
.trekker-controls input:focus {
    border-color: #2E7D32;
    box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.1);
}
.state-message {
    color: #6B7280;
    padding: 20px 0;
}
.error-message {
    color: #B91C1C;
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-radius: 6px;
    padding: 12px 15px;
    margin-top: 20px;
}
.empty-state {
    padding: 50px;
    text-align: center;
    border: 1px dashed #D1D5DB;
    border-radius: 10px;
    color: #6B7280;
}
.empty-state h3 {
    margin: 0 0 8px;
    color: #374151;
}
@media (max-width: 700px) {
    .trekker-container { width: 95%; padding: 20px 10px; }
    .trekker-header { flex-direction: column; align-items: flex-start; }
    .trekker-controls input { width: 100%; }
}
</style>