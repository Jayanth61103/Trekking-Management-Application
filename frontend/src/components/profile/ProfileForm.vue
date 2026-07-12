<template>
    <div class="profile-container">
        <h2>My Profile</h2>
        <form @submit.prevent="updateProfile">
            <div class="form-group">
                <label>Full Name</label>
                <input
                    type="text"
                    v-model="full_name"
                    required
                >
            </div>
            <div class="form-group">
                <label>Username</label>
                <input
                    type="text"
                    v-model="username"
                    required
                >
            </div>
            <div class="form-group">
                <label>Email</label>
                <input
                    type="email"
                    v-model="email"
                    required
                >
            </div>
            <div class="form-group">
                <label>Phone</label>
                <input
                    type="text"
                    v-model="phone"
                    required
                >
            </div>
            <div class="form-group">
                <label>Role</label>
                <input
                    type="text"
                    v-model="role"
                    disabled
                >
            </div>
            <button type="submit">
                Save Changes
            </button>
        </form>
        <p>{{ message }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../../services/api"

const full_name = ref("")
const username = ref("")
const email = ref("")
const phone = ref("")
const role = ref("")

const message = ref("")

onMounted(async () => {
    try {
        const response = await api.get("/profile")

        full_name.value = response.data.full_name
        username.value = response.data.username
        email.value = response.data.email
        phone.value = response.data.phone
        role.value = response.data.role
    }
    catch {
        message.value = "Unable to load profile."
    }
})
async function updateProfile(){
    try{
        const response = await api.put("/profile",{

            full_name: full_name.value,
            username: username.value,
            email: email.value,
            phone: phone.value
        })
        message.value = response.data.message
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
.profile-container{
    width:500px;
    margin:auto;
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