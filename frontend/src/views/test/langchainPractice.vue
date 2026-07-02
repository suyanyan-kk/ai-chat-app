<template>
  <div class="langchain-page">
    <h1 class="title">🧠 LangChain 实战中心</h1>

    <!-- 🧭 知识折叠区 -->
    <section class="block">
      <h2>🧭 系统能力地图</h2>

      <div class="accordion">
        <div
          v-for="(item, index) in knowledge"
          :key="index"
          class="accordion-item"
        >
          <button
            type="button"
            class="accordion-header"
            :aria-expanded="activeIndex === index"
            @click="toggle(index)"
          >
            {{ item.title }}
            <span class="accordion-icon" aria-hidden="true">+</span>
          </button>

          <div
            :class="['accordion-panel', { open: activeIndex === index }]"
            :aria-hidden="activeIndex !== index"
          >
            <div class="accordion-panel-inner">
              <div class="accordion-body">
                <dl class="detail-list">
                  <div class="detail-row">
                    <dt>作用</dt>
                    <dd>{{ item.content }}</dd>
                  </div>
                  <div class="detail-row">
                    <dt>项目实现</dt>
                    <dd>{{ item.implementation }}</dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ⚙️ RAG流程可视化 -->
    <section class="block">
      <h2>⚙️ RAG 流程演示（点击步骤）</h2>

      <div class="flow">
        <button
          v-for="(step, index) in flowSteps"
          :key="index"
          type="button"
          :class="['step', { active: currentStep === index }]"
          :aria-pressed="currentStep === index"
          @click="currentStep = index"
        >
          {{ step.title }}
        </button>
      </div>

      <div class="flow-detail">
        <dl class="detail-list">
          <div class="detail-row">
            <dt>作用</dt>
            <dd>{{ flowSteps[currentStep].desc }}</dd>
          </div>
          <div class="detail-row">
            <dt>项目实现</dt>
            <dd>{{ flowSteps[currentStep].implementation }}</dd>
          </div>
        </dl>
      </div>
    </section>

    <!-- 🧪 在线 Demo -->
    <section class="block">
      <h2>🧪 在线对话</h2>

      <div class="demo">
        <input
          v-model="question"
          placeholder="输入你的问题..."
          :disabled="isSending"
          @keydown.enter="ask"
        />

        <button :disabled="isSending" @click="ask">
          {{ isSending ? "回答生成中..." : "发送并加入会话" }}
        </button>

        <div class="response">
          <div class="response-text">
            {{ answer || "AI 回复会显示在这里..." }}
          </div>

          <button
            v-if="demoSessionId"
            type="button"
            class="conversation-link"
            @click="openConversation"
          >
            在对话窗口查看完整会话 →
          </button>
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
import { useRouter } from "vue-router";

import { useChatFlow } from "@/composables/useChatFlow";
import { useChatStore } from "@/stores/modules/chatStore";


const router = useRouter();
const chatStore = useChatStore();
const {
  isSending,
  sendMessage: sendChatMessage
} = useChatFlow();

/* 折叠 */
const activeIndex = ref(null);
const toggle = (i) => {
  activeIndex.value = activeIndex.value === i ? null : i;
};

const knowledge = [
  {
    title: "🤖 Agent 编排与路由",
    content: "让系统判断一次请求应该直接回答、查询知识库，还是调用外部工具。",
    implementation: "LangGraph 用 StateGraph 构建 Agent 与 Tool 节点循环；知识库意图进入 RAG Tool，时间、天气、计算与 MCP 工具则按路由和模型决策调用。"
  },
  {
    title: "🧰 MCP 工具生态",
    content: "用统一协议把文件系统、GitHub、PostgreSQL 和远程服务接入 Agent。",
    implementation: "项目同时支持 stdio 与 Streamable HTTP 传输，启动时并行加载各服务；工具经过 SAFE_MCP_TOOL_NAMES 白名单过滤，只向 Agent 暴露安全、只读能力。"
  },
  {
    title: "💬 会话记忆与流式响应",
    content: "保留多轮对话上下文，并把生成过程实时反馈给前端。",
    implementation: "session_id 作为 LangGraph 的 thread_id，由 MemorySaver 维护会话状态；messages 与 updates 双通道事件被转换为 Token 和 Sources，再通过 SSE 持续推送。"
  },
  {
    title: "🧪 可观测与调试",
    content: "把切分、召回和排序过程显式呈现，方便定位回答偏差。",
    implementation: "Chunk 调试中心可查看父子块与元数据；Retrieval 调试中心依次展示 Query Rewrite、Multi-Query、向量召回、BM25、RRF 和 Rerank 结果。"
  },
  {
    title: "🛡️ 认证与安全边界",
    content: "保护系统入口、用户会话和可调用工具的权限范围。",
    implementation: "密码使用 bcrypt 哈希，访问令牌与刷新会话分离并对持久化令牌做摘要；系统内置登录限流、角色权限，以及 MCP 工具白名单。"
  }
];

