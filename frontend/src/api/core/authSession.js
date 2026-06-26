const REFRESH_URL = "/api/auth/refresh"

let accessToken = null
let refreshPromise = null


export const getAccessToken = () => accessToken


export const setAccessToken = (token) => {
  accessToken = token || null
}


export const clearAccessToken = () => {
  accessToken = null
}

 
export const refreshAccessToken = async () => {
  if (refreshPromise) {
    return refreshPromise
  }

  refreshPromise = fetch(REFRESH_URL, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    }
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error("登录状态已失效")
      }

      const data = await response.json()
      setAccessToken(data.access_token)

      return data
    })
    .catch((error) => {
      clearAccessToken()
      throw error
    })
    .finally(() => {
      refreshPromise = null
    })

  return refreshPromise
}
