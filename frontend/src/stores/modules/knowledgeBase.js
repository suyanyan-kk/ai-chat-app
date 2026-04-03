import { defineStore } from "pinia"
import { v4 as uuidv4 } from "uuid"

export const useKnowledgeBaseStore = defineStore("knowledgeBase", {
  state: () => ({
    list: [
      { id: 1, title: "AI", parentId: null, type: "folder", open: false },
      { id: 2, title: "langchain", parentId: 1, type: "folder", open: false },
      { id: 3, title: "output.md", parentId: 2, type: "file", content: "xxx" }
    ]
  }),

  getters: {
    rootList: (state) => state.list.filter(i => i.parentId === null),

    getChildren: (state) => (parentId) =>
      state.list.filter(i => i.parentId === parentId),

    getNodeById: (state) => (id) =>
      state.list.find(i => i.id === id)
  },

  actions: {
    // ✅ 新增
    addNode({ title, type, parentId, content = "" }) {
      this.list.push({
        id: uuidv4(),
        title,
        type,
        parentId,
        open: false,
        content: type === "file" ? content : undefined
      })
    },

    // ✅ 删除（递归）
    deleteNode(id) {
      const deleteIds = [id]
      const findChildren = (pid) => {
        this.list.forEach(item => {
          if (item.parentId === pid) {
            deleteIds.push(item.id)
            if (item.type === "folder") {
              findChildren(item.id)
            }
          }
        })
      }

      findChildren(id)

      this.list = this.list.filter(i => !deleteIds.includes(i.id))
    },

    // ✅ 编辑（统一）
    updateNode(id, data) {
      const node = this.getNodeById(id)
      if (!node) return
      Object.assign(node, data)
    },

    // ✅ 展开/折叠
    toggleFolder(id) {
      const node = this.getNodeById(id)
      if (node && node.type === "folder") {
        node.open = !node.open
      }
    }
  }
})