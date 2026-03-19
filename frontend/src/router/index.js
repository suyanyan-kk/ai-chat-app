import { createRouter, createWebHistory } from 'vue-router'

// 页面
import Home from '../views/home/index.vue'
import About from '../views/about/index.vue'
import NotFound from '../views/NotFound.vue'

// 子页面
import Chat from '../views/chat/chatMain.vue'
import LangchainPractice from '../views/test/langchainPractice.vue'

// ⭐ 新增：布局组件（关键）
import QaContent from '../views/chat/index.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { title: '首页' }
  },

  // ⭐ 问答模块（带二级路由）
  {
    path: '/qa',
    component: QaContent,
    meta: { title: '问答' },
    children: [
      {
        path: 'chat',
        name: 'chat',
        component: Chat,
        meta: { title: '对话' }
      }
    ]
  },
  {
    path: '/langchain',
    name: 'langchainPractice',
    component: LangchainPractice,
    meta: { title: 'LangChain' }
  },
  {
    path: '/about',
    name: 'about',
    component: About,
    meta: { title: '关于' }
  },

  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router