<template>
  <div v-if="!field.hidden" class="flex flex-col ">
    <span v-if="index < 1 &&  fieldParsedDescription.qlable"
      class="text-md font-medium text-gray-900 dark:text-gray-200 block ">
      {{  fieldParsedDescription.qlable }}
    </span>
    <span v-if="fieldParsedDescription?.cenrieo && !props.isCard"
      class="text-md font-medium text-gray-900 dark:text-gray-200 block ">{{ fieldParsedDescription?.cenrieo }}
    </span>

    <!-- <p v-if="index < 1">{{ section }}</p> -->
    <div class="flex items-center justify-between">
      <label :for="field.name" class="text-md font-medium text-gray-900 dark:text-gray-200 block">
        {{ field.label }} <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
      </label>
     <div v-if=" fieldParsedDescription?.info" class="ml-2 relative">
  <Popover v-slot="{ open }" class="relative">
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
      <PopoverPanel
        class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-full right-0 sm:px-0 lg:max-w-3xl"
      >
        <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
          <div class="p-4 bg-white dark:bg-gray-800">
            <p class="text-sm text-gray-700 dark:text-gray-300">
              {{ fieldParsedDescription?.info }}
            </p>
          </div>
        </div>
      </PopoverPanel>
    </transition>
  </Popover>
</div>
    </div>
    <span v-if=" fieldParsedDescription?.desc" class="text-md font-medium text-gray-900 dark:text-gray-200 block  ">
      {{  fieldParsedDescription?.desc }}
    </span>

    <textarea :id="field.name"  :value="modelValue" @input="handleInput" @blur="handleBlur" :disabled="field.read_only"
      :required="isFieldMandatory(field)" :rows="field.rows || 4" :placeholder="field.placeholder" :class="[
        'px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
        'dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 mt-2',
        { 'border-red-500 focus:ring-red-500': error }
      ]"></textarea>
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, inject, computed } from 'vue'
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
  onfieldChange: {
    type: Boolean,
    required: false,
    default: false
  },
  formData: {
    type: Object,
    required: false,
    default: () => ({})
  },
  section: { type: String, required: false, default: '' },
  index: {
    type: Number,
    required: false,
    default: 0
  },
})

const emit = defineEmits(['update:modelValue'])
const saveAsDraft = inject('saveAsDraft')

const error = ref('')



const fieldParsedDescription = computed(() => {
  return getString(props.field.description || "")
})


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

const handleInput = (event) => {
  let value = event.target.value;
  const wordArray = value.trim().split(/\s+/); // Split words by whitespace
  const wordCount = wordArray.length;

  if (wordCount > 200) {
    error.value = `${props.field.label} cannot exceed 200 words. Currently, it has ${wordCount} words.`;
    value = wordArray.split(/\s+/).slice(0, 200).join('') // Keep only the first 200 words
    event.target.value = value; // Update the textarea value directly
  } else {
    error.value = '';
  }

  emit('update:modelValue', value);
  validateInput(value);
};


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

const handleBlur = () => {
  validateInput(props.modelValue)
  if (props.onfieldChange && !error.value) {
    saveAsDraft({ [props.field.fieldname]: props.modelValue })
  }
}

const validateInput = (value) => {
  error.value = ''

  // Check if field is required and empty
  if (props.field.reqd && !value.trim()) {
    error.value = `${props.field.label} is required.`
    return
  }

  // Check for maximum word limit
  
}
</script>

<style scoped>
.w-96 {
  width: 100% !important;
  max-width: 800px !important;
  min-width: 500px !important;
}
</style>