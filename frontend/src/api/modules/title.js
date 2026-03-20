import { post } from "../core/request"

export const generateTitle = (message) => {
  return post("/generate_title", { message })
}