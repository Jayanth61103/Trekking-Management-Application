<template>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Trek Name</th>
                    <th>Location</th>
                    <th>Difficulty</th>
                    <th>Participants</th>
                    <th>Available Slots</th>
                    <th>Start Date</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="trek in trekList" :key="trek.trek_uuid" class="trek-row">
                    <td class="trek-name">{{ trek.trek_name }}</td>
                    <td>{{ trek.location }}</td>
                    <td>{{ trek.difficulty }}</td>
                    <td>{{ trek.participants_count }}</td>
                    <td>{{ trek.available_slots }} / {{ trek.capacity }}</td>
                    <td>{{ trek.start_date }}</td>
                    <td>
                        <span class="status" :class="getStatusClass(trek.status)">
                            {{ trek.status }}
                        </span>
                    </td>
                    <td>
                        <button class="view-button" @click="selectTrek(trek.trek_uuid)">
                            Manage
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
defineProps({
    trekList: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(["select-trek"])

function selectTrek(trekUuid) {
    emit("select-trek", trekUuid)
}

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
table { width: 100%; border-collapse: collapse; }
th {
    text-align: left;
    padding: 14px;
    background: #F9FAFB;
    color: #374151;
    font-size: 14px;
    font-weight: 600;
}
td {
    padding: 14px;
    border-top: 1px solid #E5E7EB;
    color: #4B5563;
}
.trek-name { font-weight: 600; color: #1F2937; }
.trek-row:hover { background: #F9FAFB; }
.status {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}
.status-open { background: #DCFCE7; color: #166534; }
.status-upcoming { background: #DBEAFE; color: #1E40AF; }
.status-full { background: #FEF3C7; color: #92400E; }
.status-completed { background: #F3F4F6; color: #374151; }
.status-cancelled { background: #FEE2E2; color: #991B1B; }
.view-button {
    padding: 7px 14px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.view-button:hover { background: #256428; }
</style>