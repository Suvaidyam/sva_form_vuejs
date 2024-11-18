<template>
  <div class="w-full h-full bg-white dark:bg-gray-900 z-10" v-if="loading">
    <Loader />
  </div>
  <div v-else class="w-full h-full min-h-screen dark:bg-gray-900">
    <div v-if="allSections.length === 0" class="w-full h-full flex justify-center items-center text-h3 text-gray-500 dark:text-gray-400">
      Assessment Not Found
    </div>
    <div v-else class="max-w-[1920px] min-h-screen mx-auto overflow-hidden">
      <div :class="{ 'sm:flex min-h-screen': props.sidebar && !props.section }">
        <!-- Sidebar / Top Navigation -->
        <nav v-if="!props.section" :class="[
          props.sidebar ? 'lg:w-[350px]  bg-gray-50 dark:bg-gray-800 p-6 overflow-y-auto' : 'w-full bg-gray-50 dark:bg-gray-800 p-4'
        ]">
          <ul :class="[
            props.sidebar ? 'space-y-2' : 'flex space-x-2 overflow-x-auto'
          ]">
            <li v-for="tab in tabFields" :key="tab.name" :class="{ 'flex-shrink-0': !props.sidebar }">
              <button 
                @click="setActiveTab(tab.name)" 
                :class="[
                  'text-left px-4 py-2 rounded-lg transition-colors duration-150 ease-in-out w-full',
                  activeTab === tab.name
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700',
                  props.sidebar ? '' : 'whitespace-nowrap'
                ]"
              >
                {{ tab.label }}
              </button>
            </li>
          </ul>
        </nav>
        <!-- Main Content -->
        <div :class="[props.sidebar && !props.section ? 'lg:flex-1' : 'w-full', 'h-full overflow-y-auto']">
          <form @submit.prevent="handleSubmit" class="p-6 flex flex-col h-full">
            <div class="flex-grow">
              <template v-if="props.section">
                <div v-for="(section, index) in allSections" :key="index" class="mb-6">
                  <div 
                    @click="toggleSection(index)"
                    class="flex items-center justify-between cursor-pointer bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mb-2"
                  >
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                      {{ section.label }}
                    </h3>
                    <ChevronDownIcon
                      :class="['w-5 h-5 transition-transform', { 'transform rotate-180': openSections[index] }]"
                    />
                  </div>
                  <div v-show="openSections[index]" class="pl-4">
                    <div v-for="(field, fieldIndex) in section.fields" :key="field.name" class="mb-4">
                      <component 
                        v-if="isFieldVisible(field)"
                        :is="getFieldComponent(field.fieldtype)"
                        :field="field"
                        :isCard="props.isCard"
                        :matrix="section.is_matrix"
                        :index="fieldIndex"
                        v-model="formData[field.fieldname]"
                        @update:modelValue="handleFieldUpdate(field.fieldname, $event)"
                      />
                    </div>
                  </div>
                </div>
              </template>
              <template v-else>
                <div v-for="(section, index) in activeFieldSections" :key="section.name" class="mb-6">
                  <h3 :id="`section-${index}`" class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    {{ section.label }}
                  </h3>
                  <div v-if="section.fields && section.fields.length > 0" :aria-labelledby="`section-${index}`" class="space-y-4">
                    <div v-for="(field, fieldIndex) in section.fields" :key="field.name" class="mb-4">
                      <component 
                        v-if="isFieldVisible(field)"
                        :is="getFieldComponent(field.fieldtype)"
                        :field="field"
                        :isCard="true"
                        :matrix="section.is_matrix"
                        :index="fieldIndex"
                        v-model="formData[field.fieldname]"
                        @update:modelValue="handleFieldUpdate(field.fieldname, $event)"
                        :aria-label="field.label || field.fieldname"
                      />
                    </div>
                  </div>
                  <p v-else class="text-gray-500 dark:text-gray-400 italic">
                    No fields in this section.
                  </p>
                </div>
              </template>
            </div>
            <div :class="isDraft ? '' : 'justify-end'" class="mt-6 flex gap-2">
              <button 
                v-if="!props.section && !isLastTab" 
                @click="nextTab" 
                type="button"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Next
              </button>
              <button 
                :disabled="isSubmitDisabled"
                :class="isSubmitDisabled ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700 text-white'"
                v-if="props.section || isLastTab" 
                type="submit"
                class="px-4 py-2 border rounded-md focus:outline-none"
              >
                Submit
              </button>
              <button 
                @click="props.save_as_draft" 
                v-if="props.isDraft" 
                type="button"
                :disabled="isSubmitDisabled"
                :class="isSubmitDisabled ? 'bg-gray-400' : 'bg-white hover:bg-gray-100'"
                class="px-4 py-2 border shadow-md rounded-md focus:outline-none"
              >
                Save as Draft
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, watch } from 'vue'
import { ChevronDownIcon } from 'lucide-vue-next'
import Input from './Input.vue'
import Link from './Link.vue'
import LinkTable from './LinkTable.vue'
import CheckBox from './CheckBox.vue'
import Button from './Button.vue'
import { useRouter } from 'vue-router'
import Loader from './Loader.vue'
import AttachmentUpload from './AttachmentUpload.vue'

const router = useRouter()
const loading = ref(true)
const props = defineProps({
  doctype: {
    type: String,
    required: true
  },
  sidebar: {
    type: Boolean,
    default: false
  },
  section: {
    type: Boolean,
    default: false
  },
  isRoute: {
    type: String,
    default: ''
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
  }
})

const call = inject('$call')

const docTypeMeta = ref(null)
const activeTab = ref('')
const formData = ref({})
const openSections = ref([])

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
    if (field.fieldtype === 'Section Break') {
      if (currentSection) {
        sections.push(currentSection)
      }
      currentSection = { label: field.label, fields: [], is_matrix: field.is_matrix }
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
    if (field.fieldtype === 'Tab Break') {
      return
    }
    if (field.fieldtype === 'Section Break') {
      if (currentSection) {
        sections.push(currentSection)
      }
      currentSection = { label: field.label, fields: [], is_matrix: field.is_matrix }
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
  docTypeMeta.value.fields.forEach(field => {
    if (field.fieldtype === 'Table MultiSelect') {
      formData.value[field.fieldname] = []
    } else {
      formData.value[field.fieldname] = field.fieldtype === 'Data' ? '' : null
    }
  })
}

const setActiveTab = (tabName) => {
  activeTab.value = tabName
}

const nextTab = () => {
  const currentIndex = tabFields.value.findIndex(tab => tab.name === activeTab.value)
  if (currentIndex < tabFields.value.length - 1) {
    activeTab.value = tabFields.value[currentIndex + 1].name
  }
}

const toggleSection = (index) => {
  openSections.value[index] = !openSections.value[index]
}

const handleSubmit = async () => {
  try {
    const res = await call('frappe.desk.form.save.savedocs', {
      doc: JSON.stringify({ 
        doctype: props.doctype,
        ...formData.value
      }),
      action: 'Save'
    })
    console.log('Saved:', res)
    if (res && props.isRoute) {
      router.push(props.isRoute)
    }
  } catch (err) {
    console.error('Error saving form:', err)
  }
}

onMounted(getMeta)
</script>