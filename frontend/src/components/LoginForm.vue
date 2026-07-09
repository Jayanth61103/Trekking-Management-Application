<template>
<div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
        <div class="form-group">
            <label>Email</label>
            <input
                type="email"
                v-model="email"
                required
            >
        </div>
        <div class="form-group">
            <label>Password</label>
            <input
                type="password"
                v-model="password"
                required
            >
        </div>
        <button type="submit">
            Login
        </button>
    </form>
    <p>{{ message }}</p>
</div>
</template>
<script setup>

import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const email = ref("")
const password = ref("")
const message = ref("")

async function loginUser(){
    try{
        const response = await api.post("/login",{
            email: email.value,
            password: password.value
        })
        console.log(response.data)
        // Store JWT
        localStorage.setItem(
            "access_token",
            response.data.access_token
        )
        // Store User Details
        localStorage.setItem(
            "user",
            JSON.stringify(response.data.user)
        )
        message.value = response.data.message

        const role = response.data.user.role
        if (role === "Admin") {
             router.push("/admin/dashboard")
        }
        else if (role === "Staff") {
             router.push("/staff/dashboard")
        }
        else if (role === "Trekker") {
             router.push("/trekker/dashboard")
        }
        else {
             message.value = "Invalid user role."
        }
    }
    catch(error){
        if(error.response){
            message.value = error.response.data.message
        }
        else{
            message.value = "Server Not Found"
        }
    }
}
</script>
<style scoped>
.login-container{
    width:350px;
    margin:50px auto;
    border:1px solid lightgray;
    padding:30px;
    border-radius:8px;
}
.form-group{
    margin-bottom:15px;
}
input{
    width:100%;
    padding:10px;
}
button{
    width:100%;
    padding:10px;
}
</style>