//   ⭐ 流式请求
import { interceptors } from "./request"

const BASE_URL = "/api"
export async function streamRequest(url, data, onMessage) {
  let config = {
    url: BASE_URL + url,
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  }

  // 👉 复用拦截器（关键🔥）
  config = await interceptors.request.run(config)

  const response = await fetch(config.url, config)

  if (!response.ok) {
    throw new Error(`请求失败: ${response.status}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder("utf-8")

  let buffer = ""

  while (true) {
    const { done, value } = await reader.read()

    if (done) break

    buffer += decoder.decode(value, { stream: true })

    const parts = buffer.split("\n")
    buffer = parts.pop()

    for (const part of parts) {
      if (!part.trim()) continue

      try {
        const json = JSON.parse(part)
        onMessage(json)
      } catch (e) {
        console.error("解析失败:", part)
      }
    }
  }
}