import { get,post,del } from "../core/request"



// 查看全部 chunk
export const getAllChunks = () => {
  return get('/chunk/all')
}
// 查看某个文件 chunk 业务接口
// export const getChunksID = (fileId) => {
//   return get(`/chunks/${fileId}`)
// }

export const getChunksID = (fileId) => {
  return get(`/chunk/file/${fileId}`)
}
// chunk search 接口，参数可以根据需要调整
export const chunkSearch = (query, top_k) => {
  return get(`/chunk/search?query=${encodeURIComponent(query)}&top_k=${top_k}`)
}

