<template>
  <main class="login-shell">
    <section class="identity-panel">
      <div
        class="signal-field"
        aria-hidden="true"
      >
        <span class="signal-orbit signal-orbit--outer"></span>
        <span class="signal-orbit signal-orbit--inner"></span>
        <span class="signal-core"></span>
        <span class="signal-particle signal-particle--one"></span>
        <span class="signal-particle signal-particle--two"></span>
      </div>
      <span
        class="scan-line"
        aria-hidden="true"
      ></span>

      <img
        class="identity-logo"
        src="@/assets/logo.jpg"
        alt="SUSY"
      />

      <div class="identity-copy">
        <span class="system-label">AI KNOWLEDGE CONSOLE</span>
        <h1>欢迎回来</h1>
        <p>登录后进入你的 AI 工作台。</p>
      </div>

      <div class="system-status">
        <span class="status-dot" aria-hidden="true"></span>
        <span>系统已就绪</span>
      </div>
    </section>

    <section class="login-panel">
      <div class="login-form-wrap">
        <div class="login-heading">
          <span>SECURE ACCESS</span>
          <h2>账号登录</h2>
        </div>

        <n-form
          ref="formRef"
          :model="form"
          :rules="rules"
          size="large"
          @submit.prevent="handleLogin"
        >
          <n-form-item
            label="邮箱"
            path="email"
          >
            <n-input
              v-model:value="form.email"
              placeholder="admin@example.com"
              autocomplete="email"
              :disabled="authStore.loading"
            >
              <template #prefix>
                <n-icon :component="MailOutline" />
              </template>
            </n-input>
          </n-form-item>

          <n-form-item
            label="密码"
            path="password"
          >
            <n-input
              v-model:value="form.password"
              type="password"
              show-password-on="click"
              placeholder="8个8"
              autocomplete="current-password"
              :disabled="authStore.loading"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <n-icon :component="LockClosedOutline" />
              </template>
            </n-input>
          </n-form-item>

          <n-button
            attr-type="submit"
            type="primary"
            block
            :loading="authStore.loading"
            class="login-button"
          >
            登录
            <template #icon>
              <n-icon :component="ArrowForwardOutline" />
            </template>
          </n-button>
        </n-form>

        <p class="login-note">
          当前系统不开放自助注册，请使用管理员分配的账号。
        </p>
      </div>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import {
  ArrowForwardOutline,
  LockClosedOutline,
  MailOutline 
} from "@vicons/ionicons5"

import { useAuthStore } from "@/stores/modules/authStore"
import message from "@/utils/message"


const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const formRef = ref(null)

const form = reactive({
  email: "",
  password: ""
})

const rules = {
  email: [
    {
      required: true,
      message: "请输入邮箱",
      trigger: ["input", "blur"]
    },
    {
      type: "email",
      message: "邮箱格式不正确",
      trigger: ["input", "blur"]
    }
  ],
  password: [
    {
      required: true,
      message: "请输入密码",
      trigger: ["input", "blur"]
    },
    {
      min: 8,
      message: "密码至少需要 8 个字符",
      trigger: ["input", "blur"]
    }
  ]
}


const handleLogin = async () => {
  try {
    await formRef.value?.validate()
    await authStore.login(form)

    const redirect = typeof route.query.redirect === "string"
      ? route.query.redirect
      : "/"

    await router.replace(redirect)
  } catch (error) {
    if (Array.isArray(error)) return

    message.error(
      error.message || "登录失败"
    )
  }
}
</script>

<style scoped>
.login-shell {
  width: 100vw;
  height: 100vh;
  height: 100dvh;
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(420px, 0.9fr);
  background: #0b0d0f;
  color: #f4f5f2;
}

.identity-panel {
  position: relative;
  isolation: isolate;
  min-width: 0;
  overflow: hidden;
  padding: 48px 56px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  background:
    linear-gradient(rgba(139, 214, 167, 0.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 214, 167, 0.035) 1px, transparent 1px),
    #101316;
  background-size: 42px 42px;
}

.identity-panel::after {
  content: "";
  position: absolute;
  z-index: -2;
  width: 440px;
  height: 440px;
  right: -210px;
  bottom: -230px;
  border-radius: 50%;
  background: rgba(95, 208, 138, 0.11);
  filter: blur(70px);
  animation: ambient-drift 9s ease-in-out infinite alternate;
}

.signal-field {
  position: absolute;
  z-index: -1;
  width: clamp(230px, 32vw, 430px);
  aspect-ratio: 1;
  right: clamp(-130px, -8vw, -60px);
  top: 50%;
  transform: translateY(-48%);
  opacity: 0.68;
  pointer-events: none;
}

.signal-orbit,
.signal-core,
.signal-particle {
  position: absolute;
  left: 50%;
  top: 50%;
  border-radius: 50%;
}

.signal-orbit {
  border: 1px solid rgba(139, 214, 167, 0.22);
  transform: translate(-50%, -50%);
}

.signal-orbit--outer {
  width: 100%;
  height: 100%;
  border-style: dashed;
  animation: orbit-spin 26s linear infinite;
}

.signal-orbit--inner {
  width: 64%;
  height: 64%;
  box-shadow: 0 0 60px rgba(95, 208, 138, 0.07);
  animation: orbit-spin 18s linear infinite reverse;
}

.signal-core {
  width: 10px;
  height: 10px;
  background: #8bd6a7;
  box-shadow:
    0 0 0 12px rgba(139, 214, 167, 0.08),
    0 0 38px rgba(139, 214, 167, 0.5);
  transform: translate(-50%, -50%);
  animation: core-pulse 2.8s ease-in-out infinite;
}

