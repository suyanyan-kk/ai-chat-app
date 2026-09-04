<template>
  <n-message-provider>
  <router-view v-if="isPublicRoute" />
  <div
    v-else
    :class="['layout', { 'layout--leaving': isLoggingOut }]"
  >
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

        <div class="account">
          <div class="account-copy">
            <strong>{{ authStore.user?.display_name }}</strong>
            <span>{{ authStore.user?.email }}</span>
          </div>

          <button
            class="logout-button"
            type="button"
            :disabled="isLoggingOut"
            :aria-label="isLoggingOut ? '正在退出登录' : '退出登录'"
            @click="handleLogout"
          >
            <span class="logout-button__icon" aria-hidden="true">
              <n-icon :component="LogOutOutline" />
            </span>
            <span class="logout-button__label">
              {{ isLoggingOut ? "退出中" : "退出" }}
            </span>
          </button>
        </div>
      </header>

      <main
        :class="[
          'content',
          { 'content--scrollable': route.meta.scrollPage }
        ]"
      >
        <router-view />
      </main>
      <IcpFooter class="layout-icp-footer" />
    </div>

    <Transition name="logout-screen">
      <div
        v-if="isLoggingOut"
        class="logout-screen"
        role="status"
        aria-live="polite"
      >
        <div class="logout-screen__glow"></div>
        <div class="logout-screen__content">
          <span class="logout-screen__mark">
            <n-icon :component="LogOutOutline" />
          </span>
          <strong>正在安全退出</strong>
          <span>稍后见</span>
        </div>
      </div>
    </Transition>
  </div>
  </n-message-provider>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { LogOutOutline } from "@vicons/ionicons5";

import IcpFooter from "@/components/common/IcpFooter.vue";
import { useAuthStore } from "@/stores/modules/authStore";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const isLoggingOut = ref(false);
const isPublicRoute = computed(
  () => Boolean(route.meta.public)
);

// ⭐ 只取一级路由（关键！！）
const rootRoutes = computed(() =>
  router.options.routes.filter(
    (r) => r.meta?.title && !r.meta?.hideInNav
  )
);

const titleList = computed(() =>
  route.matched.filter((r) => r.meta?.title).map((r) => r.meta.title)
);
const isActiveGroup = (parentRoute) => {
  return route.matched.some((r) => r.path === parentRoute.path);
};
const goHome = () => {
  router.push('/')
}

const handleLogout = async () => {
  if (isLoggingOut.value) return;

  isLoggingOut.value = true;

  const transitionDelay = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches ? 80 : 620;

  try {
    await Promise.allSettled([
      authStore.logout(),
      new Promise((resolve) => window.setTimeout(resolve, transitionDelay)),
    ]);

    await router.replace("/login");
  } finally {
    // App.vue 在登录页不会销毁，必须清理退出状态，避免下次登录重现遮罩。
    isLoggingOut.value = false;
  }
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

.layout::after {
  content: "";
  position: fixed;
  inset: 0;
  z-index: 90;
  pointer-events: none;
  background: rgba(4, 8, 20, 0.08);
  opacity: 0;
  backdrop-filter: blur(0);
  transition:
    opacity 0.46s ease,
    backdrop-filter 0.46s ease;
}

.layout--leaving::after {
  opacity: 1;
  backdrop-filter: blur(5px);
}

.layout--leaving .sidebar,
.layout--leaving .main {
  transform: scale(0.985);
  opacity: 0.42;
  filter: saturate(0.65);
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
  transform-origin: center left;
  transition:
    transform 0.46s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.38s ease,
    filter 0.38s ease;
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
  transform-origin: center right;
  transition:
    transform 0.46s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.38s ease,
    filter 0.38s ease;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.account {
  display: flex;
  align-items: center;
  gap: 12px;
}

.account-copy {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  line-height: 1.25;
}

.account-copy strong {
  font-size: 13px;
}

.account-copy span {
  color: rgba(238, 241, 255, 0.56);
  font-size: 11px;
}

.logout-button {
  --logout-accent: #7aa7ff;
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 36px;
  padding: 0 12px 0 10px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 999px;
  color: rgba(238, 241, 255, 0.72);
  background: rgba(255, 255, 255, 0.045);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
  font: inherit;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition:
    color 0.2s ease,
    border-color 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.logout-button::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    105deg,
    transparent 10%,
    rgba(93, 164, 255, 0.2),
    rgba(125, 119, 255, 0.16),
    transparent 90%
  );
  transform: translateX(-110%);
  transition: transform 0.42s cubic-bezier(0.22, 1, 0.36, 1);
}

.logout-button:hover:not(:disabled) {
  color: #f5f8ff;
  border-color: rgba(112, 169, 255, 0.42);
  background: linear-gradient(
    135deg,
    rgba(67, 145, 255, 0.17),
    rgba(111, 105, 255, 0.12)
  );
  box-shadow: 0 8px 24px rgba(37, 94, 194, 0.2);
  transform: translateY(-1px);
}

.logout-button:hover:not(:disabled)::before {
  transform: translateX(110%);
}

.logout-button:active:not(:disabled) {
  transform: translateY(0) scale(0.97);
}

.logout-button:focus-visible {
  outline: 2px solid var(--logout-accent);
  outline-offset: 3px;
}

.logout-button:disabled {
  cursor: wait;
  color: #fff;
  border-color: rgba(112, 169, 255, 0.3);
  background: linear-gradient(
    135deg,
    rgba(67, 145, 255, 0.14),
    rgba(111, 105, 255, 0.1)
  );
}

.logout-button__icon,
.logout-button__label {
  position: relative;
  z-index: 1;
}

.logout-button__icon {
  display: grid;
  place-items: center;
  color: var(--logout-accent);
  font-size: 17px;
  transition: transform 0.24s cubic-bezier(0.22, 1, 0.36, 1);
}

.logout-button:hover:not(:disabled) .logout-button__icon {
  transform: translateX(2px);
}

.logout-button:disabled .logout-button__icon {
  animation: logout-icon-pulse 0.72s ease-in-out infinite alternate;
}

.logout-screen {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: grid;
  place-items: center;
  overflow: hidden;
  background: rgba(5, 9, 22, 0.76);
  backdrop-filter: blur(18px);
}

.logout-screen__glow {
  position: absolute;
  width: min(58vw, 620px);
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(78, 131, 255, 0.16),
    transparent 68%
  );
  animation: logout-glow 1.6s ease-in-out infinite alternate;
}

