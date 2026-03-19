<template>
  <div class="home">
    <!-- 🌌 Hero 区 -->
    <section class="hero">
      <h1 class="title">
        你的专属 AI 知识助手
      </h1>

      <p class="subtitle">
        构建属于你的知识问答系统 · 支持多会话 · 流式响应 · LangChain驱动
      </p>

      <div class="actions">
        <button class="primary" @click="goChat">
          🚀 开始对话
        </button>
        <button class="secondary" @click="goLangchain">
          🧠 LangChain练习
        </button>
      </div>
    </section>

    <!-- ⚡ 功能区 -->
    <section class="features">
      <div class="card">
        <div class="icon">💬</div>
        <h3>智能问答</h3>
        <p>支持流式输出 + 打字机效果，让对话更自然</p>
      </div>

      <div class="card">
        <div class="icon">📚</div>
        <h3>知识管理</h3>
        <p>多会话隔离，打造你的专属知识空间</p>
      </div>

      <div class="card">
        <div class="icon">🧠</div>
        <h3>LangChain驱动</h3>
        <p>支持Prompt工程 & Agent扩展能力</p>
      </div>
    </section>

    <!-- 🌙 底部 -->
    <section class="footer">
      <p>
        Built with Vue3 · FastAPI · LangChain
      </p>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const goChat = () => {
  router.push("/qa/chat");
};

const goLangchain = () => {
  router.push("/langchain");
};
</script>

<style scoped>
.home {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 60px;
  padding: 60px 20px;
  color: #eef1ff;
}

/* 🌌 Hero */
.hero {
  text-align: center;
  margin-top: 40px;
}

.title {
  font-size: 2.8rem;
  font-weight: 700;
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  margin-top: 16px;
  font-size: 1.1rem;
  opacity: 0.75;
}

.actions {
  margin-top: 28px;
  display: flex;
  justify-content: center;
  gap: 16px;
}

button {
  padding: 12px 20px;
  border-radius: 14px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s;
}

.primary {
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  color: #0c1225;
}

.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(58, 228, 255, 0.3);
}

.secondary {
  background: rgba(255,255,255,0.08);
  color: #fff;
}

.secondary:hover {
  background: rgba(255,255,255,0.15);
}

/* ⚡ 功能卡片 */
.features {
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
}

.card {
  width: 240px;
  padding: 22px;
  border-radius: 18px;
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(10px);
  text-align: center;
  transition: 0.25s;
}

.card:hover {
  transform: translateY(-6px);
  background: rgba(255,255,255,0.08);
}

.icon {
  font-size: 28px;
  margin-bottom: 12px;
}

.card h3 {
  margin-bottom: 8px;
}

.card p {
  font-size: 0.9rem;
  opacity: 0.7;
}

/* 🌙 底部 */
.footer {
  text-align: center;
  opacity: 0.5;
  font-size: 0.9rem;
}
</style>