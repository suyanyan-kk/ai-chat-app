<template>
  <n-card
    content-style="padding: 8px 12px;"
    :style="cardStyle"
    :class="['msg', msg.isUser ? 'msg-user' : 'msg-bot']"
  >
    <!-- AI -->
    <div  v-if="msg.type === 'markdown'" v-html="renderMarkdown(msg.text)"></div>

    <!-- 用户 -->
    <div  v-else v-html="msg.text"></div>

    <!-- 打字光标 -->
    <span v-if="msg.loading" class="cursor">▌</span>
  </n-card>
</template>

<script setup>
import { computed } from "vue";
import { renderMarkdown } from "@/markdown";
import { NCard } from "naive-ui";

// props
const props = defineProps({
  msg: {
    type: Object,
    required: true,
  },
});

// 样式逻辑抽离（更干净🔥）
const cardStyle = computed(() => ({
  maxWidth: "70%",
  width: "fit-content",
  wordBreak: "break-word",
  alignSelf: props.msg.isUser ? "flex-end" : "flex-start",
}));
</script>

<style scoped>
.msg {
  display: inline-block;
  max-width: 68%;
  border-radius: 16px;
  font-size: 1rem;
  line-height: 1.45;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.msg-user {
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

/* 光标 */
.cursor {
  display: inline-block;
  margin-left: 2px;
  animation: blink 1s infinite;
}

@keyframes blink {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

/* markdown 样式 */
.msg :deep(p) {
  margin: 6px 0;
}

.msg :deep(pre) {
  background: #0d1117;
  padding: 0px 10px;
  border-radius: 8px;
  overflow-x: auto;
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