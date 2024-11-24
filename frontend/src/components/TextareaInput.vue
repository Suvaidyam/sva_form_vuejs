<template>
  <div v-if="!field.hidden" class="flex flex-col gap-2">
    <div class="flex items-center">
      <label :for="field.name" class="text-sm font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }}
        <span v-if="field.reqd === 1" class="text-red-500 ml-1">*</span>
      </label>
      <div v-if="field.description" class="ml-2 relative group">
        <InfoIcon class="w-4 h-4 text-gray-400 cursor-help" />
        <div class="absolute left-0 bottom-6 bg-black text-white text-xs rounded py-1 px-2 w-48 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10">
          {{ field.description }}
        </div>
      </div>
    </div>
    <textarea
      :id="field.name"
      :value="modelValue"
      @input="handleInput"
      @blur="handleBlur"
      :disabled="field.read_only"
      :required="field.reqd"
      :rows="field.rows || 3"
      class="px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600"
    ></textarea>
  </div>
</template>

<script setup>
import { inject } from 'vue'
import { InfoIcon } from 'lucide-vue-next'

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])
const saveAsDraft = inject('saveAsDraft')

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleBlur = () => {
  saveAsDraft({ [props.field.fieldname]: props.modelValue })
}
</script>

<style scoped>
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}
</style>