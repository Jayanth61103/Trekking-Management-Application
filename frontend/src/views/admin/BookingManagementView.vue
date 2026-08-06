<template>
    <div class="booking-container">
        <div class="booking-header">
            <h1>Booking Management</h1>
            <p>View all trek booking records and history.</p>
        </div>

        <div class="booking-controls">
            <input
                v-model="search"
                type="text"
                placeholder="Search by trekker, trek name, or status..."/>
        </div>

        <p v-if="loading" class="state-message">Loading bookings...</p>
        <p v-else-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div v-else-if="filteredBookings.length === 0" class="empty-state">
            <h3>No Bookings Found</h3>
            <p v-if="search">No bookings match your search.</p>
            <p v-else>Bookings will appear here once trekkers book treks.</p>
        </div>

        <div v-else class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Trekker</th>
                        <th>Trek</th>
                        <th>People</th>
                        <th>Amount</th>
                        <th>Booking Status</th>
                        <th>Payment</th>
                        <th>Booked On</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="booking in filteredBookings" :key="booking.booking_uuid">
                        <td>
                            <div class="trekker-name">{{ booking.trekker_name }}</div>
                            <div class="trekker-email">{{ booking.trekker_email }}</div>
                        </td>
                        <td>{{ booking.trek_name }}</td>
                        <td>{{ booking.number_of_people }}</td>
                        <td>₹{{ booking.booking_amount }}</td>
                        <td>
                            <span class="status" :class="getBookingStatusClass(booking.booking_status)">
                                {{ booking.booking_status }}
                            </span>
                        </td>
                        <td>
                            <span class="status" :class="getPaymentStatusClass(booking.payment_status)">
                                {{ booking.payment_status }}
                            </span>
                        </td>
                        <td>{{ formatDate(booking.booking_date) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { getAllBookings } from "../../services/admin"

const bookings = ref([])
const search = ref("")
const loading = ref(true)
const errorMessage = ref("")

async function loadBookings() {
    try {
        loading.value = true
        errorMessage.value = ""
        const response = await getAllBookings()
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

const filteredBookings = computed(() => {
    const searchValue = search.value.toLowerCase().trim()

    if (!searchValue) {
        return bookings.value
    }

    return bookings.value.filter((booking) => {
        const trekkerName = booking.trekker_name?.toLowerCase() || ""
        const trekName = booking.trek_name?.toLowerCase() || ""
        const bookingStatus = booking.booking_status?.toLowerCase() || ""
        const paymentStatus = booking.payment_status?.toLowerCase() || ""

        return (
            trekkerName.includes(searchValue) ||
            trekName.includes(searchValue) ||
            bookingStatus.includes(searchValue) ||
            paymentStatus.includes(searchValue)
        )
    })
})

function getBookingStatusClass(status) {
    if (status === "Approved") return "status-approved"
    if (status === "Pending") return "status-pending"
    if (status === "Cancelled") return "status-cancelled"
    if (status === "Completed") return "status-completed"
    if (status === "Rejected") return "status-rejected"
    return ""
}

function getPaymentStatusClass(status) {
    if (status === "Paid") return "status-approved"
    if (status === "Pending") return "status-pending"
    if (status === "Failed") return "status-rejected"
    if (status === "Refunded") return "status-completed"
    return ""
}

function formatDate(isoString) {
    if (!isoString) return "-"
    return new Date(isoString).toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    })
}

onMounted(() => {
    loadBookings()
})
</script>

<style scoped>
.booking-container {
    width: 90%;
    max-width: 1400px;
    margin: auto;
    padding: 30px;
}
.booking-header h1 { color: #2E7D32; margin: 0 0 8px; }
.booking-header p { color: #6B7280; margin: 0; }
.booking-controls { margin: 30px 0 20px; }
.booking-controls input {
    width: 420px;
    max-width: 100%;
    padding: 11px 13px;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    font-size: 14px;
    outline: none;
    box-sizing: border-box;
}
.booking-controls input:focus {
    border-color: #2E7D32;
    box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.1);
}
.state-message { color: #6B7280; padding: 20px 0; }
.error-message {
    color: #B91C1C;
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-radius: 6px;
    padding: 12px 15px;
    margin-top: 20px;
}
.empty-state {
    padding: 50px;
    text-align: center;
    border: 1px dashed #D1D5DB;
    border-radius: 10px;
    color: #6B7280;
}
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
    vertical-align: top;
}
.trekker-name { font-weight: 600; color: #1F2937; }
.trekker-email { font-size: 13px; color: #6B7280; }
.status {
    display: inline-block;
    padding: 5px 10px;
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
@media (max-width: 700px) {
    .booking-container { width: 95%; padding: 20px 10px; }
    .booking-controls input { width: 100%; }
}
</style>