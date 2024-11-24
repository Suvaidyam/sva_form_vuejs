<template>
  <div class="w-full">
    <label :for="field.fieldname" class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
      {{ field.label }}
      <span v-if="field.reqd" class="text-red-500 ml-1">*</span>
    </label>
    <div
      class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300  rounded-md hover:border-gray-400 transition-colors duration-200"
      @dragover.prevent
      @drop.prevent="handleDrop"
    >
      <div class="space-y-1 text-center">
        <UploadCloudIcon v-if="!preview" class="mx-auto h-12 w-12 text-gray-400" />
        <div v-if="!preview" class="flex text-sm text-gray-600">
          <label :for="field.fieldname" class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
            <span>Upload a file</span>
            <input 
              :id="field.fieldname" 
              :name="field.fieldname" 
              type="file" 
              class="sr-only" 
              @change="handleFileUpload" 
              :accept="acceptedFileTypes"
            >
          </label>
          <p class="pl-1">or drag and drop</p>
        </div>
        <p v-if="!preview" class="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
        <div v-if="preview" class="relative mt-4">
          <img :src="preview" alt="File preview" class="max-w-full h-auto rounded-lg shadow-md">
          <button 
            @click="removeFile" 
            class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
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
import { UploadCloudIcon, XIcon } from 'lucide-vue-next';

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  modelValue: {
    type: [String, File],
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);
const saveAsDraft = inject('saveAsDraft');

const preview = ref('');
const error = ref('');
const fileName = ref('');
const acceptedFileTypes = '.png,.jpg,.jpeg,.gif';
const maxFileSize = 10 * 1024 * 1024; // 10MB

const isImage = computed(() => {
  if (props.modelValue instanceof File) {
    return ['image/png', 'image/jpeg', 'image/gif'].includes(props.modelValue.type);
  }
  return props.modelValue && typeof props.modelValue === 'string' && props.modelValue.match(/\.(jpeg|jpg|gif|png)$/i) != null;
});

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
    if (file.size > maxFileSize) {
      error.value = 'File size exceeds 10MB limit.';
      return;
    }
    if (!file.type.match('image.*')) {
      error.value = 'Only image files are allowed.';
      return;
    }

    error.value = '';
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
        // Save as draft
        saveAsDraft({ [props.field.fieldname]: fileUrl });
      })
      .catch((apiError) => {
        error.value = 'Failed to save file to the server.';
        console.error('API error:', apiError);
      });
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
  error.value = '';
  emit('update:modelValue', '');
  // Save as draft when file is removed
  saveAsDraft({ [props.field.fieldname]: '' });
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
}, { immediate: true });
</script>