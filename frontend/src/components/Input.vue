<template>
  <div v-if="!field.hidden" class="flex flex-col gap-2">
    <div class="flex items-center">
      <label :for="field.name" class="text-sm font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }}
        <span v-if="field.reqd === 1" class="text-red-500 ml-1">*</span>
      </label>
      <div v-if="field.description" class="ml-2 relative">
        <Popover v-slot="{ open }" class="relative">
          <PopoverButton
            @mouseenter="open = true"
            @mouseleave="open = false"
            class="focus:outline-none"
          >
            <InfoIcon class="w-4 h-4 text-gray-400" />
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
              class="absolute z-10 w-72 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl"
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
    <input
      :id="field.name"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @focusout="handleBlur"
      :type="field.fieldtype === 'Password' ? 'password' : 'text'"
      :disabled="field.read_only"
      :required="field.reqd"
      class="h-10 px-3 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600"
    />
  </div>
</template>

<script setup>
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { InfoIcon } from 'lucide-vue-next'
import { inject } from 'vue'

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])
const saveAsDraft = inject('saveAsDraft')

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleBlur = () => {
  saveAsDraft({ [props.field.fieldname]: props.modelValue })
}
</script>
