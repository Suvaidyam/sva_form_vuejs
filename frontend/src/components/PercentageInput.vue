<template>
    <div v-if="!field.hidden" class="flex flex-col gap-2">
      <div class="flex items-center">
        <label :for="field.name" class="text-sm font-medium text-gray-700 dark:text-gray-200">
          {{ field.label }}
          <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
        </label>
        <div v-if="field.description" class="ml-2 relative">
          <Popover v-slot="{ open }" class="relative">
            <PopoverButton @mouseenter="open = true" @mouseleave="open = false" class="focus:outline-none">
              <InfoIcon class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
            </PopoverButton>
  
            <transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition duration-150 ease-in"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 translate-y-1"
            >
              <PopoverPanel
                class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl"
                @mouseenter="open = true"
                @mouseleave="open = false"
              >
                <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                  <div class="p-4 bg-white dark:bg-gray-800">
                    <p class="text-sm text-gray-700 dark:text-gray-300">
                      {{ field.description }}
                    </p>
                  </div>
                </div>
              </PopoverPanel>
            </transition>
          </Popover>
        </div>
      </div>
      <div class="relative flex items-center">
        <input
          :id="field.name"
          :value="modelValue"
          @input="handleInput"
          @change="handleChange"
          type="range"
          min="0"
          max="100"
          step="1"
          :disabled="field.read_only"
          :required="isFieldMandatory(field)"
          :class="[
            'w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700',
            { 'opacity-50 cursor-not-allowed': field.read_only }
          ]"
        />
        <span class="ml-3 text-sm font-medium text-gray-700 dark:text-gray-200">
          {{ modelValue }}%
        </span>
      </div>
      <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, inject } from 'vue'
  import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
  import { InfoIcon } from 'lucide-vue-next'
  
  const props = defineProps({
    field: {
      type: Object,
      required: true
    },
    modelValue: {
      type: [Number, String],
      required: true
    },
    onfieldChange: {
      type: Boolean,
      default: false
    },
    formData: {
      type: Object,
      default: () => ({})
    }
  })
  
  const emit = defineEmits(['update:modelValue'])
  const saveAsDraft = inject('saveAsDraft')
  
  const error = ref('')
  
  const isFieldMandatory = (field) => {
    if (field.reqd) return true
    if (!field.mandatory_depends_on) return false
    const condition = field.mandatory_depends_on.replace('eval:', '').replace(/doc\./g, 'formData.')
    try {
      return new Function('formData', `return ${condition}`)(props.formData)
    } catch (error) {
      console.error('Error evaluating field visibility:', error)
      return false
    }
  }
  
  const handleInput = (event) => {
    const value = parseInt(event.target.value, 10)
    emit('update:modelValue', value)
    validateInput(value)
  }
  
  const handleChange = (event) => {
    const value = parseInt(event.target.value, 10)
    validateInput(value)
    if (props.onfieldChange && !error.value) {
      saveAsDraft({ [props.field.fieldname]: value })
    }
  }
  
  const validateInput = (value) => {
    error.value = ''
    if (props.field.reqd && (value === null || value === undefined)) {
      error.value = `${props.field.label} is required.`
    }
  }
  </script>
  
  <style scoped>
  .w-96 {
    width: 100% !important;
    max-width: 800px !important;
    min-width: 500px !important;
  }
  
  /* Styling for the range input */
  input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
    height: 8px;
    background: #ddd;
    outline: none;
    opacity: 0.7;
    transition: opacity 0.2s;
  }
  
  input[type="range"]:hover {
    opacity: 1;
  }
  
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    background: #3b82f6;
    cursor: pointer;
    border-radius: 50%;
  }
  
  input[type="range"]::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: #3b82f6;
    cursor: pointer;
    border-radius: 50%;
  }
  
  .dark input[type="range"] {
    background: #4b5563;
  }
  
  .dark input[type="range"]::-webkit-slider-thumb {
    background: #60a5fa;
  }
  
  .dark input[type="range"]::-moz-range-thumb {
    background: #60a5fa;
  }
  </style>