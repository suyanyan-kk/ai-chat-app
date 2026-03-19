import { defineStore } from "pinia"
import { v4 as uuidv4 } from "uuid"

export const useChatStore = defineStore("chat", {
  state: () => ({
    sessions: [
    // 初始数据，方便调试
    //   {
    //   id: uuidv4(),
    //   title: "新对话",
    //   messages: [],
    //   createdAt: Date.now(),
    //   messages: [{
    //     type: "markdown",
    //     isUser: false,
    //     role: "AI",
    //     content: "你好",
    //     time: Date.now(),
    //     loading: false
    //   }]
    // }
  ],
    currentSessionId: null,
  }),

  getters: {
    currentSession(state) {
      return state.sessions.find(s => s.id === state.currentSessionId)
    },
    currentMessages(state) {
      return state.currentSession?.messages || []
    }
  },

  actions: {
    createSession() {
      const id = uuidv4()
      this.sessions.push({
        id,
        title: "新对话",
        createdAt: Date.now(),
        messages: [
          {
            type: "text",
            isUser: false,
            role: "AI",
            content: "你好 👋 我是你的 AI 助手",
            time: Date.now(),
            loading: false
          }
        ]
      })
      this.currentSessionId = id
    },
    switchSession(id) {
      this.currentSessionId = id
    },

    deleteSession(id) {
      this.sessions = this.sessions.filter(s => s.id !== id)
      if (this.currentSessionId === id) {
        this.currentSessionId = this.sessions[0]?.id || null
      }
    },

    addUserMessage(content) {
      this.currentSession?.messages.push(content)
    },

    addAIMessage(msg) {
      this.currentSession?.messages.push(msg)
      return msg
    },

    updateAIMessage(chunk) {
      const msgs = this.currentMessages
      if (!msgs.length) return
      msgs[msgs.length - 1].text += chunk
    },

    finishAIMessage() {
      const msgs = this.currentMessages
      if (!msgs.length) return
      msgs[msgs.length - 1].loading = false
    }
  }
})
