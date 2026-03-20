import { streamRequest } from "../core/stream"

export const chatStream = (data, onMessage) => {
  return streamRequest("/chat-stream", data, onMessage)
}