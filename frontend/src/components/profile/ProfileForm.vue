<template>
    <div class="profile-container">
        <h2>My Profile</h2>
        <form @submit.prevent="saveProfile">
            <div class="form-group">
                <label>Full Name</label>
                <input
                    type="text"
                    v-model="full_name"
                    required
                />
            </div>
            <div class="form-group">
                <label>Username</label>
                <input
                    type="text"
                    v-model="username"
                    required
                />
            </div>
            <div class="form-group">
                <label>Email</label>

                <input
                    type="email"
                    v-model="email"
                    required
                />
            </div>
            <div class="form-group">
                <label>Phone Number</label>
                <input
                    type="tel"
                    maxlength="10"
                    v-model="phone"
                    required
                />
            </div>
            <div class="form-group">
                <label>Role</label>
                <input
                    type="text"
                    v-model="role"
                    disabled
                />
            </div>
            <button type="submit">
                Save Changes
            </button>
        </form>
        <p class="message">
            {{ message }}
        </p>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
    getProfile,
    updateProfile
} from "../../services/auth";

// Reactive Variables
const full_name = ref("");
const username = ref("");
const email = ref("");
const phone = ref("");
const role = ref("");

const message = ref("");

// Load Profile
async function loadProfile() {
    message.value = "";
    try {
        const { data } = await getProfile();
        const user = data.user;

        full_name.value = user.full_name;
        username.value = user.username;
        email.value = user.email;
        phone.value = user.phone;
        role.value = user.role;
    }
    catch (error) {
        message.value =
            error.response?.data?.message ||
            "Unable to load profile.";
    }
}
onMounted(loadProfile);

// Save Profile
async function saveProfile() {
    message.value = "";
    if (phone.value.length !== 10 || !/^\d+$/.test(phone.value)) {
        message.value = "Phone number must contain exactly 10 digits.";
        return;
    }
    try {
        const { data } = await updateProfile({

            full_name: full_name.value,
            username: username.value,
            email: email.value,
            phone: phone.value
        });
        message.value = data.message;

        // Update Local Storage
        localStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );
        localStorage.setItem(
            "role",
            data.user.role
        );
        localStorage.setItem(
            "username",
            data.user.username
        );
    }
    catch (error) {
        message.value = error.response?.data?.message ||"Unable to connect to server.";
    }
}
</script>

<style scoped>
.profile-container{
    width:500px;
    margin:50px auto;
    padding:30px;
    border:1px solid #dddddd;
    border-radius:8px;
}
.form-group{
    margin-bottom:18px;
}
label{
    display:block;
    margin-bottom:6px;
    font-weight:bold;
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
    margin-top:20px;
    text-align:center;
    color:#2E7D32;
}
</style>