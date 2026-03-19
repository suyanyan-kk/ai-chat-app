// 使用原生 fetch 实现 streaming 请求
// 封装 streaming 请求模块
// 注意：fetch 不会自动处理 JSON 流，需要手动解析每个 chunk
// onMessage 是一个回调函数，每当接收到新的数据块时会被调用
export async function streamRequest(url, data, onMessage) {

  const response = await fetch("http://127.0.0.1:8000" + url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      session_id: data.session_id,
      message: data.message,
    })
  })
  if (!response.body) {
    throw new Error("ReadableStream not supported")
  }
  const reader = response.body.getReader()
  const decoder = new TextDecoder("utf-8")
  let buffer = ""
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value, { stream: true })
    onMessage(chunk)
  }
}