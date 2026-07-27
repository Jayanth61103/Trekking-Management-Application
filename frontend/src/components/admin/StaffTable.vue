<template>
    <div class="table-container">

        <table>
            <!-- Table Header -->
            <thead>
                <tr>
                    <th>Employee Code</th>
                    <th>Name</th>
                    <th>Department</th>
                    <th>Designation</th>
                    <th>Experience</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>

            <!-- Table Body -->
            <tbody>
                <tr
                    v-for="staff in staffList"
                    :key="staff.staff_uuid"
                    class="staff-row">
                    <!-- Employee Code -->
                    <td>
                        {{ staff.employee_code }}
                    </td>
                    <!-- Staff Name -->
                    <td>
                        {{ staff.full_name }}
                    </td>
                    <!-- Department -->
                    <td>
                        {{ staff.department }}
                    </td>
                    <!-- Designation -->
                    <td>
                        {{ staff.designation }}
                    </td>
                    <!-- Experience -->
                    <td>
                        {{ staff.experience_years }} years
                    </td>
                    <!-- Status -->
                    <td>
                        <span
                            class="status"
                            :class="getStatusClass(staff.status)">
                            {{ staff.status }}
                        </span>
                    </td>
                    <!-- Action -->
                    <td>
                        <button
                            class="view-button"
                            @click="selectStaff(staff.staff_uuid)">
                            View
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
// Receive Staff List from Parent
defineProps({
    staffList: {
        type: Array,
        required: true
    }
})
// Events sent to Parent Component
const emit = defineEmits([
    "select-staff"
])
// Send Selected Staff UUID to Parent
function selectStaff(staffUUID) {
    emit(
        "select-staff",
        staffUUID
    )
}
// Return CSS Class based on Staff Status
function getStatusClass(status) {
    if (status === "Active") {
        return "status-active"
    }
    if (status === "Suspended") {
        return "status-suspended"
    }
    if (status === "Inactive") {
        return "status-inactive"
    }
    if (status === "Dismissed") {
        return "status-dismissed"
    }
    return ""
}
</script>

<style scoped>
/* Table Container */
.table-container {
    width: 100%;
    overflow-x: auto;
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
}
/* Table */
table {
    width: 100%;
    border-collapse: collapse;
}
/* Table Header */
th {
    text-align: left;
    padding: 14px;
    background: #F9FAFB;
    color: #374151;
    font-size: 14px;
    font-weight: 600;
}
/* Table Data */
td {
    padding: 14px;
    border-top: 1px solid #E5E7EB;
    color: #4B5563;
}
/* Staff Row */
.staff-row {
    transition: background 0.2s ease;
}
.staff-row:hover {
    background: #F9FAFB;
}
/* Status */
.status {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}
/* Active */
.status-active {
    background: #DCFCE7;
    color: #166534;
}
/* Suspended */
.status-suspended {
    background: #FEF3C7;
    color: #92400E;
}
/* Inactive */
.status-inactive {
    background: #F3F4F6;
    color: #4B5563;
}
/* Dismissed */
.status-dismissed {
    background: #FEE2E2;
    color: #991B1B;
}
/* View Button */
.view-button {
    padding: 7px 14px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.2s ease;
}
.view-button:hover {
    background: #256428;
}
</style>