//   ⭐ 流式请求
import { fetchWithAuth } from "./request"

export async function streamRequest(url, data, onMessage) {
  const response = await fetchWithAuth(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })

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
