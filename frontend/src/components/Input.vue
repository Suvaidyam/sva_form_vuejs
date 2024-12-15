<template>
  <div v-if="!field.hidden" class="flex flex-col ">

    <span v-if="index < 1 && parsedDescription?.qlable || fieldParsedDescription?.qlable"
      class="text-md font-medium text-gray-900 dark:text-gray-200 block  block mb-1.5 ">
      {{ parsedDescription?.qlable || fieldParsedDescription?.qlable }}
    </span>
    <span v-if="index < 1 && parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo && !props.isCard"
      class="text-md font-medium text-gray-900 dark:text-gray-200 block ">{{ parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo }}
    </span>



    <div class="flex items-center justify-between">

      <label :for="field.name" class="text-md font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }} <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
      </label>
      <div v-if="parsedDescription?.info || fieldParsedDescription?.info" class="ml-2 relative">
        <Popover v-slot="{ open }" class="relative">
          <PopoverButton class="focus:outline-none">
            <InfoIcon class="w-5 h-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
          </PopoverButton>
          <transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0" leave-active-class="transition duration-150 ease-in"
            leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
            <PopoverPanel class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-full right-0 sm:px-0 lg:max-w-3xl">
              <div class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                <div class="p-4 bg-white dark:bg-gray-800">
                  <p class="text-sm text-gray-700 dark:text-gray-300">
                    {{ parsedDescription?.info || fieldParsedDescription?.info }}
                  </p>
                </div>
              </div>
            </PopoverPanel>
          </transition>
        </Popover>
      </div>

    </div>
    <span v-if="  fieldParsedDescription?.desc" class="text-md font-medium text-gray-900 dark:text-gray-200 block  ">
      {{  fieldParsedDescription?.desc }}
    </span>
    <div class="relative">
      <input :id="field.name" :value="displayValue" @input="handleInput" @focusout="handleBlur" :type="inputType"
        :disabled="field.read_only" :required="isFieldMandatory(field)" :placeholder="field.placeholder"
        :min="minMax.min" :max="minMax.max" :class="[
          'w-full h-10 px-3 mt-2 border rounded-md text-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
          'dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:focus:ring-blue-400 dark:focus:border-blue-400',
          { 'pr-10': field.fieldtype === 'Password' },
          { 'border-red-500 focus:ring-red-500 focus:border-red-500': error }
        ]" :aria-invalid="!!error" :aria-describedby="error ? `${field.name}-error` : undefined" />
    </div>
    <p v-if="error" :id="`${field.name}-error`" class="mt-1 text-sm text-red-600 dark:text-red-400" role="alert">{{
      error }}</p>
  </div>
</template>

<script setup>
import { ref, inject, computed, onMounted } from 'vue'
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
    default: false
  },
  formData: {
    type: Object,
    default: () => ({})
  },
  section: {
    type: String,
    default: ''
  }
})

const error = ref('');
const emit = defineEmits(['update:modelValue'])
const saveAsDraft = inject('saveAsDraft')
const call = inject('$call')
const minMax = ref({})

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



const inputType = computed(() => props.field.fieldtype === 'Int' ? 'text' : 'text')

// const displayValue = computed(() => {
//   if (props.field.fieldtype === 'Int') {
//     const numValue = parseInt(props.modelValue);
//     return isNaN(numValue) || numValue < 0 ? '' : props.modelValue;
//   }
//   return props.modelValue;
// })

const displayValue = computed(() => {
  if (props.field.fieldtype === 'Int') {
    const numValue = parseInt(props.modelValue, 10);
    if (isNaN(numValue) || numValue < 0) {
      return '';
    }
    return new Intl.NumberFormat('en-US').format(numValue);
  }
  return props.modelValue;
});


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

const validateURL = (url) => {
  const urlPattern = /^(https?:\/\/)?([\w\d\-]+\.)+[a-z]{2,}(\/.*)?$/i;
  return urlPattern.test(url);
};

