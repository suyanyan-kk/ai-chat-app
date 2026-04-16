<template>
  <div class="kb-node">
    <!-- 当前节点 -->
    <div class="node-row" @click="handleClick">
      <span> {{ node.type === "file" ? "📄" : "📁" }} {{ node.title }} </span>

      <!-- ✅ 只有文件才显示按钮 v-if="node.type === 'file'"-->
      <div class="actions" >
        <n-button
          class="btn-primary"
          ghost
          type="primary"
          :parentId="node.parentId"
          @click="handleKnowledgeBaseModal('add')"
        >
          + 新建子目录
        </n-button>

        <n-button
          class="edit-btn"
          color="#fff"
          ghost
          size="small"
          @click="handleKnowledgeBaseModal('edit', node.id)"
        >
          编辑
        </n-button>
        <n-button
          class="error-btn"
          ghost
          size="small"
          type="error"
          @click="remove(node.id)"
        >
          删除
        </n-button>
      </div>
    </div>

    <!-- 子节点 -->
    <div v-if="children.length">
      <KbTree v-for="child in children" :key="child.id" :node="child" />
    </div>
  </div>
  <!-- 新增编辑弹窗组件 -->
  <KnowledgeModal v-model:show="showModal" :isEdit="isEdit" :parentId="node.parentId"/>
</template>

<script setup>
import { ref, computed } from "vue";
import KnowledgeModal from "@/components/knowledgeBase/KnowledgeModal.vue";
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";

const store = useKnowledgeBaseStore();
const showModal = ref(false);
const isEdit = ref(false);
const props = defineProps({
  node: Object,
});

const children = computed(() => store.getChildren(props.node.id));
// 👉 点击文件夹展开/折叠
const handleClick = () => {
  if (props.node.type === "folder") {
    store.toggleFolder(props.node.id)
  }
}
const handleKnowledgeBaseModal = (type) => {
  if (type === "add") {
    // 新增
    isEdit.value = false;
  } else {
    // 编辑
    isEdit.value = true;
  }
  showModal.value = true;
};
const remove = (id) => {
  store.deleteNode(id);
};
</script>

<style scoped>
/* 列表 */
.kb-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.kb-item {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  border-radius: 12px;

  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);

  transition: all 0.2s;
}

.kb-item:hover {
  border: 1px solid #4f8cff;
  box-shadow: 0 0 10px rgba(79, 140, 255, 0.3);
}
.node-row:hover {
  background: rgba(79, 140, 255, 0.08);
  border-radius: 6px;
}
.info h3 {
  margin: 0;
}

.info p {
  margin-top: 6px;
  color: #aaa;
  font-size: 13px;
}
.kb-node {
  margin-left: 10px;
}
.actions {
  display: flex;
  gap: 8px;
}
.edit-btn {
  position: relative;
  overflow: hidden;
  color: #fff;
}
.btn-primary {
  position: relative;
  overflow: hidden;
}
.edit-btn,
.btn-primary,
.error-btn {
  outline: none !important;
}

/* 🔥 取消点击后的 focus 高亮 */
.btn-primary:focus,
.btn-primary:focus-visible,
.edit-btn:focus,
.edit-btn:focus-visible,
.error-btn:focus,
.error-btn:focus-visible {
  outline: none !important;
  box-shadow: none !important;
  border-color: #fff !important;
}
.edit-btn:hover,
.btn-primary:hover {
  color: #6edcff;
}

.edit-btn:hover::after,
.btn-primary:hover::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: 1px solid rgba(110, 220, 255, 0.6);
  box-shadow: 0 0 10px rgba(110, 220, 255, 0.4);
  pointer-events: none;
}
.node-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
}

.children {
  margin-left: 16px;
  border-left: 1px dashed rgba(255, 255, 255, 0.1);
  padding-left: 10px;
}
</style>
