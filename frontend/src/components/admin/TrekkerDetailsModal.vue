<template>
    <div class="modal-overlay" @click.self="closeModal">
        <div class="modal">
            <div class="modal-header">
                <div>
                    <h2>Trekker Details</h2>
                    <p v-if="trekker" class="trekker-code">{{ trekker.trekker_uuid }}</p>
                </div>
                <button class="close-button" @click="closeModal">×</button>
            </div>

            <div v-if="loading" class="message">Loading trekker details...</div>
            <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

            <div v-else-if="trekker">
                <div class="trekker-info">
                    <div><span>Full Name</span><strong>{{ trekker.full_name }}</strong></div>
                    <div><span>Username</span><strong>{{ trekker.username }}</strong></div>
                    <div><span>Email</span><strong>{{ trekker.email }}</strong></div>
                    <div><span>Phone</span><strong>{{ trekker.phone }}</strong></div>
                    <div><span>Total Bookings</span><strong>{{ trekker.total_bookings }}</strong></div>
                    <div>
                        <span>Status</span>
                        <strong class="status-badge" :class="getStatusClass(trekker.status)">
                            {{ trekker.status }}
                        </strong>
                    </div>
                </div>

                <div class="actions">
                    <button
                        v-if="trekker.status === 'Active'"
                        class="deactivate-button"
                        :disabled="updating"
                        @click="changeStatus('INACTIVE')">
                        {{ updating ? "Updating..." : "Deactivate Trekker" }}
                    </button>

                    <button
                        v-if="trekker.status !== 'Active'"
                        class="activate-button"
                        :disabled="updating"
                        @click="changeStatus('ACTIVE')">
                        {{ updating ? "Updating..." : "Reactivate Trekker" }}
                    </button>

                    <button
                        v-if="trekker.status !== 'Blocked'"
                        class="block-button"
                        :disabled="updating"
                        @click="changeStatus('BLOCKED')">
                        {{ updating ? "Updating..." : "Blacklist Trekker" }}
                    </button>
                </div>

                <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getTrekkerDetails, updateTrekkerStatus } from "../../services/admin"

const props = defineProps({
    trekkerUuid: {
        type: String,
        required: true
    }
})

const emit = defineEmits(["close", "updated"])

const trekker = ref(null)
const loading = ref(true)
const updating = ref(false)
const errorMessage = ref("")
const successMessage = ref("")

async function loadTrekkerDetails() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getTrekkerDetails(props.trekkerUuid)
        trekker.value = response.data.trekker
    }
    catch (error) {
        console.error("Failed to load trekker details:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load trekker details."
    }
    finally {
        loading.value = false
    }
}

async function changeStatus(status) {
    let confirmationMessage = ""
    if (status === "INACTIVE") confirmationMessage = "Deactivate this trekker's account?"
    if (status === "ACTIVE") confirmationMessage = "Reactivate this trekker's account?"
    if (status === "BLOCKED") confirmationMessage = "Blacklist this trekker? They will be blocked from the platform."

    if (confirmationMessage && !window.confirm(confirmationMessage)) {
        return
    }

    try {
        updating.value = true
        errorMessage.value = ""
        successMessage.value = ""

        const response = await updateTrekkerStatus(props.trekkerUuid, status)

        trekker.value.status = response.data.trekker.status
        trekker.value.is_active = response.data.trekker.is_active
        successMessage.value = response.data.message

        emit("updated")
    }
    catch (error) {
        console.error("Failed to update trekker status:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to update trekker status."
    }
    finally {
        updating.value = false
    }
}

function getStatusClass(status) {
    if (status === "Active") return "status-active"
    if (status === "Inactive") return "status-inactive"
    if (status === "Blocked") return "status-blocked"
    return ""
}

function closeModal() {
    emit("close")
}

onMounted(() => {
    loadTrekkerDetails()
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
    max-width: 600px;
    max-height: 85vh;
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
.trekker-code { margin: 5px 0 0; color: #6B7280; font-size: 14px; }
.close-button { border: none; background: none; font-size: 28px; color: #6B7280; cursor: pointer; }
.trekker-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}
.trekker-info div { display: flex; flex-direction: column; gap: 5px; }
.trekker-info span { font-size: 13px; color: #6B7280; }
.trekker-info strong { font-size: 15px; color: #1F2937; }
.status-badge { width: fit-content; padding: 5px 10px; border-radius: 20px; }
.status-active { background: #DCFCE7; color: #166534 !important; }
.status-inactive { background: #F3F4F6; color: #4B5563 !important; }
.status-blocked { background: #FEE2E2; color: #991B1B !important; }
.actions {
    margin-top: 30px;
    display: flex;
    gap: 12px;
    border-top: 1px solid #E5E7EB;
    padding-top: 20px;
}
.actions button {
    border: none;
    border-radius: 6px;
    padding: 10px 18px;
    color: white;
    cursor: pointer;
    font-weight: 600;
}
.actions button:disabled { opacity: 0.6; cursor: not-allowed; }
.deactivate-button { background: #D97706; }
.activate-button { background: #2E7D32; }
.block-button { background: #B91C1C; }
.message { text-align: center; padding: 30px; color: #6B7280; }
.error-message { color: #B91C1C; margin-top: 15px; }
.success-message { color: #2E7D32; margin-top: 15px; font-weight: 600; }
@media (max-width: 600px) {
    .trekker-info { grid-template-columns: 1fr; }
    .actions { flex-direction: column; }
}
</style>