/* RAG流程 */
const currentStep = ref(0);

const flowSteps = [
  {
    title: "加载数据",
    desc: "读取并标准化 PDF、Word、Markdown、文本和代码资料。",
    implementation: "文件上传后由 ParserFactory 选择对应解析器，抽取正文与页码信息，并创建知识文件记录。"
  },
  {
    title: "切分文本",
    desc: "拆分为可检索的 Chunk，控制长度并保留语义结构。",
    implementation: "SplitterFactory 与 ChunkBuilder 依次完成结构切分、Parent 切分和 Child 切分。"
  },
  {
    title: "向量化",
    desc: "将 Chunk 转换为可计算语义相似度的 Embedding 向量。",
    implementation: "使用 bge-small-zh-v1.5 对 Child Chunk 批量编码，并对向量进行归一化。"
  },
  {
    title: "存储",
    desc: "保存原始内容、切块结构、向量及来源元数据。",
    implementation: "知识文件与全部 Chunk 存入 PostgreSQL，可检索的 Child Chunk 及元数据持久化到 ChromaDB。"
  },
  {
    title: "检索",
    desc: "从知识库中找到与问题最相关、上下文完整的内容。",
    implementation: "先进行 Query Rewrite 与 Multi-Query，再融合向量召回和 BM25，通过 RRF 排序、可选 Rerank，最后回溯 Parent Chunk。"
  },
  {
    title: "生成回答",
    desc: "将检索上下文交给 LLM，生成带来源依据的最终回答。",
    implementation: "RAG Tool 把 context 与 sources 写入 LangGraph 状态，DeepSeek 生成答案，后端通过 SSE 分别流式推送 Token 和引用来源。"
  }
];

/* Demo */
const question = ref("");
const answer = ref("");
const demoSessionId = ref(null);

const syncDemoAnswer = (context) => {
  const content = context.aiMessage?.content;

  if (content) {
    answer.value = content;
  }
};

const ask = async () => {
  const value = question.value.trim();

  if (!value || isSending.value) return;

  answer.value = "思考中...";
  demoSessionId.value = null;
  question.value = "";

  try {
    const context = await sendChatMessage(
      value,
      {
        newSession: true,
        onSessionReady: ({ sessionId }) => {
          demoSessionId.value = sessionId;
        },
        onEvent: (_event, eventContext) => {
          syncDemoAnswer(eventContext);
        },
        onError: (_error, errorContext) => {
          syncDemoAnswer(errorContext);
        }
      }
    );

    syncDemoAnswer(context);
  } catch {
    answer.value = "抱歉，获取回复失败";
  }
};

const openConversation = async () => {
  if (!demoSessionId.value) return;

  chatStore.switchSession(
    demoSessionId.value
  );
  await router.push("/qa/chat");
};
</script>

<style scoped>
.langchain-page {
  min-height: 100%;
  padding: 30px;
  max-width: 900px;
  margin: 0 auto;
  box-sizing: border-box;
  color: #eef1ff;
}

.title {
  font-size: 2rem;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.block {
  margin-bottom: 28px;
}

.block h2 {
  margin-bottom: 14px;
  font-size: 1.15rem;
}

/* 折叠 */
.accordion-item {
  margin-bottom: 10px;
}

.accordion-header {
  width: 100%;
  padding: 12px;
  background: rgba(255,255,255,0.06);
  color: inherit;
  border: 0;
  cursor: pointer;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font: inherit;
  text-align: left;
  transition:
    background 0.22s ease,
    box-shadow 0.22s ease;
}

.accordion-header:hover,
.accordion-header[aria-expanded="true"] {
  background: rgba(255,255,255,0.09);
}

.accordion-header:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px rgba(58, 228, 255, 0.45);
}

