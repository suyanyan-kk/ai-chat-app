<template>
  <div class="kb-page">
    <!-- 头部 -->
    <div class="kb-header">
      <div>
        <h2>📚 资料库</h2>
        <p class="sub">Knowledge Base</p>
      </div>
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
        @edit="openEdit"
        @delete="remove"
      />
    </div>

  
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import KbTree from "@/components/knowledgeBase/KbTree.vue";
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase"
const kbStore = useKnowledgeBaseStore()

const keyword = ref("");
const showModal = ref(false);
const isEdit = ref(false);
// 表单数据
const list = computed(() => kbStore.rootList)
//  list: [
//       { id: 1, title: "AI", parentId: null, type: "folder", open: false },
//       { id: 2, title: "langchain", parentId: 1, type: "folder", open: false },
//       { id: 3, title: "output.md", parentId: 2, type: "file", content: "xxx" }
//     ]


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
