<template>
    <div class="password-container">
        <h2>Change Password</h2>
        <form @submit.prevent="changePassword">
            <div class="form-group">
                <label>Current Password</label>
                <input
                    type="password"
                    v-model="current_password"
                    required
                >
            </div>
            <div class="form-group">
                <label>New Password</label>
                <input
                    type="password"
                    v-model="new_password"
                    required
                >
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <input
                    type="password"
                    v-model="confirm_password"
                    required
                >
            </div>
            <button type="submit">
                Change Password
            </button>
        </form>
        <p>{{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from "vue"

import api from "../../services/api"

const current_password = ref("")
const new_password = ref("")
const confirm_password = ref("")

const message = ref("")

async function changePassword(){
    try{
        const response = await api.put(
            "/change-password",
            {
                current_password: current_password.value,
                new_password: new_password.value,
                confirm_password: confirm_password.value
            }
        )

        message.value = response.data.message

        current_password.value = ""
        new_password.value = ""
        confirm_password.value = ""
    }
    catch(error){
        if(error.response){
            message.value = error.response.data.message
        }
        else{
            message.value = "Unable to connect to server."
        }
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
}
button{
    width:100%;
    padding:10px;
    cursor:pointer;
}
p{
    margin-top:20px;
    color:green;
}
</style>