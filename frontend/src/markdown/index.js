
import MarkdownIt from "markdown-it"
import hljs from "highlight.js"

const md = new MarkdownIt({
  highlight: function (code, lang) {
    let validLang = hljs.getLanguage(lang) ? lang : "plaintext"

    let highlighted = hljs.highlight(code, { language: validLang }).value

    return `
      <div class="code-block" >
        <div class="code-header">
          <span class="lang"> ${validLang}</span>
          <button class="copy-btn"  data-code="${encodeURIComponent(code)}">复制</button>
        </div>
         <pre><code class="hljs language-${validLang}">${highlighted}</code></pre>
      </div>
    `
  }
})
// 如果文本中包含 console.log 但没有代码块标记，则自动添加 ```js ``` 标记
function fixMarkdown(content) {
  if (content.includes("console.log") && !content.includes("```")) {
    return "```js\n" + content + "\n```"
  }
  return content
}
export const renderMarkdown = (content) => {
  return md.render(fixMarkdown(content))
}