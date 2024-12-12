<template>
  <div class="">
    <div class="inline-block min-w-full py-2 align-middle">
      <div class="overflow-hidden rounded-lg">
        <div class="grid gap-x-4" :style="gridTemplateColumns">
          <template v-if="index < 1">
            <div class="bg-gray-50 dark:bg-gray-800 p-4 text-gray-900 dark:text-gray-100 font-medium">
              Question
            </div>
            <div v-for="option in visibleOptions" :key="`header-${option.name}`"
              class="bg-gray-50 dark:bg-gray-800 p-4 text-gray-900 dark:text-gray-100 font-medium"
              :class="{ 'text-left': matrix_code, 'text-center': !matrix_code }">
              {{ matrix_code ? option.level : option.label }}
            </div>
          </template>

          <div
            class="bg-white dark:bg-gray-900 p-4 flex items-start border-t border-gray-200 dark:border-gray-700 min-h-[80px]">
            <div class="text-sm text-gray-900 dark:text-gray-100 w-full pr-6">
              <label :for="`${field.name}-${visibleOptions[0]?.name}`" class="flex items-start">
                <span class="mr-2">{{ field.label }} <span v-if="isFieldMandatory" class="text-red-500">*</span></span>
              </label>
            </div>
          </div>

          <template v-for="option in visibleOptions" :key="`radio-${option.name}`">
            <div v-if="matrix_code"
              class="bg-white dark:bg-gray-900 p-4 border-t border-l border-gray-200 dark:border-gray-700 min-h-[80px]">
              <div class="flex flex-col space-y-2">
                <div class="flex items-center">
                  <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
                    :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
                    :required="isFieldMandatory"
                    class="h-4 w-4 text-primary border-gray-300 focus:ring-primary dark:border-gray-600 dark:focus:ring-primary" />
                  <label :for="`${field.name}-${option.name}`" class="ml-2 text-sm text-gray-900 dark:text-gray-100">
                    {{ option.label }} 
                  </label>
                </div>
              </div>
            </div>
            <div v-else
              class="bg-white dark:bg-gray-900 p-4 flex justify-center items-center border-t border-l border-gray-200 dark:border-gray-700 min-h-[80px]">
              <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
                :checked="modelValue === option.name" @change="updateValue(option.name)" :disabled="field.read_only"
                :required="isFieldMandatory"
                class="h-4 w-4 text-primary border-gray-300 focus:ring-primary dark:border-gray-600 dark:focus:ring-primary" />
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

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
  visibleOptions: {
    type: Array,
    required: true
  },
  isFieldMandatory: {
    type: Boolean,
    required: true
  },
  index: {
    type: Number,
    required: false,
    default: 0
  },
  matrix_code: {
    type: Boolean,
    required: false
  }
})

const emit = defineEmits(['update:modelValue'])

const gridTemplateColumns = computed(() => {
  const optionCount = props.visibleOptions.length
  return `grid-template-columns: minmax(500px, 1fr) repeat(${optionCount}, minmax(${props.matrix_code ? '100px' : '150px'}, 1fr))`
})

const updateValue = (value) => {
  emit('update:modelValue', value)
}
</script>
