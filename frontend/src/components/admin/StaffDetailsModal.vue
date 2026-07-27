<template>
    <div
        class="modal-overlay"
        @click.self="closeModal">
        <div class="modal">
            <!-- Modal Header -->
            <div class="modal-header">
                <div>
                    <h2>Staff Details</h2>
                    <p
                        v-if="staff"
                        class="employee-code">
                        {{ staff.employee_code }}
                    </p>
                </div>
                <button
                    class="close-button"
                    @click="closeModal">
                    ×
                </button>

            </div>
            <!-- Loading -->
            <div
                v-if="loading"
                class="message">
                Loading staff details...
            </div>
            <!-- Error -->
            <div
                v-else-if="errorMessage"
                class="error-message">
                {{ errorMessage }}
            </div>

            <!-- Staff Details -->
            <div v-else-if="staff">
                <div class="staff-info">
                    <div>
                        <span>Employee Code</span>
                        <strong>
                            {{ staff.employee_code }}
                        </strong>
                    </div>
                    <div>
                        <span>Full Name</span>
                        <strong>
                            {{ staff.full_name }}
                        </strong>
                    </div>
                    <div>
                        <span>Username</span>
                        <strong>
                            {{ staff.username }}
                        </strong>
                    </div>
                    <div>
                        <span>Email</span>
                        <strong>
                            {{ staff.email }}
                        </strong>
                    </div>
                    <div>
                        <span>Phone</span>
                        <strong>
                            {{ staff.phone }}
                        </strong>
                    </div>
                    <div>
                        <span>Department</span>
                        <strong>
                            {{ staff.department }}
                        </strong>
                    </div>
                    <div>
                        <span>Designation</span>
                        <strong>
                            {{ staff.designation }}
                        </strong>
                    </div>
                    <div>
                        <span>Joining Date</span>
                        <strong>
                            {{ staff.joining_date }}
                        </strong>
                    </div>

                    <div>
                        <span>Experience</span>
                        <strong>
                            {{ staff.experience_years }} Years
                        </strong>
                    </div>

                    <div>
                        <span>Status</span>
                        <strong
                            class="status-badge"
                            :class="getStatusClass(staff.status)">
                            {{ staff.status }}
                        </strong>
                    </div>
                </div>

                <!-- Status Controls -->
                <div class="actions">

                    <!-- Suspend -->
                    <button
                        v-if="staff.status === 'Active'"
                        class="suspend-button"
                        :disabled="updating"
                        @click="changeStatus('SUSPENDED')">
                        {{ updating ? "Updating..." : "Suspend Staff" }}
                    </button>

                    <!-- Reactivate -->
                    <button
                        v-if="
                            staff.status === 'Suspended' ||
                            staff.status === 'Inactive'
                        "
                        class="activate-button"
                        :disabled="updating"
                        @click="changeStatus('ACTIVE')">
                        {{ updating ? "Updating..." : "Reactivate Staff" }}
                    </button>

                    <!-- Dismiss -->
                    <button
                        v-if="staff.status !== 'Dismissed'"
                        class="dismiss-button"
                        :disabled="updating"
                        @click="changeStatus('DISMISSED')">
                        {{ updating ? "Updating..." : "Dismiss Staff" }}
                    </button>

                </div>

                <!-- Success Message -->
                <p
                    v-if="successMessage"
                    class="success-message">
                    {{ successMessage }}
                </p>
            </div>
        </div>
    </div>
</template>


<script setup>
import {
    ref,
    onMounted
} from "vue"
import {
    getStaffDetails,
    updateStaffStatus
} from "../../services/admin"

// Props
const props = defineProps({
    staffUuid: {
        type: String,
        required: true
    }
})

// Events
const emit = defineEmits([
    "close",
    "updated"
])

// Staff Data
const staff = ref(null)

// Component States
const loading = ref(true)
const updating = ref(false)
const errorMessage = ref("")
const successMessage = ref("")

// Load Staff Details
async function loadStaffDetails() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response =
            await getStaffDetails(
                props.staffUuid
            )
        staff.value =
            response.data.staff
    }
    catch (error) {
        console.error(
            "Failed to load staff details:",
            error
        )
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load staff details."
    }
    finally {

        loading.value = false
    }
}

// Change Staff Status
async function changeStatus(status) {

    // Confirmation message
    let confirmationMessage = ""
    if (status === "SUSPENDED") {
        confirmationMessage =
            "Are you sure you want to suspend this staff member?"
    }

    if (status === "ACTIVE") {
        confirmationMessage =
            "Are you sure you want to reactivate this staff member?"}
    if (status === "DISMISSED") {
        confirmationMessage =
            "Are you sure you want to dismiss this staff member?"
    }
    // Ask Admin for confirmation
    if (
        confirmationMessage &&
        !window.confirm(confirmationMessage)
    ) {
        return
    }
    try {
        updating.value = true
        errorMessage.value = ""
        successMessage.value = ""
        const response =
            await updateStaffStatus(
                props.staffUuid,
                status
            )
        // Update Modal Data
        staff.value.status =
            response.data.staff.status
        staff.value.is_active =
            response.data.staff.is_active
        // Show Backend Message
        successMessage.value =
            response.data.message
        // Tell Parent to refresh Staff Table
        emit("updated")
    }
    catch (error) {
        console.error(
            "Failed to update staff status:",
            error
        )
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to update staff status."
    }
    finally {
        updating.value = false
    }
}
// Status Styling
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
// Close Modal
function closeModal() {
    emit("close")
}
// Load when Modal Opens
onMounted(() => {

    loadStaffDetails()
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
    max-width: 700px;
    max-height: 85vh;
    overflow-y: auto;
    border-radius: 12px;
    padding: 28px;
    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.15);
}
/* Header */
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 25px;
    padding-bottom: 20px;
    border-bottom: 1px solid #E5E7EB;
}
.modal-header h2 {
    color: #2E7D32;
    margin: 0;
}
.employee-code {
    margin: 5px 0 0;
    color: #6B7280;
    font-size: 14px;
}
.close-button {
    border: none;
    background: none;
    font-size: 28px;
    color: #6B7280;
    cursor: pointer;
}
/* Staff Information */
.staff-info {
    display: grid;
    grid-template-columns:
        repeat(2, 1fr);
    gap: 20px;
}
.staff-info div {
    display: flex;
    flex-direction: column;
    gap: 5px;
}
.staff-info span {
    font-size: 13px;
    color: #6B7280;
}
.staff-info strong {
    font-size: 15px;
    color: #1F2937;
}
/* Status */
.status-badge {
    width: fit-content;
    padding: 5px 10px;
    border-radius: 20px;
}
.status-active {
    background: #DCFCE7;
    color: #166534 !important;
}
.status-suspended {
    background: #FEF3C7;
    color: #92400E !important;
}
.status-inactive {
    background: #F3F4F6;
    color: #4B5563 !important;
}
.status-dismissed {
    background: #FEE2E2;
    color: #991B1B !important;
}
/* Actions */
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
.actions button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
.suspend-button {
    background: #D97706;
}
.activate-button {
    background: #2E7D32;
}
.dismiss-button {
    background: #B91C1C;
}
/* Messages */
.message {
    text-align: center;
    padding: 30px;
    color: #6B7280;
}
.error-message {
    color: #B91C1C;
    margin-top: 15px;
}
.success-message {
    color: #2E7D32;
    margin-top: 15px;
    font-weight: 600;
}
/* Responsive */
@media (max-width: 600px) {
    .staff-info {
        grid-template-columns: 1fr;
    }
    .actions {
        flex-direction: column;
    }
}
</style>