<template>
  <div class="staff-container">
    <h2>Create Staff Account</h2>

    <form @submit.prevent="registerStaff">
      <div class="form-group">
        <label>Full Name</label>
        <input v-model="form.full_name" type="text" required />
      </div>

      <div class="form-group">
        <label>Username</label>
        <input v-model="form.username" type="text" required />
      </div>

      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" required />
      </div>

      <div class="form-group">
        <label>Phone Number</label>
        <input
          v-model="form.phone"
          type="tel"
          maxlength="10"
          pattern="[0-9]{10}"
          required
        />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="form.password" type="password" required />
      </div>

      <div class="form-group">
        <label>Department</label>
        <select v-model="form.department" required>
          <option disabled value="">Select Department</option>
          <option value="ADMINISTRATION">Administration</option>
          <option value="OPERATIONS">Operations</option>
          <option value="SAFETY">Safety</option>
          <option value="LOGISTICS">Logistics</option>
        </select>
      </div>

      <div class="form-group">
        <label>Designation</label>
        <select v-model="form.designation" required>
          <option disabled value="">Select Designation</option>
          <option value="GUIDE">Guide</option>
          <option value="MANAGER">Manager</option>
          <option value="COORDINATOR">Coordinator</option>
          <option value="ACCOUNTANT">Accountant</option>
        </select>
      </div>

      <button type="submit" :disabled="submitting">
        {{ submitting ? "Creating..." : "Create Staff" }}
      </button>

      <p v-if="message" :class="messageType">
        {{ message }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import { createStaff } from "../../services/admin"

const router = useRouter()

const form = reactive({
  full_name: "",
  username: "",
  email: "",
  phone: "",
  password: "",
  department: "",
  designation: ""
})

const message = ref("")
const messageType = ref("")
const submitting = ref(false)

async function registerStaff() {
  message.value = ""

  if (!/^\d{10}$/.test(form.phone)) {
    message.value = "Phone number must contain exactly 10 digits."
    messageType.value = "error-message"
    return
  }

  try {
    submitting.value = true

    await createStaff({
      ...form,
      full_name: form.full_name.trim(),
      username: form.username.trim(),
      email: form.email.trim().toLowerCase(),
      phone: form.phone.trim()
    })

    message.value = "Staff account created successfully."
    messageType.value = "success-message"

    setTimeout(() => {
      router.push("/admin/staff")
    }, 1500)

  } catch (error) {
    message.value =
      error.response?.data?.message || "Unable to create staff."

    messageType.value = "error-message"

  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.staff-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 30px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.form-group {
  margin-bottom: 15px;
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
}

button {
  width: 100%;
  padding: 12px;
  cursor: pointer;
}

.success-message {
  color: green;
  text-align: center;
}

.error-message {
  color: red;
  text-align: center;
}
</style>