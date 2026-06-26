import { get, post, request } from "../core/request"


export const login = (data) => {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
    skipAuthRefresh: true
  })
}

 
export const refreshSession = () => {
  return request("/auth/refresh", {
    method: "POST",
    skipAuthRefresh: true
  })
}


export const logout = () => {
  return post("/auth/logout", {})
}


export const getCurrentUser = () => {
  return get("/auth/me")
}
