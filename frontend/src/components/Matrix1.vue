<template>
  <div class="w-full overflow-x-auto">
    <table class="w-full divide-y divide-gray-200 dark:divide-gray-700">
      <thead class=" bg-gray-50 dark:bg-gray-800">
        <tr>
          <th v-if="index < 1" scope="col" class="p-3 text-left block text-md font-medium text-gray-900 uppercase tracking-wider">
            Options 
          </th>
          <th scope="col" class="p-3 text-left">
            <div class="flex items-start justify-between">
              <span class="mr-2 block text-md font-medium text-gray-900">
                {{ field.label }}
                <span v-if="isFieldMandatory" class="text-red-500">*</span>
              </span>
              <Popover v-if="fieldParsedDescription.info" v-slot="{ open }" class="relative">
                <PopoverButton class="focus:outline-none">
                  <InfoIcon class="w-5 h-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
                </PopoverButton>
                <transition 
                  enter-active-class="transition duration-200 ease-out" 
                  enter-from-class="opacity-0 translate-y-1"
                  enter-to-class="opacity-100 translate-y-0" 
                  leave-active-class="transition duration-150 ease-in"
                  leave-from-class="opacity-100 translate-y-0" 
                  leave-to-class="opacity-0 translate-y-1"
                >
                  <PopoverPanel class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl">
                    <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                      <div class="p-4 bg-white dark:bg-gray-800">
                        <p class="text-sm text-gray-700 dark:text-gray-300">
                          {{ fieldParsedDescription.info }}
                        </p>
                      </div>
                    </div>
                  </PopoverPanel>
                </transition>
              </Popover>
            </div>
            <p v-if="fieldParsedDescription.desc" class="text-md text-gray-600 dark:text-gray-400 mt-1">
              {{ fieldParsedDescription.desc }}
            </p>
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200 dark:bg-gray-900 dark:divide-gray-700">
        <tr v-for="option in visibleOptions" :key="`row-${option.name}`">
          <td v-if="index < 1" class="p-3 text-wrap ">
            <label :for="`${field.name}-${option.name}`" class="text-[15px] text-gray-900 dark:text-gray-200">
              {{ matrix_code ? option.level : option.label }}
            </label>
          </td>
          <td class="p-3 whitespace-nowrap ">
            <input 
              :id="`${field.name}-${option.name}`" 
              :name="field.name" 
              type="radio" 
              :value="option.name"
              :checked="modelValue === option.name" 
              @change="updateValue(option.name)"
              :disabled="field.read_only" 
              :required="isFieldMandatory"
              class="h-4 w-4 text-primary border-gray-300 focus:ring-primary dark:border-gray-600 dark:focus:ring-primary"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { InfoIcon } from 'lucide-vue-next'

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    required: true
  },
  visibleOptions: {
    type: Array,
    required: true
  },
  matrix_code: {
    type: Boolean,
    required: false,
    default: false
  },
  index: {
    type: Number,
    required: false,
    default: 0
  }
})

const emit = defineEmits(['update:modelValue'])

const updateValue = (value) => {
  emit('update:modelValue', value)
}

const isFieldMandatory = computed(() => {
  return props.field.reqd || false
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
</script>

<style scoped>
/* Add any additional styles here if needed */
</style>