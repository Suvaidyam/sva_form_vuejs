<template>
  <div class="w-full">
    <div class="flex items-center justify-between mb-2">
      <span v-if="parsedDescription.qlable || fieldParsedDescription.qlable"
        class="text-sm font-medium  text-gray-700 dark:text-gray-200  block ">
        {{ parsedDescription.qlable || fieldParsedDescription.qlable }}
      </span>
      <span v-if="parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo && !props.isCard"
        class="text-sm  text-gray-700 ">{{ parsedDescription?.cenrieo || fieldParsedDescription?.cenrieo }}
      </span>

      <label :for="field.fieldname" class="block text-md font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }} <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
      </label>
     <div v-if="parsedDescription?.info || fieldParsedDescription?.info" class="ml-2 relative">
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
              {{ parsedDescription?.info || fieldParsedDescription?.info }}
            </p>
          </div>
        </div>
      </PopoverPanel>
    </transition>
  </Popover>
</div>
    </div>
    <span v-if="parsedDescription.desc || fieldParsedDescription.desc" class="text-sm text-gray-700  ">
      {{ parsedDescription.desc || fieldParsedDescription.desc }}
    </span>

    <div class="mt-1 border-2 py-2 rounded-md hover:border-gray-400 transition-colors duration-200"
      :class="{ 'border-red-500': error }" @dragover.prevent @drop.prevent="handleDrop">
      <div class="space-y-1 text-center">
        <div v-if="!preview" class="text-sm w-full text-gray-600">
          <label :for="field.fieldname"
            class="bg-white w-full text-gray-300 text-base rounded max-w-md h-52 flex flex-col items-center justify-center cursor-pointer mx-auto font-[sans-serif]">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 mb-2 fill-gray-300" viewBox="0 0 32 32">
              <path
                d="M23.75 11.044a7.99 7.99 0 0 0-15.5-.009A8 8 0 0 0 9 27h3a1 1 0 0 0 0-2H9a6 6 0 0 1-.035-12 1.038 1.038 0 0 0 1.1-.854 5.991 5.991 0 0 1 11.862 0A1.08 1.08 0 0 0 23 13a6 6 0 0 1 0 12h-3a1 1 0 0 0 0 2h3a8 8 0 0 0 .75-15.956z"
                data-original="#000000" stroke="#e2e8f0" />
              <path
                d="M20.293 19.707a1 1 0 0 0 1.414-1.414l-5-5a1 1 0 0 0-1.414 0l-5 5a1 1 0 0 0 1.414 1.414L15 16.414V29a1 1 0 0 0 2 0V16.414z"
                data-original="#000000" stroke="#e2e8f0" />
            </svg>
            Upload file

            <input :id="field.fieldname" :name="field.fieldname" type="file" class="w-full h-full hidden"
              @change="handleFileUpload" :required="isFieldMandatory(field)" :accept="acceptedFileTypes">
            <p v-if="!preview" class="text-xs font-medium text-gray-400 mt-2">PDF, DOCX up to 10MB</p>
          </label>
        </div>
        <div v-if="preview" class="relative mt-4">
          <div class="flex items-center justify-center bg-gray-100 dark:bg-gray-700 rounded-lg p-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" viewBox="0 0 20 20"
              fill="currentColor">
              <path fill-rule="evenodd"
                d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z"
                clip-rule="evenodd" />
            </svg>
            <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">{{ fileName }}</span>
          </div>
          <button @click="removeFile"
            class="absolute top-0 right-0 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
            <XIcon class="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
    <p v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject } from 'vue';
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/vue'
import { XIcon, InfoIcon } from 'lucide-vue-next';

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: [String, File],
    default: ''
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
  section: {
    type: String,
    required: false,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);
const saveAsDraft = inject('saveAsDraft');

const preview = ref('');
const error = ref('');
const fileName = ref('');
const acceptedFileTypes = '.pdf,.docx';
const maxFileSize = 10 * 1024 * 1024; // 10MB


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


const isPdfFile = (file) => {
  return file && (typeof file === 'string' ? file.endsWith('.pdf') : file.type === 'application/pdf');
};

const isDocxFile = (file) => {
  return file && (typeof file === 'string' ? file.endsWith('.docx') : file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
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

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  processFile(file);
};

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0];
  processFile(file);
};

const processFile = (file) => {
  if (file) {
    error.value = '';

    if (file.size > maxFileSize) {
      error.value = 'File size exceeds 10MB limit.';
      return;
    }

    if (!isPdfFile(file) && !isDocxFile(file)) {
      error.value = 'Only PDF or DOCX files are allowed.';
      return;
    }

    fileName.value = file.name;
    preview.value = 'file';

    saveToFrappe(file)
      .then((response) => {
        console.log('File saved successfully:', response.message.file_url);
        const fileUrl = response.message.file_url;
        emit('update:modelValue', fileUrl);
        preview.value = fileUrl;
        if (props.onfieldChange) {
          saveAsDraft({ [props.field.fieldname]: fileUrl });
        }
      })
      .catch((apiError) => {
        error.value = 'Failed to save file to the server.';
        console.error('API error:', apiError);
      });
  } else if (props.field.reqd) {
    error.value = 'Please upload a file.';
  }
};

const saveToFrappe = async (file) => {
  const frappeApiUrl = '/api/method/upload_file';

  const formData = new FormData();
  formData.append('file', file);
  formData.append('is_private', 0);
  formData.append('folder', 'Home');
  formData.append('doctype', 'Assessment');
  formData.append('docname', file.name);
  formData.append('fieldname', props.field.fieldname);

  try {
    const response = await fetch(frappeApiUrl, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Server response error:', errorText);
      throw new Error(`API error: ${response.statusText}`);
    }

    const responseData = await response.json();
    console.log('Successful response:', responseData);
    return responseData;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

const removeFile = () => {
  preview.value = '';
  fileName.value = '';
  emit('update:modelValue', '');
  saveAsDraft({ [props.field.fieldname]: '' });

  if (props.field.reqd) {
    error.value = 'Please upload a file.';
  } else {
    error.value = '';
  }
};

watch(() => props.modelValue, (newValue) => {
  if (newValue instanceof File) {
    preview.value = 'file';
    fileName.value = newValue.name;
  } else if (typeof newValue === 'string' && newValue) {
    preview.value = newValue;
    fileName.value = newValue.split('/').pop();
  } else {
    preview.value = '';
    fileName.value = '';
  }

  if (!newValue && props.field.reqd) {
    error.value = 'Please upload a file.';
  } else {
    error.value = '';
  }
}, { immediate: true });
</script>

<style scoped>
.w-96 {
  width: 100% !important;
  max-width: 800px !important;
  min-width: 500px !important;
}

.border-2 {
  border: 2px dashed #e2e8f0;
}
</style>