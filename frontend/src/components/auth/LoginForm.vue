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
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../../services/auth";

const router = useRouter();

const email = ref("");
const password = ref("");
const message = ref("");

async function loginUser() {
    message.value = "";

    try {
        const response = await login({
           email: email.value,
           password: password.value
        });

        const user = response.data.user;
        if (!user || !response.data.access_token) {
            message.value = "Invalid response from server.";
            return;
        }

        // Clear previous session
        localStorage.clear();

        // Store JWT
        localStorage.setItem("access_token", response.data.access_token);

        // Store User Details
        localStorage.setItem("user", JSON.stringify(user));
        localStorage.setItem("user_id", user.id);
        localStorage.setItem("role", user.role);
        localStorage.setItem("email", user.email);

        message.value = response.data.message;

        switch (user.role) {
            case "Admin":
                router.push("/admin/dashboard");
                break;
            case "Staff":
                router.push("/staff/dashboard");
                break;
            case "Trekker":
                router.push("/trekker/dashboard");
                break;
            default:
                message.value = "Unknown user role.";
        }
    }
    catch (error) {
        if (error.response) {
            message.value = error.response.data.message;
        }
        else if (error.request) {
            message.value = "Unable to connect to server.";
        }
        else {
            message.value = "Something went wrong.";
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