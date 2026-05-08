// ⭐ 核心请求（带拦截器）
import { InterceptorManager } from "./interceptor"

const BASE_URL = "/api"

const requestInterceptors = new InterceptorManager()
const responseInterceptors = new InterceptorManager()

// ⭐ 注册默认拦截器（自动加 token）
requestInterceptors.use(async (config) => {
  const token = localStorage.getItem("token")

  const headers = {
    ...(config.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }

  // ⭐ FormData 不要设置 Content-Type
  if (!(config.body instanceof FormData)) {
    headers["Content-Type"] = "application/json"
  }

  return {
    ...config,
    headers
  }
})

// ⭐ 请求日志
requestInterceptors.use(async (config) => {
  console.log("📤 请求:", config)
  return config
})

// ⭐ 响应日志
responseInterceptors.use(async (res) => {
  console.log("📥 响应:", res)
  return res
})

// ⭐ 错误统一处理
responseInterceptors.use(async (res) => {
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || "请求失败")
  }

  return res
})

export async function request(url, options = {}) {
  let config = {
    url: BASE_URL + url,
    method: "GET",
    ...options
  }

  // 👉 执行请求拦截
  config = await requestInterceptors.run(config)

  let response

  try {
    response = await fetch(config.url, config)
  } catch (err) {
    console.error("❌ 网络错误:", err)
    throw err
  }

  // 👉 执行响应拦截
  response = await responseInterceptors.run(response)

  return response.json()
}

// 👉 GET
export const get = (url) => request(url)

// 👉 POST（自动判断 JSON / FormData）
export const post = (url, data) => {
  const isFormData = data instanceof FormData

  return request(url, {
    method: "POST",
    body: isFormData ? data : JSON.stringify(data)
  })
}

// 👉 PUT
export const put = (url, data) => {
  const isFormData = data instanceof FormData

  return request(url, {
    method: "PUT",
    body: isFormData ? data : JSON.stringify(data)
  })
}

// 👉 DELETE
export const del = (url) =>
  request(url, {
    method: "DELETE"
  })

// 👉 暴露拦截器
export const interceptors = {
  request: requestInterceptors,
  response: responseInterceptors
}