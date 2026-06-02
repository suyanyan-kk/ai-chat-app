import { post } from "../core/request"

// 检索调试接口
export const retrievalDebug = (query) => {
  return post("/debug/retrieval", {
    query
  })
}

export const vectorDebug = (query) => {
  return post("/debug/retrieval/vector", {
    query
  })
}

export const bm25Debug = (query) => {
  return post("/debug/retrieval/bm25", {
    query
  })
}

export const rerankDebug = (query) => {
  return post("/debug/retrieval/rerank", {
    query
  })
}

export const hybridDebug = (query) => {
  return post("/debug/retrieval/hybrid", {
    query
  })
}
