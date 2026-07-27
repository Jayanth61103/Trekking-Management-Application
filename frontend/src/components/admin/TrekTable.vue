<template>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Trek ID</th>
                    <th>Trek Name</th>
                    <th>Location</th>
                    <th>Difficulty</th>
                    <th>Guide</th>
                    <th>Capacity</th>
                    <th>Available</th>
                    <th>Start Date</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>

            <tbody>
                <!-- Trek records -->
                <tr
                    v-for="trek in trekList"
                    :key="trek.trek_uuid"
                >
                    <td>{{ trek.trek_id }}</td>
                    <td class="trek-name">{{ trek.trek_name }}</td>
                    <td>{{ trek.location }}</td>
                    <td>{{ trek.difficulty }}</td>
                    <td>
                        {{ trek.assigned_guide?.full_name || "Not Assigned" }}
                    </td>
                    <td>{{ trek.capacity }}</td>
                    <td>{{ trek.available_slots }}</td>
                    <td>{{ trek.start_date }}</td>
                    <td>
                        <span
                            class="status"
                            :class="getStatusClass(trek.status)"
                        >
                            {{ trek.status }}
                        </span>
                    </td>
                    <td>
                        <button
                            class="view-button"
                            @click="selectTrek(trek.trek_uuid)"
                        >
                            View
                        </button>
                    </td>
                </tr>

                <!-- Show when no Treks are available -->
                <tr v-if="trekList.length === 0">
                    <td colspan="10" class="empty-message">
                        No Treks found.
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
// Trek list received from Trek Management page
defineProps({
    trekList: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(["select-trek"])

// Send selected Trek UUID to parent
function selectTrek(trekUuid) {
    emit("select-trek", trekUuid)
}

// Set Trek status colour
function getStatusClass(status) {
    if (status === "Open") return "status-open"
    if (status === "Upcoming") return "status-upcoming"
    if (status === "Full") return "status-full"
    if (status === "Completed") return "status-completed"
    if (status === "Cancelled") return "status-cancelled"
    return ""
}
</script>

<style scoped>
.table-container {
    width: 100%;
    overflow-x: auto;
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th {
    text-align: left;
    padding: 14px;
    background: #F9FAFB;
    color: #374151;
    font-size: 14px;
}

td {
    padding: 14px;
    border-top: 1px solid #E5E7EB;
    color: #4B5563;
}

.trek-name {
    font-weight: 600;
    color: #1F2937;
}

/* Trek status */
.status {
    font-weight: 600;
    font-size: 13px;
}

.status-open {
    color: #2E7D32;
}

.status-upcoming {
    color: #2563EB;
}

.status-full {
    color: #D97706;
}

.status-completed {
    color: #6B7280;
}

.status-cancelled {
    color: #B91C1C;
}

/* View button */
.view-button {
    padding: 7px 14px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.view-button:hover {
    background: #256428;
}

/* Empty table */
.empty-message {
    text-align: center;
    padding: 30px;
    color: #6B7280;
}
</style>