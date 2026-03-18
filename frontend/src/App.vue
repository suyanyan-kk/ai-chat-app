
<template>
  <div class="layout">
    <aside :class="['sidebar', { open: sidebarOpen }]">
      <div class="sidebar-header">
        <span class="brand">deepseek</span>
        <button class="close-btn" @click="toggleSidebar" aria-label="Close sidebar">
          ×
        </button>
      </div>

      <nav class="menu">
        <router-link
          v-for="route in navRoutes"
          :key="route.path"
          :to="route.path"
          class="menu-item"
          active-class="active"
          @click="closeSidebar"
        >
          {{ route.meta.title }}
        </router-link>
      </nav>
    </aside>

    <div class="main">
      <header class="topbar">
        <button class="hamburger" @click="toggleSidebar" aria-label="Toggle menu">
          <span />
          <span />
          <span />
        </button>
        <div class="topbar-title">
          {{ pageTitle }}
        </div>
      </header>

      <main class="content" @click="closeSidebar">
        <router-view />
      </main>
    </div>

    <div class="mask" v-if="sidebarOpen" @click="closeSidebar" />
  </div>
</template>
<script setup>
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const sidebarOpen = ref(false);

// 当前路由（用于标题）
const route = useRoute();

// ✅ 正确拿路由表
const router = useRouter();
const routes = router.options.routes;

// ✅ 过滤 + 排序（推荐写法）
const navRoutes = computed(() =>
  routes
    .filter(r => r.meta?.title && !r.meta?.hidden)
    .sort((a, b) => (a.meta?.order || 0) - (b.meta?.order || 0))
);

// ✅ 顶部标题（自动根据路由变化）
const pageTitle = computed(() => route.meta?.title || "默认标题");

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const closeSidebar = () => {
  sidebarOpen.value = false;
};
</script>
<style scoped>
.layout {
  height: 100vh;
  width: 100vw;
  display: flex;
  background: linear-gradient(135deg, #080c1b, #0f1f3f);
  color: #eef1ff;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: rgba(8, 12, 27, 0.92);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  padding: 28px 18px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  transition: transform 0.25s ease;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.brand {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #fff;
}

.close-btn {
  display: none;
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.85);
  font-size: 1.3rem;
  cursor: pointer;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.menu-item {
  padding: 12px 14px;
  border-radius: 12px;
  color: rgba(235, 240, 255, 0.78);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.18s ease;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.menu-item.active {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.12);
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.topbar {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(8, 12, 27, 0.55);
  backdrop-filter: blur(12px);
}

.hamburger {
  width: 44px;
  height: 44px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.06);
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.18s ease;
  position: relative;
}

.hamburger span {
  display: block;
  width: 20px;
  height: 2px;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 2px;
  transform-origin: center;
}

.hamburger span + span {
  margin-top: 6px;
}

.hamburger:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-1px);
}

.topbar-title {
  font-weight: 600;
  font-size: 1.05rem;
  margin-left: 14px;
}

.content {
  flex: 1;
  box-sizing: border-box;
  padding: 26px;
  overflow: hidden; /* 这里禁止浏览器滚动 */
  width: 100%;
  margin: 0 auto;
}

.mask {
  position: fixed;
  inset: 0;
  background: rgba(12, 15, 30, 0.65);
  z-index: 1;
  pointer-events: auto;
}
</style>
