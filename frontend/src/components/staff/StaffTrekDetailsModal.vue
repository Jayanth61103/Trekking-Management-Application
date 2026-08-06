<template>
    <div class="modal-overlay" @click.self="closeModal">
        <div class="modal">
            <div class="modal-header">
                <div>
                    <h2>Manage Trek</h2>
                    <p v-if="trek" class="trek-code">{{ trek.trek_uuid }}</p>
                </div>
                <button class="close-button" @click="closeModal">×</button>
            </div>

            <div v-if="loading" class="message">Loading trek details...</div>
            <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

            <div v-else-if="trek">
                <div class="trek-info">
                    <div><span>Trek Name</span><strong>{{ trek.trek_name }}</strong></div>
                    <div><span>Location</span><strong>{{ trek.location }}</strong></div>
                    <div><span>Difficulty</span><strong>{{ trek.difficulty }}</strong></div>
                    <div><span>Capacity</span><strong>{{ trek.capacity }}</strong></div>
                    <div>
                        <span>Status</span>
                        <strong class="status-badge" :class="getStatusClass(trek.status)">
                            {{ trek.status }}
                        </strong>
                    </div>
                    <div><span>Dates</span><strong>{{ trek.start_date }} – {{ trek.end_date }}</strong></div>
                </div>

                <!-- Update Slots -->
                <div class="control-block">
                    <label>Available Slots</label>
                    <div class="slots-row">
                        <input
                            v-model.number="slotsInput"
                            type="number"
                            min="0"
                            :max="trek.capacity"/>
                        <button
                            class="save-button"
                            :disabled="updatingSlots"
                            @click="saveSlots">
                            {{ updatingSlots ? "Saving..." : "Update Slots" }}
                        </button>
                    </div>
                </div>

                <!-- Update Status -->
                <div class="control-block">
                    <label>Trek Status</label>
                    <div class="status-actions">
                        <button
                            v-if="trek.status === 'Upcoming'"
                            class="status-button open-button"
                            :disabled="updatingStatus"
                            @click="changeStatus('OPEN')">
                            Mark as Open
                        </button>
                        <button
                            v-if="trek.status === 'Open'"
                            class="status-button complete-button"
                            :disabled="updatingStatus"
                            @click="changeStatus('COMPLETED')">
                            Mark as Completed
                        </button>
                        <button
                            v-if="trek.status !== 'Completed' && trek.status !== 'Cancelled'"
                            class="status-button cancel-button"
                            :disabled="updatingStatus"
                            @click="changeStatus('CANCELLED')">
                            Cancel Trek
                        </button>
                        <span v-if="trek.status === 'Completed' || trek.status === 'Cancelled'" class="locked-note">
                            This trek's status is final and cannot be changed.
                        </span>
                    </div>
                </div>

                <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

                <!-- Participants -->
                <div class="participants-section">
                    <h3>Participants ({{ totalParticipants }})</h3>
                    <div v-if="participants.length === 0" class="empty-participants">
                        No trekkers have booked this trek yet.
                    </div>
                    <table v-else class="participants-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>People</th>
                                <th>Booking Status</th>
                                <th>Payment</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="p in participants" :key="p.booking_uuid">
                                <td>{{ p.trekker_name }}</td>
                                <td>{{ p.email }}</td>
                                <td>{{ p.number_of_people }}</td>
                                <td>{{ p.booking_status }}</td>
                                <td>{{ p.payment_status }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import {
    getMyTrekDetails,
    updateTrekSlots,
    updateTrekStatus
} from "../../services/staff"

const props = defineProps({
    trekUuid: {
        type: String,
        required: true
    }
})

const emit = defineEmits(["close", "updated"])

const trek = ref(null)
const participants = ref([])
const totalParticipants = ref(0)
const slotsInput = ref(0)

const loading = ref(true)
const updatingSlots = ref(false)
const updatingStatus = ref(false)
const errorMessage = ref("")
const successMessage = ref("")

async function loadTrekDetails() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getMyTrekDetails(props.trekUuid)
        trek.value = response.data.trek
        participants.value = response.data.participants || []
        totalParticipants.value = response.data.total_participants
        slotsInput.value = trek.value.available_slots
    }
    catch (error) {
        console.error("Failed to load trek details:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load trek details."
    }
    finally {
        loading.value = false
    }
}

