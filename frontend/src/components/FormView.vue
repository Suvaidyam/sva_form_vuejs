<template>
  <div class="flex w-full h-screen bg-white dark:bg-gray-900">
    <!-- Sidebar -->
    <aside v-if="!props.section" :class="[
      'sticky top-0 h-full w-20 bg-gray-50 dark:bg-gray-800',
      isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
      'md:translate-x-0'
    ]">
      <div class="flex flex-col h-full">
        <nav class="flex-1 px-4 py-4">
          <ul class="space-y-2">
            <li v-for="(tab, index) in tabFields" :key="tab.name">
              <button @click="setActiveTab(tab.name)" :disabled="index > 0 && !allTabsUnlocked" :class="[
                'w-full text-left px-4 py-2 rounded-lg transition-colors duration-150 ease-in-out flex justify-between items-center',
                activeTab === tab.name
                  ? 'bg-orange-500 text-white'
                  : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700',
                index > 0 && !allTabsUnlocked ? 'opacity-50 cursor-not-allowed' : '',
                showErrors && tabErrors[tab.name] ? 'border-2 border-red-500' : ''
              ]">
                {{ tab.label }}
                <span class="mr-2" v-if="index > 0">
                  <LockIcon v-if="!allTabsUnlocked" class="w-4 h-4" />
                  <CheckCircleIcon v-if="allTabsUnlocked && isTabComplete(tab.name)" class="w-4 h-4 text-green-500" />
                  <XCircleIcon v-if="showErrors && tabErrors[tab.name]" class="w-4 h-4 text-red-500" />
                </span>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </aside>
    <!-- Loader -->
    <Loader v-if="loading" :show="props.isDraft" />
    <!-- Main Content -->
    <main class="flex-1 w-75 " v-else>
      <div class="mx-auto px-6 py-8">
        <div v-if="allSections.length === 0" class="text-center text-gray-500 dark:text-gray-400 text-2xl mt-20">
          Assessment Not Found
        </div>
        <div v-else>
          <!-- Loader -->
          <!-- <div v-if="isLoading" class=" bg-white  inset-0 bg-opacity-50 flex items-center justify-center z-50">
            <div class="animate-spin  rounded-full h-32 w-32 border-t-2 border-b-2 border-orange-500"></div>
          </div> -->

          <form @submit.prevent="onSubmit" class="mt-16 md:mt-0">
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
                        :is="getFieldComponent(field.fieldtype, section)" :field="field" :isCard="props.isCard" :isColumn="props.isColumn"
                        :matrix="section.is_matrix" :index="fieldIndex" v-model="formData[field.fieldname]"
                        :onfieldChange="props.onfieldChange" :isRow="props.isRow"
                        @update:modelValue="handleFieldUpdate(field.fieldname, $event)"
                        :class="{ 'border-red-500': showErrors && fieldErrors[field.fieldname] }" />
                      <p v-if="showErrors && fieldErrors[field.fieldname]" class="text-red-500 text-sm mt-1">
                        {{ fieldErrors[field.fieldname] }}
                      </p>
                    </div>
                  </div>
                </div>
              </template>
              <template v-else>
                <div v-for="(section, index) in activeFieldSections" :key="section.name" class="mb-6">
                  <h3 :id="`section-${index}`" class="text-2xl font-semibold custom dark:text-white mb-4 flex ">
                    {{ section.label }}
                    <SaveStatusIcon v-if="section.label" class=" mt-2 cust" :status="status" />
                  </h3>
                  <div v-if="section.fields && section.fields.length > 0 && !section.table_matrix" :aria-labelledby="`section-${index}`"
                    class="space-y-4">
                    <!-- {{ section }} -->
                    <div v-for="(field, fieldIndex) in section.fields" :key="field.fieldname" class="mb-4">
                      <component v-if="isFieldVisible(field)" :section="section.description"
                        :is="getFieldComponent(field.fieldtype ,section)" :field="field" :isCard="props.isCard" :isColumn="props.isColumn"
                        :dropDownOptions="field.is_dropDown" :matrix_code="is_matrix_code" :matrix="section.is_matrix"
                        :multi_matrix="section.is_multi_matrix" :index="fieldIndex" :formData="formData"
                        v-model="formData[field.fieldname]" :isRow="props.isRow"
                        @update:modelValue="handleFieldUpdate(field.fieldname, $event)"
                        :onfieldChange="props.onfieldChange" :aria-label="field.label || field.fieldname"
                        :class="{ 'border-red-500': showErrors && fieldErrors[field.fieldname] }" />
                      <p v-if="showErrors && fieldErrors[field.fieldname]" class="text-red-500 text-sm mt-1">
                        {{ fieldErrors[field.fieldname] }}
                      </p>
                    </div>
                  </div>
                  <!-- <p v-else class="text-gray-500 dark:text-gray-400 italic">
                    No fields in this section.
                  </p> -->
                  <!-- new -->
                  <div v-if="section.fields && section.fields.length > 0 && section.table_matrix" :aria-labelledby="`section-${index}`"
                    class="flex gap-3  items-center matrix-overflow">
                    <!-- {{ section }} -->
                    <div v-for="(field, fieldIndex) in section.fields" :key="field.fieldname" class="mb-4">
                      <component v-if="isFieldVisible(field)" :section="section.description"
                        :is="getFieldComponent(field.fieldtype, section)" :field="field" :isCard="props.isCard" :isColumn="props.isColumn"
                        :dropDownOptions="field.is_dropDown" :matrix_code="is_matrix_code" :matrix="section.is_matrix"
                        :table_matrix="section.table_matrix"
                        :multi_matrix="section.is_multi_matrix" :index="fieldIndex" :formData="formData"
                        v-model="formData[field.fieldname]" :isRow="props.isRow"
                        @update:modelValue="handleFieldUpdate(field.fieldname, $event)"
                        :onfieldChange="props.onfieldChange" :aria-label="field.label || field.fieldname"
                        :class="{ 'border-red-500': showErrors && fieldErrors[field.fieldname] }" />
                      <p v-if="showErrors && fieldErrors[field.fieldname]" class="text-red-500 text-sm mt-1">
                        {{ fieldErrors[field.fieldname] }}
                      </p>
                    </div>
                  </div>
                 
                </div>
              </template>
            </div>
            <div class="mt-6 flex justify-end gap-2">
              <button v-if="!props.section && !isLastTab" @click="nextTab" type="button" :disabled="!isCurrentTabValid"
                :class="[
                  'px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                  !isCurrentTabValid
                    ? 'bg-gray-300 abc cursor-not-allowed'
                    : 'bg-orange-500 text-white hover:bg-orange-600'
                ]">
                Next
              </button>
              <button :style="{ backgroundColor: props.submitButtonColor }" :class="[
                isSubmitDisabled ? 'bg-gray-400' : `bg-blue-500 hover:bg-blue-600`,
                'text-white'
              ]" v-if="props.section || isLastTab" type="submit"
                class="px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2">
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
import { ChevronDownIcon, LockIcon, CheckCircleIcon, XIcon, MenuIcon, XCircleIcon } from 'lucide-vue-next'
import Input from './Input.vue'
import Link from './Link.vue'
import LinkPW from './LinkPW.vue'
import LinkTable from './LinkTable.vue'
import CheckBox from './CheckBox.vue'
import CheckBoxPW from './CheckBoxPW.vue'
import Button from './Button.vue'
import Loader from './Loader.vue'
import AttachmentUpload from './AttachmentUpload.vue'
import DateInput from './DateInput.vue'
import Textarea from './TextareaInput.vue'
import CheckboxComponent from './CheckboxComponent.vue'
import percent from './PercentageInput.vue'
import SaveStatusIcon from './SaveStatusIcon.vue'
import MultiSelectMatrix from './MultiSelectMatrix.vue'

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
  isRow: {
    type: Boolean,
    default: false
  },
  isColumn: {
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
  },
  toast: {
    type: Function,
    required: false
  },
  status: {
    type: String,
    default: 'idle',
    required: false
  }
})

