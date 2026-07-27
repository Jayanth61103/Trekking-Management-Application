<template>
    <div class="modal-overlay" @click.self="closeModal">
        <div class="modal">
            <!-- Header -->
            <div class="modal-header">
                <div>
                    <h2>{{ editMode ? "Edit Trek" : "Trek Details" }}</h2>
                    <p v-if="trek" class="trek-code">{{ trek.trek_uuid }}</p>
                </div>
                <button class="close-button" @click="closeModal">×</button>
            </div>

            <!-- Loading and error states -->
            <div v-if="loading" class="message">Loading Trek details...</div>
            <div v-else-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>

            <!-- Trek content -->
            <div v-else-if="trek">
                <!-- View Trek details -->
                <div v-if="!editMode">
                    <div class="trek-info">
                        <div>
                            <span>Trek Name</span>
                            <strong>{{ trek.trek_name }}</strong>
                        </div>
                        <div>
                            <span>Location</span>
                            <strong>{{ trek.location }}</strong>
                        </div>
                        <div>
                            <span>Difficulty</span>
                            <strong>{{ trek.difficulty }}</strong>
                        </div>
                        <div>
                            <span>Duration</span>
                            <strong>{{ trek.duration_days }} Days</strong>
                        </div>
                        <div>
                            <span>Capacity</span>
                            <strong>{{ trek.capacity }}</strong>
                        </div>
                        <div>
                            <span>Available Slots</span>
                            <strong>{{ trek.available_slots }}</strong>
                        </div>
                        <div>
                            <span>Price</span>
                            <strong>₹{{ trek.price }}</strong>
                        </div>
                        <div>
                            <span>Status</span>
                            <strong class="status-badge" :class="getStatusClass(trek.status)">
                                {{ trek.status }}
                            </strong>
                        </div>
                        <div>
                            <span>Start Date</span>
                            <strong>{{ trek.start_date }}</strong>
                        </div>
                        <div>
                            <span>End Date</span>
                            <strong>{{ trek.end_date }}</strong>
                        </div>
                        <div>
                            <span>Meeting Point</span>
                            <strong>{{ trek.meeting_point || "-" }}</strong>
                        </div>
                        <div>
                            <span>Assigned Staff</span>
                            <strong v-if="trek.assigned_staff">
                                {{ trek.assigned_staff.full_name }}
                                ({{ trek.assigned_staff.employee_code }})
                            </strong>
                            <strong v-else>Not Assigned</strong>
                        </div>
                    </div>

                    <!-- Description -->
                    <div class="description-section">
                        <span>Description</span>
                        <p>{{ trek.description }}</p>
                    </div>

                    <!-- Actions -->
                    <div class="actions">
                        <button class="edit-button" @click="startEditing">
                            Edit Trek
                        </button>
                    </div>
                </div>

                <!-- Edit Trek details -->
                <form v-else @submit.prevent="saveChanges">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Trek Name</label>
                            <input v-model="form.trek_name" type="text" required />
                        </div>

                        <div class="form-group">
                            <label>Location</label>
                            <input v-model="form.location" type="text" required />
                        </div>

                        <div class="form-group">
                            <label>Difficulty</label>
                            <select v-model="form.difficulty" required>
                                <option value="Easy">Easy</option>
                                <option value="Moderate">Moderate</option>
                                <option value="Difficult">Difficult</option>
                                <option value="Extreme">Extreme</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Capacity</label>
                            <input
                                v-model.number="form.capacity"
                                type="number"
                                min="1"
                                required
                            />
                        </div>

                        <div class="form-group">
                            <label>Price</label>
                            <input
                                v-model.number="form.price"
                                type="number"
                                min="0"
                                step="0.01"
                                required
                            />
                        </div>

                        <div class="form-group">
                            <label>Status</label>
                            <select v-model="form.status" required>
                                <option value="Upcoming">Upcoming</option>
                                <option value="Open">Open</option>
                                <option value="Full">Full</option>
                                <option value="Completed">Completed</option>
                                <option value="Cancelled">Cancelled</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Start Date</label>
                            <input v-model="form.start_date" type="date" required />
                        </div>

                        <div class="form-group">
                            <label>End Date</label>
                            <input v-model="form.end_date" type="date" required />
                        </div>

                        <div class="form-group full-width">
                            <label>Meeting Point</label>
                            <input v-model="form.meeting_point" type="text" />
                        </div>

                        <div class="form-group full-width">
                            <label>Description</label>
                            <textarea v-model="form.description" required></textarea>
                        </div>
                    </div>

                    <!-- Edit actions -->
                    <div class="actions">
                        <button
                            type="button"
                            class="cancel-button"
                            :disabled="updating"
                            @click="cancelEditing"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            class="save-button"
                            :disabled="updating"
                        >
                            {{ updating ? "Updating..." : "Save Changes" }}
                        </button>
                    </div>
                </form>

                <p v-if="successMessage" class="success-message">
                    {{ successMessage }}
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { getTrekDetails, updateTrek } from "../../services/admin"

