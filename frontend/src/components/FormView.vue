<template>
	<div class="flex w-full h-screen dark:bg-gray-900">
		<!-- Sidebar -->
		<aside v-if="!props.section" :class="[
			'sticky top-0 h-full w-20',
			isSidebarOpen ? 'show-sidebar' : 'hide-sidebar',
			'md:translate-x-0',
		]">
			<div class="flex flex-col h-full bg-gray-50 dark:bg-gray-800 side-bar-scroll">
				<nav class="flex-1 px-4 py-4 relative">
					<ul class="space-y-2">
						<li v-for="(tab, index) in tabFields" :key="tab.name">
							<button @click="setActiveTab(tab.name)" :disabled="index > 0 && !allTabsUnlocked" :class="[
								'w-full text-left px-4 py-2 rounded-lg transition-colors duration-150 ease-in-out flex justify-between items-center',
								activeTab === tab.name
									? 'bg-orange-500 text-white'
									: 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700',
								index > 0 && !allTabsUnlocked
									? 'opacity-50 cursor-not-allowed'
									: '',
								showErrors && tabErrors[tab.name] && !isTabComplete(tab.name)
									? 'border-2 border-red-500'
									: '',
							]">
								{{ tab.label }}
								<span class="mr-2" v-if="index > 0">
									<LockIcon v-if="!allTabsUnlocked" class="w-4 h-4" />
									<CheckCircleIcon v-if="allTabsUnlocked && isTabComplete(tab.name)"
										class="w-4 h-4 text-green-500" />
									<XCircleIcon v-if="showErrors && tabErrors[tab.name] && !isTabComplete(tab.name)"
										class="w-4 h-4 text-red-500" />
								</span>
							</button>
						</li>
					</ul>
					<div>
						<!-- static info box this text ⓘ Please add any collaborators to complete the survey, if you haven't already done so. -->
						<div class="mt-6">

							<i class=" text-[14px] ">
								<span class="block " style="color: #616161 !important;"> ⓘ Please add any collaborators
									to complete the survey, if you haven't already done so.</span>
							</i>
						</div>

					</div>
				</nav>
				<span @click="toggleSidebar" class="fixed border md:hidden h-full w-1 max-w-[2px] z-50" :style="{
					left: isSidebarOpen ? '240px !important' : '250px !important',
					borderColor: '#9ca3af !important',
					paddingTop: '5px !important',
				}">
					<span v-if="isSidebarOpen"
						class="w-6 h-6 flex items-center justify-center shadow-lg shadow-gray-400 rounded-full bg-white absolute top-[15%] text-gray-500"
						style="left: -12px">
						<CircleChevronLeft class="w-4 h-4 text-gray-700" />
					</span>
					<span v-else
						class="w-6 h-6 flex items-center justify-center shadow-lg shadow-gray-400 rounded-full bg-white absolute top-[15%] text-gray-500"
						style="left: -12px">
						<CircleChevronRight class="w-4 h-4 text-gray-500" />
					</span>
				</span>
			</div>
		</aside>

		<!-- Loader -->
		<Loader v-if="loading" :show="props.isDraft" />

		<!-- Main Content -->
		<main :class="[props.width ? 'w-full' : 'w-75', 'flex-1']" v-else>
			<div :class="[section_hidden ? 'mx-auto pb-8 ' : 'mx-auto pb-8 px-4']">
				<div v-if="allSections.length === 0"
					class="text-center text-gray-500 dark:text-gray-400 text-2xl mt-20">
					Assessment Not Found
				</div>
				<div v-else>
					<form @submit.prevent="onSubmit" class="mt-2">
						<div>
							<template v-if="props.section">
								<div v-for="(section, index) in allSections" :key="index" class="mb-4 mt-2">
									<div @click="toggleSection(index)" :class="[section_hidden ? 'hidden' : '']"
										class="flex items-center justify-between cursor-pointer bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mb-2">
										<h3 class="text-lg font-semibold text-gray-900 dark:text-white">
											{{ section.label }}
										</h3>
										<ChevronDownIcon v-if="!openSections[index]" :class="[
											'w-5 h-5 transition-transform',
											{ 'transform rotate-180': openSections[index] },
										]" />
										<ChevronUpIcon v-if="openSections[index]" :class="[
											'w-5 h-5 transition-transform',
											{ 'transform rotate-180': openSections[index] },
										]" />
									</div>
									<div v-show="openSections[index]" class="pl-4">
										<div v-for="(field, fieldIndex) in section.fields" :key="field.name"
											class="mb-4">
											<component :section="section.description" v-if="isFieldVisible(field)"
												:is="getFieldComponent(field.fieldtype, section)" :field="field"
												:isCard="props.isCard" :isColumn="props.isColumn"
												:matrix="section.is_matrix" :index="field.qno"
												v-model="formData[field.fieldname]" :onfieldChange="props.onfieldChange"
												:isRow="props.isRow" @update:modelValue="
													handleFieldUpdate(field.fieldname, $event)
													" :class="{
														'border-red-500':
															showErrors && fieldErrors[field.fieldname],
													}" />
											<p v-if="showErrors && fieldErrors[field.fieldname]"
												class="text-red-500 text-sm mt-1">
												{{ fieldErrors[field.fieldname] }}
											</p>
											<p v-if="calculatedFieldErrors[field.fieldname]"
												class="text-red-500 text-sm mt-1">
												{{ calculatedFieldErrors[field.fieldname] }}
											</p>
										</div>
									</div>
								</div>
							</template>
							<template v-else>
								<div v-for="(section, index) in activeFieldSections" :key="section.name" :class="section.is_matrix || section.is_multi_matrix
									? 'matrix-overflow1'
									: ''
									">
									<h3 v-if="section?.label" :id="`section-${index}`"
										class="text-2xl font-semibold custom dark:text-white flex"
										:class="section.label ? 'padding' : 'mb-4'">
										{{ section.label }}
										<SaveStatusIcon v-if="section.label" class="mt-2 cust" :status="status" />
									</h3>
									<!-- section.fields.every((field) => {return isFieldVisible(field)}) && -->
									<div v-if="
										isFieldVisible(section) &&
										((section.fields.some((field) => {
											return isFieldVisible(field);
										}) &&
											getString(section?.description).qlable) ||
											getString(section?.description)?.cenrieo ||
											getString(section?.description)?.info)
									" class="flex justify-between items-center">
										<div v-if="
											getString(section?.description).qlable ||
											getString(section?.description)?.cenrieo
										">
											<span v-if="getString(section?.description).qlable"
												class="text-md font-medium text-gray-900 dark:text-gray-200 block">
												{{ getString(section?.description)?.qlable }}
											</span>
											<p v-if="getString(section?.description)?.cenrieo"
												class="text-md font-medium text-gray-900 dark:text-gray-200 block">
												{{ getString(section?.description)?.cenrieo }}
											</p>
										</div>

										<div v-if="getString(section?.description)?.info" class="relative">
											<Popover v-slot="{ open }" class="relative">
												<PopoverButton class="focus:outline-none">
													<InfoIcon
														class="w-5 h-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300" />
												</PopoverButton>
												<transition enter-active-class="transition duration-200 ease-out"
													enter-from-class="opacity-0 translate-y-1"
													enter-to-class="opacity-100 translate-y-0"
													leave-active-class="transition duration-150 ease-in"
													leave-from-class="opacity-100 translate-y-0"
													leave-to-class="opacity-0 translate-y-1">
													<PopoverPanel
														class="absolute z-10 w-96 px-4 mt-3 transform -translate-x-full right-0 sm:px-0 lg:max-w-3xl">
														<div
															class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
															<div class="p-4 bg-white dark:bg-gray-800">
																<p
																	class="text-sm text-gray-700 dark:text-gray-200 block">
																	{{
																		getString(
																			section?.description
																		)?.info
																	}}
																</p>
															</div>
														</div>
													</PopoverPanel>
												</transition>
											</Popover>
										</div>
									</div>
									<div v-if="
										section.fields &&
										section.fields.length > 0 &&
										section.fields.some((field) => {
											return isFieldVisible(field);
										})
									" :aria-labelledby="`section-${index}`" class="space-y-6 mb-6">
										<div v-if="!section.table_matrix" v-for="(field, fieldIndex) in section.fields"
											:key="field.fieldname" class="">
											<component v-if="isFieldVisible(field)" :section="section.description"
												:is="getFieldComponent(field.fieldtype, section)"
												:allTabsUnlocked="allTabsUnlocked" :field="field" :isCard="props.isCard"
												:isColumn="props.isColumn" :dropDownOptions="field.is_dropDown"
												:matrix_code="section.is_matrix_code" :matrix="section.is_matrix"
												:multi_matrix="section.is_multi_matrix" :index="fieldIndex"
												:formData="formData" v-model="formData[field.fieldname]"
												:isRow="props.isRow" @update:modelValue="
													handleFieldUpdate(field.fieldname, $event)
													" :onfieldChange="props.onfieldChange" :aria-label="field.label || field.fieldname" :class="{
														'border-red-500':
															showErrors && fieldErrors[field.fieldname],
													}" />
											<p v-if="showErrors && fieldErrors[field.fieldname]"
												class="text-red-500 text-sm mt-1">
												{{ fieldErrors[field.fieldname] }}
											</p>
											<p v-if="calculatedFieldErrors[field.fieldname]"
												class="text-red-500 text-sm mt-1">
												{{ calculatedFieldErrors[field.fieldname] }}
											</p>
										</div>
										<div v-if="section.table_matrix" class="flex">
											<div v-for="(field, fieldIndex) in section.fields" :key="field.fieldname">
												<component class="border  border-gray-200 mt-2"
													v-if="isFieldVisible(field)" :section="section.description" :is="getFieldComponent(field.fieldtype, section)
														" :allTabsUnlocked="allTabsUnlocked" :field="field" :isCard="props.isCard" :isColumn="props.isColumn"
													:dropDownOptions="field.is_dropDown"
													:matrix_code="section.is_matrix_code" :matrix="section.is_matrix"
													:table_matrix="section.table_matrix"
													:multi_matrix="section.is_multi_matrix" :index="fieldIndex"
													:formData="formData" v-model="formData[field.fieldname]"
													:isRow="props.isRow" @update:modelValue="
														handleFieldUpdate(field.fieldname, $event)
														" :onfieldChange="props.onfieldChange" :aria-label="field.label || field.fieldname" :class="{
															'border-red-500':
																showErrors &&
																fieldErrors[field.fieldname],
														}" />
												<p v-if="
													showErrors && fieldErrors[field.fieldname]
												" class="text-red-500 text-sm mt-1">
													{{ fieldErrors[field.fieldname] }}
												</p>
												<p v-if="calculatedFieldErrors[field.fieldname]"
													class="text-red-500 text-sm mt-1">
													{{ calculatedFieldErrors[field.fieldname] }}
												</p>
											</div>
										</div>
									</div>
								</div>
							</template>
						</div>
						<div class="mt-6 flex justify-end gap-2">
							<button v-if="!props.section && !isLastTab" @click="nextTab" type="button"
								:disabled="!isCurrentTabValid" :class="[
									'px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
									!isCurrentTabValid
										? 'bg-gray-300 abc cursor-not-allowed'
										: 'bg-orange-500 text-white hover:bg-orange-600',
								]">
								Next
							</button>
							<button :style="{ backgroundColor: props.submitButtonColor }" :class="[
								isSubmitDisabled
									? 'bg-gray-400'
									: `bg-blue-500 hover:bg-blue-600`,
								'text-white',
							]" v-if="props.section || isLastTab" type="submit"
								class="px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2">
								Submit
							</button>
							<button @click="save_as_draft(formData)" v-if="props.isDraft" type="button"
								:disabled="isSubmitDisabled" :class="isSubmitDisabled ? 'bg-gray-400' : 'bg-white hover:bg-gray-100'
									" class="px-4 py-2 border shadow-md rounded-md focus:outline-none">
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
import { ref, computed, onMounted, inject, watch, provide } from "vue";
import {
	ChevronDownIcon,
	LockIcon,
	CheckCircleIcon,
	XCircleIcon,
	ChevronUpIcon,
} from "lucide-vue-next";
import Input from "./Input.vue";
import Link from "./Link.vue";
import LinkPW from "./LinkPW.vue";
import LinkTable from "./LinkTable.vue";
import CheckBox from "./CheckBox.vue";
import CheckBoxPW from "./CheckBoxPW.vue";
import Button from "./Button.vue";
import Loader from "./Loader.vue";
import AttachmentUpload from "./AttachmentUpload.vue";
import DateInput from "./DateInput.vue";
import Textarea from "./TextareaInput.vue";
import CheckboxComponent from "./CheckboxComponent.vue";
import percent from "./PercentageInput.vue";
import SaveStatusIcon from "./SaveStatusIcon.vue";
import MultiSelectMatrix from "./MultiSelectMatrix.vue";
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import { InfoIcon, CircleChevronRight, CircleChevronLeft } from "lucide-vue-next";

