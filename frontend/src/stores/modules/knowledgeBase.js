import { defineStore } from "pinia"
import { v4 as uuidv4 } from "uuid"
export const useKnowledgeBaseStore = defineStore("knowledgeBase", {
  state: () => ({
    list: [
      { id: 1, title: "AI", parent_id: null, type: "folder", description: '', is_open: false, file_id: 1 },
      { id: 2, title: "langchain", parent_id: 1, type: "folder", description: '', is_open: false, file_id: 2 },
      { id: 3, title: "output.md", parent_id: 2, type: "file", description: '', content: "xxx", file_id: 3 }//content上传文件的数据
    ],
    currentId: null,//当前选中项 
    currentDetail: null,//当前详情 包含树信息和文件信息
    // tree: [
    //   {
    //     id: 1, title: "AI", parent_id: null, type: "folder", description: '', is_open: false,
    //     children: [{
    //       id: 2, title: "langchain", parent_id: 1, type: "folder", description: '', is_open: false,
    //       children: [
    //         { id: 3, title: "output.md", parent_id: 2, type: "file", description: '', content: "xxx" }
    //       ]
    //     }]
    //   },
    // ]
  }
  ),

  getters: {
    buildTree(state) {
      const map = {}
      const tree = []
      const validList = state.list.filter(item => item && item.id != null)
      console.log("原始 list 👉", state.list)
      validList.forEach(item => {
        map[item.id] = { ...item, children: [] }
      })

      validList.forEach(item => {
        const node = map[item.id]

        if (item.parent_id === null || !map[item.parent_id]) {
          tree.push(node)
        } else {
          map[item.parent_id].children.push(node)
        }
      })
      // console.log("tree", tree)
      return tree

    },
    rootList: (state) => state.list.filter(i => i.parent_id === null),

    getChildren: (state) => (id) => {
      // debugger
      console.log("========= 我执行了！id =", id);
      console.log("list:", state.list)
      if (!Array.isArray(state.list)) return []
      if (id === null) return []
      return state.list.filter(i => i && i.parent_id === id)
    },

    getNodeById: (state) => (id) =>
      state.list.find(i => i.id === id),

    // currentItem: (state) => {
    //   return state.list.find(i => i.id === state.currentId) || null
    // }
  },

  actions: {
    // ✅ 设置数据（入口）list是接口返回的列表数据
    setList(list) {
      this.list = list
    },
    // // ✅ 新增
    addNode(obj) {
      console.log("addNode obj:", obj)
      this.list.push(obj)
    },
    getcurrentDetail(data) {
      this.currentDetail = data
    },
    setCurrentId(id) {
      this.currentId = id
    },
    // ✅ 删除（递归）
    deleteNode(id) {
      const deleteIds = [id]
      const findChildren = (pid) => {
        this.list.forEach(item => {
          if (item.parent_id === pid) {
            deleteIds.push(item.id)
            if (item.type === "folder") {
              findChildren(item.id)
            }
          }
        })
      }

      findChildren(id)
      // ⭐ 如果当前选中的节点被删了
      if (deleteIds.includes(this.currentId)) {
        const remainList = this.list.filter(
          item => !deleteIds.includes(item.id)
        )

        this.currentId = remainList[0]?.id || null
      }
      this.list = this.list.filter(i => !deleteIds.includes(i.id))

    },

    // ✅ 展开/折叠
    toggleFolder(id) {
      const node = this.getNodeById(id)
      if (node && node.type === "folder") {
        node.is_open = !node.is_open
      }
    }
  }
})