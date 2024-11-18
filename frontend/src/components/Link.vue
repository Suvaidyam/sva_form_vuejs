<template>
  <div class="w-full">
    <div v-if="matrix" class="overflow-x-auto">
      <table class="w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
          <tr v-if="index < 1">
            <th scope="col"
              class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              Question
            </th>
            <th v-for="option in options" :key="option.name" scope="col"
              class="px-4 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              {{ option.label }}
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200 dark:bg-gray-900 dark:divide-gray-700">
          <tr>
            <td class="px-4 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">
             {{ field.label }}
            </td>
            <td v-for="option in options" :key="option.name" class="px-4 py-4 text-center">
              <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
                :checked="modelValue === option.name" @change="$emit('update:modelValue', option.name)"
                :disabled="field.read_only"
                class="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="space-y-2">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">{{ field.label }}</label>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div v-for="option in options" :key="option.name" class="flex items-center">
          <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
            :checked="modelValue === option.name" @change="$emit('update:modelValue', option.name)"
            :disabled="field.read_only"
            class="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
          <label :for="`${field.name}-${option.name}`" class="ml-2 block text-sm text-gray-700 dark:text-gray-200">
           {{ option.label }}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, inject } from 'vue'

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    required: false
  },
  matrix: {
    type: Boolean,
    required: false
  },
  isCard: {
    type: Boolean,
    required: false
  },
  index: {
    type: Number,
    required: false
  }
})

const emit = defineEmits(['update:modelValue'])

const call = inject('$call')

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
      filters = { field: props.field.fieldname, ref_doctype: props.field.parent }
    }
    const response = await call('sva_form_vuejs.controllers.api.get_option', {
      filters: filters
    })
    options.value = response
  } catch (err) {
    console.error('Error fetching options:', err)
  }
}

watch(() => props.field, getOptions, { immediate: true })
</script>