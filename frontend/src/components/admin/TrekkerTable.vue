<template>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Full Name</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Bookings</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="trekker in trekkerList"
                    :key="trekker.trekker_uuid"
                    class="trekker-row">
                    <td>{{ trekker.full_name }}</td>
                    <td>{{ trekker.username }}</td>
                    <td>{{ trekker.email }}</td>
                    <td>{{ trekker.phone }}</td>
                    <td>{{ trekker.total_bookings }}</td>
                    <td>
                        <span class="status" :class="getStatusClass(trekker.status)">
                            {{ trekker.status }}
                        </span>
                    </td>
                    <td>
                        <button class="view-button" @click="selectTrekker(trekker.trekker_uuid)">
                            View
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
defineProps({
    trekkerList: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(["select-trekker"])

function selectTrekker(trekkerUUID) {
    emit("select-trekker", trekkerUUID)
}

function getStatusClass(status) {
    if (status === "Active") return "status-active"
    if (status === "Inactive") return "status-inactive"
    if (status === "Blocked") return "status-blocked"
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
.trekker-row:hover { background: #F9FAFB; }
.status {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}
.status-active { background: #DCFCE7; color: #166534; }
.status-inactive { background: #F3F4F6; color: #4B5563; }
.status-blocked { background: #FEE2E2; color: #991B1B; }
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