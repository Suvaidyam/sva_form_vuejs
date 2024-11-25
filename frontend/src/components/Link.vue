<template>
  <div v-if="!field.hidden" class="w-full">
    <div v-if="matrix" class="overflow-x-auto">
      <div class="inline-block min-w-full py-2 align-middle">
        <div class="overflow-hidden rounded-lg">
          <span v-if="index < 1" class="text-sm font-medium text-gray-700 dark:text-gray-200 mb-8">
            {{ section }}
          </span>
          <div class="grid" :style="gridTemplateColumns">
            <div v-if="index < 1" class="bg-gray-50 dark:bg-gray-800 p-4 text-gray-900 dark:text-gray-100">
              Question
            </div>
            <div v-if="index < 1" v-for="option in options" :key="`header-${option.name}`"
              class="bg-gray-50 dark:bg-gray-800 p-4 text-center text-gray-900 dark:text-gray-100">
              {{ option.label }}
            </div>

            <div class="bg-white dark:bg-gray-900 p-4 flex items-center border-t border-gray-200 dark:border-gray-700">
              <div class="text-sm text-gray-900 dark:text-gray-100">
                <label :for="`${field.name}-${options[0]?.name}`" class="flex items-center">
                  <span class="mr-2">{{ field.label }}</span>
                  <span v-if="field.reqd" class="text-red-500">*</span>
                </label>
                <div v-if="field.description" class="ml-2 inline-block relative">
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
            </div>
            <div v-for="option in options" :key="`radio-${option.name}`"
              class="bg-white dark:bg-gray-900 p-4 flex justify-center items-center border-t border-l border-gray-200 dark:border-gray-700">
              <input v-if="isOptionVisible(option)" :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
                :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
                :required="field.reqd"
                class="h-4 w-4 text-primary border-gray-300 focus:ring-primary dark:border-gray-600 dark:focus:ring-primary" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="flex items-center" :class="props.isCard ? 'py-2 gap-2' : 'mb-2'">
        <p v-if="props.isCard"
          class="w-6 h-6 text-sm flex items-center justify-center rounded-full bg-gray-500 text-white">{{ index + 1 }}
        </p>
        <label :for="`${field.name}-${options[0]?.name}`" class="block text-sm font-medium text-gray-700 dark:text-gray-200">
          {{ field.label }}
          <span v-if="field.reqd" class="text-red-500 ml-1">*</span>
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
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
        :class="props.isCard ? 'px-6' : ''">
        <template v-for="option in options" :key="option.name">
          <label v-if="isOptionVisible(option)" :for="`${field.name}-${option.name}`"
            :class="[
              props.isCard ? 'border p-2 rounded-md shadow-sm' : '',
              'flex items-center text-sm cursor-pointer'
            ]">
            <div class="flex-shrink-0 w-5 h-5 mr-2">
              <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
                :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
                :required="field.reqd"
                class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
            </div>
            <span class="flex-grow">{{ option.label }}</span>
          </label>
        </template>
      </div>
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject, onMounted } from 'vue'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { InfoIcon } from 'lucide-vue-next'

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

const gridTemplateColumns = computed(() => {
  const optionCount = options.value.length
  return `grid-template-columns: minmax(200px, 2fr) repeat(${optionCount}, minmax(100px, 1fr))`
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
  if (props.onfieldChange && !error.value) {
    saveAsDraft({ [props.field.fieldname]: value })
  }
}

const isOptionVisible = (option) => {
  if (!option.depends_on) return true
  const condition = option.depends_on.replace('eval:', '').replace(/doc\./g, 'props.formData.')
  try {
    return new Function('props', `return ${condition}`)(props)
  } catch (error) {
    console.error('Error evaluating option visibility:', error)
    return false
  }
}

watch(() => props.field, getOptions, { immediate: true })

onMounted(() => {
  getOptions()
})
</script>

<style scoped>
/* Add any additional scoped styles here */
</style>