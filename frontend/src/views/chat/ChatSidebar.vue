<template>
  <div class="sidebar">
    <!-- 🔍 搜索 -->
    <n-input placeholder="搜索标题..." v-model:value="keyword" clearable round />

    <!-- 🔍 搜索结果 -->
    <div v-if="keyword">
      <div
        v-for="item in searchResults"
        :key="item.id"
        class="session-item"
        @click="selectSession(item.id)"
      >
        <div class="title-row">
          <!-- ⭐ 小标识 -->
          <span class="tag-dot" :class="item.matchType"></span>
          <div class="title" v-html="highlight(item.title)" />
        </div>
        <!--     
        <div class="desc">
          {{ item.matchType === 'title' ? '标题匹配' : '内容匹配' }}
        </div> -->
      </div>

      <div v-if="searchResults.length === 0" class="empty">没有找到结果</div>
    </div>

    <!-- 📋 默认会话列表 -->
    <div v-else class="session-list">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="session-item"
        @click="selectSession(session.id)"
      >
        {{ session.title }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { useChatStore } from "@/stores/modules/chatStore";
import { computed, nextTick } from "vue";
import { storeToRefs } from "pinia";
const chatStore = useChatStore();
const { sessions, keyword, searchResults } = storeToRefs(chatStore);

// ⭐ 点击搜索结果（核心🔥）
const selectSession = async (sessionId) => {
  // 1️⃣ 切换会话
  chatStore.switchSession(sessionId);

  await nextTick();

  // 2️⃣ 如果是内容匹配 → 滚动定位
  if (sessionId.matchType === "message") {
    scrollToMessage(sessionId?.message?.messageIndex);
  }
};

// ⭐ 滚动到消息（重点🔥）
const scrollToMessage = (index) => {
  const el = document.querySelectorAll(".msg-item")[index];

  if (el) {
    el.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });

    // ⭐ 高亮闪烁
    el.classList.add("flash");
    setTimeout(() => {
      el.classList.remove("flash");
    }, 1500);
  }
};
// ⭐ 高亮
const highlight = (text) => {
  if (!keyword.value) return text;
  const reg = new RegExp(`(${keyword.value})`, "gi");
  return text.replace(reg, `<span class="hl">$1</span>`);
};
</script>

<style scoped>
.sidebar {
  width: 240px;
  height: 100%;
  background: #0c1225;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  padding: 12px;
}

/* 搜索框 */
.sidebar :deep(.n-input) {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: all 0.2s ease;
}

.sidebar :deep(.n-input:hover) {
  border-color: rgba(122, 92, 255, 0.6);
}

.sidebar :deep(.n-input:focus-within) {
  border-color: #7a5cff;
  box-shadow: 0 0 0 2px rgba(122, 92, 255, 0.25);
}

.sidebar :deep(.n-input__input-el) {
  color: rgba(244, 248, 255, 0.92);
}

/* 会话列表 */
.session-list {
  flex: 1;
  overflow-y: auto;
  margin-top: 12px;
  padding-right: 4px;
}

/* 滚动条美化 */
.session-list::-webkit-scrollbar {
  width: 6px;
}

.session-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 6px;
}

/* 每一项 */
.session-item {
  border-radius: 12px;
  padding: 10px 12px;
  cursor: pointer;
  color: rgba(244, 248, 255, 0.85);
  transition: all 0.18s ease;
  margin-bottom: 6px;
}

.session-item:hover {
  background: rgba(255, 255, 255, 0.06);
  transform: translateX(2px);
}

.session-item.active {
  background: linear-gradient(135deg, rgba(122, 92, 255, 0.35), rgba(58, 228, 255, 0.25));
  color: #fff;
}

/* 标题 */
.title {
  font-size: 14px;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 小圆点 */
.tag-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
  opacity: 0.8;
}

/* 标题匹配（蓝色） */
.tag-dot.title {
  background: #3ae4ff;
}

/* 内容匹配（紫色） */
.tag-dot.message {
  background: #7a5cff;
}
/* 搜索高亮 */
.hl {
  color: #3ae4ff;
  font-weight: 600;
}

/* 空状态 */
.empty {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
  opacity: 0.6;
}
</style>
