<template>
    <div class="empty-state">
        <h3>{{ title }}</h3>
        <p>{{ message }}</p>
    </div>
</template>

<script setup>
defineProps({
    title:{
        type:String,
        default:"No Data"
    },
    message:{
        type:String,
        default:"Nothing to display."
    }
})
</script>

<style scoped>
.empty-state{
    padding:40px;
    text-align:center;
    border:2px dashed #D1D5DB;
    border-radius:12px;
    background:#F9FAFB;

}
.empty-state h3{
    margin-bottom:10px;
    color:#374151;
}
.empty-state p{
    color:#6B7280;
}
</style>