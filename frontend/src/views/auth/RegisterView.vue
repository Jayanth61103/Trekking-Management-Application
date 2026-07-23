<template>
    <div class="register-page">
        <h1>Register</h1>
        <p>Create your Trekker account.</p>

        <RegisterForm />
    </div>
</template>

<script setup>
import RegisterForm from "../../components/auth/RegisterForm.vue";
</script>

<style scoped>
.register-page {
    width: 80%;
    margin: auto;
    padding: 30px;
}

h1 {
    color: #2E7D32;
}

p {
    margin-bottom: 25px;
}
</style>