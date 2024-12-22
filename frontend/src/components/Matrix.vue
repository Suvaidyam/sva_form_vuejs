<template>
	<div class="">
		<div class="inline-block min-w-full p-2 align-middle">
			<div class="overflow-hidden rounded-lg">
				<div class="grid gap-x-4" :style="gridTemplateColumns">
					<template v-if="index < 1">
						<div
							class="bg-gray-50 dark:bg-gray-800 p-3 text-gray-900 dark:text-gray-100 font-medium"
						>
							{{ fieldParsedDescription.qlable || "Question" }}
						</div>
						<div
							v-for="option in visibleOptions"
							:key="`header-${option.name}`"
							class="bg-gray-50 dark:bg-gray-800 py-3 text-gray-900 dark:text-gray-100 font-medium"
							:class="{ 'text-left': matrix_code, 'text-center': !matrix_code }"
						>
							{{ matrix_code ? option.level : option.label }}
						</div>
					</template>

					<div
						class="bg-white  py-1 px-3 flex items-start border-t border-gray-200 dark:border-gray-700 min-h-[80px]"
					>
						<div class="w-full pr-6">
							<div class="flex items-start justify-between">
								<label
									:for="`${field.name}-${visibleOptions[0]?.name}`"
									class="flex items-start"
								>
									<span
										class="mr-2 text-[15px]  block"
									>
										{{ field.label }}
										<span v-if="isFieldMandatory" class="text-red-500">*</span>
									</span>
								</label>
								<Popover
									v-if="fieldParsedDescription.info"
									v-slot="{ open }"
									class="relative"
								>
									<PopoverButton class="focus:outline-none">
										<InfoIcon
											class="w-5 h-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
										/>
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
											<div
												class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5"
											>
												<div class="p-4 bg-white dark:bg-gray-800">
													<p
														class="text-sm text-gray-700 dark:text-gray-300"
													>
														{{ fieldParsedDescription.info }}
													</p>
												</div>
											</div>
										</PopoverPanel>
									</transition>
								</Popover>
							</div>
							<p
								v-if="fieldParsedDescription.desc"
								class="text-sm text-gray-600 dark:text-gray-400 mt-1"
							>
								{{ fieldParsedDescription.desc }}
							</p>
						</div>
					</div>

					<template v-for="option in visibleOptions" :key="`radio-${option.name}`">
						<div
							v-if="matrix_code"
							class="bg-white dark:bg-gray-900 py-2 border-t border-l border-gray-200 dark:border-gray-700 min-h-[80px]"
						>
							<div class="flex flex-col space-y-2">
								<div class="flex items-center">
									<input
										:id="`${field.name}-${option.name}`"
										:name="field.name"
										type="radio"
										:value="option.name"
										:checked="modelValue === option.name"
										@change="updateValue(option.name)"
										:disabled="field.read_only"
										:required="isFieldMandatory"
										class="h-4 w-4 text-primary border-gray-300 focus:ring-primary dark:border-gray-600 dark:focus:ring-primary"
									/>
									<label
										:for="`${field.name}-${option.name}`"
										class="ml-2 text-[15px]"
									>
										{{ option.label }}
									</label>
								</div>
							</div>
						</div>
						<div
							v-else
							class="bg-white dark:bg-gray-900 py-2 flex justify-center items-center border-t border-l border-gray-200 dark:border-gray-700 min-h-[80px]"
						>
							<input
								:id="`${field.name}-${option.name}`"
								:name="field.name"
								type="radio"
								:value="option.name"
								:checked="modelValue === option.name"
								@change="updateValue(option.name)"
								:disabled="field.read_only"
								:required="isFieldMandatory"
								class="h-4 w-4 text-primary border-gray-300 focus:ring-primary dark:border-gray-600 dark:focus:ring-primary"
							/>
						</div>
					</template>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue";
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import { InfoIcon } from "lucide-vue-next";

const props = defineProps({
	field: {
		type: Object,
		required: true,
	},
	modelValue: {
		type: String,
		required: false,
		default: "",
	},
	visibleOptions: {
		type: Array,
		required: true,
	},
	isFieldMandatory: {
		type: Boolean,
		required: true,
	},
	index: {
		type: Number,
		required: false,
		default: 0,
	},
	matrix_code: {
		type: Boolean,
		required: false,
	},
});

const emit = defineEmits(["update:modelValue"]);

const gridTemplateColumns = computed(() => {
	const optionCount = props.visibleOptions.length;
	return `grid-template-columns: minmax(500px, 1fr) repeat(${optionCount}, minmax(${
		props.matrix_code ? "100px" : "150px"
	}, 1fr))`;
});

const updateValue = (value) => {
	emit("update:modelValue", value);
};

const fieldParsedDescription = computed(() => {
	return getString(props.field.description || "");
});

function getString(str) {
	let desc = "";
	let info = "";
	let qlable = "";
	let cenrieo = "";

	const match = str.match(/\{([^}]+)\}/);
	if (match) {
		info = match[1];
		str = str.replace(match[0], "").trim();
	}

	const cenrieoSplit = str.split("@@");
	if (cenrieoSplit.length > 1) {
		cenrieo = cenrieoSplit[1].trim();
		str = cenrieoSplit[0].trim();
	}

	const parts = str.split("$$");
	if (parts.length > 1) {
		qlable = parts[1].trim();
		str = parts[0].trim();
	}

	desc = str.trim();

	return { desc, info, qlable, cenrieo };
}
</script>