const props = defineProps({
	doctype: {
		type: String,
		required: true,
	},
	section: {
		type: Boolean,
		default: false,
	},
	section_hidden: {
		type: Boolean,
		default: false,
	},
	isTable: {
		type: Boolean,
		default: false,
	},
	isCard: {
		type: Boolean,
		default: false,
	},
	isDraft: {
		type: Boolean,
		default: false,
	},
	isRow: {
		type: Boolean,
		default: false,
	},
	isColumn: {
		type: Boolean,
		default: false,
	},
	save_as_draft: {
		type: Function,
		default: () => console.log("save_as_draft..."),
	},
	initialData: {
		type: Object,
		default: () => ({}),
	},
	onSubmit: {
		type: Function,
		required: true,
	},
	onfieldChange: {
		type: Boolean,
		default: false,
	},
	submitButtonColor: {
		type: String,
		default: "#255b97",
	},
	toast: {
		type: Function,
		required: false,
	},
	width: {
		type: Function,
		required: false,
		default: false,
	},
	status: {
		type: String,
		default: "idle",
		required: false,
	},
});

const call = inject("$call");
const loading = ref(true);
const isLoading = ref(false);
const docTypeMeta = ref(null);
const activeTab = ref("");
const formData = ref({});
const openSections = ref([]);
const allTabsUnlocked = ref(false);
const tabCompletionStatus = ref({});
const isSidebarOpen = ref(false);
const fieldErrors = ref({});
const tabErrors = ref({});
const showErrors = ref(false);
const calculatedFieldErrors = ref({});
const minMaxValue = ref({});
const saveAsDraft = inject("saveAsDraft");

