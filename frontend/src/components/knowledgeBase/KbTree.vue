<template>
  <div class="kb-node">
    <!-- 当前节点 -->
    <div class="node-row">
      <span> {{ node.type === "file" ? "📄" : "📁" }} {{ node.title }} </span>

      <!-- ✅ 只有文件才显示按钮 -->
      <div  class="actions">
        <n-button class="btn-primary" @click="handleKnowledgeBaseModal('add')"> + 新建 </n-button>
        
        <n-button class="edit-btn" ghost size="small" @click="handleKnowledgeBaseModal('edit', node.id)">
          编辑
        </n-button>
        <n-button ghost size="small" type="error" @click="remove(node.id)">
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
    <KnowledgeModal
      v-model:show="showModal"
      :isEdit="isEdit"
    />
</template>

<script setup>
import { ref, computed } from "vue";
import KnowledgeModal from "@/components/knowledgeBase/KnowledgeModal.vue";
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";

const store = useKnowledgeBaseStore();

const props = defineProps({
  node: Object,
});

const children = computed(() => store.getChildren(props.node.id));

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
.edit-btn,.btn-primary {
  position: relative;
  overflow: hidden;
  color: #fff;
}

.edit-btn:hover,.btn-primary:hover {
  color: #6edcff;
}

.edit-btn:hover::after,.btn-primary:hover::after {
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
