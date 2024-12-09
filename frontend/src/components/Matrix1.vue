<template>
    <div v-if="!field.hidden" class="w-full">
        <div class="flex items-center gap-2">
            <!-- <span v-if="index < 1" class="text-md font-medium text-gray-700 dark:text-gray-200 mb-3 block">
                {{ parsedDescription.qlable || fieldParsedDescription.qlable }}
            </span> -->
            <div v-if="index < 1 && (parsedDescription.info || fieldParsedDescription.info)" class="relative">
                <Popover v-slot="{ open }" class="relative z-50">
                    <PopoverButton @mouseenter="open = true" @mouseleave="open = false" class="focus:outline-none">
                        <InfoIcon
                            class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
                    </PopoverButton>
                    <transition enter-active-class="transition duration-200 ease-out"
                        enter-from-class="opacity-0 translate-y-1" enter-to-class="opacity-100 translate-y-0"
                        leave-active-class="transition duration-150 ease-in"
                        leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
                        <PopoverPanel
                            class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl"
                            @mouseenter="open = true" @mouseleave="open = false">
                            <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                                <div class="p-4 bg-white dark:bg-gray-800">
                                    <p class="text-sm text-gray-700 dark:text-gray-300">
                                        {{ parsedDescription.info || fieldParsedDescription.info }}
                                    </p>
                                </div>
                            </div>
                        </PopoverPanel>
                    </transition>
                </Popover>
            </div>
        </div>
  
        <p v-if="index < 1 && (parsedDescription.cenrieo || fieldParsedDescription.cenrieo)"
            class="text-sm text-gray-500">
            {{ parsedDescription.cenrieo || fieldParsedDescription.cenrieo }}
        </p>
        <p v-if="index < 1 && (parsedDescription.desc || fieldParsedDescription.desc)"
            class="text-sm text-gray-500 mb-2">
            {{ parsedDescription.desc || fieldParsedDescription.desc }}
        </p>
  
        <div class="flex items-center matrix-label-row">
            <label :for="`${field.name}-${visibleOptions[0]?.name}`"
                class="block text-md font-medium text-gray-900 dark:text-gray-200">
                {{ field.label }}
                <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
            </label>
            <div v-if="parsedDescription.info || fieldParsedDescription.info" class="ml-2 relative">
                <Popover v-slot="{ open }" class="relative">
                    <PopoverButton @mouseenter="open = true" @mouseleave="open = false" class="focus:outline-none">
                        <InfoIcon
                            class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
                    </PopoverButton>
                    <transition enter-active-class="transition duration-200 ease-out"
                        enter-from-class="opacity-0 translate-y-1" enter-to-class="opacity-100 translate-y-0"
                        leave-active-class="transition duration-150 ease-in"
                        leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
                        <PopoverPanel
                            class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl"
                            @mouseenter="open = true" @mouseleave="open = false">
                            <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                                <div class="p-4 bg-white dark:bg-gray-800">
                                    <p class="text-sm text-gray-700 dark:text-gray-300">
                                        {{ parsedDescription.info || fieldParsedDescription.info }}
                                    </p>
                                </div>
                            </div>
                        </PopoverPanel>
                    </transition>
                </Popover>
            </div>
        </div>
  
        <div :class="[
            isRow ? 'flex flex-col md:flex-row gap-3 w-full' : 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 mt-2'
        ]">
            <label v-for="option in visibleOptions" :key="option.name" :for="`${field.name}-${option.name}`"
                :class="[isRow ? 'w-full' : '']" class="flex items-center text-sm cursor-pointer">
                <div class="flex-shrink-0 w-5 h-5 mr-2">
                    <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
                        :checked="modelValue === option.name" @change="updateValue(option.name)"
                        :disabled="field.read_only" :required="isFieldMandatory(field)"
                        class="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:focus:ring-blue-600" />
                </div>
                <span class="flex-grow">{{ option.label }}</span>
            </label>
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
    formData: {
        type: Object,
        required: true
    },
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
  
  const parsedDescription = computed(() => {
    return getString(props.section || "")
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
  .matrix-label-row{
    width: 400px !important;
    min-width: 400px !important;
  }
  </style>