const call = inject('$call')
const loading = ref(true)
const isLoading = ref(false)
const docTypeMeta = ref(null)
const activeTab = ref('')
const formData = ref({})
const openSections = ref([])
const allTabsUnlocked = ref(false)
const tabCompletionStatus = ref({})
const isSidebarOpen = ref(false)
const fieldErrors = ref({})
const tabErrors = ref({})
const showErrors = ref(false)

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
      currentSection = { label: field.label, fields: [], is_matrix: field.is_matrix, description: field.description, is_multi_matrix: field.is_multi_matrix, is_matrix_code: field.is_matrix_code,table_matrix:field.table_matrix }
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
  let mismatchedDependsOn = []
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
      if (field.depends_on) {
        if (field.mandatory_depends_on && field.mandatory_depends_on != field.depends_on) {
          mismatchedDependsOn.push(field.label)
        }
      }

      currentSection.fields.push(field)
    }
  })
  console.log(mismatchedDependsOn, 'mismatchedDependsOn');

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

const isCurrentTabValid = computed(() => {
  const currentTabFields = getTabFields(activeTab.value)
  return currentTabFields.every(field => {
    const value = formData.value[field.fieldname]
    return !field.reqd || (value !== null && value !== '' && (!Array.isArray(value) || value.length > 0))
  })
})

