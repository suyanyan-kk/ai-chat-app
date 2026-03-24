<template>
  <div class="sidebar">
    <!-- 🔍 搜索 -->
    <n-input placeholder="搜索标题..." v-model:value="keyword" clearable round />

    <!-- 📋 列表统一 -->
<div class="session-list">
  <div
    v-for="item in displayList"
    :key="item.id"
    class="session-item"
    @click="selectSession(item)"
  >
    <div :class="['title-row', isSearching ? 'title-search-row' : 'title-edit-row']">
      <!-- ⭐ 搜索模式的小点 -->
      <span
        v-if="isSearching"
        class="tag-dot"
        :class="item.matchType"
      />

      <!-- ✏️ 编辑态 -->
      <template v-if="editingId === item.id && !isSearching">
        <input
          v-model="editingTitle"
          class="edit-input"
          @blur="saveTitle(item)"
          @keydown.enter="saveTitle(item)"
          @keydown.esc="cancelEdit"
          autofocus
        />
      </template>

      <!-- 📄 普通展示态 -->
      <template v-else>
        <div
          class="title"
          @dblclick.stop="!isSearching && handleEdit(item)"
          v-html="isSearching ? highlight(item.title) : item.title"
        />
      </template>

      <!-- ❌ 删除按钮（仅默认模式） -->
      <span
        v-if="!isSearching"
        class="delete-btn"
        @click.stop="handleDelete(item.id)"
      >
        ✕
      </span>

    </div>
  </div>

  <div v-if="displayList.length === 0" class="empty">
    没有找到结果
  </div>
</div>
  </div>
</template>

<script setup>
import { useChatStore } from "@/stores/modules/chatStore";
import { ref, nextTick,computed } from "vue";
import { storeToRefs } from "pinia";
const chatStore = useChatStore();
const { sessions, keyword, searchResults } = storeToRefs(chatStore);
// 每一项增加一个 editingId，只允许一个在编辑。
const editingId = ref(null);
const editingTitle = ref("");

const isSearching = computed(() => !!keyword.value);

const displayList = computed(() => {
  return isSearching.value ? searchResults.value : sessions.value;
});
// 编辑
const handleEdit = (session) => {
  editingId.value = session.id;
  editingTitle.value = session.title;
};
// 保存
const saveTitle = (session) => {
  if (!editingTitle.value.trim()) return;

  chatStore.updateSessionTitle(session.id, editingTitle.value);

  editingId.value = null;
};
// 取消编辑
const cancelEdit = () => {
  editingId.value = null;
};
// 删除会话
const handleDelete = (id) => {
  if (confirm("确定要删除这个会话吗？")) {
    // 保持至少有一个会话
    if (sessions.value.length <= 1) {
      alert("至少需要保留一个会话");
      return;
    }
    // 如果删除的是当前会话，切换到第一个会话（如果有的话）
    chatStore.deleteSession(id);
  }
}
// ⭐ 点击搜索结果（核心🔥）
const selectSession = async (item) => {
  // 1️⃣ 切换会话
  chatStore.switchSession(item.id);

  await nextTick();

  // 2️⃣ 如果是内容匹配 → 滚动定位
  if (item.matchType === "message") {
    scrollToMessage(item?.message?.messageIndex);
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
.title-search-row{
   justify-content: left;
}
.title-edit-row{
  justify-content: space-between;
}
.edit-input {
  flex: 1;
  border: none;
  outline: none;
  background: rgba(255,255,255,0.08);
  color: #fff;
  border-radius: 6px;
  padding: 2px 6px;
  font-size: 14px;
}
/* 删除按钮默认隐藏 */
.delete-btn {
  opacity: 0;
  transition: all 0.2s ease;
  cursor: pointer;
  font-size: 12px;
  color: rgba(255,255,255,0.5);
}

/* hover 时出现 */
.session-item:hover .delete-btn {
  opacity: 1;
}

/* hover 高亮 */
.delete-btn:hover {
  color: #ff6b6b;
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
