<template>
  <div v-if="!field.hidden" class="flex flex-col">
    <div  class="flex items-center gap-2 pb-4 pt-2">
      <p 
        class="w-7 min-w-7 min-h-7 h-7 rounded-full bg-gray-700 text-white flex justify-center items-center text-sm">
        {{ 1 }}
      </p>
      <label :class="!props.isCard ? 'text-md' : 'text-sm'"
        class="font-medium text-black dark:text-gray-200 break-words">
        {{ field.label }} {{ field.description }}
        <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
      </label>
    </div>
    <div v-if="options.length" class="flex flex-col border pt-2 rounded-sm items-center justify-center">
      <p></p>
        <label v-for="option in options" :key="option.name" :for="`${field.name}-${option.name}`"
          class="w-full flex bg-white items-center gap-2 border rounded-md p-2 mb-2">
          <input :id="`${field.name}-${option.name}`" :name="field.name" type="checkbox" :checked="isChecked(option)"
            @change="updateValue(option)" :disabled="field.read_only"
            :required="isFieldMandatory(field) && modelValue.length === 0"
            class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600 flex-shrink-0" />
          <p class="ml-2 block text-sm text-black dark:text-gray-200 break-words">
            {{ option.label }}
          </p>
        </label>
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, watch, inject, computed } from 'vue'

const props = defineProps({
  field: { type: Object, required: true },
  isCard: { type: Boolean, default: false },
  modelValue: { type: Array, default: () => [] },
  onfieldChange: { type: Boolean, default: false },
  formData: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:modelValue'])
const call = inject('$call')
const saveAsDraft = inject('saveAsDraft')

const options = ref([])
const error = ref('')

const fieldParsedDescription = computed(() => {
  const str = props.field.description || ""
  return { desc: str.split('$$')[0]?.split('@@')[0]?.trim() || "" }
})

const isFieldMandatory = (field) => {
  if (field.reqd) return true
  if (!field.mandatory_depends_on) return false
  try {
    const condition = field.mandatory_depends_on.replace('eval:', '').replace(/doc\./g, 'formData.')
    return new Function('formData', `return ${condition}`)(props?.formData)
  } catch {
    return false
  }
}

const splitOptions = computed(() => {
  const columns = 4
  if (options.value.length <= 8) return [options.value]
  const itemsPerColumn = Math.ceil(options.value.length / columns)
  return Array.from({ length: columns }, (_, index) =>
    options.value.slice(index * itemsPerColumn, (index + 1) * itemsPerColumn)
  )
})

const columnClasses = computed(() =>
  options.value.length <= 6 ? 'w-full' : 'w-full sm:w-1/2 md:w-1/4'
)

const getOptions = async () => {
  try {
    const filters = props.field.link_filters ? JSON.parse(props.field.link_filters) : { field: props.field.fieldname, ref_doctype: props.field.parent }
    options.value = await call('sva_form_vuejs.controllers.api.get_option', { filters })
  } catch (err) {
    console.error('Error fetching options:', err)
  }
}

const isChecked = (option) =>
  Array.isArray(props.modelValue) && props.modelValue.some(item => item.field_options === option.name)

const validateInput = (newValue) => {
  error.value = props.field.reqd && newValue.length === 0 ? `${props.field.label} is required.` : ''
}

const updateValue = (option) => {
  if (!Array.isArray(props.modelValue)) return console.error('modelValue is not an array:', props.modelValue)

  let newValue = [...props.modelValue]

  if (option.group) {
    // If a grouped option is selected, deselect all non-grouped options
    newValue = [{ doctype: "Options Child", parentfield: props.field.fieldname, parenttype: props.field.parent, field_options: option.name }]
  } else {
    // If a non-grouped option is selected, ensure grouped options are deselected
    const index = newValue.findIndex(item => item.field_options === option.name)
    if (index === -1) {
      newValue.push({ doctype: "Options Child", parentfield: props.field.fieldname, parenttype: props.field.parent, field_options: option.name })
    } else {
      newValue.splice(index, 1)
    }

    // Ensure grouped options are removed
    newValue = newValue.filter(item => {
      const matchedOption = options.value.find(opt => opt.name === item.field_options)
      return !matchedOption?.group
    })
  }

  validateInput(newValue)
  emit('update:modelValue', newValue)
  if (props.onfieldChange && !error.value) saveAsDraft({ [props.field.fieldname]: newValue })
}

watch(() => props.field, getOptions, { immediate: true })
</script>

<style scoped>
input[type="checkbox"] {
  min-width: 1rem;
  min-height: 1rem;
}

label,
p {
  max-width: calc(100% - 1.5rem);
  word-wrap: break-word;
  overflow-wrap: break-word;
}
</style>
