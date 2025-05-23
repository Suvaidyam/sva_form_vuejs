<template>
  <div v-if="!field.hidden" class="flex flex-col gap-1">
    <div :class="props.isCard ? 'gap-2' : ''" class="flex items-center gap-">
      <div class="flex items-center">
        <label :for="field.name" class="text-sm text-gray-900 dark:text-gray-200">{{ field.placeholder }}</label>
        <input :id="field.name" :name="field.name" type="checkbox" :checked="modelValue" @change="handleChange"
          @blur="handleBlur" :disabled="field.read_only" :required="isFieldMandatory(field)"
          class="h-4 w-4 mr-2 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600"
          :class="{ 'border-red-500 focus:ring-red-500': error }" />
      </div>
      <div class="flex items-center justify-between">
        <p v-if="props.isCard"
          class="w-6 h-6 rounded-full bg-gray-500 text-white flex justify-center items-center text-sm mr-2">
          {{ 1 }}
        </p>
         <span v-if="fieldParsedDescription?.qlable" class="text-md text-gray-900 dark:text-gray-300">
      {{ fieldParsedDescription?.qlable }}
    </span>
    <span v-if="fieldParsedDescription?.cenrieo" class="text-sm text-gray-900 dark:text-gray-400">
      {{ fieldParsedDescription?.cenrieo }}
    </span>
        <label :for="field.name" :class="props.isCard ? 'text-sm' : 'text-md'"
          class="font-medium text-gray-900 dark:text-gray-200">
          {{ field.label }}
          <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
        </label>
        <div v-if="fieldParsedDescription?.info" class="ml-2 relative">
          <Popover v-slot="{ open }" class="relative">
            <PopoverButton class="focus:outline-none">
              <InfoIcon class="w-5 h-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
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
                class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-full right-0 sm:px-0 lg:max-w-3xl"
              >
                <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                  <div class="p-4 bg-white dark:bg-gray-800">
                    <p class="text-sm text-gray-700 dark:text-gray-300">
                      {{ fieldParsedDescription?.info }}
                    </p>
                  </div>
                </div>
              </PopoverPanel>
            </transition>
          </Popover>
        </div>
      </div>
      
    </div>
     <span v-if="fieldParsedDescription?.desc" class="text-md font-medium text-gray-900 dark:text-gray-200 block">
      {{ fieldParsedDescription?.desc }}
    </span>
   
   
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
    type: Boolean,
    required: true
  },
  isCard: {
    type: Boolean,
    required: false,
    default: false
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

const handleChange = (event) => {
  const value = event.target.checked
  emit('update:modelValue', value)
  validateInput(value)
}

const handleBlur = () => {
  validateInput(props.modelValue)
  if (props.onfieldChange && !error.value) {
    saveAsDraft({ [props.field.fieldname]: props.modelValue })
  }
}

const validateInput = (value) => {
  error.value = ''
  if (props.field.reqd && !value) {
    error.value = `${props.field.label} is required.`
  }
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

const fieldParsedDescription = computed(() => {
  return getString(props.field.description || "")
})

function getString(str) {
  let desc = ""
  let info = ""
  let qlable = ""
  let cenrieo = ""

  const match = str.match(/\{([^}]+)\}/)
  if (match) {
    info = match[1]
    str = str.replace(match[0], "").trim()
  }

  const cenrieoSplit = str.split("@@")
  if (cenrieoSplit.length > 1) {
    cenrieo = cenrieoSplit[1].trim()
    str = cenrieoSplit[0].trim()
  }

  const parts = str.split("$$")
  if (parts.length > 1) {
    qlable = parts[1].trim()
    str = parts[0].trim()
  }

  desc = str.trim()

  return { desc, info, qlable, cenrieo }
}
</script>
