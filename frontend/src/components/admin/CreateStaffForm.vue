<template>
  <div class="staff-container">
    <h2>Create Staff Account</h2>
    <form @submit.prevent="createStaff">
      <div class="form-group">
        <label>Full Name</label>
        <input
          type="text"
          v-model="full_name"
          placeholder="Enter Full Name"
          required
        >
      </div>
      <div class="form-group">
        <label>Username</label>
        <input
          type="text"
          v-model="username"
          placeholder="Enter Username"
          required
        >
      </div>
      <div class="form-group">
        <label>Email</label>
        <input
          type="email"
          v-model="email"
          placeholder="Enter Email"
          required
        >
      </div>
      <div class="form-group">
        <label>Phone Number</label>
        <input
          type="text"
          v-model="phone"
          placeholder="Enter Phone Number"
          required
        >
      </div>
      <div class="form-group">
        <label>Password</label>
        <input
          type="password"
          v-model="password"
          placeholder="Enter Password"
          required
        >
      </div>
      <button type="submit">
        Create Staff
      </button>
    </form>

    <p v-if="message">
      {{ message }}
    </p>

  </div>
</template>

<script setup>

import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"

const router = useRouter()

const full_name = ref("")
const username = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")

const message = ref("")

async function createStaff() {
    try {
        // Get JWT Token
        const token = localStorage.getItem("access_token")

        // Check if token exists
        if (!token) {
            message.value = "Please login again."
            router.push("/login")
            return
        }

        // Send request to Backend
        const response = await api.post(
            "/admin/create-staff",
            {
                full_name: full_name.value,
                username: username.value,
                email: email.value,
                phone: phone.value,
                password: password.value
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        )

        message.value = response.data.message
        // Clear Form
        full_name.value = ""
        username.value = ""
        email.value = ""
        phone.value = ""
        password.value = ""

        // Redirect after successful creation
        setTimeout(() => {
            router.push("/admin/dashboard")
        }, 1500)

    }
    catch (error) {
        if (error.response) {
            message.value = error.response.data.message
        }
        else {
            message.value = "Unable to connect to server."
        }
    }
}
</script>

<style scoped>
.staff-container{
    width:450px;
    margin:40px auto;
    padding:30px;
    border:1px solid #cccccc;
    border-radius:10px;
    background:white;
}
.form-group{
    margin-bottom:15px;
}
label{
    display:block;
    margin-bottom:5px;
    font-weight:bold;
}
input{
    width:100%;
    padding:10px;
    border:1px solid #cccccc;
    border-radius:5px;
}
button{
    width:100%;
    padding:12px;
    background:#2E7D32;
    color:white;
    border:none;
    border-radius:5px;
    cursor:pointer;
    font-size:16px;
}
button:hover{
    background:#256428;
}
p{
    margin-top:20px;
    color:green;
    text-align:center;
    font-weight:bold;
}
</style>