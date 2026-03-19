<template>
  <div class="qa-layout">
    <!-- ⭐ 左侧（二级菜单 + 会话） -->
    <aside class="sidebar">
      <!-- 二级菜单 -->
      <!-- <nav class="menu">
        <router-link
          v-for="child in childRoutes"
          :key="child.path"
          :to="`/qa/${child.path}`"
          class="menu-item"
          active-class="active"
        >
          {{ child.meta.title }}
        </router-link>
      </nav> -->

      <!-- ⭐ 会话列表 -->
      <ChatSidebar />
    </aside>

    <!-- 右侧内容 -->
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import ChatSidebar from "./ChatSidebar.vue";

const router = useRouter();

// ⭐ 拿到 /qa 下的 children
const qaRoute = router.options.routes.find(r => r.path === "/qa");

const childRoutes = computed(() =>
  qaRoute.children.filter(r => r.meta?.title)
);
</script>

<style scoped>
.qa-layout {
  display: flex;
  height: 100%;
}

/* ⭐ 复用你原来的 sidebar 风格 */
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: rgba(8, 12, 27, 0.92);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 16px;
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
}

/* 右侧内容 */
.content {
  flex: 1;
  overflow: hidden;
}
</style>