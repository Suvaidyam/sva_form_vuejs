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
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6.33333 10.333H7.66666V6.33301H6.33333V10.333ZM7 4.99967C7.18888 4.99967 7.34733 4.93567 7.47533 4.80767C7.60333 4.67967 7.66711 4.52145 7.66666 4.33301C7.66622 4.14456 7.60222 3.98634 7.47466 3.85834C7.34711 3.73034 7.18888 3.66634 7 3.66634C6.81111 3.66634 6.65288 3.73034 6.52533 3.85834C6.39777 3.98634 6.33377 4.14456 6.33333 4.33301C6.33288 4.52145 6.39688 4.6799 6.52533 4.80834C6.65377 4.93679 6.812 5.00056 7 4.99967ZM7 13.6663C6.07777 13.6663 5.21111 13.4912 4.4 13.141C3.58889 12.7908 2.88333 12.3159 2.28333 11.7163C1.68333 11.1168 1.20844 10.4112 0.858662 9.59967C0.508885 8.78812 0.333774 7.92145 0.333329 6.99967C0.332885 6.0779 0.507996 5.21123 0.858662 4.39967C1.20933 3.58812 1.68422 2.88256 2.28333 2.28301C2.88244 1.68345 3.588 1.20856 4.4 0.858341C5.212 0.508119 6.07866 0.333008 7 0.333008C7.92133 0.333008 8.788 0.508119 9.6 0.858341C10.412 1.20856 11.1176 1.68345 11.7167 2.28301C12.3158 2.88256 12.7909 3.58812 13.142 4.39967C13.4931 5.21123 13.668 6.0779 13.6667 6.99967C13.6653 7.92145 13.4902 8.78812 13.1413 9.59967C12.7924 10.4112 12.3176 11.1168 11.7167 11.7163C11.1158 12.3159 10.4102 12.791 9.6 13.1417C8.78977 13.4923 7.92311 13.6672 7 13.6663Z" fill="#464547"/>
              </svg>
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
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.33333 10.333H7.66666V6.33301H6.33333V10.333ZM7 4.99967C7.18888 4.99967 7.34733 4.93567 7.47533 4.80767C7.60333 4.67967 7.66711 4.52145 7.66666 4.33301C7.66622 4.14456 7.60222 3.98634 7.47466 3.85834C7.34711 3.73034 7.18888 3.66634 7 3.66634C6.81111 3.66634 6.65288 3.73034 6.52533 3.85834C6.39777 3.98634 6.33377 4.14456 6.33333 4.33301C6.33288 4.52145 6.39688 4.6799 6.52533 4.80834C6.65377 4.93679 6.812 5.00056 7 4.99967ZM7 13.6663C6.07777 13.6663 5.21111 13.4912 4.4 13.141C3.58889 12.7908 2.88333 12.3159 2.28333 11.7163C1.68333 11.1168 1.20844 10.4112 0.858662 9.59967C0.508885 8.78812 0.333774 7.92145 0.333329 6.99967C0.332885 6.0779 0.507996 5.21123 0.858662 4.39967C1.20933 3.58812 1.68422 2.88256 2.28333 2.28301C2.88244 1.68345 3.588 1.20856 4.4 0.858341C5.212 0.508119 6.07866 0.333008 7 0.333008C7.92133 0.333008 8.788 0.508119 9.6 0.858341C10.412 1.20856 11.1176 1.68345 11.7167 2.28301C12.3158 2.88256 12.7909 3.58812 13.142 4.39967C13.4931 5.21123 13.668 6.0779 13.6667 6.99967C13.6653 7.92145 13.4902 8.78812 13.1413 9.59967C12.7924 10.4112 12.3176 11.1168 11.7167 11.7163C11.1158 12.3159 10.4102 12.791 9.6 13.1417C8.78977 13.4923 7.92311 13.6672 7 13.6663Z" fill="#464547"/>
                  </svg>
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