<template>
    <div class="modal-overlay" @click.self="closeModal">
        <div class="modal">
            <div class="modal-header">
                <h2>{{ trek ? trek.trek_name : "Trek Details" }}</h2>
                <button class="close-button" @click="closeModal">×</button>
            </div>

            <div v-if="loading" class="message">Loading trek details...</div>
            <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

            <div v-else-if="trek">
                <div class="trek-info">
                    <div><span>Location</span><strong>{{ trek.location }}</strong></div>
                    <div><span>Difficulty</span><strong>{{ trek.difficulty }}</strong></div>
                    <div><span>Duration</span><strong>{{ trek.duration_days }} Days</strong></div>
                    <div><span>Available Slots</span><strong>{{ trek.available_slots }}</strong></div>
                    <div><span>Price per person</span><strong>₹{{ trek.price }}</strong></div>
                    <div><span>Dates</span><strong>{{ trek.start_date }} → {{ trek.end_date }}</strong></div>
                    <div class="full-width"><span>Meeting Point</span><strong>{{ trek.meeting_point || "-" }}</strong></div>
                </div>

                <p class="description">{{ trek.description }}</p>

                <div v-if="alreadyBooked" class="already-booked-note">
                    You already have an active booking for this trek.
                </div>

                <form v-else @submit.prevent="submitBooking" class="booking-form">
                    <label>Number of People</label>
                    <input
                        v-model.number="numberOfPeople"
                        type="number"
                        min="1"
                        :max="trek.available_slots"
                        required/>

                    <p class="total-amount">
                        Total: ₹{{ (numberOfPeople * trek.price).toFixed(2) }}
                    </p>

                    <p v-if="bookingError" class="error-message">{{ bookingError }}</p>
                    <p v-if="bookingSuccess" class="success-message">{{ bookingSuccess }}</p>

                    <button type="submit" class="confirm-button" :disabled="booking">
                        {{ booking ? "Booking..." : "Confirm Booking" }}
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getTrekForBooking, createBooking } from "../../services/trekker"

const props = defineProps({
    trekUuid: {
        type: String,
        required: true
    }
})

const emit = defineEmits(["close", "booked"])

const trek = ref(null)
const alreadyBooked = ref(false)
const numberOfPeople = ref(1)

const loading = ref(true)
const booking = ref(false)
const errorMessage = ref("")
const bookingError = ref("")
const bookingSuccess = ref("")

async function loadTrekDetails() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getTrekForBooking(props.trekUuid)
        trek.value = response.data.trek
        alreadyBooked.value = response.data.already_booked
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

async function submitBooking() {
    bookingError.value = ""
    bookingSuccess.value = ""

    if (numberOfPeople.value < 1 || numberOfPeople.value > trek.value.available_slots) {
        bookingError.value = "Please enter a valid number of people within available slots."
        return
    }

    try {
        booking.value = true

        const response = await createBooking({
            trek_uuid: props.trekUuid,
            number_of_people: numberOfPeople.value
        })

        bookingSuccess.value = response.data.message

        setTimeout(() => {
            emit("booked")
        }, 1000)
    }
    catch (error) {
        console.error("Booking failed:", error)
        bookingError.value =
            error.response?.data?.message ||
            "Unable to complete booking."
    }
    finally {
        booking.value = false
    }
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
    max-width: 600px;
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
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #E5E7EB;
}
.modal-header h2 { color: #2E7D32; margin: 0; }
.close-button { border: none; background: none; font-size: 28px; color: #6B7280; cursor: pointer; }
.trek-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}
.trek-info div { display: flex; flex-direction: column; gap: 4px; }
.trek-info .full-width { grid-column: 1 / -1; }
.trek-info span { font-size: 13px; color: #6B7280; }
.trek-info strong { font-size: 15px; color: #1F2937; }
.description { color: #4B5563; line-height: 1.6; margin-bottom: 20px; }
.already-booked-note {
    background: #FEF3C7;
    color: #92400E;
    padding: 15px;
    border-radius: 8px;
    font-weight: 600;
}
.booking-form {
    border-top: 1px solid #E5E7EB;
    padding-top: 20px;
}
.booking-form label {
    display: block;
    font-weight: 600;
    color: #374151;
    margin-bottom: 8px;
}
.booking-form input {
    width: 100%;
    padding: 10px;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    box-sizing: border-box;
    margin-bottom: 12px;
}
.total-amount { font-size: 18px; font-weight: 700; color: #2E7D32; margin-bottom: 15px; }
.confirm-button {
    width: 100%;
    padding: 12px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}
.confirm-button:hover:not(:disabled) { background: #256428; }
.confirm-button:disabled { opacity: 0.6; cursor: not-allowed; }
.message { text-align: center; padding: 30px; color: #6B7280; }
.error-message { color: #B91C1C; margin: 10px 0; }
.success-message { color: #2E7D32; margin: 10px 0; font-weight: 600; }
</style>