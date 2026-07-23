<template>
    <div class="staff-container">
        <h2>Create Staff Account</h2>
        <form @submit.prevent="registerStaff">
            <div class="form-group">
                <label>Full Name</label>
                <input
                    type="text"
                    v-model="full_name"
                    placeholder="Enter Full Name"
                    required
                />
            </div>
            <div class="form-group">
                <label>Username</label>
                <input
                    type="text"
                    v-model="username"
                    placeholder="Enter Username"
                    required
                />
            </div>
            <div class="form-group">
                <label>Email</label>
                <input
                    type="email"
                    v-model="email"
                    placeholder="Enter Email"
                    required
                />
            </div>
            <div class="form-group">
                <label>Phone Number</label>
                <input
                    type="tel"
                    maxlength="10"
                    v-model="phone"
                    placeholder="Enter Phone Number"
                    required
                />
            </div>
            <div class="form-group">
                <label>Password</label>
                <input
                    type="password"
                    v-model="password"
                    placeholder="Enter Password"
                    required
                />
            </div>
            <div class="form-group">
                <label>Department</label>
                <select
                    v-model="department"
                    required
                >
                    <option disabled value="">
                        Select Department
                    </option>
                    <option value="ADMINISTRATION">
                        Administration
                    </option>
                    <option value="OPERATIONS">
                        Operations
                    </option>
                    <option value="FINANCE">
                        Finance
                    </option>
                    <option value="SAFETY">
                        Safety
                    </option>
                    <option value="MARKETING">
                        Marketing
                    </option>
                </select>
            </div>
            <div class="form-group">
                <label>Designation</label>
                <select
                    v-model="designation"
                    required
                >
                    <option disabled value="">
                        Select Designation
                    </option>
                    <option value="MANAGER">
                        Manager
                    </option>
                    <option value="TREK_GUIDE">
                        Trek Guide
                    </option>
                    <option value="COORDINATOR">
                        Coordinator
                    </option>
                    <option value="ACCOUNTANT">
                        Accountant
                    </option>
                </select>
            </div>
            <button type="submit">
                Create Staff
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

import { createStaff } from "../../services/admin";

const router = useRouter();

const full_name = ref("");
const username = ref("");
const email = ref("");
const phone = ref("");
const password = ref("");

const department = ref("");
const designation = ref("");

const message = ref("");

async function registerStaff() {
    message.value = "";

    // Phone Validation
    if (phone.value.length !== 10 || !/^\d+$/.test(phone.value)) {
        message.value =
            "Phone number must contain exactly 10 digits.";
        return;
    }
    try {
        const { data } = await createStaff({

            full_name: full_name.value,
            username: username.value,
            email: email.value,
            phone: phone.value,
            password: password.value,
            department: department.value,
            designation: designation.value
        });
        message.value = data.message;

        // Clear Form
        full_name.value = "";
        username.value = "";
        email.value = "";
        phone.value = "";
        password.value = "";
        department.value = "";
        designation.value = "";
        setTimeout(() => {
            router.push("/admin/dashboard");
        },1500);
    }
    catch(error){
        message.value =
            error.response?.data?.message ||
            "Unable to connect to server.";
    }
}
</script>

<style scoped>
.staff-container{
    width:500px;
    margin:40px auto;
    padding:30px;
    border:1px solid #cccccc;
    border-radius:10px;
    background:white;
}
.form-group{
    margin-bottom:18px;
}
label{
    display:block;
    margin-bottom:5px;
    font-weight:bold;
}
input,
select{
    width:100%;
    padding:10px;
    box-sizing:border-box;
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
.message{
    margin-top:20px;
    text-align:center;
    color:#2E7D32;
    font-weight:bold;
}
</style>