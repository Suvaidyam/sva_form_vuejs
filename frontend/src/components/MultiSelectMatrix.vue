<template>
  <div v-if="!field.hidden" class="w-full">
    <div class="flex items-center gap-2 mb-2">
      <span v-if="parsedDescription?.qlable || fieldParsedDescription?.qlable"
        class="text-md font-medium text-gray-700 dark:text-gray-200 block break-words">
        {{ parsedDescription?.qlable || fieldParsedDescription?.qlable }}
      </span>
      <div v-if="parsedDescription?.info || fieldParsedDescription?.info" class="relative">
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
                  <p class="text-sm text-gray-700 dark:text-gray-300 break-words">
                    {{ parsedDescription?.info || fieldParsedDescription?.info }}
                  </p>
                </div>
              </div>
            </PopoverPanel>
          </transition>
        </Popover>
      </div>
    </div>
    <p v-if="parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo"
      class="text-sm text-gray-500 mb-2 break-words">
      {{ parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo }}
    </p>
    <div class="overflow-x-auto">

      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead v-if="index < 1" class="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              Questions
            </th>
            <th v-for="option in columnOptions" :key="option.name" scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              {{ option.label }}
            </th>
          </tr>
        </thead>

        <tbody class="bg-white divide-y divide-gray-200 dark:bg-gray-900 dark:divide-gray-700">
          <tr v-for="rowOption in columnOptions" :key="rowOption.name">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
              {{ field.label }}
            </td>
            <td v-for="columnOption in columnOptions" :key="columnOption.name"
              class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
              <input :id="`${field.name}-${rowOption.name}-${columnOption.name}`"
                :name="`${field.name}-${rowOption.name}`" type="checkbox" :checked="isChecked(rowOption, columnOption)"
                @change="updateValue(rowOption, columnOption)" :disabled="isOptionDisabled(rowOption, columnOption)"
                :required="isFieldMandatory(field) && !hasSelection(rowOption)"
                class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="error" class="mt-2 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject } from 'vue'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { InfoIcon } from 'lucide-vue-next'

const props = defineProps({
  field: {
    type: Object,
    required: true
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
  },
  section: {
    type: String,
    required: false,
  },
  index: {
    type: Number,
    required: false,
    default: 0
  },

})

const emit = defineEmits(['update:modelValue'])

const call = inject('$call')
const saveAsDraft = inject('saveAsDraft')

const options = ref([])
const error = ref('')

const parsedDescription = computed(() => getString(props.section || ""))
const fieldParsedDescription = computed(() => getString(props.field.description || ""))

function getString(str) {
  let desc = "";
  let info = "";
  let qlable = "";
  let cenrieo = "";

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

const isFieldMandatory = (field) => {
  if (field.reqd) return true
  if (!field.mandatory_depends_on) return false
  const condition = field.mandatory_depends_on.replace('eval:', '').replace(/doc\./g, 'formData.')
  try {
    return new Function('formData', `return ${condition}`)(props.formData)
  } catch (error) {
    console.error('Error evaluating field mandatory condition:', error)
    return false
  }
}

const isOptionVisible = (option) => {
  if (!option.depends_on) return true
  const condition = option.depends_on.replace('eval:', '').replace(/doc\./g, 'formData.')
  try {
    return new Function('formData', `return ${condition}`)(props.formData)
  } catch (error) {
    console.error('Error evaluating option visibility:', error)
    return false
  }
}

const rowOptions = computed(() => options.value.filter(option => option.is_row && isOptionVisible(option)))
const columnOptions = computed(() => options.value.filter(option => !option.is_row && isOptionVisible(option)))

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

const isChecked = (rowOption, columnOption) => {
  return props.modelValue.some(item =>
    item.row_option === rowOption.name && item.column_option === columnOption.name
  )
}

const hasSelection = (rowOption) => {
  return props.modelValue.some(item => item.row_option === rowOption.name)
}

const validateInput = (newValue) => {
  error.value = ''
  if (isFieldMandatory(props.field) && newValue.length === 0) {
    error.value = `${props.field.label} is required.`
  }
}

const isOptionDisabled = (rowOption, columnOption) => {
  // Implement any disabling logic here if needed
  return false
}

const updateValue = (rowOption, columnOption) => {
  const newValue = [...props.modelValue]
  const index = newValue.findIndex(item =>
    item.row_option === rowOption.name && item.column_option === columnOption.name
  )

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

watch(() => props.formData, () => {
  // Re-evaluate visibility when formData changes
  rowOptions.value
  columnOptions.value
}, { deep: true })
</script>

<style scoped>
.w-96 {
  width: 100% !important;
  max-width: 800px !important;
  min-width: 500px !important;
}
</style>