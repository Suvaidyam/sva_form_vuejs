<template>
  <div v-if="!field.hidden" class="flex flex-col">

    
    <div >
      <span v-if="parsedDescription?.qlable || fieldParsedDescription?.qlable"
        class="text-md font-medium text-gray-700 dark:text-gray-200 block break-words">
        {{ parsedDescription?.qlable || fieldParsedDescription?.qlable }}
      </span>
      <span v-if="parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo"
        class="text-sm text-gray-500 break-words">
        {{ parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo }}
      </span>

      <div class="flex items-center">
        <div v-if="parsedDescription?.info || fieldParsedDescription?.info" class="ml-2 relative">
          <Popover v-slot="{ open }" class="relative">
            <PopoverButton @mouseenter="open = true" @mouseleave="open = false" class="focus:outline-none">
              <InfoIcon class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
            </PopoverButton>

            <transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition duration-150 ease-in"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <PopoverPanel
                class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl"
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

      <span v-if="parsedDescription?.desc || fieldParsedDescription.desc"
        class="text-sm text-gray-500 mb-2 break-words">
        {{ parsedDescription?.desc || fieldParsedDescription?.desc }}
      </span>

      <div class="">
        <div class="inline-block min-w-full py-2 align-middle">
          <div class="overflow-hidden rounded-lg">
            <div class="grid gap-x-4" :style="gridTemplateColumns">
              <template v-if="index < 1">
                <div
                  class="bg-gray-50 dark:bg-gray-800 p-4 text-gray-900 dark:text-gray-100 font-medium sticky left-0 z-10">
                  Question
                </div>
                <div v-for="option in visibleOptions" :key="`header-${option.name}`"
                  class="bg-gray-50 dark:bg-gray-800 p-4 text-gray-900 dark:text-gray-100 font-medium"
                  :class="{ 'text-left': matrix_code, 'text-center': !matrix_code }">
                  {{ matrix_code ? option.level : option.label }}
                </div>
              </template>

              <div
                class="bg-white dark:bg-gray-900 p-4 flex items-start border-t border-gray-200 dark:border-gray-700 min-h-[80px] sticky left-0 z-10">
                <div class="text-sm text-gray-900 dark:text-gray-100 w-full pr-6">
                  <label :for="`${field.name}-${visibleOptions[0]?.name}`" class="flex items-start">
                    <span class="mr-2">{{ field.label }} <span v-if="isFieldMandatory"
                        class="text-red-500">*</span></span>
                  </label>
                </div>
              </div>

              <template v-for="option in visibleOptions" :key="`checkbox-${option.name}`">
                <div v-if="matrix_code"
                  class="bg-white dark:bg-gray-900 p-4 border-t border-l border-gray-200 dark:border-gray-700 min-h-[80px]">
                  <div class="flex flex-col space-y-2">
                    <div class="flex items-center">
                      <input :id="`${field.name}-${option.name}`" :name="field.name" type="checkbox"
                        :checked="isChecked(option)" @change="updateValue(option)" :disabled="isOptionDisabled(option)"
                        :required="field.reqd && modelValue.length === 0"
                        class="h-4 w-4 text-primary border-gray-300 rounded focus:ring-primary dark:border-gray-600 dark:focus:ring-primary" />
                      <label :for="`${field.name}-${option.name}`"
                        class="ml-2 text-sm text-gray-900 dark:text-gray-100">
                        {{ option.label }}
                      </label>
                    </div>
                  </div>
                </div>
                <div v-else
                  class="bg-white dark:bg-gray-900 p-4 flex justify-center items-center border-t border-l border-gray-200 dark:border-gray-700 min-h-[80px]">
                  <input :id="`${field.name}-${option.name}`" :name="field.name" type="checkbox"
                    :checked="isChecked(option)" @change="updateValue(option)" :disabled="isOptionDisabled(option)"
                    :required="field.reqd && modelValue.length === 0"
                    class="h-4 w-4 text-primary border-gray-300 rounded focus:ring-primary dark:border-gray-600 dark:focus:ring-primary" />
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>

      <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, inject, computed } from 'vue'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { InfoIcon } from 'lucide-vue-next'
