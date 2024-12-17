<template>
  <transition name="fade" mode="in-out">
    <div v-if="!field.hidden" class="flex flex-col gap-2 py-2 w-full bg-red-600">
      <div class="flex gap-2 ">
        <div
          class="w-7 min-w-7 min-h-7 h-7 rounded-full flex items-center justify-center text-xs text-white bg-slate-700">
          {{ index + 1 }}
        </div>
        <h2 class="text-sebase text-h5 min-w-full">{{ field.label }} {{ fieldParsedDescription.desc }}

          <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
        </h2>
        <div v-if="(fieldParsedDescription?.info)" class="ml-2 relative">
          <Popover v-slot="{ open }" class="relative">
            <PopoverButton class="focus:outline-none">
              <InfoIcon class="w-5 h-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
            </PopoverButton>
            <transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition duration-150 ease-in"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <PopoverPanel
                class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-full right-0 sm:px-0 lg:max-w-3xl">
                <div class="overflow-hidden rounded-lg border-2 shadow-lg ring-1 ring-black ring-opacity-5">
                  <div class="p-4 bg-white dark:bg-gray-800">
                    <p class="text-sm text-gray-900 dark:text-gray-300">
                      {{ fieldParsedDescription?.info }}
                    </p>
                  </div>
                </div>
              </PopoverPanel>
            </transition>
          </Popover>
        </div>
      </div>
      <div class="flex h-full flex-col border mt-3 w-full text-sm">
        <div class="w-full h-8 bg-tatary min-h-8 border-b flex">
          <div class="w-10 h-full border-r"></div>
          <div class="w-28 border-r flex items-center justify-center">Level</div>
          <div class="w-full border-r flex items-center justify-center">Options</div>
        </div>
        <div class="flex w-full  min-h-12 h-full border-b" v-for="option in options" :key="option.name">
          <div class="w-10 border-r flex items-center justify-center">
            <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
              :checked="modelValue === option.name" @change="$emit('update:modelValue', option.name)"
              :disabled="field.read_only" :required="isFieldMandatory(field)">
          </div>
          <div class="w-28 border-r flex items-center justify-center bg-primary text-white"
            :style="{ opacity: (10 - option.level) / 10 }">
            Level {{ option.level }}
          </div>
          <div class="flex w-full p-1">
            <label :for="`${field.name}-${option.name}`" class="w-full flex items-center py-3 px-4"> {{ option.label }}
            </label>
            <div v-if="(option?.desc)" class="ml-2 relative">
              <Popover v-slot="{ open }" class="relative">
                <PopoverButton class="focus:outline-none">
                  <InfoIcon
                    class="w-5 h-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
                </PopoverButton>
                <transition enter-active-class="transition duration-200 ease-out"
                  enter-from-class="opacity-0 translate-y-1" enter-to-class="opacity-100 translate-y-0"
                  leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100 translate-y-0"
                  leave-to-class="opacity-0 translate-y-1">
                  <PopoverPanel
                    class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-full right-0 sm:px-0 lg:max-w-3xl">
                    <div class="overflow-hidden border-2 border-gray-700 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                      <div class="p-4 bg-white dark:bg-gray-800">
                        <p class="text-sm text-gray-900 dark:text-gray-300">
                          {{ option?.desc }}
                        </p>
                      </div>
                    </div>
                  </PopoverPanel>
                </transition>
              </Popover>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, inject, computed } from 'vue'
import Popper from "vue3-popper";
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { InfoIcon } from 'lucide-vue-next'
const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    required: false
  },
  index: {
    type: Number,
    required: false,
    default: 0
  }
})

const emit = defineEmits(['update:modelValue'])

const call = inject('$call')

const options = ref([])

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

watch(() => props.field, getOptions, { immediate: true })
document.addEventListener('focusin', (e) => {
  if (e.target.tagName === 'INPUT' && e.target.validationMessage) {
    const rect = e.target.getBoundingClientRect();
    if (rect.top < 215) {
      window.scrollBy(0, rect.top - 215);
    }
  }
});
</script>\

<style scoped>
.w-96 {
  width: 28rem;
}
</style>