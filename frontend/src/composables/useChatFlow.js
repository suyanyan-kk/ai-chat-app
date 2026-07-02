import { ref } from "vue"

import {
  chatStream,
  generateTitle
} from "@/api"
import { useChatStore } from "@/stores/modules/chatStore"


const buildFallbackTitle = (message) => {
  const compact = message.replace(/\s+/g, " ").trim()

  return compact.length > 20
    ? `${compact.slice(0, 20)}…`
    : compact
}


export const useChatFlow = () => {
  const chatStore = useChatStore()
  const isSending = ref(false)

  const getContext = (
    sessionId,
    aiMessageId
  ) => {
    const session = chatStore.getSession(
      sessionId
    )

    return {
      sessionId,
      session,
      aiMessage: session?.messages.find(
        message => message.id === aiMessageId
      ) || null
    }
  }

  const sendMessage = async (
    rawMessage,
    options = {}
  ) => {
    const message = rawMessage?.trim()

    if (!message || isSending.value) {
      return null
    }

    isSending.value = true

    const shouldCreateSession = (
      options.newSession
      || !chatStore.currentSessionId
      || !chatStore.getSession()
    )

    const sessionId = shouldCreateSession
      ? chatStore.createSession()
      : chatStore.currentSessionId

    const session = chatStore.getSession(
      sessionId
    )
    const isFirstQuestion = !session?.messages.some(
      item => item.isUser
    )

    chatStore.addUserMessage(
      {
        type: "text",
        isUser: true,
        role: "user",
        content: message,
        time: Date.now(),
        id: Date.now() + Math.random(),
        messageIndex:
          chatStore.getNextMessageIndex(
            sessionId
          )
      },
      sessionId
    )

    const aiMessage = {
      type: "markdown",
      content: "",
      isUser: false,
      role: "AI",
      loading: true,
      status: "thinking",
      runningTool: null,
      sources: [],
      tools: [],
      time: Date.now(),
      id: Date.now() + Math.random(),
      messageIndex:
        chatStore.getNextMessageIndex(
          sessionId
        )
    }

    chatStore.addAIMessage(
      aiMessage,
      sessionId
    )

    if (isFirstQuestion) {
      chatStore.updateSessionTitle(
        sessionId,
        buildFallbackTitle(message)
      )
    }

    const initialContext = getContext(
      sessionId,
      aiMessage.id
    )

    options.onSessionReady?.(
      initialContext
    )

    try {
      await chatStream(
        {
          session_id: sessionId,
          message
        },
        (event) => {
          chatStore.handleStreamEvent(
            event,
            sessionId
          )

          options.onEvent?.(
            event,
            getContext(
              sessionId,
              aiMessage.id
            )
          )
        }
      )

      return getContext(
        sessionId,
        aiMessage.id
      )
    } catch (error) {
      chatStore.finishAIMessage(
        {
          answer: "抱歉，获取回复失败"
        },
        sessionId
      )

      options.onError?.(
        error,
        getContext(
          sessionId,
          aiMessage.id
        )
      )

      throw error
    } finally {
      if (isFirstQuestion) {
        try {
          const result = await generateTitle(
            message
          )

          if (result?.title) {
            chatStore.updateSessionTitle(
              sessionId,
              result.title
            )
          }
        } catch {
          // 已设置问题摘要作为标题，标题接口失败不影响会话。
        }
      }

      chatStore.persistSessions()
      isSending.value = false
    }
  }

  return {
    isSending,
    sendMessage
  }
}
