<template>
    <div class="staff-container">
        <h2>Create Staff Account</h2>
        <form @submit.prevent="registerStaff">
            <!-- Full Name -->
            <div class="form-group">
                <label>Full Name</label>
                <input
                    type="text"
                    v-model="full_name"
                    placeholder="Enter Full Name"
                    required/>
            </div>
            <!-- Username -->
            <div class="form-group">
                <label>Username</label>
                <input
                    type="text"
                    v-model="username"
                    placeholder="Enter Username"
                    required/>
            </div>
            <!-- Email -->
            <div class="form-group">
                <label>Email</label>
                <input
                    type="email"
                    v-model="email"
                    placeholder="Enter Email"
                    required/>
            </div>
            <!-- Phone -->
            <div class="form-group">
                <label>Phone Number</label>
                <input
                    type="tel"
                    maxlength="10"
                    v-model="phone"
                    placeholder="Enter Phone Number"
                    required/>
            </div>
            <!-- Password -->
            <div class="form-group">
                <label>Password</label>
                <input
                    type="password"
                    v-model="password"
                    placeholder="Enter Password"
                    required/>
            </div>
            <!-- Department -->
            <div class="form-group">
                <label>Department</label>
                <select
                    v-model="department"
                    required>
                    <option disabled value="">
                        Select Department
                    </option>
                    <option value="ADMINISTRATION">
                        Administration
                    </option>
                    <option value="OPERATIONS">
                        Operations
                    </option>
                    <option value="SAFETY">
                        Safety
                    </option>
                    <option value="LOGISTICS">
                        Logistics
                    </option>
                </select>
            </div>
            <!-- Designation -->
            <div class="form-group">
                <label>Designation</label>
                <select
                    v-model="designation"
                    required>
                    <option disabled value="">
                        Select Designation
                    </option>
                    <option value="GUIDE">
                        Guide
                    </option>
                    <option value="MANAGER">
                        Manager
                    </option>
                    <option value="COORDINATOR">
                        Coordinator
                    </option>
                    <option value="ACCOUNTANT">
                        Accountant
                    </option>
                </select>
            </div>
            <!-- Submit -->
            <button
                type="submit"
                :disabled="submitting">
                {{ submitting ? "Creating Staff..." : "Create Staff" }}
            </button>
        </form>
        <!-- Response Message -->
        <p
            v-if="message"
            :class="messageType">
            {{ message }}
        </p>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { createStaff } from "../../services/admin"

const router = useRouter()

// Form Fields
const full_name = ref("")
const username = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")
const department = ref("")
const designation = ref("")

// Page State
const message = ref("")
const messageType = ref("")
const submitting = ref(false)

// Create Staff
async function registerStaff() {
    message.value = ""
    messageType.value = ""
    // Phone Validation
    if (
        phone.value.length !== 10 ||
        !/^\d+$/.test(phone.value)
    ) {
        message.value =
            "Phone number must contain exactly 10 digits."
        messageType.value = "error-message"
        return
    }
    try {
        submitting.value = true
        const { data } = await createStaff({
            full_name: full_name.value.trim(),
            username: username.value.trim(),
            email: email.value.trim(),
            phone: phone.value.trim(),
            password: password.value,
            department: department.value,
            designation: designation.value
        })
        // Success Message
        message.value = data.message
        messageType.value = "success-message"
        // Clear Form
        full_name.value = ""
        username.value = ""
        email.value = ""
        phone.value = ""
        password.value = ""
        department.value = ""
        designation.value = ""
        // Return to Staff Management
        setTimeout(() => {
            router.push("/admin/staff")
        }, 1500)
    }
    catch (error) {
        console.error(
            "Create Staff Error:",
            error
        )
        message.value =
            error.response?.data?.message ||
            "Unable to create Staff."
        messageType.value = "error-message"
    }
    finally {
        submitting.value = false
    }
}
</script>

<style scoped>
.staff-container {
    width: 500px;
    max-width: 100%;
    margin: 40px auto;
    padding: 30px;
    border: 1px solid #cccccc;
    border-radius: 10px;
    background: white;
    box-sizing: border-box;
}
.staff-container h2 {
    margin-top: 0;
    margin-bottom: 25px;
    color: #1F2937;
}
.form-group {
    margin-bottom: 18px;
}
label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}
input,
select {
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    border: 1px solid #D1D5DB;
    border-radius: 4px;
}
input:focus,
select:focus {
    outline: none;
    border-color: #2E7D32;
}
button {
    width: 100%;
    padding: 12px;
    background: #2E7D32;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}
button:hover:not(:disabled) {
    background: #256428;
}
button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
/* Success */
.success-message {
    margin-top: 20px;
    text-align: center;
    color: #2E7D32;
    font-weight: bold;
}
/* Error */
.error-message {
    margin-top: 20px;
    text-align: center;
    color: #B91C1C;
    font-weight: bold;
}
</style>