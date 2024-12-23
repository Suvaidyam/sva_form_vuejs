<template>
  <div v-if="!field.hidden" class="w-full">
    <div> 
      <div class="flex items-center gap-2 pt-4 pb-4">
        <p v-if="isCard"
          class="w-7 h-7 min-w-7 min-h-7 text-sm flex items-center justify-center rounded-full bg-gray-700 text-white">
          {{ index + 1 }}
        </p>
        <label :for="`${field.name}-${visibleOptions[0]?.name}`"
          :class="isCard ? 'text-h5' : 'text-md font-medium text-gray-900 dark:text-gray-200'"
          class="block font-medium text-gray-900 dark:text-gray-200">
          {{ field.label }} {{ field.description }}
          <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
        </label>
       
      </div>
      <div v-if="dropDownOptions" class="mt-1">
        <select :id="`${field.name}-select`" :name="field.name" v-model="selectedOption"
          @change="updateValue(selectedOption)" :disabled="field.read_only" :required="isFieldMandatory(field)"
          class="mt-1 block w-full pl-3 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          <option value="" disabled selected>Select an option</option>
          <option v-for="option in visibleOptions" :key="option.name" :value="option.name">
            {{ option.label }}
          </option>
        </select>
      </div>
      <div v-else :class="[
        isRow ? 'flex-col md:flex-row' : 'flex-col border py-2 rounded-sm' ,'flex px-3 w-full gap-2'
      ]">
        <label v-for="option in options" :key="option.name" :for="`${field.name}-${option.name}`"
          :class="[isCard ? 'border p-2 bg-white rounded-md shadow-sm' : 'ml-5', isRow ? 'w-full' : '']"
          class="flex items-center text-sm cursor-pointer">
          <div class="flex items-center gap-2 w-5 min-w-6 h-5">
            <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
              :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
              :required="isFieldMandatory(field)"
              class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
          </div>
          <span class="flex-grow">{{ option.label }}</span>
        </label>
      </div>
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject, onMounted } from 'vue'

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    required: false,
    default: ''
  },
  isCard: {
    type: Boolean,
    required: false,
    default: false
  },
  isRow: {
    type: Boolean,
    required: false,
    default: false
  },
  isColumn: {
    type: Boolean,
    required: false,
    default: false
  },
  index: {
    type: Number,
    required: false,
    default: 0
  },
  section: {
    type: String,
    required: false,
  },
  onfieldChange: {
    type: Boolean,
    required: false,
    default: false
  },
  dropDownOptions: {
    type: Boolean,
    required: false,
    default: false
  },
  formData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])
const call = inject('$call')
const saveAsDraft = inject('saveAsDraft')
const options = ref([])
const error = ref('')
const selectedOption = ref('')

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

const visibleOptions = computed(() => {
  return options.value.filter(option => isOptionVisible(option))
})


const fieldParsedDescription = computed(() => {
  return getString(props.field.description || "")
})

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
    let response = []
    if (props.field.options === "Field Options") {
      response = await call('sva_form_vuejs.controllers.api.get_option', {
        filters: filters
      })
    } else {
      response = await call('sva_form_vuejs.controllers.api.get_option_with_dt', {
        dt: props.field.options,
        filters: props.field.link_filters ? JSON.parse(props.field.link_filters) : []
      })
    }
    options.value = response
  } catch (err) {
    console.error('Error fetching options:', err)
  }
}

const validateInput = (value) => {
  error.value = ''
  if (isFieldMandatory(props.field) && !value) {
    error.value = `${props.field.label} is required.`
  }
}

const updateValue = (value) => {
  emit('update:modelValue', value)
  validateInput(value)
  if (props.onfieldChange) {
    saveAsDraft({ [props.field.fieldname]: value })
  }
}

watch(() => props.field, getOptions, { immediate: true })

watch(() => props.modelValue, (newValue) => {
  selectedOption.value = newValue
}, { immediate: true })

onMounted(() => {
  getOptions()
})
document.addEventListener('focusin', (e) => {
  if (e.target.tagName === 'INPUT' && e.target.validationMessage) {
    const rect = e.target.getBoundingClientRect();
    if (rect.top < 150) { 
      window.scrollBy(0, rect.top - 150);
    }
  }
});

</script>

<style scoped>
.w-96 {
  width: 100% !important;
  max-width: 800px !important;
  min-width: 500px !important;
}
</style>