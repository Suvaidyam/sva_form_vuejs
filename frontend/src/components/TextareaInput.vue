<template>
  <div v-if="!field.hidden" class="flex flex-col gap-2">
    <p v-if="index < 1 " >{{  section }}</p>
    <div class="flex items-center">
      <label :for="field.name" class="text-sm font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }} <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
      </label>
      <div v-if="field.description" class="ml-2 relative">
        <Popover v-slot="{ open }" class="relative">
          <PopoverButton @mouseenter="open = true" @mouseleave="open = false" class="focus:outline-none">
            <InfoIcon class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
          </PopoverButton>

          <transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0" leave-active-class="transition duration-150 ease-in"
            leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
            <PopoverPanel class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl"
              @mouseenter="open = true" @mouseleave="open = false">
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
   
    <textarea :id="field.name" :value="modelValue" @input="handleInput" @blur="handleBlur" :disabled="field.read_only"
      :required="isFieldMandatory(field)" :rows="field.rows || 3" :placeholder="field.placeholder" :class="[
        'px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
        'dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600',
        { 'border-red-500 focus:ring-red-500': error }
      ]"></textarea>
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
    type: String,
    required: true
  },
  onfieldChange: {
    type: Boolean,
    required: false,
    default: false
  },
  formData: {
    type: Object,
    required: false,
    default: () => ({})
  },
  section: { type: String, required: false, default: '' },
  index: {
    type: Number,
    required: false,
    default: 0
  },
})

const emit = defineEmits(['update:modelValue'])
const saveAsDraft = inject('saveAsDraft')

const error = ref('')

const handleInput = (event) => {
  const value = event.target.value
  emit('update:modelValue', value)
  validateInput(value)
}

const isFieldMandatory = (field) => {
  if (field.reqd) return true
  if (!field.mandatory_depends_on) return false
  const condition = field.mandatory_depends_on.replace('eval:', '').replace(/doc\./g, 'formData.')
  try {
    return new Function('formData', `return ${condition}`)(props?.formData)
  } catch (error) {
    console.error('Error evaluating field visibility:', error)
    return false
  }
}

const handleBlur = () => {
  validateInput(props.modelValue)
  if (props.onfieldChange && !error.value) {
    saveAsDraft({ [props.field.fieldname]: props.modelValue })
  }
}

const validateInput = (value) => {
  error.value = ''
  if (props.field.reqd && !value.trim()) {
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
</style>