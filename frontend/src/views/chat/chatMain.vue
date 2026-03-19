<template>
  <div class="chat-page">
    <div class="chat-header">
      <h1>个人知识问答</h1>
      <p class="sub-title">和你的 AI 助手对话，实时获取答案</p>
    </div>

    <div class="chat-body">
      <div class="msg-list" ref="msgList">
          <ChatMessage
            v-for="(msg, index) in chatStore.currentMessages"
            :key="msg.id || index"
            :msg="msg"
          />
      </div>

      <div class="chat-input">
        <n-input
          v-model:value="newMessage"
          type="textarea"
          placeholder="输入消息..."
          :autosize="{ minRows: 1, maxRows: 4 }"
          @keydown.enter.prevent="sendMessage"
          size="large"
          rounded
          class="ask-input"
        />

        <n-button type="primary" @click="sendMessage"> 发送 </n-button>
        <button class="new-btn" @click="handleNewSession"> + 新建会话</button>
      </div>
    </div>
    <n-alert title="Warning 类型" type="warning" v-show="isWarningVisible">
      输入内容过长，请精简后再试！ (我要省点钱💰)
    </n-alert>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, reactive, watch } from "vue";
import { chatStream, langchainPractice } from "@/api";
import ChatMessage from '@/components/chat/ChatMessage.vue'
import { useChatStore } from "@/stores/modules/chatStore";
import { useUIStore } from "@/stores/modules/uiStore";
import { storeToRefs } from 'pinia';
const chatStore = useChatStore()
const uiStore = useUIStore()
const { isWarningVisible } = storeToRefs(uiStore)
const messages = ref([{ 
  // type: "markdown",
  // isUser: false,
  // role: "AI",
  // content: "你好",
  // time: Date.now(),
  // loading: false
 }]);


const newMessage = ref("");
const msgList = ref(null);
// 初始化一个会话（第一次进入）
if (!chatStore.currentSessionId) {
  chatStore.createSession()
}
const scrollToBottom = async () => {
  await nextTick();
  if (msgList.value) {
    msgList.value.scrollTop = msgList.value.scrollHeight;
  }
};
let queue = [];
let isTyping = false;

const typeWriter = async (target) => {
  if (isTyping) return;
  isTyping = true;

  while (queue.length > 0) {
    const text = queue.shift();

    for (let char of text) {
      target.content += char;  
      smartScroll();
      await new Promise((r) => setTimeout(r, 10 + Math.random() * 20));
    }
  }

  isTyping = false;
};
let lastScroll = Date.now();
// ⭐ 优化滚动频率，避免每个字符都触发滚动导致性能问题
const smartScroll = () => {
  const now = Date.now();
  if (now - lastScroll > 100) {
    scrollToBottom();
    lastScroll = now;
  }
};
const sendMessage = async () => {
  const value = newMessage.value.trim();
  if (!value) return;
  if (newMessage.value.length > 2000) {
     uiStore.showWarning()
     return
  }
  // 1️⃣ 前端先插入用户消息
  chatStore.addUserMessage({
    type: "text",
    isUser: true,
    role: "user",
    content: value,
    time: Date.now()
  })
  newMessage.value = "";
  await scrollToBottom();

  // 2️⃣AI消息先插入一个空的
  // ⭐关键，后续通过修改这个对象的text属性来实现流式更新
  let aiMessage = reactive({
    type: "markdown",
    content: "",
    isUser: false,
    role: "AI",
    loading: true,
    time: Date.now(),
  })

  chatStore.addAIMessage(aiMessage)
  await scrollToBottom()
  try {
    // ⭐ 这里的流式接口需要后端配合，逐步返回数据
    // await chatStream(value, async (chunk) => {
    // 提示词模版练习接口
    await langchainPractice({
      session_id: chatStore.currentSessionId, 
      message: value
    }, async (chunk) => {
      
      queue.push(chunk);
      // 每次收到新数据时尝试触发打字机效果，如果正在打字则会排队等候
      typeWriter(aiMessage);
    });
  } catch (error) {
    aiMessage.content = "抱歉，获取回复失败";
  } finally {
    aiMessage.loading = false;
    await nextTick();
  }
};
// 新建会话
const handleNewSession = () => {
  chatStore.createSession();
};
// 监听会话数据变化，自动保存到 localStorage
watch(chatStore.sessions, () => {
  localStorage.setItem("sessions", JSON.stringify(chatStore.sessions))
}, { deep: true })
onMounted(() => {
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("copy-btn")) {
      const code = decodeURIComponent(e.target.dataset.code);

      navigator.clipboard.writeText(code);

      e.target.innerText = "已复制";
      setTimeout(() => {
        e.target.innerText = "复制";
      }, 1500);
    }
  });
  scrollToBottom(); // 初始消息滚动到底部
});
</script>

<style scoped>

.chat-page {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding-top: 26px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-header h1 {
  margin: 0;
  font-size: 1.75rem;
}

.chat-header p {
  margin: 8px 0 0;
  color: rgba(255, 255, 255, 0.67);
  font-size: 0.98rem;
}
.sub-title {
  opacity: 0.7;
}
.chat-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 14px;
  min-height: 0;
}

.msg-list {
  flex: 1;
  overflow-y: auto; /* 内部滚动 */
  padding-right: 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
  scroll-behavior: smooth; /* 平滑滚动 */
}

.chat-input {
  display: flex;
  gap: 12px;
  /* padding-top: 10px; */
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  color: rgba(244, 248, 255, 0.92);
}

.chat-input :deep(.n-input) {
  flex: 1;
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
  color: rgba(244, 248, 255, 0.92);
  font-size: 1rem;
  outline: none;
  text-align: left;
}
.chat-input :deep(.n-input__input-el),
.chat-input :deep(.n-input__textarea-el) {
  color: rgba(244, 248, 255, 0.92) !important; /* 输入文字 */
  padding: 6px 5px !important;
  line-height: 1.9;
}

.chat-input :deep(.n-input__placeholder) {
  color: rgba(255, 255, 255, 0.4) !important; /* placeholder */
}

.chat-input input {
  flex: 1;
}
.chat-input input:focus {
  border-color: rgba(130, 118, 255, 0.55);
  box-shadow: 0 0 0 2px rgba(130, 118, 255, 0.24);
}

.chat-input button,.new-btn {
  width: 80px;
  height: 100%;
  padding: 0px 10px;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #7a5cff, #3ae4ff);
  color: #0c1225;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.16s ease, box-shadow 0.16s ease;
}

.chat-input button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(58, 228, 255, 0.3);
}
.chat-input .new-btn {
  width: 120px;
}

/* 消息样式 */
.msg :deep(p) {
  margin: 6px 0;
}

.msg :deep(pre) {
  margin: 8px 0;
}

.msg :deep(code) {
  font-size: 0.9em;
}

.msg :deep(ul),
.msg :deep(ol) {
  margin: 6px 0;
  padding-left: 20px;
}

.msg :deep(h1),
.msg :deep(h2),
.msg :deep(h3) {
  margin: 10px 0 6px;
}

</style>