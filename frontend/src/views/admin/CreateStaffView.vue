<template>
    <div class="create-staff-page">
        <h1>Create Staff</h1>
        <p>
            Fill in the details below to create a new Staff account.
        </p>
        <CreateStaffForm />
    </div>
</template>
<script setup>

import CreateStaffForm from "../../components/admin/CreateStaffForm.vue"
</script>
<style scoped>
.create-staff-page{
    width:80%;
    margin:auto;
    padding:40px;
}
h1{
    color:#2E7D32;
    margin-bottom:10px;
}
p{
    margin-bottom:30px;
    color:#555;
}
</style>