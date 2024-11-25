<template>
  <div v-if="!field.hidden" class="flex flex-col gap-2">
    <div class="flex items-center">
      <label :for="field.name" class="text-sm font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }}
        <span v-if="field.reqd === 1" class="text-red-500 ml-1">*</span>
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
    <div class="relative">
      <input :id="field.name" :value="modelValue" @focusout="handleBlur" :type="inputType" :disabled="field.read_only"
        :required="field.reqd" :placeholder="field.placeholder" :class="[
          'w-full h-10 px-3 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
          'dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:focus:ring-blue-400 dark:focus:border-blue-400',
          { 'pr-10': field.fieldtype === 'Password' },
          { 'border-red-500 focus:ring-red-500 focus:border-red-500': error }
        ]" />
      <button v-if="field.fieldtype === 'Password'" @click="togglePasswordVisibility" type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
        <EyeIcon v-if="inputType === 'password'" class="h-5 w-5" />
        <EyeOffIcon v-else class="h-5 w-5" />
      </button>
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { InfoIcon, EyeIcon, EyeOffIcon } from 'lucide-vue-next'

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
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])
const saveAsDraft = inject('saveAsDraft')

const inputType = ref(props.field.fieldtype === 'Password' ? 'password' : 'text')
const error = ref('')

const togglePasswordVisibility = () => {
  inputType.value = inputType.value === 'password' ? 'text' : 'password'
}

// const handleInput = (event) => {
//   const value = event.target.value
//   emit('update:modelValue', value)
//   validateInput(value)
// }

const handleBlur = (event) => {
  const value = event.target.value;
  console.log(value,'value');
  emit('update:modelValue', value)
  validateInput(props.modelValue)
  if (props.onfieldChange && !error.value) {
    saveAsDraft({ [props.field.fieldname]: value })
  }
}

const validateInput = (value) => {
  error.value = ''
  if (props.field.reqd && !value) {
    error.value = `${props.field.label} is required.`
  }
}

</script>