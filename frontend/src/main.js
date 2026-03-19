import { createApp } from 'vue'
import "@/styles/index.css"
import "github-markdown-css/github-markdown.css"
import App from './App.vue'
import router from './router'  
import naive from 'naive-ui'
import { createPinia } from 'pinia'
const pinia = createPinia()
createApp(App).use(router).use(pinia).use(naive).mount('#app')  