function getString(str) {
	let desc = "";
	let info = "";
	let qlable = "";
	let cenrieo = "";

	const match = str?.match(/\{([^}]+)\}/);
	if (match) {
		info = match[1];
		str = str.replace(match[0], "").trim();
	}

	const cenrieoSplit = str?.split("@@");
	if (cenrieoSplit?.length > 1) {
		cenrieo = cenrieoSplit[1].trim();
		str = cenrieoSplit[0].trim();
	}

	const parts = str?.split("$$");
	if (parts?.length > 1) {
		qlable = parts[1].trim();
		str = parts[0].trim();
	}

	desc = str?.trim();

	return { desc, info, qlable, cenrieo };
}
const tabFields = computed(
	() => docTypeMeta.value?.fields.filter((field) => field.fieldtype === "Tab Break") || []
);

const activeFieldSections = computed(() => {
	if (!docTypeMeta.value || !activeTab.value) return [];
	const fields = docTypeMeta.value.fields;
	const startIndex = fields.findIndex((f) => f.name === activeTab.value);
	const endIndex = fields.findIndex((f, i) => i > startIndex && f.fieldtype === "Tab Break");
	const relevantFields = fields.slice(startIndex + 1, endIndex === -1 ? undefined : endIndex);
	const sections = [];
	let currentSection = null;

	relevantFields.forEach((field) => {
		if (field.fieldname === "amended_from") {
			return;
		}
		if (field.fieldtype === "Section Break") {
			if (currentSection) {
				sections.push(currentSection);
			}
			currentSection = {
				label: field.label,
				fields: [],
				is_matrix: field.is_matrix,
				depends_on: field.depends_on,
				description: field.description,
				is_multi_matrix: field.is_multi_matrix,
				is_matrix_code: field.is_matrix_code,
				table_matrix: field.table_matrix,
			};
		} else if (currentSection) {
			// if (allTabsUnlocked.value && activeTab.value === tabFields.value[0]?.name) {
			//  currentSection.fields.push({ ...field, read_only: 1 })
			//} else {
			currentSection.fields.push(field);
			//}
		}
	});

	if (currentSection) {
		sections.push(currentSection);
	}
	return sections;
});
const allSections = computed(() => {
	if (!docTypeMeta.value) return [];
	let qno = 0;
	const sections = [];
	let currentSection = null;
	let mismatchedDependsOn = [];
	let mislineousDependsOn = [];
	docTypeMeta.value.fields.forEach((field) => {
		if (field.fieldname === "amended_from") {
			return;
		}
		if (field.fieldtype === "Tab Break") {
			return;
		}
		if (field.fieldtype === "Section Break") {
			if (currentSection) {
				sections.push(currentSection);
			}
			currentSection = {
				label: field.label,
				fields: [],
				is_matrix: field.is_matrix,
				description: field.description,
			};
		} else if (currentSection) {
			if (field.depends_on) {
				if (field.mandatory_depends_on && field.mandatory_depends_on != field.depends_on) {
					mismatchedDependsOn.push(field.label);
				}
				if (field.reqd && (field.depends_on || field.hidden)) {
					mislineousDependsOn.push(field.label);
				}
			}
			field["qno"] = qno;
			qno++;
			currentSection.fields.push(field);
		}
	});
	console.log(mismatchedDependsOn, "mismatchedDependsOn");
	console.log(mislineousDependsOn, "mislineousDependsOn");

	if (currentSection) {
		sections.push(currentSection);
	}

	return sections;
});

