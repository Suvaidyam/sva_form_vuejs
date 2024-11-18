<template>
    <div class="w-full">
      <label :for="field.fieldname" class="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
        {{ field.label }}
        <span v-if="field.reqd" class="text-red-500 ml-1">*</span>
      </label>
      <div
        class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md"
        @dragover.prevent
        @drop.prevent="handleDrop"
      >
        <div class="space-y-1 text-center">
          <svg
            class="mx-auto h-12 w-12 text-gray-400"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 48 48"
            aria-hidden="true"
          >
            <path
              d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <div class="flex text-sm text-gray-600">
            <label
              :for="field.fieldname"
              class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
            >
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
          <p class="text-xs text-gray-500">
            PNG, JPG, GIF up to 10MB
          </p>
        </div>
      </div>
      <div v-if="preview" class="mt-4">
        <img v-if="isImage" :src="preview" alt="File preview" class="max-w-full h-auto rounded-lg shadow-md">
        <div v-else class="p-4 bg-gray-100 rounded-lg shadow-md">
          <p class="text-sm text-gray-600">File selected: {{ fileName }}</p>
        </div>
      </div>
      <p v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, computed } from 'vue';
  
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
  
  const preview = ref('');
  const error = ref('');
  const fileName = ref('');
  const acceptedFileTypes = '.png,.jpg,.jpeg,.gif';
  const maxFileSize = 10 * 1024 * 1024; // 10MB
  
  const isImage = computed(() => {
    return ['image/png', 'image/jpeg', 'image/gif'].includes(props.modelValue?.type);
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
      
      error.value = ''; // Clear any previous errors
      emit('update:modelValue', file);
      fileName.value = file.name;
      
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.value = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  };
  
  watch(() => props.modelValue, (newValue) => {
    if (typeof newValue === 'string' && newValue.startsWith('http')) {
      preview.value = newValue;
    }
  });
  </script>