.logout-screen__content {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #f5f7ff;
  animation: logout-content-in 0.48s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.logout-screen__content strong {
  margin-top: 7px;
  font-size: 17px;
  letter-spacing: 0.06em;
}

.logout-screen__content > span:last-child {
  color: rgba(238, 241, 255, 0.48);
  font-size: 12px;
  letter-spacing: 0.12em;
}

.logout-screen__mark {
  display: grid;
  width: 48px;
  height: 48px;
  place-items: center;
  border: 1px solid rgba(142, 174, 255, 0.28);
  border-radius: 16px;
  color: #a9c2ff;
  background: rgba(126, 161, 255, 0.08);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    0 16px 48px rgba(0, 0, 0, 0.28);
  font-size: 23px;
}

.logout-screen-enter-active {
  transition: opacity 0.42s ease;
}

.logout-screen-enter-from {
  opacity: 0;
}

@keyframes logout-icon-pulse {
  to {
    opacity: 0.45;
    transform: translateX(3px);
  }
}

@keyframes logout-content-in {
  from {
    opacity: 0;
    transform: translateY(12px) scale(0.96);
  }
}

@keyframes logout-glow {
  to {
    opacity: 0.65;
    transform: scale(1.08);
  }
}

@media (max-width: 720px) {
  .layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    padding: 8px 10px;
    flex-direction: row;
    align-items: center;
    gap: 10px;
    border-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    overflow-x: auto;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }

  .sidebar::-webkit-scrollbar {
    display: none;
  }

  .logo-box,
  .menu,
  .menu-group,
  .menu-item {
    flex-shrink: 0;
  }

  .logo {
    width: 68px;
    height: 36px;
    padding: 2px;
    border-radius: 8px;
  }

  .menu {
    flex-direction: row;
    gap: 4px;
  }

  .menu-group {
    flex-direction: row;
    align-items: center;
    gap: 4px;
  }

  .menu-group-title {
    display: none;
  }

  .menu-item,
  .menu-group .menu-item {
    padding: 8px 10px;
    font-size: 0.82rem;
    white-space: nowrap;
  }

  .menu-group .menu-item::before {
    display: none;
  }

  .main {
    width: 100%;
    min-height: 0;
  }

  .topbar {
    padding: 10px 14px;
  }

  .topbar-title {
    margin-left: 0;
    font-size: 0.95rem;
  }

  .account-copy {
    display: none;
  }

  .logout-button {
    width: 36px;
    padding: 0;
    justify-content: center;
  }

  .logout-button__label {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip-path: inset(50%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .layout::after,
  .layout .sidebar,
  .layout .main,
  .logout-button,
  .logout-button::before,
  .logout-button__icon,
  .logout-screen-enter-active {
    transition-duration: 0.01ms !important;
  }

  .logout-button__icon,
  .logout-screen__glow,
  .logout-screen__content {
    animation: none !important;
  }
}

.content {
  flex: 1;
  min-height: 0;
  box-sizing: border-box;
  overflow: hidden; /* 这里禁止浏览器滚动 */
  width: 100%;
  margin: 0 auto;
}

.content--scrollable {
  overflow-x: hidden;
  overflow-y: auto;
}

.layout-icp-footer {
  flex-shrink: 0;
}

.topbar-title span {
  opacity: 0.7;
}

.topbar-title span:last-child {
  opacity: 1;
  font-weight: 600;
}
</style>
