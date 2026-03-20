<template>
  <div class="layout">
    <!-- 一级菜单 -->
    <aside :class="['sidebar']">
      <div class="logo-box" @click="goHome">
        <img class="logo" src="@/assets/logo.jpg" />
      </div>
      <nav class="menu">
        <template v-for="route in rootRoutes" :key="route.path">
          <!-- ✅ 没有子路由（一级） -->
          <router-link
            v-if="!route.children"
            :to="route.path"
            class="menu-item"
            active-class="active"
          >
            {{ route.meta.title }}
          </router-link>

          <!-- ✅ 有子路由（二级） -->
          <div v-else :class="['menu-group', { active: isActiveGroup(route) }]">
            <div class="menu-group-title">
              {{ route.meta.title }}
            </div>
            <router-link
              v-for="child in route.children"
              :key="child.path"
              :to="route.path + '/' + child.path"
              class="menu-item"
              active-class="active"
            >
              {{ child.meta.title }}
            </router-link>
          </div>
        </template>
      </nav>
    </aside>
    <!-- 主体 -->
    <div class="main">
      <header class="topbar">
        <div class="topbar-title">
          <span v-for="(item, index) in titleList" :key="index">
            {{ item }}
            <span v-if="index < titleList.length - 1"> / </span>
          </span>
        </div>
      </header>

      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

// ⭐ 只取一级路由（关键！！）
const rootRoutes = computed(() => router.options.routes.filter((r) => r.meta?.title));

const titleList = computed(() =>
  route.matched.filter((r) => r.meta?.title).map((r) => r.meta.title)
);
const isActiveGroup = (parentRoute) => {
  return route.matched.some((r) => r.path === parentRoute.path);
};
const goHome = () => {
  router.push('/')
}
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
.logo {
  width: 150px;
  height: 75px;
  padding: 6px;
  box-sizing: border-box;
  border-radius: 50px;
  object-fit: cover;
  transition: all 0.2s ease;
  cursor: pointer;
}

.logo-box:hover .logo {
  transform: scale(1.1) translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.menu-group .menu-item {
  padding-left: 24px;
  font-size: 0.95rem;
}
.menu-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.menu-group-title {
  font-size: 0.8rem;
  opacity: 0.5;
  padding: 6px 12px;
  margin-top: 8px;
}
.menu-item {
  padding: 12px 14px;
  border-radius: 12px;
  color: rgba(235, 240, 255, 0.78);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.18s ease;
}
.menu-group .menu-item::before {
  content: "•";
  margin-right: 6px;
  opacity: 0.4;
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
.menu-group.active .menu-group-title {
  color: #fff;
  opacity: 1;
}

.menu-group.active {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
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

.topbar-title {
  font-weight: 600;
  font-size: 1.05rem;
  margin-left: 14px;
}

.content {
  flex: 1;
  box-sizing: border-box;
  overflow: hidden; /* 这里禁止浏览器滚动 */
  width: 100%;
  margin: 0 auto;
}
.topbar-title span {
  opacity: 0.7;
}

.topbar-title span:last-child {
  opacity: 1;
  font-weight: 600;
}
</style>
