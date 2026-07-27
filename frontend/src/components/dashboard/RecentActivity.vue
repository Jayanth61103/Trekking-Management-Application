<template>

    <section class="recent-activity">
        <h2>Recent Activity</h2>
        <div v-if="activities.length">
            <div
                v-for="activity in activities"
                :key="activity.id"
                class="activity-card">
                <h4>{{ activity.title }}</h4>
                <p>{{ activity.description }}</p>
            </div>
        </div>
        <EmptyState
            v-else
            title="No Recent Activity"
            message="Activities will appear here once the system is used."
        />
    </section>
</template>

<script setup>
import EmptyState from "../common/EmptyState.vue"
defineProps({
    activities:{
        type:Array,
        default:()=>[]
    }
})
</script>

<style scoped>
.recent-activity{
    margin-top:40px;
}
.recent-activity h2{
    margin-bottom:20px;
    color:#2E7D32;
}
.activity-card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:10px;
    padding:18px;
    margin-bottom:15px;
}
.activity-card h4{
    margin-bottom:8px;
    color:#374151;
}
.activity-card p{
    color:#6B7280;
}
</style>