const isSubmitDisabled = computed(() => {
  return !Object.entries(formData.value).some(([key, value]) => {
    const field = docTypeMeta.value?.fields.find(f => f.fieldname === key);
    return field && value !== null && value !== '' && (!Array.isArray(value) || value.length > 0);
  });
})

const getFieldComponent = (fieldtype, section) => {
  // console.log(section, 'section');
  switch (fieldtype) {
    case 'Link': return props.isTable ? LinkTable : props.isColumn ? LinkPW : Link
    case 'Data': return Input
    case 'Table MultiSelect': return props.isCard ? CheckBoxPW : (section.is_multi_matrix ? MultiSelectMatrix :CheckBox)
    case 'Button': return Button
    case 'Attach': return AttachmentUpload
    case 'Date': return DateInput
    case 'Small Text': return Textarea
    case 'Check': return CheckboxComponent
    case 'Int': return Input
    case 'Percent': return percent
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

const isTabComplete = (tabName) => {
  const tabFields = getTabFields(tabName)
  return tabFields.every(field => {
    const value = formData.value[field.fieldname]
    return !field.reqd || (value !== null && value !== '' && (!Array.isArray(value) || value.length > 0))
  })
}

const getTabFields = (tabName) => {
  if (!docTypeMeta.value) return []
  const fields = docTypeMeta.value.fields
  const startIndex = fields.findIndex(f => f.name === tabName)
  const endIndex = fields.findIndex((f, i) => i > startIndex && f.fieldtype === 'Tab Break')
  return fields.slice(startIndex + 1, endIndex === -1 ? undefined : endIndex)
}

const handleFieldUpdate = (fieldName, value) => {
  formData.value[fieldName] = value
  if (showErrors.value) {
    validateField(fieldName)
  }
}

const validateField = (fieldName) => {
  const field = docTypeMeta.value.fields.find(f => f.fieldname === fieldName)
  if (!field) return

  if (field.reqd && (!formData.value[fieldName] || formData.value[fieldName] === '')) {
    fieldErrors.value[fieldName] = 'This field is required'
  } else {
    delete fieldErrors.value[fieldName]
  }

  updateTabErrors()
}

const updateTabErrors = () => {
  tabErrors.value = {}
  tabFields.value.forEach(tab => {
    const tabFieldNames = getTabFields(tab.name).map(f => f.fieldname)
    if (tabFieldNames.some(fieldName => fieldErrors.value[fieldName])) {
      tabErrors.value[tab.name] = true
    }
  })
}

const getMeta = async () => {
  loading.value = true
  isLoading.value = true
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
    isLoading.value = false
  }
}

const initializeFormData = () => {
  if (!docTypeMeta.value) return
  const newFormData = { ...formData.value }
  if (formData.value?.active_tab) {
    const firstTab = tabFields.value[0]?.name
    if (firstTab != formData.value?.active_tab && !allTabsUnlocked.value) {
      allTabsUnlocked.value = true
      setActiveTab(formData.value?.active_tab, true)
    }
  }
  docTypeMeta.value.fields.forEach(field => {
    if (!(field.fieldname in newFormData)) {
      if (field.fieldtype === 'Table MultiSelect') {
        newFormData[field.fieldname] = []
      } else {
        newFormData[field.fieldname] = field.fieldtype === 'Data' ? '' : null
      }
    }
  })
  formData.value = newFormData
}

const initializeTabCompletionStatus = () => {
  tabFields.value.forEach(tab => {
    tabCompletionStatus.value[tab.name] = false
  })
}

const setActiveTab = async (tabName, fromMounted = false) => {
  if (!fromMounted) {
    isLoading.value = true
    try {
      await props.save_as_draft({ 'active_tab': tabName })
      if (allTabsUnlocked.value || tabFields.value.indexOf(tabFields.value.find(tab => tab.name === tabName)) === 0) {
        activeTab.value = tabName
      }
      await fetchTabData(tabName)
    } finally {
      isLoading.value = false
    }
  } else {
    if (allTabsUnlocked.value || tabFields.value.indexOf(tabFields.value.find(tab => tab.name === tabName)) === 0) {
      activeTab.value = tabName
    }
  }
}

const nextTab = async () => {
  if (isCurrentTabValid.value) {
    isLoading.value = true
    try {
      const currentIndex = tabFields.value.findIndex(tab => tab.name === activeTab.value)
      if (currentIndex === 0 && !allTabsUnlocked.value) {
        allTabsUnlocked.value = true
      }

      tabCompletionStatus.value[activeTab.value] = true

      if (currentIndex < tabFields.value.length - 1) {
        const nextTabName = tabFields.value[currentIndex + 1].name
        await setActiveTab(nextTabName)
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      }
    } finally {
      isLoading.value = false
    }
  } else {
    validateCurrentTab()
  }
}

const fetchTabData = async (tabName) => {
  await new Promise(resolve => setTimeout(resolve, 1000))
  console.log(`Fetched data for tab: ${tabName}`)
}

const toggleSection = (index) => {
  openSections.value[index] = !openSections.value[index]
}

const onSubmit = () => {
  showErrors.value = true
  validateAllFields()
  const { isValid, firstErrorTab, sectionsWithErrors } = validateForm()

  if (!isValid) {
    if (firstErrorTab) {
      setActiveTab(firstErrorTab)
    }
    const errorMessage = `Mandatory fields not filled in sections`
    props.toast.error(errorMessage, {
      timeout: 5000,
      closeOnClick: true,
    })
    const firstErrorField = document.querySelector('.border-red-500')
    if (firstErrorField) {
      firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  } else {
    props.onSubmit(formData.value)
  }
}

const validateForm = () => {
  const sectionsWithErrors = new Set()
  let firstErrorTab = null

  docTypeMeta.value.fields.forEach(field => {
    if (field.reqd && (!formData.value[field.fieldname] || formData.value[field.fieldname] === '')) {
      const section = allSections.value.find(s => s.fields.some(f => f.fieldname === field.fieldname))
      if (section) {
        sectionsWithErrors.add(section.label)
      }
      if (!firstErrorTab) {
        firstErrorTab = tabFields.value.find(tab =>
          tab.name === field.parent ||
          (field.idx > tab.idx && field.idx < (tabFields.value[tabFields.value.indexOf(tab) + 1]?.idx || Infinity))
        )?.name
      }
    }
  })

  return { isValid: sectionsWithErrors.size === 0, firstErrorTab, sectionsWithErrors }
}

const validateAllFields = () => {
  docTypeMeta?.value?.fields?.forEach(field => {
    validateField(field.fieldname)
  })
}

provide('saveAsDraft', props.save_as_draft)

onMounted(() => {
  getMeta()
  if (Object.keys(props.initialData).length > 0) {
    formData.value = { ...props.initialData }
  }

  isSidebarOpen.value = window.innerWidth >= 768

  window.addEventListener('resize', () => {
    isSidebarOpen.value = window.innerWidth >= 768
  })

  document.addEventListener('click', (event) => {
    if (isSidebarOpen.value && window.innerWidth < 768 && !event.target.closest('aside') && !event.target.closest('button')) {
      isSidebarOpen.value = false
    }
  })
})

watch(() => props.initialData, (newVal) => {
  formData.value = { ...newVal }
  initializeFormData()
  validateAllFields()
}, { deep: true, immediate: true })

watch(formData, () => {
  if (showErrors.value) {
    validateAllFields()
  }
}, { deep: true })
</script>

<style scoped>
.w-20 {
  width: 15% !important;
  min-width: 15% !important;
}
.w-75 {
  width: 75% !important;
  min-width: 75% !important;
}

.custom {
  color: #0E4688 !important;
  margin-top: -15px !important;
}

.ml-5 {
  margin-left: 1.25rem !important;
  color: #0E4688 !important;
}

.abc {
  background-color: #EFEFEF !important;
  color: rgb(119, 119, 119) !important;
}

aside {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

main::-webkit-scrollbar,
aside::-webkit-scrollbar {
  display: none;
}

main,
aside {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.cust {
  margin-left: 20px !important;
}
.matrix-overflow{
  overflow-x: scroll !important;
  overflow-y: hidden !important;
}
</style>