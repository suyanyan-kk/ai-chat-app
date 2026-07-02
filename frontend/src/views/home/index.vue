<template>
  <div class="home">
    <!-- 🌌 Hero 区 -->
    <section class="hero">
      <p class="eyebrow">PERSONAL KNOWLEDGE AGENT</p>

      <h1 class="title">
        让你的知识，成为 AI 的答案
      </h1>

      <p class="subtitle">
        从资料入库、智能切分到混合检索与来源引用，
        构建可追溯、可调试、可扩展的个人知识问答系统。
      </p>

      <div class="tech-stack" aria-label="核心技术栈">
        <span>Vue 3</span>
        <span>FastAPI</span>
        <span>LangGraph</span>
        <span>ChromaDB</span>
        <span>MCP</span>
      </div>

      <div class="actions">
        <button class="primary" @click="goChat">
          🚀 进入知识问答
        </button>
        <button class="secondary" @click="goKnowledgeBase">
          📚 管理知识库
        </button>
      </div>
    </section>

    <!-- ⚡ 功能区 -->
    <section class="features">
      <div class="card">
        <div class="icon">💬</div>
        <h3>流式 Agent 对话</h3>
        <p>基于 LangGraph 编排对话与工具调用，通过 SSE 实时返回答案、状态和引用来源。</p>
      </div>

      <div class="card">
        <div class="icon">🔎</div>
        <h3>混合 RAG 检索</h3>
        <p>融合向量召回、BM25 与 RRF 排序，结合 Parent-Child Chunk 找准内容并保留上下文。</p>
      </div>

      <div class="card">
        <div class="icon">🧩</div>
        <h3>知识处理闭环</h3>
        <p>支持 PDF、Word、Markdown、文本与代码资料，并提供切块预览和检索链路调试。</p>
      </div>
    </section>

    <!-- 🌙 底部 -->
    <section class="footer">
      <p>
        Vue 3 + Pinia · FastAPI · LangChain / LangGraph · ChromaDB · PostgreSQL
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

const goKnowledgeBase = () => {
  router.push("/kb");
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
  overflow-y: auto;
}

/* 🌌 Hero */
.hero {
  text-align: center;
  margin-top: 40px;
}

.eyebrow {
  margin-bottom: 14px;
  color: #65ddf4;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.2em;
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
  margin-inline: auto;
  max-width: 760px;
  font-size: 1.1rem;
  line-height: 1.85;
  opacity: 0.75;
}

.tech-stack {
  margin-top: 22px;
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.tech-stack span {
  padding: 5px 10px;
  border: 1px solid rgba(122, 92, 255, 0.22);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.035);
  color: rgba(238, 241, 255, 0.68);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
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
  width: 280px;
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
  line-height: 1.75;
  opacity: 0.7;
}

/* 🌙 底部 */
.footer {
  text-align: center;
  opacity: 0.5;
  font-size: 0.9rem;
}

@media (max-width: 720px) {
  .home {
    gap: 40px;
    padding: 38px 18px 28px;
  }

  .hero {
    margin-top: 16px;
  }

  .title {
    font-size: clamp(2rem, 10vw, 2.6rem);
    line-height: 1.2;
  }

  .subtitle {
    font-size: 0.95rem;
    line-height: 1.75;
  }

  .actions {
    width: 100%;
    max-width: 360px;
    margin-inline: auto;
    flex-direction: column;
    gap: 10px;
  }

  .actions button {
    width: 100%;
    min-height: 46px;
  }

  .features {
    gap: 14px;
  }

  .card {
    width: 100%;
    max-width: 420px;
    padding: 20px;
  }

  .footer {
    padding-inline: 10px;
    font-size: 0.78rem;
    line-height: 1.7;
  }
}

@media (prefers-reduced-motion: reduce) {
  button,
  .card {
    transition: none;
  }
}
</style>
