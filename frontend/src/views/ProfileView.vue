<template>
    <div class="profile-page">
        <h1>My Profile</h1>
        <ProfileForm />
        <hr>
        <ChangePasswordForm />
    </div>
</template>

<script setup>
import ProfileForm from "../components/profile/ProfileForm.vue"
import ChangePasswordForm from "../components/profile/ChangePasswordForm.vue"
</script>

<style scoped>
.profile-page{
    width:80%;
    margin:auto;
    padding:40px;
}
hr{
    margin:40px 0;
}
</style>