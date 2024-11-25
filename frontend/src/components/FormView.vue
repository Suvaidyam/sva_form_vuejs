<template>
  <div class="w-full h-full bg-white dark:bg-gray-900 z-10" v-if="loading">
    <Loader />
  </div>
  <div v-else class="flex h-screen bg-white dark:bg-gray-900 overflow-hidden">
    <!-- Sidebar -->
    <aside v-if="!props.section" :class="[
      ' static inset-y-0 left-0  w-20 transform transition-transform duration-300 ease-in-out bg-gray-50 dark:bg-gray-800 shadow-lg overflow-y-auto',
      isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
      'md:translate-x-0 md:static md:inset-auto'
    ]">
      <div class="flex flex-col h-full">
        <div class="flex items-center  justify-between p-4 border-b dark:border-gray-700">
          <h3 class="text-lg ml-4 text-gray-800 dark:text-white">Section</h3>
        </div>
        <nav class="flex-1 px-4 py-4">
          <ul class="space-y-2">
            <li v-for="(tab, index) in tabFields" :key="tab.name">
              <button @click="setActiveTab(tab.name)" :disabled="index > 0 && !allTabsUnlocked" :class="[
                'w-full text-left px-4 py-2 rounded-lg transition-colors duration-150 ease-in-out flex justify-between items-center',
                activeTab === tab.name
                  ? 'bg-orange-500 text-white'
                  : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700',
                index > 0 && !allTabsUnlocked ? 'opacity-50 cursor-not-allowed' : ''
              ]">
                {{ tab.label }}
                <span class="mr-2" v-if="index > 0">
                  <LockIcon v-if="!allTabsUnlocked" class="w-4 h-4" />
                  <CheckCircleIcon v-if="allTabsUnlocked && tabCompletionStatus[tab.name]"
                    class="w-4 h-4 text-green-500" />
                </span>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-x-hidden overflow-y-auto bg-white dark:bg-gray-900">
      <h2 v-if="!props.section" class="text-3xl flex  items-center font-semibold text-[#0E4688] dark:text-white">
        Assessment Simple Test</h2>
      <div class=" mx-auto px-6 py-8">


        <div v-if="allSections.length === 0" class="text-center text-gray-500 dark:text-gray-400 text-2xl mt-20">
          Assessment Not Found
        </div>
        <div v-else>
          <form @submit.prevent="onSubmit(formData)" class="mt-16 md:mt-0">
            <div class="space-y-6">
              <template v-if="props.section">
                <div v-for="(section, index) in allSections" :key="index" class="mb-6">
                  <div @click="toggleSection(index)"
                    class="flex items-center justify-between cursor-pointer bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mb-2">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                      {{ section.label }}
                    </h3>
                    <ChevronDownIcon
                      :class="['w-5 h-5 transition-transform', { 'transform rotate-180': openSections[index] }]" />
                  </div>
                  <div v-show="openSections[index]" class="pl-4">
                    <div v-for="(field, fieldIndex) in section.fields" :key="field.name" class="mb-4">
                      <component :section="section.description" v-if="isFieldVisible(field)"
                        :is="getFieldComponent(field.fieldtype)" :field="field" :isCard="props.isCard"
                        :matrix="section.is_matrix" :index="fieldIndex" v-model="formData[field.fieldname]"
                        :onfieldChange="props.onfieldChange"
                        @update:modelValue="handleFieldUpdate(field.fieldname, $event)" />
                    </div>
                  </div>
                </div>
              </template>
              <template v-else>
                <div v-for="(section, index) in activeFieldSections" :key="section.name" class="mb-6">
                  <h3 :id="`section-${index}`" class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    {{ section.label }}
                  </h3>
                  <div v-if="section.fields && section.fields.length > 0" :aria-labelledby="`section-${index}`"
                    class="space-y-4">
                    <div v-for="(field, fieldIndex) in section.fields" :key="field.name" class="mb-4">
                      <component v-if="isFieldVisible(field)" :section="section.description"
                        :is="getFieldComponent(field.fieldtype)" :field="field" :isCard="props.isCard"
                        :matrix="section.is_matrix" :index="fieldIndex" v-model="formData[field.fieldname]"
                        @update:modelValue="handleFieldUpdate(field.fieldname, $event)"
                        :onfieldChange="props.onfieldChange" :aria-label="field.label || field.fieldname" />
                    </div>
                  </div>
                  <p v-else class="text-gray-500 dark:text-gray-400 italic">
                    No fields in this section.
                  </p>
                </div>
              </template>
            </div>
            <div class="mt-6 flex justify-end gap-2">
              <button v-if="!props.section && !isLastTab" @click="nextTab" type="button"
                :disabled="isFirstTab && !isFirstTabCompletelyFilled" :class="[
                  'px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                  isFirstTab && !isFirstTabCompletelyFilled
                    ? 'bg-gray-300 cursor-not-allowed'
                    : 'bg-orange-500 text-white hover:bg-orange-600'
                ]">
                Next
              </button>
              <button
              :style="{ backgroundColor: props.submitButtonColor }"
               :class="[
                isSubmitDisabled ? 'bg-gray-400' : `bg-blue-500 hover:bg-blue-600`,
                'text-white'
              ]" v-if="props.section || isLastTab" type="submit"
                class="px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2"
                :disabled="isSubmitDisabled">
                Submit
              </button>
              <button @click="save_as_draft(formData)" v-if="props.isDraft" type="button" :disabled="isSubmitDisabled"
                :class="isSubmitDisabled ? 'bg-gray-400' : 'bg-white hover:bg-gray-100'"
                class="px-4 py-2 border shadow-md rounded-md focus:outline-none">
                Save as Draft
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, watch, provide } from 'vue'
import { ChevronDownIcon, LockIcon, CheckCircleIcon, XIcon, MenuIcon } from 'lucide-vue-next'
import Input from './Input.vue'
import Link from './Link.vue'
import LinkTable from './LinkTable.vue'
import CheckBox from './CheckBox.vue'
import Button from './Button.vue'
import Loader from './Loader.vue'
import AttachmentUpload from './AttachmentUpload.vue'
import DateInput from './DateInput.vue'
import Textarea from './TextareaInput.vue'
import CheckboxComponent from './CheckboxComponent.vue'