const isLastTab = computed(() => {
	const currentTabIndex = tabFields.value.findIndex((tab) => tab.name === activeTab.value);
	return currentTabIndex === tabFields.value.length - 1;
});

const isFirstTab = computed(() => {
	return activeTab.value === tabFields.value[0]?.name;
});

const isCurrentTabValid = computed(() => {
	const currentTabFields = getTabFields(activeTab.value);
	if (activeTab.value == 'nl44l3lvff' && calculatedFieldErrors.value.isValue) {
		return false;
	}
	return currentTabFields
		.filter((f) => !["Section Break", "Column Break"].includes(f.fieldtype))
		.every((field) => {
			const value = formData.value[field.fieldname];
			return (
				!isFieldMandatory(field) ||
				(value != null &&
					value != undefined &&
					value != "" &&
					(!Array.isArray(value) || value.length > 0))
			);
		});
});

const isSubmitDisabled = computed(() => {
	return !Object.entries(formData.value).some(([key, value]) => {
		const field = docTypeMeta.value?.fields.find((f) => f.fieldname === key);
		return (
			field && value !== null && value !== "" && (!Array.isArray(value) || value.length > 0)
		);
	});
});

const getFieldComponent = (fieldtype, section) => {
	switch (fieldtype) {
		case "Link":
			return props.isTable ? LinkTable : props.isColumn ? LinkPW : Link;
		case "Data":
			return Input;
		case "Table MultiSelect":
			return props.isCard
				? CheckBoxPW
				: section.is_multi_matrix
					? MultiSelectMatrix
					: CheckBox;
		case "Button":
			return Button;
		case "Attach":
			return AttachmentUpload;
		case "Date":
			return DateInput;
		case "Small Text":
			return Textarea;
		case "Check":
			return CheckboxComponent;
		case "Int":
			return Input;
		case "Percent":
			return percent;
		default:
			return "div";
	}
};

