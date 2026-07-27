<template>
    <div class="create-trek-page">
        <!-- Page Header -->
        <div class="page-header">
            <div>
                <h1>Create Trek</h1>
                <p>
                    Create a new trekking activity and assign a guide.
                </p>
            </div>
            <!-- Back Button -->
            <button
                class="back-button"
                @click="goBackToTreks">
                ← Back to Treks
            </button>
        </div>
        <!-- Trek Form -->
        <CreateTrekForm />
    </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import CreateTrekForm from "../../components/admin/CreateTrekForm.vue"
const router = useRouter()
// Back to Trek Management
function goBackToTreks() {
    router.push("/admin/treks")
}
</script>

<style scoped>
.create-trek-page {
    width: 80%;
    max-width: 1200px;
    margin: auto;
    padding: 40px;
}
/* Header */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 30px;
}
.page-header h1 {
    color: #2E7D32;
    margin: 0 0 10px;
}
.page-header p {
    margin: 0;
    color: #555;
}
/* Back Button */
.back-button {
    width: auto;
    padding: 10px 18px;
    background: white;
    color: #2E7D32;
    border: 1px solid #2E7D32;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
}
.back-button:hover {
    background: #F0FDF4;
}
/* Responsive */
@media (max-width: 700px) {
    .create-trek-page {
        width: 90%;
        padding: 25px 10px;
    }
    .page-header {
        flex-direction: column;
    }
}
</style>