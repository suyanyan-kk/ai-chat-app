// 封装聊天响应请求  axios 不适合 streaming，使用原生 fetch 实现 streaming 请求
// 普通聊天
// import request from "./request"

// export function chat(message) {
//   return request.post("/chat", { message })
// }

// 流式聊天

import { streamRequest } from "./streamRequest"

export function chatStream(message, onMessage) {
  return streamRequest("/chat-stream", { message }, onMessage)
}
