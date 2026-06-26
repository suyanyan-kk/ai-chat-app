import { createApp } from 'vue'
import "@/styles/index.css"
import "github-markdown-css/github-markdown.css"
import App from './App.vue'
import router from './router'  
import naive from 'naive-ui'
import pinia from './stores/pinia'

createApp(App)
  .use(pinia)
  .use(router)
  .use(naive)
  .mount('#app')
