<template>
  <div class="fixed inset-0 flex items-center justify-center p-4 bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md overflow-hidden">
      <div class="p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Disclaimer</h2>
        <p class="text-gray-600 mb-6">
          Changing the above selected thematic area midway will result in losing progress on the programmatic sections.
          We recommend avoiding multiple changes to ensure smooth completion of the survey.
        </p>
        <div class="flex justify-end gap-3">
          <button type="button" @click="emit('proceedChanging', false)"
            class="px-4 py-2 rounded-full text-gray-700 bg-gray-200 hover:bg-gray-300 transition-colors duration-200">
            No
          </button>
          <button type="button" @click="emit('proceedChanging', fieldValue)"
            class="px-4 py-2 rounded-full text-white bg-orange-500 hover:bg-orange-600 transition-colors duration-200">
            Yes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  fieldValue: {
    type: String,
    required: false,
    default: ''
  }
})
const emit = defineEmits(['proceedChanging'])
</script>