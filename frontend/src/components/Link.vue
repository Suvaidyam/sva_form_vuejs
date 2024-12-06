<template>
  <div v-if="!field.hidden" class="w-full">
    <div v-if="matrix" class="overflow-x-auto">
      <div class="inline-block min-w-full py-2 align-middle">
        <div class="overflow-hidden rounded-lg">
          <div class=" flex item-center gap-2 ">
            <span v-if="index < 1" class="text-md font-medium  text-gray-700 dark:text-gray-200 mb-3  block ">
              {{ parsedDescription.qlable || fieldParsedDescription.qlable }}
            </span>

            <div v-if="index < 1 && parsedDescription.info || fieldParsedDescription.info" class="  relative ">
              <Popover v-slot="{ open }" class="relative z-50 ">
                <PopoverButton @mouseenter="open = true" @mouseleave="open = false" class="focus:outline-none">
                  <InfoIcon
                    class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
                </PopoverButton>

                <transition enter-active-class="transition duration-200 ease-out"
                  enter-from-class="opacity-0 translate-y-1" enter-to-class="opacity-100 translate-y-0"
                  leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100 translate-y-0"
                  leave-to-class="opacity-0 translate-y-1">
                  <PopoverPanel
                    class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl"
                    @mouseenter="open = true" @mouseleave="open = false">
                    <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                      <div class="p-4 bg-white dark:bg-gray-800">
                        <p class="text-sm text-gray-700 dark:text-gray-300">
                          {{ parsedDescription.info }}
                        </p>
                      </div>
                    </div>
                  </PopoverPanel>
                </transition>
              </Popover>
            </div>
          </div>
          <p v-if="index < 1 && parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo && !props.isCard"
            class="text-sm text-gray-500  ">{{ parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo }}
          </p>

          <p v-if="index < 1 && parsedDescription.desc || fieldParsedDescription.desc"
            class="text-sm text-gray-500 mb-2">
            {{
              parsedDescription.desc || fieldParsedDescription.desc }}</p>
          <div class="grid gap-x-4" :style="gridTemplateColumns">
            <div v-if="index < 1" class="bg-gray-50 dark:bg-gray-800 p-4 text-gray-900 dark:text-gray-100 font-medium">
              Question
            </div>
            <div v-if="index < 1" v-for="option in options" :key="`header-${option.name}`"
              class="bg-gray-50 dark:bg-gray-800 p-4 text-center text-gray-900 dark:text-gray-100 font-medium">
              {{ option.label }}
            </div>

            <div
              class="bg-white dark:bg-gray-900 p-4 flex items-start border-t border-gray-200 dark:border-gray-700 min-h-[80px]">
              <div class="text-sm text-gray-900 dark:text-gray-100 w-full pr-6">
                <label :for="`${field.name}-${options[0]?.name}`" class="flex items-start">
                  <span class="mr-2">{{ field.label }} <span v-if="isFieldMandatory(field)"
                      class="text-red-500">*</span></span>
                </label>


              </div>
            </div>
            <div v-for="option in options" :key="`radio-${option.name}`"
              class="bg-white dark:bg-gray-900 p-4 flex justify-center items-center border-t border-l border-gray-200 dark:border-gray-700 min-h-[80px]">
              <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
                :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
                :required="field.reqd"
                class="h-4 w-4 text-primary border-gray-300 focus:ring-primary dark:border-gray-600 dark:focus:ring-primary" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p v-if="parsedDescription?.qlable || fieldParsedDescription?.qlable && !props.isCard"
        class="text-md font-medium text-gray-900 dark:text-gray-200"> {{
          parsedDescription?.qlable || fieldParsedDescription?.qlable }}</p>
      <p v-if="parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo && !props.isCard"
        class="text-sm text-gray-500  ">{{ parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo }}
      </p>
      <div class="flex items-center" :class="props.isCard ? 'py-2 gap-2' : ''">
        <p v-if="props.isCard"
          class="w-7 h-7 min-w-7 min-h-7 text-sm flex items-center justify-center rounded-full bg-gray-700 text-white">
          {{ index + 1 }}
        </p>

        <label :for="`${field.name}-${options[0]?.name}`"
          :class="props.isCard ? 'text-sm' : 'text-md font-medium text-gray-900 dark:text-gray-200'"
          class="block font-medium text-gray-900 dark:text-gray-200">
          {{ field.label }}{{ props.isCard ? fieldParsedDescription.desc : '' }} <span v-if="isFieldMandatory(field)"
            class="text-red-500 ml-1">*</span>
        </label>
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
                    <p class="text-sm text-gray-700 dark:text-gray-300">
                      {{ parsedDescription?.info || fieldParsedDescription?.info }}
                    </p>
                  </div>
                </div>
              </PopoverPanel>
            </transition>
          </Popover>
        </div>
      </div>
      <p v-if="parsedDescription?.desc || fieldParsedDescription?.desc && !props.isCard"
        class="text-sm text-gray-500  mb-2">{{ parsedDescription?.desc || fieldParsedDescription?.desc }}
      </p>


      <div v-if="dropDownOptions" class="mt-1">
        <select :id="`${field.name}-select`" :name="field.name" v-model="selectedOption"
          @change="updateValue(selectedOption)" :disabled="field.read_only" :required="field.reqd"
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          <option value="" disabled selected>Select an option</option>
          <option v-for="option in options" :key="option.name" :value="option.name">
            {{ option.label }}
          </option>
        </select>
      </div>
      <div v-else :class="[
        props.isCard ? 'px-6' : '',
        props.isRow ? 'flex flex-col md:flex-row gap-3 w-full' : 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 mt-2'
      ]">
        <label v-if="props.isCard" :for="`${field.name}-${option.name}`" v-for="option in options" :key="option.name"
          :class="[props.isCard ? 'border p-2 rounded-md shadow-sm' : '',
          props.isRow ? 'w-full' : ''
          ]" class="flex items-center text-sm cursor-pointer">
          <div class="flex-shrink-0 w-5 h-5 mr-2">
            <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
              :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
              :required="field.reqd"
              class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
          </div>
          <span class="flex-grow">{{ option.label }}</span>
        </label>
        <div v-if="!props.isCard" v-for="option in options" :key="option.name"
          :class="props.isCard ? 'border p-2 rounded-md' : ''" class="flex items-center ">
          <div class="flex-shrink-0 w-5 h-5 mr-2 ml-4 ">
            <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
              :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
              :required="isFieldMandatory(field)"
              class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
          </div>
          <label :for="`${field.name}-${option.name}`"
            class="flex-grow text-sm text-gray-700 dark:text-gray-200 cursor-pointer">
            {{ option.label }}
          </label>
        </div>
      </div>
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject, onMounted } from 'vue'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { CloudCog, InfoIcon } from 'lucide-vue-next'

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
  matrix: {
    type: Boolean,
    required: false,
    default: false
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

console.log(props.section, "props.field")
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
    return new Function('formData', `return ${condition}`)(props?.formData)
  } catch (error) {
    console.error('Error evaluating field visibility:', error)
    return false
  }
}

const gridTemplateColumns = computed(() => {
  const optionCount = options.value.length
  return `grid-template-columns: minmax(500px, 1fr) repeat(${optionCount}, minmax(100px, 1fr))`
})

const parsedDescription = computed(() => {
  return getString(props.section || "")


})
const fieldParsedDescription = computed(() => {
  return getString(props.field.description || "")
})

// function getString(str) {
//   console.log(str, "str")
//   const match = str.match(/\{([^}]+)\}/)
//   if (match) {
//     let arr = str.split(match[0])
//     if (arr.length > 1) {
//       return { desc: arr[0], info: match[1] }
//     } else {
//       return { desc: arr[0], info: '' }
//     }
//   } else {
//     return { desc: str, info: '' }
//   }
// }


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
  if (props.field.reqd && !value) {
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
</script>

<style scoped>
.w-96 {
  width: 100% !important;
  max-width: 800px !important;
  min-width: 500px !important;
}
</style>
