<template>
  <div v-if="!field.hidden" class="flex flex-col gap-2">

    <span v-if="index < 1 &&   fieldParsedDescription?.qlable"
      class="text-md font-medium text-gray-900 dark:text-gray-200 block">
      {{  fieldParsedDescription?.qlable }}
    </span>
    <span v-if="index < 1 &&  fieldParsedDescription?.cenrieo && !props.isCard"
      class="text-sm text-gray-700  ">{{  fieldParsedDescription?.cenrieo }}
    </span>

    <div class="flex items-center justify-between">
      <label :for="field.name" class="text-md font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }}
        <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
      </label>
      <div v-if=" fieldParsedDescription?.info" class="ml-2 relative">
        <Popover v-slot="{ open }" class="relative">
          <PopoverButton class="focus:outline-none">
            <InfoIcon class="w-5 h-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
          </PopoverButton>
          <transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0" leave-active-class="transition duration-150 ease-in"
            leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
            <PopoverPanel class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-full right-0 sm:px-0 lg:max-w-3xl">
              <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                <div class="p-4 bg-white dark:bg-gray-800">
                  <p class="text-sm text-gray-700 dark:text-gray-300">
                    {{  fieldParsedDescription?.info }}
                  </p>
                </div>
              </div>
            </PopoverPanel>
          </transition>
        </Popover>
      </div>
    </div>
    <span v-if=" fieldParsedDescription?.desc" class="text-md font-medium text-gray-900 dark:text-gray-200 block">
      {{  fieldParsedDescription?.desc }}
    </span>
    <div class="relative">
      <input :id="field.name" :value="manipulateModelValue(modelValue)" @input="handleInput" @focus="openPicker"
        type="month" :disabled="field.read_only" :required="isFieldMandatory(field)" :placeholder="field.placeholder"
        :class="[
          'w-full h-10 px-3 border rounded-md text-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
          'dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:focus:ring-blue-400 dark:focus:border-blue-400',
          { 'opacity-50 cursor-not-allowed': field.read_only },
          { 'border-red-500 focus:ring-red-500 focus:border-red-500': error }
        ]" />
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, inject, computed } from 'vue'
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
    default: false
  },
  formData: {
    type: Object,
    default: () => ({})
  },
 
  index: {
    type: Number,
    default: 0
  }
})

const fieldParsedDescription = computed(() => {
  return getString(props.field.description || "")
})


function getString(str) {
  let desc = "";
  let info = "";
  let qlable = "";
  let cenrieo = "";

  // Handle {} first
  const match = str.match(/\{([^}]+)\}/);
  if (match) {
    info = match[1]; // Extract content inside {}
    str = str.replace(match[0], "").trim(); // Remove {} and its content from the string
  }

  // Handle @@ next
  const cenrieoSplit = str.split("@@");
  if (cenrieoSplit.length > 1) {
    cenrieo = cenrieoSplit[1].trim(); // Extract content after @@
    str = cenrieoSplit[0].trim(); // Keep content before @@
  }

  // Handle $$ last
  const parts = str.split("$$");
  if (parts.length > 1) {
    qlable = parts[1].trim(); // Extract content after $$
    str = parts[0].trim(); // Keep content before $$
  }

  // The remaining string is desc
  desc = str.trim();

  return { desc, info, qlable, cenrieo };
}



const manipulateModelValue = (modelValue) => {
  if (!modelValue) return ''
  if (modelValue.split('-').length === 3) {
    return modelValue.split('-').slice(0, 2).join('-')
  } else if (modelValue.split('-').length === 2) {
    return modelValue
  }
}

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
  const value = event.target.value
  emit('update:modelValue', value + '-01')
  validateInput(value + '-01')
  if (props.onfieldChange) {
    saveAsDraft({ [props.field.fieldname]: value + '-01' })
  }
}

const openPicker = (event) => {
  const input = event.target
  if (input.showPicker) {
    input.showPicker()
  } else {
    console.warn('showPicker is not supported in this browser.')
    // Fallback (e.g., display a custom modal or instruct the user to click the input field)
  }
}

const validateInput = (value) => {
  error.value = ''
  if (props.field.reqd && !value) {
    error.value = `${props.field.label} is required.`
  }
}
</script>
