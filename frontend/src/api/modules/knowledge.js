import { get,post,del } from "../core/request"
// 获取知识库列表
export const getKnowledge = (message) => {
  return get("/getKnowledge")
}

export const getKnowledgeDetail = (id) => {
  return get(`/getKnowledgeDetail/${id}`)
}
// 新增知识库项
export const addKnowledge = (data) => {
  return post("/addKnowledge",data)
}

export const deleteKnowledge = (id) => {
  return del("/deleteKnowledge/" + id)
}

// 上传文件
export const uploadFile = (file) => {
  const formData = new FormData()
  formData.append("file", file)
  return post("/uploadKnowledgeFile", formData)
}
// chunk preview
export const getChunks = (fileId) => {
  return get(`/chunks/${fileId}`)
}