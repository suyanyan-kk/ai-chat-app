<template>
  <aside class="sidebar">
    <!-- 会话列表 -->
    <div class="session-list">
      <div
        v-for="session in chatStore.sessions"
        :key="session.id"
        :class="['session-item', { active: session.id === chatStore.currentSessionId }]"
        @click="switchSession(session.id)"
      >
        <span class="title">
          {{ session.title || '新对话' }}
        </span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { useChatStore } from "@/stores/modules/chatStore";

const chatStore = useChatStore();

// 切换会话
const switchSession = (id) => {
  chatStore.switchSession(id);
};
</script>

<style scoped>
.sidebar {
  width: 240px;
  height: 100%;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255,255,255,0.08);
}


.session-list {
  flex: 1;
  overflow-y: auto;
}

.session-item {
  border-radius: 14px;
  padding: 10px 12px;
  cursor: pointer;
  color: rgba(244, 248, 255, 0.92);
  transition: 0.2s;
}

.session-item:hover {
  background: rgba(255,255,255,0.08);
}

.session-item.active {
  background: rgba(122,92,255,0.25);
  color: #fff;
}

.title {
  color: rgba(244, 248, 255, 0.92);
  font-size: 14px;
  transition: all 0.2s ease;
}
</style>