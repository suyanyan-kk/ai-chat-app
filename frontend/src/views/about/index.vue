<template>
  <div class="about-page">
    <!-- 👋 头部 -->
    <section class="hero">
      <h1 class="title">关于这个项目</h1>
      <p class="subtitle">
        一个基于 AI 的个人知识问答系统 · 持续进化中 🚀
      </p>
    </section>

    <!-- 📦 项目介绍 -->
    <section class="block">
      <h2>📌 项目简介</h2>
      <p>
        这个项目是我基于 Vue3 + FastAPI + LangChain 构建的 AI 应用，
        目标是打造一个类似 ChatGPT 的多会话问答系统，并逐步扩展为
        一个真正“可用”的个人知识助手。
      </p>
    </section>

    <!-- ⚙️ 技术栈 -->
    <section class="block">
      <h2>⚙️ 技术栈</h2>

      <div class="tech-grid">
        <div class="tech">Vue3</div>
        <div class="tech">Pinia</div>
        <div class="tech">Naive UI</div>
        <div class="tech">FastAPI</div>
        <div class="tech">LangChain</div>
        <div class="tech">Streaming</div>
      </div>
    </section>

    <!-- 🚀 功能亮点 -->
    <section class="block">
      <h2>🚀 已实现功能</h2>

      <ul class="list">
        <li>💬 多会话聊天（类似 ChatGPT）</li>
        <li>⚡ 流式输出（Streaming）</li>
        <li>⌨️ 打字机效果（前端实现）</li>
        <li>🧠 LangChain 接入</li>
        <li>📂 会话持久化（localStorage）</li>
      </ul>
    </section>

    <!-- 🔮 未来规划 -->
    <section class="block highlight">
      <h2>🔮 未来规划</h2>

      <ul class="list">
        <li>📚 构建 RAG 知识库（支持上传文档）</li>
        <li>🤖 Agent 工具调用能力</li>
        <li>🔍 会话搜索 & 分类</li>
        <li>🌐 部署上线，做成真实产品</li>
      </ul>
    </section>

    <!-- 👨‍💻 个人 -->
    <section class="block">
      <h2>👨‍💻 关于我</h2>
      <p>
        一名正在深入学习 AI 应用开发的开发者，目前专注于：
      </p>

      <ul class="list">
        <li>🔹 前端工程化（Vue3 / 组件设计）</li>
        <li>🔹 AI 应用开发（LangChain / LLM）</li>
        <li>🔹 全栈能力（FastAPI + 前端联动）</li>
      </ul>
    </section>

    <!-- 🌙 Footer -->
    <section class="footer">
      <p>Made with ❤️ · 持续迭代中</p>
    </section>
  </div>
</template>

<style scoped>
.about-page {
  padding: 30px;
  max-width: 900px;
  margin: 0 auto;
  color: #eef1ff;
}

/* 👋 头部 */
.hero {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 2.4rem;
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  margin-top: 10px;
  opacity: 0.7;
}

/* 📦 block */
.block {
  margin-bottom: 30px;
}

.block h2 {
  margin-bottom: 10px;
}

/* ⚙️ 技术栈 */
.tech-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tech {
  padding: 8px 14px;
  border-radius: 20px;
  background: rgba(255,255,255,0.08);
  font-size: 0.9rem;
}

/* 📄 列表 */
.list {
  padding-left: 18px;
  line-height: 1.8;
}

/* 🌟 高亮 */
.highlight {
  background: rgba(122,92,255,0.1);
  padding: 16px;
  border-radius: 12px;
}

/* 🌙 footer */
.footer {
  text-align: center;
  margin-top: 40px;
  opacity: 0.5;
  font-size: 0.9rem;
}
</style>