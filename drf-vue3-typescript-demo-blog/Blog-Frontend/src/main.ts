import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import { StateKey, store } from "./store";
// import 'element-plus/lib/theme-chalk/index.css';
import 'element-plus/theme-chalk/base.css';
import 'element-plus/dist/index.css';


// @ts-ignore
import VMdEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
// @ts-ignore
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';

// highlightjs
import hljs from 'highlight.js';

VMdEditor.use(githubTheme, {
    Hljs: hljs,
});
import {
    ElAffix,
    ElButton,
    ElCard,
    ElCascader,
    ElCol,
    ElDescriptions,
    ElDescriptionsItem,
    ElDialog,
    ElDrawer,
    ElDropdown,
    ElDropdownItem,
    ElDropdownMenu,
    ElForm,
    ElFormItem,
    ElIcon,
    ElInput,
    ElLoading,
    ElMenu,
    ElMenuItem,
    ElMessage,
    ElMessageBox,
    ElOption,
    ElPagination,
    ElPopconfirm,
    ElProgress,
    ElRow,
    ElSelect,
    ElTable,
    ElTableColumn,
    ElTag,
    ElTimeline,
    ElTimelineItem,
    ElTooltip,
    ElTree,
    ElUpload,
} from 'element-plus';

const app = createApp(App)


const components = [
    ElAffix,
    ElButton,
    ElCard,
    ElCascader,
    ElCol,
    ElDescriptions,
    ElDescriptionsItem,
    ElDialog,
    ElDrawer,
    ElDropdown,
    ElDropdownItem,
    ElDropdownMenu,
    ElForm,
    ElFormItem,
    ElIcon,
    ElInput,
    ElLoading,
    ElMenu,
    ElMenuItem,
    ElMessage,
    ElMessageBox,
    ElOption,
    ElPagination,
    ElPopconfirm,
    ElProgress,
    ElRow,
    ElSelect,
    ElTable,
    ElTableColumn,
    ElTag,
    ElTimeline,
    ElTimelineItem,
    ElTooltip,
    ElTree,
    ElUpload,
]

const plugins = [
    ElLoading,
    ElMessage,
    ElMessageBox,
]

components.forEach(component => {
    app.component(component.name, component)
})

plugins.forEach(plugin => {
    app.use(plugin)
})

app.use(router).use(store, StateKey).use(VMdEditor).mount('#app')