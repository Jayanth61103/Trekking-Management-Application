<template>
    <div class="staff-container">

        <!-- Page Header -->
        <div class="staff-header">
            <div>
                <h1>Staff Management</h1>
                <p>View and manage staff members.</p>
            </div>
            <button
                class="create-button"
                @click="goToCreateStaff">
                + Create Staff
            </button>
        </div>

        <!-- Search -->
        <div class="staff-controls">
            <input
                v-model="search"
                type="text"
                placeholder="Search by name, employee code, department or designation..."/>
        </div>

        <!-- Loading -->
        <p
            v-if="loading"
            class="state-message"
        >
            Loading staff...
        </p>

        <!-- Error -->
        <p
            v-else-if="errorMessage"
            class="error-message">
            {{ errorMessage }}
        </p>

        <!-- Empty State -->
        <div
            v-else-if="filteredStaff.length === 0"
            class="empty-state">
            <h3>No Staff Found</h3>
            <p v-if="search">
                No staff members match your search.
            </p>
            <p v-else>
                Staff members will appear here once they are created.
            </p>
        </div>

        <!-- Staff Table -->
        <StaffTable
            v-else
            :staff-list="filteredStaff"
            @select-staff="openStaffDetails"/>

        <!-- Staff Details Modal -->
        <StaffDetailsModal
            v-if="selectedStaffUUID"
            :staff-uuid="selectedStaffUUID"
            @close="closeStaffDetails"
            @updated="handleStaffUpdated"/>
    </div>
</template>

<script setup>
import {
    ref,
    computed,
    onMounted
} from "vue"

import { useRouter } from "vue-router"

// Components
import StaffTable from "../../components/admin/StaffTable.vue"
import StaffDetailsModal from "../../components/admin/StaffDetailsModal.vue"

// API Service
import {
    getAllStaff
} from "../../services/admin"

// Router
const router = useRouter()

// Staff Data

// Stores all Staff received from Backend
const staffList = ref([])

// Stores currently selected Staff UUID
const selectedStaffUUID = ref(null)

// Search
const search = ref("")

// Page States
const loading = ref(true)
const errorMessage = ref("")

// Load Staff from Backend
async function loadStaff() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getAllStaff()
        staffList.value =
            response.data.staff || []
    }
    catch (error) {
        console.error(
            "Failed to load staff:",
            error
        )
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load staff members."
    }
    finally {
        loading.value = false
    }
}
// Search / Filter Staff
const filteredStaff = computed(() => {
    const searchValue =
        search.value
            .toLowerCase()
            .trim()
    // No search entered
    if (!searchValue) {
        return staffList.value
    }
    return staffList.value.filter((staff) => {
        const fullName =
            staff.full_name
                ?.toLowerCase() || ""
        const employeeCode =
            staff.employee_code
                ?.toLowerCase() || ""
        const department =
            staff.department
                ?.toLowerCase() || ""
        const designation =
            staff.designation
                ?.toLowerCase() || ""
        const status =
            staff.status
                ?.toLowerCase() || ""
        return (
            fullName.includes(searchValue) ||
            employeeCode.includes(searchValue) ||
            department.includes(searchValue) ||
            designation.includes(searchValue) ||
            status.includes(searchValue)
        )
    })
})
// Navigate to Create Staff
function goToCreateStaff() {
    router.push("/admin/create-staff")
}
// Open Staff Details
function openStaffDetails(staffUUID) {
    selectedStaffUUID.value = staffUUID
}
// Close Staff Details
function closeStaffDetails() {
    selectedStaffUUID.value = null
}
// Staff Updated
async function handleStaffUpdated() {
    // Reload Staff list so the table
    // immediately displays the new status
    await loadStaff()
}
// Component Mounted
onMounted(() => {
    loadStaff()
})
</script>

<style scoped>
/* Main Container */
.staff-container {
    width: 90%;
    max-width: 1400px;
    margin: auto;
    padding: 30px;
}
/* Header */
.staff-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}
h1 {
    color: #2E7D32;
    margin: 0 0 8px;
}
.staff-header p {
    color: #6B7280;
    margin: 0;
}
/* Create Staff Button */
.create-button {
    padding: 12px 20px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    transition: background 0.2s ease;
}
.create-button:hover {
    background: #256428;
}
/* Search */
.staff-controls {
    margin: 30px 0 20px;
}
.staff-controls input {
    width: 420px;
    max-width: 100%;
    padding: 11px 13px;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
    box-sizing: border-box;
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}
.staff-controls input:focus {
    border-color: #2E7D32;
    box-shadow:
        0 0 0 2px rgba(46, 125, 50, 0.1);
}
/* Loading */
.state-message {
    color: #6B7280;
    padding: 20px 0;
}
/* Error */
.error-message {
    color: #B91C1C;
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-radius: 6px;
    padding: 12px 15px;
    margin-top: 20px;
}
/* Empty State */
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
.empty-state p {
    margin: 0;
}
/* Responsive */
@media (max-width: 700px) {
    .staff-container {
        width: 95%;

        padding: 20px 10px;
    }
    .staff-header {
        flex-direction: column;

        align-items: flex-start;
    }
    .create-button {
        width: 100%;
    }
    .staff-controls input {
        width: 100%;
    }
}
</style>