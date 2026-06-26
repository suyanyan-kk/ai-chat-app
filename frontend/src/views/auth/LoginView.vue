<template>
  <main class="login-shell">
    <section class="identity-panel">
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
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(420px, 0.9fr);
  background: #0b0d0f;
  color: #f4f5f2;
}

.identity-panel {
  min-width: 0;
  padding: 48px 56px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  background: #101316;
}

.identity-logo {
  width: 146px;
  height: 72px;
  object-fit: cover;
  border-radius: 6px;
}

.identity-copy {
  max-width: 620px;
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
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #5fd08a;
  box-shadow: 0 0 0 4px rgba(95, 208, 138, 0.12);
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
}

@media (max-width: 860px) {
  .login-shell {
    grid-template-columns: 1fr;
    overflow-y: auto;
  }

  .identity-panel {
    min-height: 280px;
    padding: 28px 24px;
    border-right: 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .identity-copy h1 {
    font-size: 40px;
  }

  .login-panel {
    padding: 36px 24px 48px;
  }
}
</style>
