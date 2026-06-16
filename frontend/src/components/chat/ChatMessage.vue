<template>
  <div :class="['msg-row', msg.isUser ? 'row-user' : 'row-bot']">
    <!-- AI头像 -->
    <img v-if="!msg.isUser" class="avatar" src="/ai.png" />

    <!-- 消息区域 -->
    <div class="msg-wrapper">
      <n-card
        content-style="padding: 8px 12px;"
        :style="cardStyle"
        :class="['msg', msg.isUser ? 'msg-user' : 'msg-bot']"
      >
        <!-- AI -->
        <div v-if="msg.type === 'markdown'" v-html="renderMarkdown(msg.content)"></div>

        <!-- 用户 -->
        <div v-else v-html="msg.content"></div>

        <!-- 打字光标 -->
        <span v-if="msg.loading" class="cursor"> ▌ </span>
      </n-card>
      <!-- Thinking -->

      <Thinking :show="msg.status === 'thinking'" />
      <!-- Tool -->

      <ToolStatus :tool="msg.runningTool" />
      <!-- Sources -->

      <SourceList :sources="msg.sources" />
      <!-- ========================= -->
      <!-- 来源引用 -->
      <!-- ========================= -->
      <div v-for="(fileSource, index) in msg.sources" :key="index" class="source-item">
        <div class="source-file" @click="openReference(fileSource)">
          📄 {{ fileSource.file_name || "未知文件" }}
          <span
            v-if="formatSource(fileSource)"
            class="source-meta"
            style="font-size: 12px; opacity: 0.6; margin-left: 6px"
          >
            {{ formatSource(fileSource) }}
          </span>
        </div>
      </div>
    </div>

    <!-- 用户头像 -->
    <img v-if="msg.isUser" class="avatar" src="/user.png" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { renderMarkdown } from "@/markdown";
import { NCard } from "naive-ui";
import { useRouter } from "vue-router";
import Thinking from "@/components/chat/Thinking.vue"
import ToolStatus from "@/components/chat/ToolStatus.vue"
import SourceList from "@/components/chat/SourceList.vue"

const router = useRouter();
// props
defineProps({
  msg: {
    type: Object,
    required: true,
  },
});
const openReference = (fileSource) => {
  console.log("打开引用：", fileSource);
  const fileId = fileSource.file_id;
  router.push({
    path: "/kb",
    query: {
      file_id: fileSource.file_id,
      page: fileSource.locator_value,
      keywordRoute: fileSource.locatorType, //chunk_text 高亮文本
    },
  });
};
const formatSource = (fileSource) => {
  const locatorType = fileSource.locator_type;
  const locatorValue = fileSource.locator_value;

  if (locatorType === "page") {
    return `第 ${locatorValue} 页`;
  }

  if (locatorType === "section") {
    return locatorValue;
  }

  if (locatorType === "heading") {
    return locatorValue;
  }

  if (locatorType === "code") {
    return `代码块 ${locatorValue}`;
  }

  return "";
};
// 卡片样式
const cardStyle = computed(() => ({
  maxWidth: "70%",
  width: "fit-content",
  wordBreak: "break-word",
  marginBottom: "6px",
}));
</script>

<style scoped>
/* =========================
   行布局
========================= */

.msg-row {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  margin: 8px 0;
}

.row-user {
  justify-content: flex-end;
}

.row-bot {
  justify-content: flex-start;
}

/* =========================
   包裹层
========================= */

.msg-wrapper {
  width: 60%;
  display: flex;
  flex-direction: column;
  max-width: 70%;
}

/* =========================
   头像
========================= */

.avatar {
  width: 36px;
  height: 36px;

  border-radius: 50%;

  object-fit: cover;

  flex-shrink: 0;

  border: 1px solid rgba(255, 255, 255, 0.1);

  transition: transform 0.2s;
}

.avatar:hover {
  transform: scale(1.05);
}

/* =========================
   消息气泡
========================= */

.msg {
  display: inline-block;

  border-radius: 16px;

  font-size: 1rem;

  line-height: 1.45;

  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);

  backdrop-filter: blur(10px);
}

/* 用户气泡 */

.msg-user {
  align-self: flex-end;

  background: rgba(119, 103, 255, 0.22);

  border: 1px solid rgba(119, 103, 255, 0.38);

  color: rgba(240, 244, 255, 0.95);

  text-align: right;
}

/* AI气泡 */

.msg-bot {
  align-self: flex-start;

  background: rgba(255, 255, 255, 0.06);

  border: 1px solid rgba(255, 255, 255, 0.12);

  color: rgba(230, 235, 255, 0.87);

  text-align: left;
}

/* =========================
   来源引用
========================= */

.sources {
  width: 70%;
  margin-top: 10px;

  padding-left: 6px;
}

.sources-title {
  font-size: 12px;

  opacity: 0.6;

  margin-bottom: 8px;
}

.source-item {
  width: 70%;
  padding: 10px 12px;

  margin-bottom: 8px;

  border-radius: 12px;

  background: rgba(255, 255, 255, 0.04);

  border: 1px solid rgba(255, 255, 255, 0.06);

  transition: all 0.2s ease;

  cursor: pointer;
}

.source-item:hover {
  background: rgba(255, 255, 255, 0.08);

  transform: translateY(-1px);
}

.source-file {
  font-size: 14px;

  font-weight: 600;

  color: rgba(255, 255, 255, 0.92);
}

.source-meta {
  margin-top: 4px;

  font-size: 12px;

  opacity: 0.65;
}

/* =========================
   打字光标
========================= */

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

/* =========================
   markdown
========================= */

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