// Props and events
const props = defineProps({
    trekUuid: {
        type: String,
        required: true
    }
})

const emit = defineEmits(["close", "updated"])

// Trek data and page states
const trek = ref(null)
const loading = ref(true)
const updating = ref(false)
const editMode = ref(false)
const errorMessage = ref("")
const successMessage = ref("")

// Edit form
const form = reactive({
    trek_name: "",
    location: "",
    difficulty: "",
    capacity: 0,
    price: 0,
    start_date: "",
    end_date: "",
    meeting_point: "",
    description: "",
    status: ""
})

// Load Trek details
async function loadTrekDetails() {
    try {
        loading.value = true
        errorMessage.value = ""

        const response = await getTrekDetails(props.trekUuid)
        trek.value = response.data.trek
    }
    catch (error) {
        console.error("Failed to load Trek details:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load Trek details."
    }
    finally {
        loading.value = false
    }
}

// Start editing Trek
function startEditing() {
    successMessage.value = ""
    errorMessage.value = ""

    form.trek_name = trek.value.trek_name
    form.location = trek.value.location
    form.difficulty = trek.value.difficulty
    form.capacity = trek.value.capacity
    form.price = trek.value.price
    form.start_date = trek.value.start_date
    form.end_date = trek.value.end_date
    form.meeting_point = trek.value.meeting_point || ""
    form.description = trek.value.description
    form.status = trek.value.status

    editMode.value = true
}

// Cancel editing
function cancelEditing() {
    editMode.value = false
    errorMessage.value = ""
}

// Save Trek changes
async function saveChanges() {
    if (form.start_date && form.end_date && form.end_date < form.start_date) {
        errorMessage.value = "End date cannot be before start date."
        return
    }

    if (!window.confirm("Are you sure you want to update this Trek?")) {
        return
    }

    try {
        updating.value = true
        errorMessage.value = ""
        successMessage.value = ""

        const updateData = {
            trek_name: form.trek_name,
            location: form.location,
            difficulty: form.difficulty,
            capacity: form.capacity,
            price: form.price,
            start_date: form.start_date,
            end_date: form.end_date,
            meeting_point: form.meeting_point,
            description: form.description,
            status: form.status
        }

        const response = await updateTrek(props.trekUuid, updateData)

        // Reload updated Trek from backend
        await loadTrekDetails()
        successMessage.value = response.data.message
        editMode.value = false

        // Refresh Trek list in parent
        emit("updated")
    }
    catch (error) {
        console.error("Failed to update Trek:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to update Trek."
    }
    finally {
        updating.value = false
    }
}

// Set status colour
function getStatusClass(status) {
    if (status === "Open") return "status-open"
    if (status === "Upcoming") return "status-upcoming"
    if (status === "Full") return "status-full"
    if (status === "Completed") return "status-completed"
    if (status === "Cancelled") return "status-cancelled"
    return ""
}

// Close modal
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
    max-width: 800px;
    max-height: 85vh;
    overflow-y: auto;
    border-radius: 12px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

/* Modal header */
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

.trek-code {
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

/* Trek information */
.trek-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.trek-info div {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.trek-info span,
.description-section span {
    font-size: 13px;
    color: #6B7280;
}

.trek-info strong {
    font-size: 15px;
    color: #1F2937;
}

.description-section {
    margin-top: 25px;
}

.description-section p {
    color: #1F2937;
    line-height: 1.6;
}

/* Edit form */
.form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    font-size: 13px;
    color: #4B5563;
    font-weight: 600;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
}

.form-group textarea {
    min-height: 110px;
    resize: vertical;
}

/* Trek status */
.status-badge {
    width: fit-content;
    padding: 5px 10px;
    border-radius: 20px;
}

.status-open {
    background: #DCFCE7;
    color: #166534 !important;
}

.status-upcoming {
    background: #DBEAFE;
    color: #1E40AF !important;
}

.status-full {
    background: #FEF3C7;
    color: #92400E !important;
}

.status-completed {
    background: #F3F4F6;
    color: #374151 !important;
}

.status-cancelled {
    background: #FEE2E2;
    color: #991B1B !important;
}

/* Action buttons */
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

.edit-button,
.save-button {
    background: #2E7D32;
}

.cancel-button {
    background: #6B7280;
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

/* Mobile layout */
@media (max-width: 600px) {
    .trek-info,
    .form-grid {
        grid-template-columns: 1fr;
    }

    .full-width {
        grid-column: auto;
    }

    .actions {
        flex-direction: column;
    }
}
</style>