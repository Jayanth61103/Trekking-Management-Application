<template>
    <div class="password-container">
        <h2>Change Password</h2>
        <form @submit.prevent="updatePassword">
            <div class="form-group">
                <label>Current Password</label>
                <input
                    type="password"
                    v-model="current_password"
                    required
                />
            </div>
            <div class="form-group">
                <label>New Password</label>
                <input
                    type="password"
                    v-model="new_password"
                    required
                />
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <input
                    type="password"
                    v-model="confirm_password"
                    required
                />
            </div>
            <button type="submit">
                Change Password
            </button>
        </form>
        <p class="message">
            {{ message }}
        </p>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { changePassword } from "../../services/auth";

const current_password = ref("");
const new_password = ref("");
const confirm_password = ref("");

const message = ref("");

async function updatePassword() {
    message.value = "";

    // Client-side Validation
    if (new_password.value !== confirm_password.value) {
        message.value = "New Password and Confirm Password do not match.";
        return;
    }
    if (current_password.value === new_password.value) {
        message.value = "New password cannot be the same as the current password.";
        return;
    }
    try {
        const { data } = await changePassword({
            current_password: current_password.value,
            new_password: new_password.value,
            confirm_password: confirm_password.value
        });
        message.value = data.message;

        // Clear Form
        current_password.value = "";
        new_password.value = "";
        confirm_password.value = "";
    }
    catch (error) {
        message.value =
            error.response?.data?.message ||
            "Unable to connect to server.";
    }
}
</script>

<style scoped>
.password-container{
    width:500px;
    margin:50px auto;
    padding:30px;
}
.form-group{
    margin-bottom:15px;
}
label{
    display:block;
    margin-bottom:5px;
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