import MultiSelectMatrix from './MultiSelectMatrix.vue'

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
  multi_matrix: {
    type: [Boolean, String],
    required: false,
  },
  matrix_code: {
    type: Boolean,
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

  const match = str.match(/\{([^}]+)\}/);
  if (match) {
    info = match[1];
    str = str.replace(match[0], "").trim();
  }

  const cenrieoSplit = str.split("@@");
  if (cenrieoSplit.length > 1) {
    cenrieo = cenrieoSplit[1].trim();
    str = cenrieoSplit[0].trim();
  }

  const parts = str.split("$$");
  if (parts.length > 1) {
    qlable = parts[1].trim();
    str = parts[0].trim();
  }

  desc = str.trim();

  return { desc, info, qlable, cenrieo };
}

const isFieldMandatory = computed(() => {
  if (props.field.reqd) return true
  if (!props.field.mandatory_depends_on) return false
  return evaluateCondition(props.field.mandatory_depends_on, props.formData)
})

const isOptionVisible = (option) => {
  if (!option.depends_on) return true
  return evaluateCondition(option.depends_on, props.formData)
}

function evaluateCondition(condition, formData) {
  const parsedCondition = condition.replace('eval:', '').replace(/doc\./g, 'formData.')
  try {
    return new Function('formData', `return ${parsedCondition}`)(formData)
  } catch (error) {
    console.error('Error evaluating condition:', error)
    return false
  }
}

const visibleOptions = computed(() => options.value.filter(isOptionVisible))

const gridTemplateColumns = computed(() => {
  const optionCount = visibleOptions.value.length
  return `grid-template-columns: minmax(300px, 1fr) repeat(${optionCount}, minmax(${props.matrix_code ? '150px' : '100px'}, 1fr))`
})

const getOptions = async () => {
  try {
    const filters = props.field.link_filters
      ? JSON.parse(props.field.link_filters)
      : { field: props.field.fieldname, ref_doctype: props.field.parent }

    options.value = await call('sva_form_vuejs.controllers.api.get_option', { filters })
  } catch (err) {
    console.error('Error fetching options:', err)
  }
}

const isChecked = (option) =>
  Array.isArray(props.modelValue) && props.modelValue.some(item => item.field_options === option.name)

const validateInput = (newValue) => {
  error.value = props.field.reqd && newValue.length === 0
    ? `${props.field.label} is required.`
    : ''
}

const getSelectedGroup = computed(() => {
  if (!Array.isArray(props.modelValue) || props.modelValue.length === 0) return null
  const selectedOption = options.value.find(option =>
    props.modelValue.some(item => item.field_options === option.name)
  )
  return selectedOption?.group
})

const isOptionDisabled = (option) => {
  const selectedGroup = getSelectedGroup.value
  return option.group && selectedGroup !== null && selectedGroup !== option.group
}

const updateValue = (option) => {
  if (!Array.isArray(props.modelValue)) {
    console.error('modelValue is not an array:', props.modelValue)
    return
  }

  const newValue = [...props.modelValue]
  const index = newValue.findIndex(item => item.field_options === option.name)

  if (index === -1 && !isOptionDisabled(option)) {
    newValue.push({
      doctype: "Options Child",
      parentfield: props.field.fieldname,
      parenttype: props.field.parent,
      field_options: option.name
    })
  } else if (index !== -1) {
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
  visibleOptions.value
}, { deep: true })
</script>

<style scoped>
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

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

.w-96 {
  width: 100% !important;
  max-width: 800px !important;
  min-width: 500px !important;
}

.overflow-x-auto {
  overflow-x: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.sticky {
  position: sticky;
  background-color: inherit;
}
</style>