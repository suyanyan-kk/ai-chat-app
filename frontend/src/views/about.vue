<!-- src/views/about.vue -->
<template>
  <div class="about-page">
    <div class="about-main">
      <div class="about-head">
        <h1>关于我</h1>
        <p>这是一份简洁、沉稳、有氛围感的简介页面布局。</p>
      </div>

      <div class="about-grid">
        <div class="about-card">
          <h3>技能</h3>
          <p>Vue.js / TypeScript / UI 设计 / 响应式布局</p>
        </div>

        <div class="about-card">
          <h3>兴趣</h3>
          <p>AI 交互、视觉氛围、产品体验优化</p>
        </div>

        <div class="about-card">
          <h3>理念</h3>
          <p>干净布局 + 轻微渐变 + 友好交互</p>
        </div>

        <div class="about-card">
          <h3>目标</h3>
          <p>打造既稳重又有氛围感的 Web 应用界面</p>
        </div>
      </div>
    </div>

    <div class="about-visual">
      <div class="glow-ring"></div>
      <div class="glow-dot"></div>
    </div>
  </div>
</template>

<script setup>
// 无须脚本
</script>

<style scoped>
.about-page {
  min-height: 100%;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 32px;
  align-items: start;
}

.about-main {
  max-width: 920px;
}

.about-head h1 {
  margin: 0;
  font-size: 2.4rem;
  letter-spacing: 0.02em;
}

.about-head p {
  margin: 12px 0 28px;
  color: rgba(255, 255, 255, 0.72);
  font-size: 1.05rem;
  line-height: 1.55;
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.about-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.10);
  border-radius: 16px;
  padding: 22px 20px;
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.35);
}

.about-card h3 {
  margin: 0;
  font-size: 1.15rem;
}

.about-card p {
  margin: 10px 0 0;
  color: rgba(245, 245, 255, 0.78);
  line-height: 1.5;
}

.about-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 420px;
}

.glow-ring {
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle at top, rgba(105, 224, 255, 0.37), transparent 58%);
  filter: blur(16px);
  animation: glow 4.4s ease-in-out infinite;
}

.glow-dot {
  position: absolute;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 0 22px rgba(255, 255, 255, 0.55);
  top: 24%;
  left: 38%;
  animation: float 3.8s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% { transform: scale(1); opacity: 0.52; }
  50% { transform: scale(1.12); opacity: 0.78; }
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(12px, -14px); }
}

@media (max-width: 1024px) {
  .about-page {
    grid-template-columns: 1fr;
  }
  .about-visual {
    margin-top: 28px;
  }
  .about-grid {
    grid-template-columns: 1fr;
  }
}
</style>