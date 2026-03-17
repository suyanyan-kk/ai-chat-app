import { marked } from "marked"
import hljs from "highlight.js"
import "highlight.js/styles/github.css"

marked.setOptions({
  highlight: function (code, lang) {
    return hljs.highlightAuto(code).value
  }
})

export function renderMarkdown(content) {
  return marked.parse(content)
}