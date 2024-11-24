<template>
  <div v-if="!field.hidden" class="flex flex-col gap-2">
    <div :class="props.isCard?'gap-2':''" class="flex items-center">
      <p class="w-6 h-6 rounded-full bg-gray-500 text-white flex justify-center items-center text-sm" v-if="props.isCard">{{ 1 }}</p>
      <label class="text-sm font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }}
        <span v-if="field.reqd" class="text-red-500 ml-1">*</span>
      </label>
      <div v-if="field.description" class="ml-2 relative group">
        <InfoIcon class="w-4 h-4 text-gray-400 cursor-help" />
        <div class="absolute left-0 bottom-6 bg-black text-white text-xs rounded py-1 px-2 w-48 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10">
          {{ field.description }}
        </div>
      </div>
    </div>
    <div class="space-y-2" v-if="!props.isCard">
      <div v-for="option in options" :key="option.name" class="flex items-center">
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
        <label :for="`${field.name}-${option.name}`" class="ml-2 block text-sm text-gray-700 dark:text-gray-200">
          {{ option.label }}
        </label>
      </div>
    </div>
    <div v-else class="flex flex-col gap-2 px-6">
      <label :for="`${field.name}-${option.name}`" v-for="option in options" :key="option.name" class="flex items-center gap-2 border rounded-md p-2">
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
        <p class="ml-2 block text-sm text-gray-700 dark:text-gray-200">
          {{ option.label }}
        </p>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, inject } from 'vue'
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
  }
})

const emit = defineEmits(['update:modelValue'])

const call = inject('$call')
const saveAsDraft = inject('saveAsDraft')

const options = ref([])

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
  
  emit('update:modelValue', newValue)
  
  // Save as draft after updating the value
  saveAsDraft({ [props.field.fieldname]: newValue })
}

watch(() => props.field, getOptions, { immediate: true })
</script>

<style scoped>
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}
</style>