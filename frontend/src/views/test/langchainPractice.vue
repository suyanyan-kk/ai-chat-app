<template>
  <div class="langchain-page">
    <h1 class="title">🧠 LangChain 实战中心</h1>

    <!-- 🧭 知识折叠区 -->
    <section class="block">
      <h2>📚 核心知识体系</h2>

      <div class="accordion">
        <div
          v-for="(item, index) in knowledge"
          :key="index"
          class="accordion-item"
        >
          <div class="accordion-header" @click="toggle(index)">
            {{ item.title }}
            <span>{{ activeIndex === index ? '−' : '+' }}</span>
          </div>

          <div v-if="activeIndex === index" class="accordion-body">
            {{ item.content }}
          </div>
        </div>
      </div>
    </section>

    <!-- ⚙️ RAG流程可视化 -->
    <section class="block">
      <h2>⚙️ RAG 流程演示（点击步骤）</h2>

      <div class="flow">
        <div
          v-for="(step, index) in flowSteps"
          :key="index"
          :class="['step', { active: currentStep === index }]"
          @click="currentStep = index"
        >
          {{ step.title }}
        </div>
      </div>

      <div class="flow-detail">
        {{ flowSteps[currentStep].desc }}
      </div>
    </section>

    <!-- 🧪 在线 Demo -->
    <section class="block">
      <h2>🧪 在线对话 Demo</h2>

      <div class="demo">
        <input
          v-model="question"
          placeholder="输入你的问题..."
          @keydown.enter="ask"
        />

        <button @click="ask">发送</button>

        <div class="response">
          {{ answer || "AI 回复会显示在这里..." }}
        </div>
      </div>
    </section>

    <!-- 💡 总结 -->
    <section class="block highlight">
      <h2>💡 我的理解</h2>
      <ul>
        <li>LangChain 本质是：LLM 编排框架</li>
        <li>RAG = 数据增强 + Prompt 拼接</li>
        <li>Agent = 决策 + 工具调用</li>
        <li>核心价值：让 AI “可控 + 可扩展”</li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { chatStream } from "@/api";

/* 折叠 */
const activeIndex = ref(null);
const toggle = (i) => {
  activeIndex.value = activeIndex.value === i ? null : i;
};

const knowledge = [
  {
    title: "📦 Document Loader",
    content: "用于加载 PDF、网页、文本等数据"
  },
  {
    title: "✂️ Text Splitter",
    content: "将长文本拆分为 chunk，便于 embedding"
  },
  {
    title: "🧠 Embedding",
    content: "把文本转为向量，用于语义搜索"
  },
  {
    title: "📚 Vector Store",
    content: "存储向量数据，如 FAISS / Chroma"
  },
  {
    title: "🤖 Agent",
    content: "根据问题自动调用工具，完成复杂任务"
  }
];

/* RAG流程 */
const currentStep = ref(0);

const flowSteps = [
  { title: "加载数据", desc: "读取 PDF / 文本 / 数据库内容" },
  { title: "切分文本", desc: "拆分为 chunk，控制上下文长度" },
  { title: "向量化", desc: "转为 embedding 向量" },
  { title: "存储", desc: "写入向量数据库" },
  { title: "检索", desc: "根据问题找到相关内容" },
  { title: "生成回答", desc: "拼接 prompt 交给 LLM" }
];

/* Demo */
const question = ref("");
const answer = ref("");

const ask = async () => {
  if (!question.value) return;

  answer.value = "思考中...";

  try {
    await chatStream(
      { message: question.value },
      (chunk) => {
        answer.value += chunk;
      }
    );
  } catch (e) {
    answer.value = "请求失败";
  }
};
</script>

<style scoped>
.langchain-page {
  padding: 30px;
  max-width: 900px;
  margin: 0 auto;
  color: #eef1ff;
}

.title {
  font-size: 2rem;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 折叠 */
.accordion-item {
  margin-bottom: 10px;
}

.accordion-header {
  padding: 12px;
  background: rgba(255,255,255,0.06);
  cursor: pointer;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
}

.accordion-body {
  padding: 12px;
  opacity: 0.8;
}

/* 流程 */
.flow {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.step {
  padding: 8px 12px;
  border-radius: 10px;
  background: rgba(255,255,255,0.06);
  cursor: pointer;
}

.step.active {
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  color: #000;
}

.flow-detail {
  margin-top: 12px;
  opacity: 0.8;
}

/* demo */
.demo {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.demo input {
  padding: 10px;
  border-radius: 10px;
  border: none;
}

.demo button {
  padding: 10px;
  border-radius: 10px;
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  border: none;
  cursor: pointer;
}

.response {
  min-height: 80px;
  padding: 10px;
  background: rgba(255,255,255,0.05);
  border-radius: 10px;
}

/* highlight */
.highlight {
  background: rgba(122,92,255,0.1);
  padding: 16px;
  border-radius: 12px;
}
</style>