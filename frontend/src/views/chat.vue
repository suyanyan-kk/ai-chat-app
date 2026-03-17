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
          content-style="padding: 8px 12px;"
          :style="{
           maxWidth: '70%',
           width: 'fit-content',
           wordBreak: 'break-word',
           alignSelf: msg.isUser ? 'flex-end' : 'flex-start'
            }"
          :class="['msg', msg.isUser ? 'msg-user' : 'msg-bot']"
        >

          <div v-html="renderMarkdown(msg.text)" ></div>
          <!-- ⭐ AI 正在输出时的光标 -->
          <span v-if="msg.loading" class="cursor">▌</span>
        </n-card>
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
// 文本打字机效果
// ⭐ 简单版本，直接逐字更新整个文本 会卡顿
// const typeWriter = async (text, target) => {
//   for (let char of text) {
//     target.text += char
//     await new Promise(resolve => setTimeout(resolve, 20)) // 速度可调
//   }
// }

let queue = []
let isTyping = false

const typeWriter = async (target) => {
  if (isTyping) return
  isTyping = true

  while (queue.length > 0) {
    const text = queue.shift()

    for (let char of text) {
      target.text += char
      smartScroll()
      await new Promise(r => setTimeout(r, 10 + Math.random() * 20))
    }
  }

  isTyping = false
}
let lastScroll = Date.now()
// ⭐ 优化滚动频率，避免每个字符都触发滚动导致性能问题
const smartScroll = () => {
  const now = Date.now()
  if (now - lastScroll > 100) {
    scrollToBottom()
    lastScroll = now
  }
}
const sendMessage = async () => {
  const value = newMessage.value.trim()
  if (!value) return

  // 用户消息
  messages.value.push({ text: value, isUser: true })

  newMessage.value = ""

  await scrollToBottom()

  // AI消息先插入一个空的 
  // ⭐关键，后续通过修改这个对象的text属性来实现流式更新
  let aiMessage = reactive({ text: "", isUser: false,loading: true })
  messages.value.push(aiMessage)

  await scrollToBottom()
   loading.value = true
  try {
      // let fullText = ""
    await chatStream(value, async chunk => {

      // fullText += chunk   // 实时更新
      // messages.value = [...messages.value]   // ⭐ 强制触发响应式
      // aiMessage.text = fullText   // 每次重新渲染
      // await typeWriter(chunk, aiMessage)  // 打字机效果逐字更新
       queue.push(chunk) 
       typeWriter(aiMessage)
      
    })

  } catch (error) {
    aiMessage.text = "抱歉，获取回复失败"
  }finally {
    aiMessage.loading = false 
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
  display: inline-block;   /* ⭐进一步确保自适应 */
  max-width: 68%;
  border-radius: 16px;
  font-size: 1rem;
  line-height: 1.45;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.10);
  backdrop-filter: blur(10px);
}
.msg :deep(pre) {
  max-width: 100%;
  overflow-x: auto;
}
.msg-user {
  /* align-self: flex-end; */
  background: rgba(119, 103, 255, 0.22);
  border: 1px solid rgba(119, 103, 255, 0.38);
  color: rgba(240, 244, 255, 0.95);
  text-align: right;
}
/* loading */
.msg-bot {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: rgba(230, 235, 255, 0.87);
  text-align: left;
}
.cursor {
  display: inline-block;
  margin-left: 2px;
  animation: blink 1s infinite;
  opacity: 1;
}

@keyframes blink {
  0% { opacity: 1 }
  50% { opacity: 0 }
  100% { opacity: 1 }
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
/* 代码块样式 */
.msg :deep(pre) {
  background: #0d1117;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
}

.msg :deep(code) {
  font-size: 0.9em;
}

.msg :deep(p) {
  margin: 6px 0;
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