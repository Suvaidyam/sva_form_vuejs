<template>
  <transition name="fade" mode="in-out">
    <div  class="flex flex-col gap-2">
      <div class="">
        <div class="flex gap-2">
          <div class="w-5 h-5 rounded-full flex items-center justify-center text-xs text-white bg-slate-700">
            {{ 1 }}
          </div>
          <h2 class="text-sebase text-h5">{{ field.label }}</h2>
        </div>
        <div class="flex h-full flex-col border mt-3 w-full text-sm">
          <div class="w-full h-8 bg-tatary min-h-8 border-b flex">
            <div class="w-10 h-full border-r"></div>
            <div class="w-28 border-r flex items-center justify-center">Level</div>
            <div class="w-full border-r flex items-center justify-center">Options</div>
          </div>
          <div class="flex w-full max-h-12 min-h-12 h-12 border-b" v-for="option in options" :key="option.name">
            <div class="w-10 border-r flex items-center justify-center">
              <input :id="`${field.name}-${option.name}`" :name="field.name" type="radio" :value="option.name"
                :checked="modelValue === option.name" @change="$emit('update:modelValue', option.name)"
                :disabled="field.read_only">
            </div>
            <div class="w-28 border-r flex items-center justify-center bg-primary text-white"
              :style="{ opacity: (10 - option.level) / 10 }">
              Level {{ option.level }}
            </div>
            <label :for="`${field.name}-${option.name}`" class="w-full flex items-center px-4"> {{ option.label }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, inject } from 'vue'

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    required: false
  }
})

const emit = defineEmits(['update:modelValue'])

const call = inject('$call')

const options = ref([])

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

watch(() => props.field, getOptions, { immediate: true })
</script>