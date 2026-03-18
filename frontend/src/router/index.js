// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import chat from '../views/chat.vue'
import langchainPractice  from '../views/langchainPractice.vue'
import about from '../views/about.vue'

import NotFound from '../views/NotFound.vue'  // 导入404组件
const routes = [
  {
    path: '/',
    name: 'chat',
    component: chat,
    meta: {
      title: '首页'
    }
  },
   {
    path: '/langchainPractice',
    name: 'langchainPractice',
    component: langchainPractice,
    meta: {
      title: '练习LangChain'
    }
  },
  {
    path: '/about',
    name: 'about',
    component: about,
    meta: {
      title: '关于'
    }
  },
  {
    path: '/:pathMatch(.*)*',  // 添加404路由，必须放在最后
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router