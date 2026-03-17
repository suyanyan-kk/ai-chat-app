// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import chat from '../views/chat.vue'
import about from '../views/about.vue'
import NotFound from '../views/NotFound.vue'  // 导入404组件
const routes = [
  {
    path: '/',
    name: 'chat',
    component: chat
  },
  {
    path: '/about',
    name: 'about',
    component: about
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