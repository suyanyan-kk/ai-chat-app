<template>
  <div class="kb-page">
    <!-- 头部 -->
    <div class="kb-header">
      <div>
        <h2>📚 资料库</h2>
        <p class="sub">Knowledge Base</p>
      </div>

      <n-button class="btn-primary" ghost type="primary" @click="handleKnowledgeBaseModal('add')"> + 新建目录 </n-button>
    </div>

    <!-- 搜索 -->
    <div class="search-box">
      <n-input v-model:value="keyword" placeholder="🔍 搜索资料..." clearable />
    </div>

    <!-- 列表 -->
    <div class="kb-list">
      <KbTree
        v-for="item in list"
        :key="item.id"
        :node="item"
      />
    </div>
     <!-- 新增编辑弹窗组件 -->
    <KnowledgeModal
      v-model:show="showModal"
      :isEdit="isEdit"
      :parentId="null"
    />
  
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import KbTree from "@/components/knowledgeBase/KbTree.vue";
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase"
import KnowledgeModal from "@/components/knowledgeBase/KnowledgeModal.vue";
import { storeToRefs } from "pinia"
const kbStore = useKnowledgeBaseStore()
const keyword = ref("");
const showModal = ref(false);
const isEdit = ref(false);
// 表单数据 俩种响应式
const list = computed(() => kbStore.buildTree)
//  list: [
//       { id: 1, title: "AI", parentId: null, type: "folder", open: false },
//       { id: 2, title: "langchain", parentId: 1, type: "folder", open: false },
//       { id: 3, title: "output.md", parentId: 2, type: "file", content: "xxx" }
//     ]
  // tree: [
    //   {
    //     id: 1, title: "AI", parentId: null, type: "folder", description: '', open: false,
    //     children: [{
    //       id: 2, title: "langchain", parentId: 1, type: "folder", description: '', open: false,
    //       children: [
    //         { id: 3, title: "output.md", parentId: 2, type: "file", description: '', content: "xxx" }
    //       ]
    //     }]
    //   },
    // ]
const handleKnowledgeBaseModal = (type) => {
    if(type === 'add') {
        // 新增
        isEdit.value = false;
    } else {
        // 编辑
        isEdit.value = true;
    }
    showModal.value = true;
};
</script>

<style scoped>
.kb-page {
  padding: 20px;
  color: #fff;
}

/* 头部 */
.kb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sub {
  font-size: 12px;
  color: #888;
}

/* 科技按钮 */
.btn-primary {
  position: relative;
  overflow: hidden;
  /* color: #fff; */
}

.btn-primary:hover {
  color: #6edcff;
}
.btn-primary {
  outline: none !important;
}
.btn-primary:focus,
.btn-primary:focus-visible{
  outline: none !important;
  box-shadow: none !important;
}
/* 🔥 针对 Naive UI 内部按钮 */
.btn-primary :deep(.n-button:focus),
.btn-primary :deep(.n-button:focus-visible) {
  box-shadow: none !important;
  outline: none !important;
}
/* 🔥 再补一刀（有些主题用这个类） */
.btn-primary :deep(.n-button--focus) {
  box-shadow: none !important;
}
.btn-primary:hover::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: 1px solid rgba(110, 220, 255, 0.6);
  box-shadow: 0 0 10px rgba(110, 220, 255, 0.4);
  pointer-events: none;
}


/* 搜索框科技风 */
.search-box {
  margin: 15px 0;
}

.search-box :deep(.n-input) {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  backdrop-filter: blur(6px);
}
</style>