const isFieldVisible = (field) => {
	if (!field.depends_on) return true;
	const condition = field.depends_on.replace("eval:", "").replace(/doc\./g, "formData.");
	try {
		let status = new Function("formData", `return ${condition}`)(formData.value);
		if (
			!status &&
			(Array.isArray(formData.value[field.fieldname])
				? formData.value[field.fieldname].length > 0
				: formData.value[field.fieldname])
		) {
			saveAsDraft({
				[field.fieldname]: Array.isArray(formData.value[field.fieldname]) ? [] : "",
			});
			handleFieldUpdate(
				field.fieldname,
				Array.isArray(formData.value[field.fieldname]) ? [] : ""
			);
		}
		return status;
		// return new Function('formData', `return ${condition}`)(formData.value)
	} catch (error) {
		console.error("Error evaluating field visibility:", error);
		return false;
	}
};
const isFieldMandatory = (field) => {
	if (field.reqd) return true;
	if (!field.mandatory_depends_on) return false;
	const condition = field.mandatory_depends_on
		.replace("eval:", "")
		.replace(/doc\./g, "formData.");
	try {
		return new Function("formData", `return ${condition}`)(formData.value);
	} catch (error) {
		console.error("Error evaluating field mandatory condition:", error);
		return false;
	}
};
const isTabComplete = (tabName) => {
	const tabFields = getTabFields(tabName);
	if (tabName == 'nl44l3lvff' && calculatedFieldErrors.value.isValue) {
		return false;
	}
	return tabFields
		.filter((f) => !["Section Break", "Column Break"].includes(f.fieldtype))
		.every((field) => {
			const value = formData.value[field.fieldname];
			return (
				!isFieldMandatory(field) ||
				(value !== null &&
					value !== undefined &&
					value !== "" &&
					(!Array.isArray(value) || value.length > 0))
			);
		});
};

