<template>
  <div class="mt-1">
    <select
      :id="`${field.name}-select`"
      :name="field.name"
      :value="modelValue"
      @change="updateValue($event.target.value)"
      :disabled="field.read_only"
      :required="isFieldMandatory"
      class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
    >
      <option value="" disabled>Select an option</option>
      <option v-for="option in visibleOptions" :key="option.name" :value="option.name">
        {{ option.label }}
      </option>
    </select>
  </div>
</template>

<script setup>
const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    required: false,
    default: ''
  },
  visibleOptions: {
    type: Array,
    required: true
  },
  isFieldMandatory: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const updateValue = (value) => {
  emit('update:modelValue', value)
}
</script>