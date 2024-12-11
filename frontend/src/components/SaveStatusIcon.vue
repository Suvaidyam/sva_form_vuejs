<template>
    <div class="relative w-5 h-5 mr-2">
        <transition name="fade" mode="out-in">
            <SaveIcon v-if="status === 'idle'" class="w-5 h-5 text-gray-400" />
            <Loader v-else-if="status === 'saving'" class="w-5 h-5 text-blue-500 animate-spin" />
            <SaveIcon v-else-if="status === 'completed'" class="w-5 h-5 text-green-600" />
        </transition>
    </div>
</template>

<script setup>
import { SaveIcon, Loader } from 'lucide-vue-next'

defineProps({
    status: {
        type: String,
        required: true,
        validator: (value) => ['idle', 'saving', 'completed'].includes(value)
    }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>