<template>
    <div class="trek-form-container">
        <h2>Create Trek</h2>
        <form @submit.prevent="submitTrek">
            <!-- Row 1 -->
            <div class="form-row">
                <!-- Trek Name -->
                <div class="form-group">
                    <label>Trek Name</label>
                    <input
                        v-model="form.trek_name"
                        type="text"
                        placeholder="Enter Trek Name"
                        required/>
                </div>
                <!-- Location -->
                <div class="form-group">
                    <label>Location</label>
                    <input
                        v-model="form.location"
                        type="text"
                        placeholder="Enter Location"
                        required/>
                </div>
            </div>
            <!-- Row 2 -->
            <div class="form-row">
                <!-- Difficulty -->
                <div class="form-group">
                    <label>Difficulty</label>
                    <select
                        v-model="form.difficulty"
                        required>
                        <option disabled value="">
                            Select Difficulty
                        </option>
                        <option value="EASY">
                            Easy
                        </option>
                        <option value="MODERATE">
                            Moderate
                        </option>
                        <option value="DIFFICULT">
                            Difficult
                        </option>
                        <option value="EXTREME">
                            Extreme
                        </option>
                    </select>
                </div>
                <!-- Guide -->
                <div class="form-group">
                    <label>Assign Guide</label>
                    <select
                        v-model="form.staff_uuid"
                        required>
                        <option disabled value="">
                            Select Guide
                        </option>
                        <option
                            v-for="guide in guides"
                            :key="guide.staff_uuid"
                            :value="guide.staff_uuid">
                            {{ guide.employee_code }}
                            - {{ guide.full_name }}
                        </option>
                    </select>
                    <small
                        v-if="guidesLoading"
                        class="helper-text">
                        Loading eligible guides...
                    </small>
                    <small
                        v-else-if="guides.length === 0"
                        class="error-text">
                        No eligible guides are currently available.
                    </small>
                </div>
            </div>
            <!-- Row 3 -->
            <div class="form-row">
                <!-- Capacity -->
                <div class="form-group">
                    <label>Capacity</label>
                    <input
                        v-model.number="form.capacity"
                        type="number"
                        min="1"
                        placeholder="Enter Capacity"
                        required/>
                </div>
                <!-- Price -->
                <div class="form-group">
                    <label>Price (₹)</label>
                    <input
                        v-model.number="form.price"
                        type="number"
                        min="0"
                        step="0.01"
                        placeholder="Enter Trek Price"
                        required/>
                </div>
            </div>
            <!-- Row 4 -->
            <div class="form-row">
                <!-- Start Date -->
                <div class="form-group">
                    <label>Start Date</label>
                    <input
                        v-model="form.start_date"
                        type="date"
                        required/>
                </div>
                <!-- End Date -->
                <div class="form-group">
                    <label>End Date</label>
                    <input
                        v-model="form.end_date"
                        type="date"
                        required/>
                </div>
            </div>
            <!-- Meeting Point -->
            <div class="form-group">
                <label>Meeting Point</label>
                <input
                    v-model="form.meeting_point"
                    type="text"
                    placeholder="Enter Meeting Point"
                    required/>
            </div>
            <!-- Description -->
            <div class="form-group">
                <label>Description</label>
                <textarea
                    v-model="form.description"
                    rows="5"
                    placeholder="Enter Trek Description"
                    required
                ></textarea>
            </div>
            <!-- Error -->
            <p
                v-if="errorMessage"
                class="error-message">
                {{ errorMessage }}
            </p>
            <!-- Success -->
            <p
                v-if="successMessage"
                class="success-message">
                {{ successMessage }}
            </p>
            <!-- Buttons -->
            <div class="form-actions">
                <button
                    type="button"
                    class="cancel-button"
                    @click="cancel">
                    Cancel
                </button>
                <button
                    type="submit"
                    class="create-button"
                    :disabled="submitting || guidesLoading">
                    {{
                        submitting
                            ? "Creating Trek..."
                            : "Create Trek"
                    }}
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import {ref,reactive,onMounted} from "vue"
import { useRouter } from "vue-router"
import {createTrek,getEligibleGuides} from "../../services/admin"

const router = useRouter()
// Trek Form
const form = reactive({
    trek_name: "",
    location: "",
    difficulty: "",
    staff_uuid: "",
    capacity: null,
    price: null,
    start_date: "",
    end_date: "",
    meeting_point: "",
    description: ""
})
// Eligible Guides
const guides = ref([])
const guidesLoading = ref(false)

// Form States
const submitting = ref(false)
const errorMessage = ref("")
const successMessage = ref("")

