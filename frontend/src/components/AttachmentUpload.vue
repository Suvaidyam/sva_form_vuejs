<template>
  <div class="w-full">
    <div class="flex items-center mb-2">
      <label :for="field.fieldname" class="block text-sm font-medium text-gray-700 dark:text-gray-200">
        {{ field.label }}
        <span v-if="isFieldMandatory(field)" class="text-red-500 ml-1">*</span>
      </label>
      <Popover v-if="field.description" class="relative inline-block ml-2">
        <PopoverButton class="focus:outline-none">
          <InfoIcon class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
        </PopoverButton>
        <transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 translate-y-1"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-1"
        >
          <PopoverPanel class="absolute z-10 w-64 px-4 mt-3 transform -translate-x-1/2 left-1/2 sm:px-0 lg:max-w-3xl">
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
    <div
      class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 rounded-md hover:border-gray-400 transition-colors duration-200"
      :class="{ 'border-red-500': error }"
      @dragover.prevent @drop.prevent="handleDrop"
    >
      <div class="space-y-1 text-center">
        <UploadCloudIcon v-if="!preview" class="mx-auto h-12 w-12 text-gray-400" />
        <div v-if="!preview" class="flex text-sm text-gray-600">
          <label :for="field.fieldname"
            class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
            <span>Upload a file</span>
            <input :id="field.fieldname" :name="field.fieldname" type="file" class="sr-only" @change="handleFileUpload" :required="isFieldMandatory(field)"
              :accept="acceptedFileTypes">
          </label>
          <p class="pl-1">or drag and drop</p>
        </div>
        <p v-if="!preview" class="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
        <div v-if="preview" class="relative mt-4">
          <img :src="preview" alt="File preview" class="max-w-full h-auto rounded-lg shadow-md">
          <button @click="removeFile"
            class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
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
import { UploadCloudIcon, XIcon, InfoIcon } from 'lucide-vue-next';

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
  }
});

const emit = defineEmits(['update:modelValue']);
const saveAsDraft = inject('saveAsDraft');

const preview = ref('');
const error = ref('');
const fileName = ref('');
const acceptedFileTypes = '.png,.jpg,.jpeg,.gif';
const maxFileSize = 10 * 1024 * 1024; // 10MB

const isImageFile = (file) => {
  return file && file.type.startsWith('image/');
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

    if (!isImageFile(file)) {
      error.value = 'Only image files are allowed.';
      return;
    }

    fileName.value = file.name;

    // Set preview immediately
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.value = e.target.result;
    };
    reader.readAsDataURL(file);

    saveToFrappe(file)
      .then((response) => {
        console.log('File saved successfully:', response.message.file_url);
        const fileUrl = response.message.file_url;
        emit('update:modelValue', fileUrl);
        // Update preview with the URL from the server
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
  // Save as draft when file is removed
  saveAsDraft({ [props.field.fieldname]: '' });
  
  if (props.field.reqd) {
    error.value = 'Please upload a file.';
  } else {
    error.value = '';
  }
};

watch(() => props.modelValue, (newValue) => {
  if (newValue instanceof File) {
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.value = e.target.result;
    };
    reader.readAsDataURL(newValue);
  } else if (typeof newValue === 'string' && newValue) {
    preview.value = newValue;
  } else {
    preview.value = '';
  }
  
  if (!newValue && props.field.reqd) {
    error.value = 'Please upload a file.';
  } else {
    error.value = '';
  }
}, { immediate: true });
</script>