const props = defineProps({
  doctype: {
    type: String,
    required: true
  },
  section: {
    type: Boolean,
    default: false
  },
  isTable: {
    type: Boolean,
    default: false
  },
  isCard: {
    type: Boolean,
    default: false
  },
  isDraft: {
    type: Boolean,
    default: false
  },
  save_as_draft: {
    type: Function,
    default: () => console.log('save_as_draft...')
  },
  initialData: {
    type: Object,
    default: () => ({})
  },
  onSubmit: {
    type: Function,
    required: true
  },
  onfieldChange: {
    type: Boolean,
    default: false
  },
  submitButtonColor: {
    type: String,
    default: '#255b97'
  }
})

const call = inject('$call')

const loading = ref(true)
const docTypeMeta = ref(null)
const activeTab = ref('')
const formData = ref({})
const openSections = ref([])
const allTabsUnlocked = ref(false)
const tabCompletionStatus = ref({})
const isSidebarOpen = ref(false)

const tabFields = computed(() =>
  docTypeMeta.value?.fields.filter(field => field.fieldtype === 'Tab Break') || []
)

const activeFieldSections = computed(() => {
  if (!docTypeMeta.value || !activeTab.value) return []
  const fields = docTypeMeta.value.fields
  const startIndex = fields.findIndex(f => f.name === activeTab.value)
  const endIndex = fields.findIndex((f, i) => i > startIndex && f.fieldtype === 'Tab Break')
  const relevantFields = fields.slice(startIndex + 1, endIndex === -1 ? undefined : endIndex)
  const sections = []
  let currentSection = null

  relevantFields.forEach(field => {
    if (field.fieldname === 'amended_from') {
      return
    }
    if (field.fieldtype === 'Section Break') {
      if (currentSection) {
        sections.push(currentSection)
      }
      currentSection = { label: field.label, fields: [], is_matrix: field.is_matrix, description: field.description }
    } else if (currentSection) {
      currentSection.fields.push(field)
    }
  })

  if (currentSection) {
    sections.push(currentSection)
  }
  return sections
})

const allSections = computed(() => {
  if (!docTypeMeta.value) return []

  const sections = []
  let currentSection = null

  docTypeMeta.value.fields.forEach(field => {
    if (field.fieldname === 'amended_from') {
      return
    }
    if (field.fieldtype === 'Tab Break') {
      return
    }
    if (field.fieldtype === 'Section Break') {
      if (currentSection) {
        sections.push(currentSection)
      }
      currentSection = { label: field.label, fields: [], is_matrix: field.is_matrix, description: field.description }
    } else if (currentSection) {
      currentSection.fields.push(field)
    }
  })

  if (currentSection) {
    sections.push(currentSection)
  }

  return sections
})

const isLastTab = computed(() => {
  const currentTabIndex = tabFields.value.findIndex(tab => tab.name === activeTab.value)
  return currentTabIndex === tabFields.value.length - 1
})

const isFirstTab = computed(() => {
  return activeTab.value === tabFields.value[0]?.name
})