async function saveSlots() {
    try {
        updatingSlots.value = true
        errorMessage.value = ""
        successMessage.value = ""

        const response = await updateTrekSlots(props.trekUuid, slotsInput.value)
        trek.value.available_slots = response.data.trek.available_slots
        successMessage.value = response.data.message

        emit("updated")
    }
    catch (error) {
        console.error("Failed to update slots:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to update slots."
    }
    finally {
        updatingSlots.value = false
    }
}

async function changeStatus(status) {
    if (!window.confirm(`Are you sure you want to change this trek's status?`)) {
        return
    }

    try {
        updatingStatus.value = true
        errorMessage.value = ""
        successMessage.value = ""

        const response = await updateTrekStatus(props.trekUuid, status)
        trek.value.status = response.data.trek.status
        successMessage.value = response.data.message

        emit("updated")
    }
    catch (error) {
        console.error("Failed to update trek status:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to update trek status."
    }
    finally {
        updatingStatus.value = false
    }
}

function getStatusClass(status) {
    if (status === "Open") return "status-open"
    if (status === "Upcoming") return "status-upcoming"
    if (status === "Full") return "status-full"
    if (status === "Completed") return "status-completed"
    if (status === "Cancelled") return "status-cancelled"
    return ""
}

function closeModal() {
    emit("close")
}

onMounted(() => {
    loadTrekDetails()
})
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    z-index: 1000;
}
.modal {
    background: white;
    width: 90%;
    max-width: 750px;
    max-height: 88vh;
    overflow-y: auto;
    border-radius: 12px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 25px;
    padding-bottom: 20px;
    border-bottom: 1px solid #E5E7EB;
}
.modal-header h2 { color: #2E7D32; margin: 0; }
.trek-code { margin: 5px 0 0; color: #6B7280; font-size: 14px; }
.close-button { border: none; background: none; font-size: 28px; color: #6B7280; cursor: pointer; }
.trek-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}
.trek-info div { display: flex; flex-direction: column; gap: 5px; }
.trek-info span { font-size: 13px; color: #6B7280; }
.trek-info strong { font-size: 15px; color: #1F2937; }
.status-badge { width: fit-content; padding: 5px 10px; border-radius: 20px; }
.status-open { background: #DCFCE7; color: #166534 !important; }
.status-upcoming { background: #DBEAFE; color: #1E40AF !important; }
.status-full { background: #FEF3C7; color: #92400E !important; }
.status-completed { background: #F3F4F6; color: #374151 !important; }
.status-cancelled { background: #FEE2E2; color: #991B1B !important; }
.control-block {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #E5E7EB;
}
.control-block label {
    display: block;
    font-weight: 600;
    color: #374151;
    margin-bottom: 10px;
}
.slots-row {
    display: flex;
    gap: 10px;
}
.slots-row input {
    width: 120px;
    padding: 9px 10px;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
}
.save-button,
.status-button {
    border: none;
    border-radius: 6px;
    padding: 9px 16px;
    color: white;
    cursor: pointer;
    font-weight: 600;
}
.save-button { background: #2E7D32; }
.save-button:disabled,
.status-button:disabled { opacity: 0.6; cursor: not-allowed; }
.status-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}
.open-button { background: #2E7D32; }
.complete-button { background: #2563EB; }
.cancel-button { background: #B91C1C; }
.locked-note { color: #6B7280; font-size: 13px; }
.message { text-align: center; padding: 30px; color: #6B7280; }
.error-message { color: #B91C1C; margin-top: 15px; }
.success-message { color: #2E7D32; margin-top: 15px; font-weight: 600; }
.participants-section {
    margin-top: 25px;
    padding-top: 20px;
    border-top: 1px solid #E5E7EB;
}
.participants-section h3 {
    color: #1F2937;
    margin: 0 0 15px;
}
.empty-participants {
    color: #6B7280;
    padding: 20px 0;
}
.participants-table {
    width: 100%;
    border-collapse: collapse;
}
.participants-table th {
    text-align: left;
    padding: 10px;
    background: #F9FAFB;
    font-size: 13px;
    color: #374151;
}
.participants-table td {
    padding: 10px;
    border-top: 1px solid #E5E7EB;
    font-size: 14px;
    color: #4B5563;
}
@media (max-width: 600px) {
    .trek-info { grid-template-columns: 1fr; }
}
</style>