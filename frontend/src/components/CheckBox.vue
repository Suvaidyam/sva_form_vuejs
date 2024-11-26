<template>
  <div v-if="!field.hidden" class="flex flex-col gap-2">
    <div :class="props.isCard ? 'gap-2' : ''" class="flex items-center">
      <p v-if="props.isCard" class="w-6 h-6 rounded-full bg-gray-500 text-white flex justify-center items-center text-sm">
        {{ 1 }}
      </p>
      <label class="text-sm font-medium text-gray-700 dark:text-gray-200">
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
    <div v-if="!props.isCard" class="flex flex-wrap -mx-2">
      <div v-for="(columnOptions, columnIndex) in splitOptions" :key="columnIndex" 
           :class="columnClasses"
           class="px-2 mb-4">
        <div v-for="option in columnOptions" :key="option.name" class="flex items-center mb-2">
          <input 
            :id="`${field.name}-${option.name}`" 
            :name="field.name" 
            type="checkbox" 
            :checked="isChecked(option)"
            @change="updateValue(option)" 
            :disabled="field.read_only" 
            :required="field.reqd && modelValue.length === 0"
            class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" 
          />
          <label :for="`${field.name}-${option.name}`" class="ml-2 block text-sm text-gray-700 dark:text-gray-200 truncate">
            {{ option.label }}
          </label>
        </div>
      </div>
    </div>
    <div v-else class="flex flex-wrap -mx-2 px-6">
      <div v-for="(columnOptions, columnIndex) in splitOptions" :key="columnIndex" 
           :class="columnClasses"
           class="px-2 mb-4">
        <label 
          v-for="option in columnOptions" 
          :key="option.name"
          :for="`${field.name}-${option.name}`" 
          class="flex items-center gap-2 border rounded-md p-2 mb-2"
        >
          <input 
            :id="`${field.name}-${option.name}`" 
            :name="field.name" 
            type="checkbox" 
            :checked="isChecked(option)"
            @change="updateValue(option)" 
            :disabled="field.read_only" 
            :required="isFieldMandatory(field) && modelValue.length === 0"
            class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600 flex-shrink-0" 
          />
          <p class="ml-2 block text-sm text-gray-700 dark:text-gray-200 truncate">
            {{ option.label }}
          </p>
        </label>
      </div>
    </div>
    <div v-else class="flex flex-wrap -mx-2 px-6">
      <div v-for="(columnOptions, columnIndex) in splitOptions" :key="columnIndex" 
           :class="columnClasses"
           class="px-2 mb-4">
        <label 
          v-for="option in columnOptions" 
          :key="option.name"
          :for="`${field.name}-${option.name}`" 
          class="flex items-center gap-2 border rounded-md p-2 mb-2"
        >
          <input 
            :id="`${field.name}-${option.name}`" 
            :name="field.name" 
            type="checkbox" 
            :checked="isChecked(option)"
            @change="updateValue(option)" 
            :disabled="field.read_only" 
            :required="isFieldMandatory(field) && modelValue.length === 0"
            class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" 
          />
          <p class="ml-2 block text-sm text-gray-700 dark:text-gray-200">
            {{ option.label }}
          </p>
        </label>
      </div>
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, watch, inject, computed } from 'vue'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { InfoIcon } from 'lucide-vue-next'

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  isCard: {
    type: Boolean,
    required: false,
    default: false
  },
  modelValue: {
    type: Array,
    default: () => []
  },
  onfieldChange: {
    type: Boolean,
    required: false,
    default: false
  },
  formData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const call = inject('$call')
const saveAsDraft = inject('saveAsDraft')

const options = ref([])
const error = ref('')


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
const splitOptions = computed(() => {
  if (options.value.length <= 8) {
    return [options.value]
  } else {
    const columns = 4
    const itemsPerColumn = Math.ceil(options.value.length / columns)
    return Array.from({ length: columns }, (_, index) => 
      options.value.slice(index * itemsPerColumn, (index + 1) * itemsPerColumn)
    )
  }
})

const columnClasses = computed(() => {
  if (options.value.length <= 6) {
    return 'w-full'
  } else {
    return 'w-full sm:w-1/2 md:w-1/4'
  }
})

const getOptions = async () => {
  try {
    let filters = {}
    if (props.field.link_filters) {
      try {
        filters = JSON.parse(props.field.link_filters)
      } catch (e) {
        console.error('Invalid link_filters JSON:', e)
      }
    } else {
      filters = { field: props.field.fieldname }
    }
    const response = await call('frappe.client.get_list', {
      doctype: 'Field Options',
      filters: filters,
      fields: ['*'],
    })
    options.value = response
  } catch (err) {
    console.error('Error fetching options:', err)
  }
}

const isChecked = (option) => {
  return Array.isArray(props.modelValue) && props.modelValue.some(item => item.field_options === option.name)
}

const validateInput = (newValue) => {
  error.value = ''
  if (props.field.reqd && newValue.length === 0) {
    error.value = `${props.field.label} is required.`
  }
}

const updateValue = (option) => {
  if (!Array.isArray(props.modelValue)) {
    console.error('modelValue is not an array:', props.modelValue)
    return
  }

  const newValue = [...props.modelValue]
  const index = newValue.findIndex(item => item.field_options === option.name)

  if (index === -1) {
    newValue.push({
      doctype: "Options Child",
      parentfield: props.field.fieldname,
      parenttype: props.field.parent,
      field_options: option.name
    })
  } else {
    newValue.splice(index, 1)
  }

  validateInput(newValue)
  emit('update:modelValue', newValue)

  if (props.onfieldChange && !error.value) {
    saveAsDraft({ [props.field.fieldname]: newValue })
  }
}

watch(() => props.field, getOptions, { immediate: true })
</script>



<style scoped>
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

/* Add these new styles */
input[type="checkbox"] {
  min-width: 1rem;
  min-height: 1rem;
}

label, p {
  max-width: calc(100% - 1.5rem);
}


.w-96{
  width: 100% !important;
  max-width: 800px !important;
  min-width: 500px !important;
 }
</style>