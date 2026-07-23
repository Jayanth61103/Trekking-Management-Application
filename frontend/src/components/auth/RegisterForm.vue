<template>
  <div class="register-container">

    <h2>Create Account</h2>
    <form @submit.prevent="registerUser">
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
        <label>Phone</label>
        <input
          type="text"
          v-model="phone"
          placeholder="Enter Phone Number"
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
      <button type="submit">
        Register
      </button>

    </form>
    <p v-if="message">
      {{ message }}
    </p>
  </div>
</template>

<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import { register } from "../../services/auth";

const router = useRouter();

const full_name = ref("");
const username = ref("");
const email = ref("");
const phone = ref("");
const password = ref("");

const message = ref("");

async function registerUser() {

    message.value = "";
    try {
        const { data } = await register({
            full_name: full_name.value,
            username: username.value,
            email: email.value,
            phone: phone.value,
            password: password.value
        });
        message.value = data.message;

        // Clear Form
        full_name.value = "";
        username.value = "";
        email.value = "";
        phone.value = "";
        password.value = "";

        // Redirect to Login
        setTimeout(() => {
            router.push("/login");
        }, 1500);
    }
    catch (error) {
        message.value =
            error.response?.data?.message ||
            "Unable to connect to server.";
    }
}
</script>

<style scoped>
.register-container{
    width:400px;
    margin:40px auto;
    padding:30px;
    border:1px solid #ccc;
    border-radius:10px;

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