// Load Eligible Guides
async function loadEligibleGuides() {
    guidesLoading.value = true
    errorMessage.value = ""
    try {
        const response =
            await getEligibleGuides()
        guides.value =
            response.data.guides || []
    }
    catch (error) {
        console.error(
            "Failed to load eligible guides:",
            error
        )
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load eligible guides."
    }
    finally {
        guidesLoading.value = false
    }
}
// Validate Trek
function validateForm() {
    if (!form.trek_name.trim()) {
        errorMessage.value =
            "Trek name is required."
        return false
    }
    if (!form.location.trim()) {
        errorMessage.value =
            "Location is required."
        return false
    }
    if (!form.difficulty) {
        errorMessage.value =
            "Please select Trek difficulty."

        return false
    }
    if (!form.staff_uuid) {
        errorMessage.value =
            "Please select a Guide."
        return false
    }
    if (
        !form.capacity ||
        form.capacity <= 0
    ) {
        errorMessage.value =
            "Capacity must be greater than 0."
        return false
    }
    if (
        form.price === null ||
        form.price < 0
    ) {
        errorMessage.value =
            "Price cannot be negative."
        return false
    }
    if (
        !form.start_date ||
        !form.end_date
    ) {
        errorMessage.value =
            "Start Date and End Date are required."
        return false
    }
    if (
        new Date(form.end_date) <
        new Date(form.start_date)
    ) {
        errorMessage.value =
            "End Date cannot be before Start Date."
        return false
    }
    if (!form.description.trim()) {
        errorMessage.value =
            "Description is required."
        return false
    }
    return true
}
// Create Trek
async function submitTrek() {
    errorMessage.value = ""
    successMessage.value = ""

    // Frontend Validation
    if (!validateForm()) {
        return
    }
    submitting.value = true
    try {
        // Data sent to Backend
        const trekData = {
            trek_name:
                form.trek_name.trim(),
            location:
                form.location.trim(),
            difficulty:
                form.difficulty,
            staff_uuid:
                form.staff_uuid,
            capacity:
                Number(form.capacity),
            price:
                Number(form.price),
            start_date:
                form.start_date,
            end_date:
                form.end_date,
            meeting_point:
                form.meeting_point.trim(),
            description:
                form.description.trim()
        }
        console.log(
            "Creating Trek:",
            trekData
        )
        const response =
            await createTrek(trekData)
        successMessage.value =
            response.data.message ||
            "Trek created successfully."
        // Return to Trek Management
        setTimeout(() => {
            router.push("/admin/treks")
        }, 1200)
    }
    catch (error) {
        console.error(
            "Create Trek Error:",
            error
        )
        console.error(
            "Backend Response:",
            error.response?.data
        )
        errorMessage.value =
            error.response?.data?.message ||
            error.response?.data?.error ||
            "Unable to create Trek."
    }
    finally {
        submitting.value = false
    }
}
// Cancel
function cancel() {
    router.push("/admin/treks")
}
// Component Mounted
onMounted(() => {

    loadEligibleGuides()
})
</script>

<style scoped>
.trek-form-container {
    width: 100%;
    padding: 30px;
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    box-sizing: border-box;
}
.trek-form-container h2 {
    margin-top: 0;
    margin-bottom: 25px;
    color: #1F2937;
}
/* Form Rows */
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
}
/* Form Group */
.form-group {
    margin-bottom: 20px;
}
label {

    display: block;
    margin-bottom: 7px;
    color: #374151;
    font-weight: 600;
}
input,
select,
textarea {
    width: 100%;
    padding: 11px 12px;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    box-sizing: border-box;
    font-size: 14px;
    background: white;
}
input:focus,
select:focus,
textarea:focus {
    outline: none;
    border-color: #2E7D32;
}
textarea {
    resize: vertical;
}
/* Helper Text */
.helper-text {
    display: block;
    margin-top: 6px;
    color: #6B7280;
}
.error-text {
    display: block;
    margin-top: 6px;
    color: #B91C1C;
}
/* Messages */
.error-message {
    color: #B91C1C;
    margin: 15px 0;
}
.success-message {
    color: #2E7D32;
    margin: 15px 0;
}
/* Actions */
.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 30px;
}
.form-actions button {
    width: auto;
    padding: 11px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
}
.cancel-button {
    background: white;
    color: #374151;
    border: 1px solid #D1D5DB;
}
.cancel-button:hover {
    background: #F9FAFB;
}
.create-button {
    background: #2E7D32;
    color: white;
    border: 1px solid #2E7D32;
}
.create-button:hover:not(:disabled) {
    background: #256428;
}
.create-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
/* Responsive */
@media (max-width: 700px) {
    .form-row {
        grid-template-columns: 1fr;
        gap: 0;}
    .form-actions {
        flex-direction: column;}
    .form-actions button {
        width: 100%;}
}
</style>