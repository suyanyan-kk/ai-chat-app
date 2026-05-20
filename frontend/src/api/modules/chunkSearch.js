import { get,post,del } from "../core/request"
// chunk preview
export const getChunks = (fileId) => {
  return get(`/chunks/${fileId}`)
}

// chunk search 接口，参数可以根据需要调整
export const chunkSearch = (query, top_k) => {
  return get(`/chunk/search?query=${encodeURIComponent(query)}&top_k=${top_k}`)
}