const isFirstTabCompletelyFilled = computed(() => {
  if (!isFirstTab.value) return true
  const firstTabFields = activeFieldSections.value.flatMap(section => section.fields)
  return firstTabFields.every(field => {
    const value = formData.value[field.fieldname]
    return value !== null && value !== '' && (!Array.isArray(value) || value.length > 0)
  })
})

const isSubmitDisabled = computed(() => {
  return Object.entries(formData.value).some(([key, value]) => {
    const field = docTypeMeta.value?.fields.find(f => f.fieldname === key)
    return field && field.reqd && (value === null || value === '' || (Array.isArray(value) && value.length === 0))
  })
})

const getFieldComponent = (fieldtype) => {
  switch (fieldtype) {
    case 'Link': return props.isTable ? LinkTable : Link
    case 'Data': return Input
    case 'Table MultiSelect': return CheckBox
    case 'Button': return Button
    case 'Attach': return AttachmentUpload
    case 'Date': return DateInput
    case 'Small Text': return Textarea
    case 'Check': return CheckboxComponent
    default: return 'div'
  }
}

const isFieldVisible = (field) => {
  if (!field.depends_on) return true
  const condition = field.depends_on.replace('eval:', '').replace(/doc\./g, 'formData.')
  try {
    return new Function('formData', `return ${condition}`)(formData.value)
  } catch (error) {
    console.error('Error evaluating field visibility:', error)
    return false
  }
}

const handleFieldUpdate = (fieldName, value) => {
  formData.value[fieldName] = value
  // if (props.onfieldChange) {
  //   props.save_as_draft({ [fieldName]: value })
  // }
}

const getMeta = async () => {
  loading.value = true
  try {
    const res = await call('sva_form_vuejs.controllers.api.get_meta', {
      doctype: props.doctype,
    })
    if (res) {
      docTypeMeta.value = res
      activeTab.value = tabFields.value[0]?.name || ''
      openSections.value = new Array(allSections.value.length).fill(true)
      initializeFormData()
      initializeTabCompletionStatus()
    } else {
      console.error('Error fetching meta data: No document found')
    }
  } catch (error) {
    console.error('Error fetching meta data:', error)
  } finally {
    loading.value = false
  }
}

const initializeFormData = () => {
  if (!docTypeMeta.value) return
  const newFormData = { ...formData.value }
  docTypeMeta.value.fields.forEach(field => {
    if (!(field.fieldname in newFormData)) {
      if (field.fieldtype === 'Table MultiSelect') {
        newFormData[field.fieldname] = []
      } else {
        newFormData[field.fieldname] = field.fieldtype === 'Data' ? '' : null
      }
    }
  })
  // formData.value = newFormData
}

const initializeTabCompletionStatus = () => {
  tabFields.value.forEach(tab => {
    tabCompletionStatus.value[tab.name] = false
  })
}

const setActiveTab = (tabName) => {
  if (allTabsUnlocked.value || tabFields.value.indexOf(tabFields.value.find(tab => tab.name === tabName)) === 0) {
    activeTab.value = tabName
  }
}

const nextTab = () => {
  const currentIndex = tabFields.value.findIndex(tab => tab.name === activeTab.value)
  if (currentIndex === 0 && !allTabsUnlocked.value) {
    allTabsUnlocked.value = true
  }

  const currentTabFields = activeFieldSections.value.flatMap(section => section.fields)
  const isCurrentTabComplete = currentTabFields.some(field => {
    const value = formData.value[field.fieldname]
    return value !== null && value !== '' && (!Array.isArray(value) || value.length > 0)
  })

  if (isCurrentTabComplete) {
    tabCompletionStatus.value[activeTab.value] = true
  }

  if (currentIndex < tabFields.value.length - 1) {
    activeTab.value = tabFields.value[currentIndex + 1].name
  }
}

const toggleSection = (index) => {
  openSections.value[index] = !openSections.value[index]
}


provide('saveAsDraft', props.save_as_draft)

onMounted(() => {
  getMeta()
  if (Object.keys(props.initialData).length > 0) {
    formData.value = { ...props.initialData }
  }

  // Set initial sidebar state based on screen size
  isSidebarOpen.value = window.innerWidth >= 768

  // Update sidebar state on window resize
  window.addEventListener('resize', () => {
    isSidebarOpen.value = window.innerWidth >= 768
  })

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (event) => {
    if (isSidebarOpen.value && window.innerWidth < 768 && !event.target.closest('aside') && !event.target.closest('button')) {
      isSidebarOpen.value = false
    }
  })
})

// watch(formData, (newVal) => {
//   console.log('Form data updated:', newVal)
// }, { deep: true })

</script>

<style scoped>
.w-20 {
  width: 15% !important;
}

/* Add any additional styles here */
</style>