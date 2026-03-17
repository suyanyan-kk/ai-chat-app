<!-- src/views/chat.vue -->
<template>
  <div class="chat-page">
    <div class="chat-header">
      <h1>个人知识问答</h1>
      <p>和 AI 聊天，体验即时互动</p>
    </div>

    <div class="chat-body">
      <div class="msg-list" ref="msgList">
        <n-card
          v-for="(msg, index) in messages"
          :key="index"
          :style="{
          maxWidth: '70%',
          alignSelf: msg.isUser ? 'flex-end' : 'flex-start'
          }"
          :class="['msg', msg.isUser ? 'msg-user' : 'msg-bot']"
        >

          <div v-html="renderMarkdown(msg.text)" ></div>
        </n-card>
        <n-spin v-if="loading" size="small">
          <div style="padding: 8px;">AI 正在思考...</div>
        </n-spin>
      </div>

      <div class="chat-input">
          <n-input
          v-model:value="newMessage"
          type="textarea"
          placeholder="输入消息..."
          :autosize="{ minRows: 1, maxRows: 4 }"
          @keydown.enter.prevent="sendMessage"
          size="large" rounded
          class="ask-input"
          />

          <n-button type="primary" @click="sendMessage">
          发送
          </n-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted,reactive,onUpdated } from 'vue';
import { chatStream } from "@/api";
import { renderMarkdown,addCopyButtons } from "@/utils"
import { NInput, NButton,NSpin,NCard } from 'naive-ui'
const messages = ref([
  { text: '欢迎来到智能聊天，请输入内容并回车开始。', isUser: false },
]);

const newMessage = ref('');
const msgList = ref(null);
const loading = ref(false)
const scrollToBottom = async () => {
  await nextTick();
  if (msgList.value) {
    msgList.value.scrollTop = msgList.value.scrollHeight;
  }
};

const sendMessage = async () => {
  const value = newMessage.value.trim()
  if (!value) return

  // 用户消息
  messages.value.push({ text: value, isUser: true })

  newMessage.value = ""

  await scrollToBottom()

  // AI消息先插入一个空的
  let aiMessage = reactive({ text: "", isUser: false })
  messages.value.push(aiMessage)

  await scrollToBottom()
   loading.value = true
  try {
      let fullText = ""
    await chatStream(value, async chunk => {

      fullText += chunk   // 实时更新
      // messages.value = [...messages.value]   // ⭐ 强制触发响应式
      aiMessage.text = fullText   // 每次重新渲染
      await nextTick()
      scrollToBottom()
    })

  } catch (error) {
    aiMessage.text = "抱歉，获取回复失败"
  }finally {
    loading.value = false
  }

}
onUpdated(() => {
  addCopyButtons()
})
onMounted(() => {
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
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.10);
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

.chat-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-top: 14px;
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

.msg {
  max-width: 68%;
  border-radius: 16px;
  font-size: 1rem;
  line-height: 1.45;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.10);
  backdrop-filter: blur(10px);
}

.msg-user {
  /* align-self: flex-end; */
  background: rgba(119, 103, 255, 0.22);
  border: 1px solid rgba(119, 103, 255, 0.38);
  color: rgba(240, 244, 255, 0.95);
  text-align: right;
}

.msg-bot {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: rgba(230, 235, 255, 0.87);
  text-align: left;
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
  color: rgba(244, 248, 255, 0.92) !important;   /* 输入文字 */
}

.chat-input :deep(.n-input__placeholder) {
  color: rgba(255, 255, 255, 0.4) !important; /* placeholder */
}
.chat-message :deep(.n-card__content) {
  padding: 0px 0px !important;
}
.chat-input input {
  flex: 1;
}
.chat-input input:focus {
  border-color: rgba(130, 118, 255, 0.55);
  box-shadow: 0 0 0 2px rgba(130, 118, 255, 0.24);
}

.chat-input button {
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

/* 手机/窄屏 */
@media (max-width: 720px) {
  .msg {
    max-width: 90%;
  }
  .chat-input {
    flex-direction: column;
  }
  .chat-input button {
    width: 100%;
  }
}
</style>