import { defineStore } from "pinia"
import { v4 as uuidv4 } from "uuid"

const normalizePage = (page) => {
  if (Array.isArray(page)) {
    return normalizePage(page[0])
  }

  if (page === undefined || page === null || page === "") {
    return null
  }

  const numericPage = Number(page)

  return Number.isNaN(numericPage) ? page : numericPage
}

const normalizeSource = (source = {}) => {
  const page = normalizePage(
    source.page ?? (source.locator_type === "page" ? source.locator_value : null)
  )

  return {
    id: source.id ?? `${source.file_id ?? "unknown"}-${page ?? "file"}`,
    file_id: source.file_id,
    file_name: source.file_name,
    file_type: source.file_type,
    page,
  }
}

const normalizeSources = (sources = []) => {
  if (!Array.isArray(sources)) return []

  return sources.map(normalizeSource)
}

const getEventSources = (event = {}) => {
  return event.sources ?? event.data?.sources ?? []
}

export const useChatStore = defineStore("chat", {
  state: () => ({
    sessions: [
      // 初始数据，方便调试
      //   {
      //   id: uuidv4(),
      //   title: "新对话",
      //   messages: [],
      //   createdAt: Date.now(),
      //   matchType: "title" | "message",
      //   messages: [{
      //     id: Date.now() + Math.random(), // ⭐ 唯一ID
      //     type: "markdown",
      //     isUser: false,
      //     role: "AI",//角色：AI 或 User
      //     content: "你好",
      //     time: Date.now(),
      //     loading: false,
      //     messageIndex // ⭐ 命中的消息位置

      //   }],
      //   messageIndexCounter: 1 
      // }
    ],
    currentSessionId: null,
    keyword: "" // ⭐ 搜索关键词
  }),

  getters: {
    // 获取当前会话对象
    currentSession(state) {
      return state.sessions.find(s => s.id === state.currentSessionId)
    },
    // 获取当前会话的消息列表
    currentMessages() {
      return this.currentSession?.messages || []
    },
    // ⭐ 搜索后的会话列表
    searchResults(state) {
      if (!state.keyword) return []

      const keyword = state.keyword.toLowerCase()
      const results = []

      state.sessions.forEach(session => {
        // ⭐ 1. 标题匹配
        if (session.title?.toLowerCase().includes(keyword)) {
          results.push({
            id: session.id,
            title: session.title,
            matchType: "title"
          })
        }

        // ⭐ 2. 消息匹配
        session.messages.forEach((msg, index) => {
          if (msg.content?.toLowerCase().includes(keyword)) {
            results.push({
              id: session.id,
              title: session.title,
              matchType: "message",
              message: {
                messageIndex: index
              }
            })
          }
        })
      })

      return results
    }
  },

  actions: {
    createSession() {
      const id = uuidv4()
      this.sessions.push({
        id,
        title: "新对话",
        createdAt: Date.now(),
        matchType: "title" | "message",
        messages: [
          {
            type: "text",
            isUser: false,
            role: "AI",
            content: "你好 👋 我是你的 AI 助手",
            // RAG引用
            sources: [],
            // Tool调用
            tools: [],
            // Graph状态
            status: "",
            // 是否正在调用Tool
            runningTool: null,
            time: Date.now(),
            loading: false,
            id: Date.now() + Math.random(), // ⭐ 唯一ID
            messageIndex: 0, // ⭐ 命中的消息位置
          }
        ],
        // messageIndex 应该由 session 内的计数器统一生成
        messageIndexCounter: 1 // ✅ 从1开始
      })
      this.currentSessionId = id
    },
    switchSession(id) {
      this.currentSessionId = id
    },
    getCurrentSession() {
      const session = this.sessions.find(
        s => s.id === this.currentSessionId
      )

      if (!session) {
        console.warn("⚠️ 当前 session 不存在")
        return {
          id: null,
          title: "新会话",
          messages: []
        }
      }

      return session
    },
    getNextMessageIndex() {
      const session = this.getCurrentSession()
      if (!session) return 0

      const index = session.messageIndexCounter
      session.messageIndexCounter++

      return index
    },
    deleteSession(id) {
      this.sessions = this.sessions.filter(s => s.id !== id)
      // 如果删除的是当前会话，切换到第一个会话（如果有的话）
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
    // 更新 AI 消息（流式更新）
    updateAIMessage(event) {
      const msgs = this.currentMessages

      if (!msgs.length) return

      const ai = msgs[msgs.length - 1]

      switch (event.type) {

        // =========================
        // Token
        // =========================
        case "token":

          ai.content += event.content || ""

          break

        // =========================
        // Sources
        // =========================
        case "sources":

          ai.sources = normalizeSources(getEventSources(event))

          break

        // =========================
        // Tool Start
        // =========================
        case "tool_start":

          ai.runningTool = event.tool_name

          ai.status = "tool_running"

          break

        // =========================
        // Tool End
        // =========================
        case "tool_end":

          ai.runningTool = null

          ai.status = "tool_finished"

          break

        // =========================
        // Graph Start
        // =========================
        case "graph_start":

          ai.status = "thinking"

          break

        // =========================
        // Graph End
        // =========================
        case "graph_end":

          ai.status = "finished"

          break
      }
    },
    // 结束 AI 消息（流式更新结束）
    finishAIMessage(event = {}) {
      console.log(event,'finishAIMessage')
      const msgs = this.currentMessages

      if (!msgs.length) return

      const ai = msgs[msgs.length - 1]

      ai.loading = false

      ai.status = "finished"

      if (event.sources) {

        ai.sources = normalizeSources(event.sources)

      }

      if (event.answer) {

        ai.content = event.answer

      }

    },
    updateSessionTitle(sessionId, title) {
      const session = this.sessions.find(s => s.id === sessionId);
      if (session) {
        session.title = title;
      }
    },
    setKeyword(keyword) {
      this.keyword = keyword
    }
  }
})
