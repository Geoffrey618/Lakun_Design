import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus';
import 'element-plus/theme-chalk/index.css';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios'; // 导入axios

library.add(faThumbsUp);

const app = createApp(App);

// 全局注册 FontAwesome 图标组件
app.component('font-awesome-icon', FontAwesomeIcon);
app.use(ElementPlus);
app.use(router);
app.use(store);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 配置axios，并绑定到Vue实例
app.config.globalProperties.$axios = axios;

app.mount('#app');
