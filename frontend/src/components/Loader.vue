<template>
    <transition name="fade" mode="in-out">
        <div class="w-full h-screen flex items-center justify-center text-xl">
            <div class="h-14 w-14" v-if="props.show">
                <div class="animate-spin h-full w-full rounded-full border-4 border-t-[#002C77] border-b-[#255B97]">
                </div>
            </div>
            <div class="" v-else>
                <div class=" bg-white  inset-0 bg-opacity-50 flex items-center justify-center z-50">
            <div class="animate-spin  rounded-full h-32 w-32 border-t-2 border-b-2 border-orange-500"></div>
          </div>
            </div>
        </div>
    </transition>
</template>

<script setup>

const props = defineProps({
    show: Boolean,
});
</script>