.accordion-icon {
  flex: 0 0 auto;
  color: rgba(238, 241, 255, 0.72);
  font-size: 1.2rem;
  line-height: 1;
  transition: transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
}

.accordion-header[aria-expanded="true"] .accordion-icon {
  transform: rotate(45deg);
}

.accordion-panel {
  display: grid;
  grid-template-rows: 0fr;
  opacity: 0;
  visibility: hidden;
  transition:
    grid-template-rows 0.38s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.24s ease,
    visibility 0s linear 0.38s;
}

.accordion-panel.open {
  grid-template-rows: 1fr;
  opacity: 1;
  visibility: visible;
  transition:
    grid-template-rows 0.38s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.28s 0.06s ease,
    visibility 0s;
}

.accordion-panel-inner {
  min-height: 0;
  overflow: hidden;
}

.accordion-body {
  padding: 14px 12px 12px;
  transform: translateY(-6px);
  transition: transform 0.38s cubic-bezier(0.22, 1, 0.36, 1);
}

.accordion-panel.open .accordion-body {
  transform: translateY(0);
}

.detail-list {
  margin: 0;
}

.detail-row {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr);
  gap: 14px;
  align-items: start;
  padding: 9px 0;
}

.detail-row + .detail-row {
  border-top: 1px solid rgba(255,255,255,0.08);
}

.detail-row dt {
  color: rgba(113, 223, 241, 0.86);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.detail-row dd {
  margin: 0;
  color: rgba(238, 241, 255, 0.7);
  font-size: 0.92rem;
  line-height: 1.75;
}

/* 流程 */
.flow {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.step {
  padding: 8px 12px;
  border: 0;
  border-radius: 10px;
  background: rgba(255,255,255,0.06);
  color: inherit;
  cursor: pointer;
  font: inherit;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.step:hover {
  transform: translateY(-1px);
  background: rgba(255,255,255,0.1);
}

.step.active {
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  color: #000;
}

.flow-detail {
  margin-top: 14px;
  padding: 7px 14px;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  background: rgba(255,255,255,0.025);
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

.demo button:disabled {
  cursor: not-allowed;
  opacity: 0.62;
}

.response {
  min-height: 80px;
  padding: 10px;
  background: rgba(255,255,255,0.05);
  border-radius: 10px;
}

.response-text {
  min-height: 58px;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.demo .conversation-link {
  width: auto;
  margin-top: 10px;
  padding: 5px 0;
  background: none;
  color: #71dff1;
  font-size: 0.84rem;
  text-align: left;
}

.demo .conversation-link:hover {
  color: #ffffff;
}

/* highlight */
.highlight {
  background: rgba(122,92,255,0.1);
  padding: 16px;
  border-radius: 12px;
}

.highlight ul {
  display: grid;
  gap: 6px;
}

@media (max-width: 720px) {
  .langchain-page {
    width: 100%;
    padding: 22px 14px 32px;
  }

  .title {
    font-size: clamp(1.55rem, 8vw, 2rem);
    line-height: 1.3;
  }

  .block {
    margin-bottom: 24px;
  }

  .block h2 {
    font-size: 1rem;
    line-height: 1.5;
  }

  .accordion-header {
    min-height: 48px;
    padding: 11px 12px;
  }

  .accordion-body {
    padding: 12px 8px 10px;
  }

  .flow {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
  }

  .step {
    padding: 9px 8px;
    text-align: center;
  }

  .flow-detail {
    padding: 6px 11px;
  }

  .demo input {
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
  }

  .response,
  .detail-row dd {
    overflow-wrap: anywhere;
  }

  .highlight {
    font-size: 0.9rem;
  }
}

@media (max-width: 420px) {
  .detail-row {
    grid-template-columns: 62px minmax(0, 1fr);
    gap: 8px;
  }

  .detail-row dd {
    font-size: 0.88rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .accordion-header,
  .accordion-icon,
  .accordion-panel,
  .accordion-body,
  .step {
    transition: none;
  }
}
</style>