.signal-particle {
  width: 6px;
  height: 6px;
  background: #8bd6a7;
  box-shadow: 0 0 14px rgba(139, 214, 167, 0.8);
}

.signal-particle--one {
  animation: particle-orbit 12s linear infinite;
}

.signal-particle--two {
  width: 4px;
  height: 4px;
  animation: particle-orbit 17s linear -6s infinite reverse;
}

.scan-line {
  position: absolute;
  z-index: -1;
  inset: 0 auto 0 -20%;
  width: 24%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(139, 214, 167, 0.045),
    transparent
  );
  transform: skewX(-12deg);
  animation: scan-across 8s ease-in-out infinite;
}

.identity-logo {
  width: 146px;
  height: 72px;
  object-fit: cover;
  border-radius: 6px;
  animation: reveal-up 0.65s ease-out both;
}

.identity-copy {
  max-width: 620px;
  animation: reveal-up 0.7s 0.12s ease-out both;
}

.system-label,
.login-heading span {
  display: block;
  margin-bottom: 18px;
  color: #8bd6a7;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 12px;
  letter-spacing: 0;
}

.identity-copy h1 {
  margin: 0;
  font-size: 56px;
  line-height: 1.05;
  letter-spacing: 0;
}

.identity-copy p {
  margin-top: 20px;
  color: rgba(244, 245, 242, 0.62);
  font-size: 18px;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(244, 245, 242, 0.58);
  font-size: 13px;
  animation: reveal-up 0.7s 0.24s ease-out both;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #5fd08a;
  box-shadow: 0 0 0 4px rgba(95, 208, 138, 0.12);
  animation: status-pulse 2.4s ease-in-out infinite;
}

.login-panel {
  min-width: 0;
  padding: 48px;
  display: grid;
  place-items: center;
  background: #e9ebe6;
  color: #171a18;
}

.login-form-wrap {
  width: min(100%, 410px);
  text-align: left;
  animation: form-arrive 0.72s 0.08s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.login-heading {
  margin-bottom: 38px;
}

.login-heading span {
  color: #357d50;
  margin-bottom: 12px;
}

.login-heading h2 {
  margin: 0;
  font-size: 34px;
  line-height: 1.2;
  letter-spacing: 0;
}

.login-button {
  height: 48px;
  margin-top: 8px;
  border-radius: 6px;
  background: #1f6d3d;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(31, 109, 61, 0.22);
}

.login-note {
  margin-top: 22px;
  color: #667068;
  font-size: 13px;
  line-height: 1.7;
}

:deep(.n-form-item-label) {
  color: #333936;
}

:deep(.n-input) {
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.72);
  text-align: left;
}

/* 覆盖 #app 的全局居中，确保输入内容、placeholder 和光标都从左侧开始。 */
:deep(.n-input__input-el) {
  text-align: left !important;
  caret-color: #1f6d3d;
}

@keyframes reveal-up {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes form-arrive {
  from {
    opacity: 0;
    transform: translateX(24px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes orbit-spin {
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

@keyframes particle-orbit {
  from {
    transform: translate(-50%, -50%) rotate(0deg) translateX(clamp(105px, 15vw, 195px)) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg) translateX(clamp(105px, 15vw, 195px)) rotate(-360deg);
  }
}

@keyframes core-pulse {
  50% {
    transform: translate(-50%, -50%) scale(1.18);
    opacity: 0.72;
  }
}

@keyframes scan-across {
  0%,
  18% {
    transform: translateX(0) skewX(-12deg);
    opacity: 0;
  }
  34% {
    opacity: 1;
  }
  62%,
  100% {
    transform: translateX(520%) skewX(-12deg);
    opacity: 0;
  }
}

@keyframes status-pulse {
  50% {
    box-shadow: 0 0 0 7px rgba(95, 208, 138, 0.06);
  }
}

@keyframes ambient-drift {
  to {
    transform: translate(-42px, -30px) scale(1.08);
  }
}

@media (max-width: 860px) {
  .login-shell {
    grid-template-columns: 1fr;
    grid-template-rows: minmax(220px, 36dvh) auto;
    overflow-y: auto;
  }

  .identity-panel {
    min-height: 220px;
    padding: 28px 24px;
    border-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .identity-copy h1 {
    font-size: clamp(36px, 9vw, 44px);
  }

  .login-panel {
    min-height: 460px;
    padding: 34px 24px max(40px, env(safe-area-inset-bottom));
    place-items: start center;
  }

  .signal-field {
    width: min(58vw, 280px);
    right: -72px;
    opacity: 0.48;
  }

  .login-heading {
    margin-bottom: 30px;
  }
}

@media (max-width: 480px) {
  .login-shell {
    grid-template-rows: minmax(205px, 32dvh) auto;
  }

  .identity-panel {
    padding: 22px 20px;
  }

  .identity-logo {
    width: 112px;
    height: 55px;
  }

  .identity-copy p {
    margin-top: 10px;
    font-size: 15px;
  }

  .system-label {
    margin-bottom: 10px;
    font-size: 10px;
  }

  .system-status {
    display: none;
  }

  .login-panel {
    min-height: 440px;
    padding: 28px 20px max(32px, env(safe-area-inset-bottom));
  }

  .login-heading h2 {
    font-size: 30px;
  }

  .login-note {
    font-size: 12px;
  }

  /* 避免 iOS/窄屏浏览器聚焦输入框时自动放大页面。 */
  :deep(.n-input__input-el) {
    font-size: 16px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .identity-logo,
  .identity-copy,
  .system-status,
  .login-form-wrap,
  .signal-orbit--outer,
  .signal-orbit--inner,
  .signal-core,
  .signal-particle,
  .scan-line,
  .status-dot,
  .identity-panel::after {
    animation: none;
  }

  .login-button {
    transition: none;
  }
}
</style>
