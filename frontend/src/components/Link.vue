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
                {{ field.label }}
                <span v-if="field.reqd" class="text-red-500 ml-1">*</span>
                <InfoIcon v-if="field.description" class="inline-block w-4 h-4 ml-1 text-gray-400 cursor-help"
                  v-tooltip="field.description" />
              </div>
            </div>
            <div v-for="option in options" :key="`radio-${option.name}`"
              class="bg-white dark:bg-gray-900 p-4 flex justify-center items-center border-t border-l border-gray-200 dark:border-gray-700">
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
      <div class="flex items-center" :class="props.isCard ? 'py-2 gap-2' : 'mb-2'">
        <p v-if="props.isCard"
          class="w-6 h-6 text-sm flex items-center justify-center rounded-full bg-gray-500 text-white">{{ index + 1 }}
        </p>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
          {{ field.label }}
          <span v-if="field.reqd" class="text-red-500 ml-1">*</span>
        </label>
        <div v-if="field.description" class="ml-2 relative group">
          <InfoIcon class="w-4 h-4 text-gray-400 cursor-help" />
          <div
            class="absolute left-0 bottom-6 bg-black text-white text-xs rounded py-1 px-2 w-48 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10">
            {{ field.description }}
          </div>
        </div>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
        :class="props.isCard ? 'px-6' : ''">
        <label v-if="props.isCard" :for="`${field.name}-${option.name}`" v-for="option in options" :key="option.name"
          :class="props.isCard ? 'border p-2 rounded-md gap-1.5 shadow-sm' : 'gap-1.5'"
          class="flex text-sm items-center">
          <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
            :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
            :required="field.reqd"
            class="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
          {{ option.label }}
        </label>
        <div v-if="!props.isCard" :for="`${field.name}-${option.name}`" v-for="option in options" :key="option.name"
          :class="props.isCard ? 'border p-2 rounded-md gap-2' : ''" class="flex items-center">
          <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
            :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
            :required="field.reqd"
            class="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
          <label class="ml-2 block text-sm text-gray-700 dark:text-gray-200">
            {{ option.label }}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject, onMounted } from 'vue'
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
  }
})

const emit = defineEmits(['update:modelValue'])
const call = inject('$call')
const saveAsDraft = inject('saveAsDraft')
const options = ref([])

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

const updateValue = (value) => {
  emit('update:modelValue', value)
  // Save as draft after updating the value
  saveAsDraft({ [props.field.fieldname]: value })
}

watch(() => props.field, getOptions, { immediate: true })

onMounted(() => {
  getOptions()
})
</script>

<style scoped>
/* Add any additional scoped styles here */
</style>