const getTabFields = (tabName) => {
	if (!docTypeMeta.value) return [];
	const fields = docTypeMeta.value.fields;
	const startIndex = fields.findIndex((f) => f.name === tabName);
	const endIndex = fields.findIndex((f, i) => i > startIndex && f.fieldtype === "Tab Break");
	return fields.slice(startIndex + 1, endIndex === -1 ? undefined : endIndex);
};

const handleFieldUpdate = (fieldName, value) => {
	let field = docTypeMeta.value.fields.find((f) => f.fieldname === fieldName);

	formData.value[fieldName] = value;
	if (showErrors.value) {
		validateField(fieldName);
	}
	// auto calculate
	if (["Int", "Percent", "Float"].includes(field.fieldtype)) {
		let auto_cal_field = docTypeMeta.value.fields.filter(
			(e) => "auto_calculate" in e && e.auto_calculate.includes(fieldName)
		);
		auto_cal_field.forEach(async (fieldMeta) => {
			let formula = fieldMeta.auto_calculate.match(/eval:\(([^)]+)\)/)?.[1];
			let evaluatedFormula = formula.replace(/\b\w+\b/g, (match) => {
				return formData.value[match] || 0;
			});

			let sum;
			try {
				sum = eval(evaluatedFormula);
			} catch (error) {
				sum = 0;
				console.error("Error evaluating formula:", formula, error);
			}

			formData.value[fieldMeta.fieldname] = sum;
			if (sum <= (minMaxValue.value?.max || 10000000000000) && sum >= (minMaxValue.value?.min || 0)) {
				// saveAsDraft({ [fieldMeta.fieldname]: sum });
				calculatedFieldErrors.value['calculated_value'] = "";
				calculatedFieldErrors.value['isValue'] = false;
			} else {
				calculatedFieldErrors.value['isValue'] = true;
				calculatedFieldErrors.value['calculated_value'] = `Sum of all options must be 100% Otherwise the value will not be accepted.`;
				// props.toast.error(
				//  `The last input will not be accepted if the total of all options exceeds 100%.`,
				//  {
				//      timeout: 5000,
				//      closeOnClick: true,
				//  }
				// );
			}
			console.log(isCurrentTabValid.value, "isCurrentTabValid");
			saveAsDraft({ [fieldMeta.fieldname]: sum });
		});
	}
};

const getMinMaxValue = async () => {
	const response = await call("sva_form_vuejs.controllers.api.get_min_max_criteria", {
		filters: { field: 'calculated_value' },
	});
	if (response) {
		minMaxValue.value = response;
	}
}

const validateField = async (fieldName) => {
	const field = docTypeMeta.value.fields.find((f) => f.fieldname === fieldName);
	if (!field) return;
	if (isFieldMandatory(field) && (!formData.value[fieldName] || formData.value[fieldName] === "" || (Array.isArray(formData.value[fieldName]) && formData.value[fieldName].length == 0))) {
		fieldErrors.value[fieldName] = "This field is required";
	}
	else {
		delete fieldErrors.value[fieldName];
	}
	// await handleFieldUpdate(fieldName, formData.value[fieldName]);

	updateTabErrors();
};

const updateTabErrors = () => {
	tabErrors.value = {};
	tabFields.value.forEach((tab) => {
		const tabFieldNames = getTabFields(tab.name).map((f) => f.fieldname);
		if (tabFieldNames.some((fieldName) => fieldErrors.value[fieldName])) {
			tabErrors.value[tab.name] = true;
		} else {
			delete tabErrors.value[tab.name]
		}
	});
};

