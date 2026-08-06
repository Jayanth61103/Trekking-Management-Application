<template>
    <div class="bookings-container">
        <div class="bookings-header">
            <h1>My Bookings</h1>
            <p>Track your trekking bookings and history.</p>
        </div>

        <p v-if="loading" class="state-message">Loading bookings...</p>
        <p v-else-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div v-else-if="bookings.length === 0" class="empty-state">
            <h3>No Bookings Yet</h3>
            <p>Browse treks and make your first booking.</p>
        </div>

        <div v-else class="bookings-list">
            <div v-for="booking in bookings" :key="booking.booking_uuid" class="booking-card">
                <div class="booking-main">
                    <h3>{{ booking.trek_name }}</h3>
                    <p class="location">{{ booking.location }}</p>
                    <p class="dates">{{ booking.start_date }} → {{ booking.end_date }}</p>
                    <div class="booking-meta">
                        <span>{{ booking.number_of_people }} People</span>
                        <span>₹{{ booking.booking_amount }}</span>
                    </div>
                </div>
                <div class="booking-side">
                    <span class="status" :class="getStatusClass(booking.booking_status)">
                        {{ booking.booking_status }}
                    </span>
                    <button
                        v-if="booking.booking_status === 'Approved' || booking.booking_status === 'Pending'"
                        class="cancel-button"
                        :disabled="cancellingId === booking.booking_uuid"
                        @click="cancel(booking.booking_uuid)">
                        {{ cancellingId === booking.booking_uuid ? "Cancelling..." : "Cancel" }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getMyBookings, cancelBooking } from "../../services/trekker"

const bookings = ref([])
const loading = ref(true)
const errorMessage = ref("")
const cancellingId = ref(null)

async function loadBookings() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getMyBookings()
        bookings.value = response.data.bookings || []
    }
    catch (error) {
        console.error("Failed to load bookings:", error)
        errorMessage.value =
            error.response?.data?.message ||
            "Unable to load bookings."
    }
    finally {
        loading.value = false
    }
}

async function cancel(bookingUuid) {
    if (!window.confirm("Are you sure you want to cancel this booking?")) {
        return
    }

    try {
        cancellingId.value = bookingUuid
        await cancelBooking(bookingUuid)
        await loadBookings()
    }
    catch (error) {
        console.error("Failed to cancel booking:", error)
        alert(
            error.response?.data?.message ||
            "Unable to cancel booking."
        )
    }
    finally {
        cancellingId.value = null
    }
}

function getStatusClass(status) {
    if (status === "Approved") return "status-approved"
    if (status === "Pending") return "status-pending"
    if (status === "Cancelled") return "status-cancelled"
    if (status === "Completed") return "status-completed"
    if (status === "Rejected") return "status-rejected"
    return ""
}

onMounted(() => {
    loadBookings()
})
</script>

<style scoped>
.bookings-container {
    width: 90%;
    max-width: 1000px;
    margin: auto;
    padding: 30px;
}
.bookings-header h1 { color: #2E7D32; margin: 0 0 8px; }
.bookings-header p { color: #6B7280; margin: 0 0 20px; }
.state-message { color: #6B7280; padding: 20px 0; }
.error-message { color: #B91C1C; padding: 15px 0; }
.empty-state {
    padding: 50px;
    text-align: center;
    border: 1px dashed #D1D5DB;
    border-radius: 10px;
    color: #6B7280;
}
.bookings-list { display: flex; flex-direction: column; gap: 15px; }
.booking-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
}
.booking-main h3 { margin: 0 0 5px; color: #1F2937; }
.location { color: #6B7280; font-size: 14px; margin: 0 0 5px; }
.dates { color: #6B7280; font-size: 13px; margin: 0 0 10px; }
.booking-meta { display: flex; gap: 15px; }
.booking-meta span { font-size: 14px; color: #374151; font-weight: 600; }
.booking-side {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
}
.status {
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    white-space: nowrap;
}
.status-approved { background: #DCFCE7; color: #166534; }
.status-pending { background: #FEF3C7; color: #92400E; }
.status-cancelled { background: #FEE2E2; color: #991B1B; }
.status-completed { background: #F3F4F6; color: #374151; }
.status-rejected { background: #FEE2E2; color: #991B1B; }
.cancel-button {
    padding: 7px 14px;
    background: white;
    color: #B91C1C;
    border: 1px solid #B91C1C;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
}
.cancel-button:hover:not(:disabled) { background: #FEF2F2; }
.cancel-button:disabled { opacity: 0.6; cursor: not-allowed; }
@media (max-width: 600px) {
    .booking-card { flex-direction: column; }
    .booking-side { align-items: flex-start; width: 100%; }
}
</style>