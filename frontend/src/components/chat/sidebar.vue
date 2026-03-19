<template>
  <div class="chat-container">
    <div class="sidebar">
      <div
        v-for="s in chatStore.sessions"
        :key="s.id"
        @click="chatStore.switchSession(s.id)"
        :class="['session-item', { active: s.id === chatStore.currentSessionId }]"
      >
        {{ s.title || "未命名会话" }}
      </div>

      <button class="new-session-btn" @click="chatStore.createSession()">
        + 新建会话
      </button>
    </div>
    <template v-if="!chatStore.currentSessionId">
      <div class="empty-state">
        <p>请选择一个会话或创建新的会话开始聊天</p>
      </div>
    </template>
    <template v-else>
      <div class="chat-header">
        <h1>个人知识问答</h1>
        <p class="sub-title">和你的 AI 助手对话，实时获取答案</p>
      </div>
    </template>
  </div>
</template>