const getMeta = async () => {
	loading.value = true;
	isLoading.value = true;
	try {
		const res = await call("sva_form_vuejs.controllers.api.get_meta", {
			doctype: props.doctype,
		});
		if (res) {
			docTypeMeta.value = res;
			activeTab.value = tabFields.value[0]?.name || "82am78mpee";
			openSections.value = new Array(allSections.value.length).fill(true);
			initializeFormData();
			initializeTabCompletionStatus();
		} else {
			console.error("Error fetching meta data: No document found");
		}
	} catch (error) {
		console.error("Error fetching meta data:", error);
	} finally {
		loading.value = false;
		isLoading.value = false;
	}
};

const initializeFormData = () => {
	if (!docTypeMeta.value) return;
	const newFormData = { ...formData.value };
	if (formData.value?.active_tab) {
		const firstTab = tabFields.value[0]?.name;
		if (isTabComplete(firstTab) && !allTabsUnlocked.value) {
			allTabsUnlocked.value = true;
			setActiveTab(formData.value?.active_tab, true);
		}
	}
	docTypeMeta.value.fields.forEach((field) => {
		if (!(field.fieldname in newFormData)) {
			if (field.fieldtype === "Table MultiSelect") {
				newFormData[field.fieldname] = [];
			} else {
				newFormData[field.fieldname] = field.fieldtype === "Data" ? "" : null;
			}
		}
	});
	formData.value = newFormData;
};

const initializeTabCompletionStatus = () => {
	tabFields.value.forEach((tab) => {
		tabCompletionStatus.value[tab.name] = false;
	});
};

const setActiveTab = async (tabName, fromMounted = false) => {
	if (!fromMounted) {
		isLoading.value = true;
		try {
			await props.save_as_draft({ active_tab: tabName });
			if (
				allTabsUnlocked.value ||
				tabFields.value.indexOf(tabFields.value.find((tab) => tab.name === tabName)) === 0
			) {
				activeTab.value = tabName;
			}
			await fetchTabData(tabName);
			// window.scrollTo({
			// 	top: 0,
			// 	behavior: "smooth",
			// });
		} finally {
			isLoading.value = false;
		}
	} else {
		if (
			allTabsUnlocked.value ||
			tabFields.value.indexOf(tabFields.value.find((tab) => tab.name === tabName)) === 0
		) {
			activeTab.value = tabName;
		}
	}
};

const nextTab = async () => {
	if (isCurrentTabValid.value) {
		isLoading.value = true;
		try {
			const currentIndex = tabFields.value.findIndex((tab) => tab.name === activeTab.value);
			if (currentIndex === 0 && !allTabsUnlocked.value) {
				allTabsUnlocked.value = true;
			}

			tabCompletionStatus.value[activeTab.value] = true;

			if (currentIndex < tabFields.value.length - 1) {
				const nextTabName = tabFields.value[currentIndex + 1].name;
				await setActiveTab(nextTabName);
				window.scrollTo({
					top: 0,
					behavior: "smooth",
				});
			}
		} finally {
			isLoading.value = false;
		}
	} else {
		validateCurrentTab();
	}
};

const fetchTabData = async (tabName) => {
	await new Promise((resolve) => setTimeout(resolve, 1000));
	console.log(`Fetched data for tab: ${tabName}`);
};

const toggleSection = (index) => {
	openSections.value[index] = !openSections.value[index];
};

const onSubmit = () => {
	showErrors.value = true;
	validateAllFields();
	const { isValid, firstErrorTab, sectionsWithErrors } = validateForm();
	if (calculatedFieldErrors.value.isValue) {
		setActiveTab('nl44l3lvff');
		props.toast.error(
			`Sum of all options must be 100% Otherwise the value will not be accepted.`,
			{
				timeout: 5000,
				closeOnClick: true,
			}
		);
		const firstErrorField = document.querySelector(".text-red-500");
		if (firstErrorField) {
			firstErrorField.scrollIntoView({ behavior: "smooth", block: "end" });
		}

		return
	}
	if (!isValid) {
		if (firstErrorTab) {
			setActiveTab(firstErrorTab);
		}
		const errorMessage = `Please complete all mandatory questions before proceeding. Ensure no required fields are left blank.`;
		props.toast.error(errorMessage, {
			timeout: 5000,
			closeOnClick: true,
		});
		const firstErrorField = document.querySelector(".border-red-500");
		if (firstErrorField) {
			firstErrorField.scrollIntoView({ behavior: "smooth", block: "center" });
		}
	} else {
		props.onSubmit(formData.value);
	}
};

