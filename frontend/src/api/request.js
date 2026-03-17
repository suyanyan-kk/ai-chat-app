// axios 不适合 streaming
// 封装请求模块 
import axios from "axios"

const request = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 10000
})

// 请求拦截
request.interceptors.request.use(config => {
  console.log("请求发送:", config.url)
  return config
})

// 响应拦截
request.interceptors.response.use(
  res => {
    return res.data
  },
  err => {
    console.error("请求错误:", err)
    return Promise.reject(err)
  }
)

export default request