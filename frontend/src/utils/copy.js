// 为什么不直接用组件？因为：v-html 渲染的内容 ≠ Vue组件👉 Vue 不会解析它
export const addCopyButtons = () => {
  const blocks = document.querySelectorAll("pre code")

  blocks.forEach((block) => {
    const pre = block.parentElement

    if (pre.querySelector(".copy-btn")) return

    const button = document.createElement("button")
    button.className = "copy-btn"
    button.innerText = "复制"

    button.onclick = async () => {
      await navigator.clipboard.writeText(block.innerText)
      button.innerText = "✓"
      setTimeout(() => (button.innerText = "复制"), 1500)
    }

    pre.style.position = "relative"
    pre.appendChild(button)
  })
}