const validateForm = () => {
	const sectionsWithErrors = new Set();
	let firstErrorTab = null;

	docTypeMeta.value.fields.forEach((field) => {
		if (
			isFieldMandatory(field) &&
			(!formData.value[field.fieldname] || formData.value[field.fieldname] === "" || (Array.isArray(formData.value[field.fieldname]) && formData.value[field.fieldname].length == 0))
		) {
			const section = allSections.value.find((s) =>
				s.fields.some((f) => f.fieldname === field.fieldname)
			);
			if (section) {
				sectionsWithErrors.add(section.label);
			}
			if (!firstErrorTab) {
				firstErrorTab = tabFields.value.find(
					(tab) =>
						tab.name === field.parent ||
						(field.idx > tab.idx &&
							field.idx <
							(tabFields.value[tabFields.value.indexOf(tab) + 1]?.idx ||
								Infinity))
				)?.name;
			}
		}
	});

	return { isValid: sectionsWithErrors.size === 0, firstErrorTab, sectionsWithErrors };
};

const validateAllFields = () => {
	docTypeMeta?.value?.fields?.forEach((field) => {
		validateField(field.fieldname);
	});
};

provide("saveAsDraft", props.save_as_draft);

onMounted(async () => {
	getMeta();
	if (Object.keys(props.initialData).length > 0) {
		formData.value = { ...props.initialData };
	}
	await getMinMaxValue();
	if (formData.value['calculated_value'] <= (minMaxValue.value?.max || 10000000000000) && formData.value['calculated_value'] >= (minMaxValue.value?.min || 0)) {
		calculatedFieldErrors.value['calculated_value'] = "";
		calculatedFieldErrors.value['isValue'] = false;
	}
	else {
		calculatedFieldErrors.value['isValue'] = true;
		calculatedFieldErrors.value['calculated_value'] = `Sum of all options must be 100% Otherwise the value will not be accepted.`;
	}
});
const toggleSidebar = () => {
	isSidebarOpen.value = !isSidebarOpen.value;
};
watch(
	() => props.initialData,
	(newVal) => {
		formData.value = { ...newVal };
		initializeFormData();
		validateAllFields();
	},
	{ deep: true, immediate: true }
);

watch(
	formData,
	() => {
		if (showErrors.value) {
			validateAllFields();
		}
	},
	{ deep: true }
);
</script>

<style scoped>
.w-20 {
	width: 240px !important;
	min-width: 240px !important;
	/* padding-top: 64px !important; */
}

.w-75 {
	width: 75% !important;
	/* padding-left: 240px !important; */
	min-width: 75% !important;
}

.custom {
	color: #0e4688 !important;
	margin-top: -15px !important;
}

.ml-5 {
	margin-left: 1.25rem !important;
	color: #0e4688 !important;
}

.abc {
	background-color: #efefef !important;
	color: rgb(119, 119, 119) !important;
}

aside {
	position: sticky;
	top: 2px;
	height: 100vh;
}

.side-bar-scroll {
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

.abcd {
	overflow-x: scroll !important;
	/* Hide horizontal scrollbar */
}

.w-96 {
	min-width: 400px !important;
}

@media screen and (max-width: 768px) {
	aside {
		position: fixed;
		top: 0;
		height: 100vh;
	}

	.hide-sidebar {
		transform: translateX(-100%) !important;
		transition: transform 0.3s ease !important;
		z-index: 1000 !important;
	}

	.show-sidebar {
		transform: translateX(0) !important;
		z-index: 1000 !important;
		transition: transform 0.3s ease !important;
	}

	.w-75 {
		padding-left: 0px !important;
		overflow-x: auto !important;
	}

	.top-11 {
		top: 60px !important;
	}

	.w-20 {
		padding-top: 64px !important;
	}

	.matrix-overflow1 {
		overflow-x: scroll !important;
	}
}

.cust {
	margin-left: 20px !important;
}

.bg {
	background: red;
}

.matrix-overflow {
	overflow-x: scroll !important;
	overflow-y: hidden !important;
}

.padding {
	padding-top: 30px !important;
	padding-bottom: 4px !important;
}

.matrix-overflow1 {
	overflow-x: auto !important;
	overflow-y: hidden;
}
</style>