// const handleInput = (event) => {
//   let value = event.target.value;
//   if (props.field.fieldtype === 'Int') {
//     const numValue = parseInt(value);
//     if (isNaN(numValue) || numValue < 0) {
//       error.value = 'Please enter a non-negative integer.';
//       emit('update:modelValue', '');
//     }// Check if the value is less than the minimum allowed
//     else if (minMax.value?.min !== undefined && numValue < minMax.value.min) {
//       error.value = `Value should not be less than ${minMax.value.min}.`; // Added error for min value
//       emit('update:modelValue', numValue.toString());
//     }
//     // Check if the value is greater than the maximum allowed
//     else if (minMax.value?.max !== undefined && numValue > minMax.value.max) {
//       error.value = `Value should not exceed ${minMax.value.max}.`; // Added error for max value
//       emit('update:modelValue', numValue.toString());
//     }
//     else {
//       error.value = '';
//       emit('update:modelValue', numValue.toString());
//     }
//   } else {
//     emit('update:modelValue', value);
//   }
// }

const handleInput = (event) => {
  let value = event.target.value;

  if (props.field.fieldtype === 'Int') {
    const rawValue = value.replace(/[^\d]/g, '');

    if (rawValue !== value) {
      error.value = 'Only integers are allowed.';
    } else {
      error.value = '';
    }

    const numValue = parseInt(rawValue, 10);

    if (isNaN(numValue) || numValue < 0) {
      error.value = 'Please enter a valid non-negative integer.';
      emit('update:modelValue', '');
      event.target.value = '';
    } else {
      error.value = '';
      emit('update:modelValue', numValue);
      event.target.value = rawValue;
    }
  } else {
    emit('update:modelValue', value);
  }
};

const handleBlur = (event) => {
  let value = event.target.value;

  if (props.field.fieldname === 'organisation_website') {
    if (value && !validateURL(value)) {
      error.value = 'Please enter a valid URL.';
      emit('update:modelValue', '');
      return;
    } else {
      error.value = '';
    }
  }

  if (props.field.fieldtype === 'Int') {
    const inputValue = value.replace(/,/g, '');
    const numValue = parseInt(inputValue);

    if (isNaN(numValue) || numValue < 0) {
      error.value = 'Please enter a valid non-negative integer.';
      emit('update:modelValue', '');
      event.target.value = '';
    } else if (minMax.value?.min !== undefined && numValue < minMax.value.min) {
      error.value = `Value should not be less than ${minMax.value.min}.`;
      emit('update:modelValue', '');
      event.target.value = '';
    } else if (minMax.value?.max !== undefined && numValue > minMax.value.max) {
      error.value = `Value should not exceed ${minMax.value.max}.`;
      emit('update:modelValue', '');
      event.target.value = '';
    } else {
      error.value = '';
      const formattedValue = new Intl.NumberFormat('en-US').format(numValue);
      emit('update:modelValue', numValue.toString());
      event.target.value = formattedValue;
    }
    if (props.onfieldChange && !error.value) {
      saveAsDraft({ [props.field.fieldname]: event.target.value.replace(/,/g, '') });
    }
  } else {
    error.value = '';
    emit('update:modelValue', value);
    if (props.onfieldChange && !error.value) {
      saveAsDraft({ [props.field.fieldname]: value });
    }
  }
};


// const handleBlur = (event) => {
// if (props.field.fieldtype === 'Int') {
//   const numValue = parseInt(value);
//   if (isNaN(numValue) || numValue < 0) {
//     error.value = 'Please enter a non-negative integer.';
//     emit('update:modelValue', '');
//   }
//   else if (minMax.value?.min !== undefined && numValue < minMax.value.min) {
//     error.value = `Value should not be less than ${minMax.value.min}.`; // Added error for min value
//     emit('update:modelValue', '');
//   }
//   // Check if the value is greater than the maximum allowed
//   else if (minMax.value?.max !== undefined && numValue > minMax.value.max) {
//     error.value = `Value should not exceed ${minMax.value.max}.`; // Added error for max value
//     emit('update:modelValue', '');
//   }
//   else {
//     error.value = '';
//     emit('update:modelValue', numValue.toString());
//   }
// } else {
//   error.value = '';
//   emit('update:modelValue', value);


//   if (props.onfieldChange && !error.value) {
//     saveAsDraft({ [props.field.fieldname]: value })
//   }
// }


const getMinMax = async () => {
  const response = await call('sva_form_vuejs.controllers.api.get_min_max_criteria', {
    filters: { field: props.field.fieldname}
  })
  if (response) {
    minMax.value = response
  }
}

onMounted(async () => {
  if (props.field.fieldtype === 'Int') {
    await getMinMax()
  }
})
</script>

<style scoped>
.w-96 {
  width: 100% !important;
  max-width: 800px !important;
  min-width: 500px !important;
}
</style>
