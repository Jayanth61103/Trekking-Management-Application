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
                />
            </div>
            <div class="form-group">
                <label>Password</label>
                <input
                    type="password"
                    v-model="password"
                    required
                />
            </div>
            <button type="submit">
                Login
            </button>
        </form>
        <p class="message">
            {{ message }}
        </p>
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
        const { access_token, user, message: successMessage } = response.data;
        if (!access_token || !user) {
            message.value = "Invalid response from server.";
            return;
        }
        message.value = successMessage;

        // Clear Form
        email.value = "";
        password.value = "";

        // Redirect According to Role
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
        message.value =
            error.response?.data?.message ||
            "Unable to connect to server.";
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
    box-sizing:border-box;
}
button{
    width:100%;
    padding:10px;
    cursor:pointer;
}
.message{
    margin-top:15px;
    text-align:center;
    color:#d32f2f;
}
</style>