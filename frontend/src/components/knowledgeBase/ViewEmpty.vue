<template>
    <div>
     <div class="empty-container">
        <div class="content">
          <div class="icon">📄</div>

          <h2 class="title">暂无内容</h2>

          <p class="desc">请选择左侧文件，或新建一个文档开始记录 ✨</p>

          <div class="actions">
            <n-button type="primary" size="small" @click="createFile">
              新建文件
            </n-button>

            <n-button size="small" @click="createFolder"> 新建文件夹 </n-button>
          </div>
        </div>
      </div>
        <!-- 新建弹窗组件 -->
    <KnowledgeModal
      v-model:show="showModal"
      :type="type"
      :parentId="null"
    />
    </div>
</template>
<script setup>
import KnowledgeModal from "@/components/knowledgeBase/KnowledgeModal.vue";
import { ref } from "vue"; 
const showModal = ref(false);
const type = ref("file"); // 用于区分是新建文件还是目录

function createFile() {
  type.value = "file";
  showModal.value = true;
}
function createFolder() {
  type.value = "folder";
  showModal.value = true;
}
</script>
<style scoped>
/* 资料视图 */

.empty-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  /* background: #0d0d0d; */
}

/* 内容卡片 */
.content {
  text-align: center;
  color: #888;
  padding-top: 40px;
}
/* 图标 */
.icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.6;
}

/* 标题 */
.title {
  font-size: 20px;
  color: #ddd;
  margin-bottom: 8px;
}

/* 描述 */
.desc {
  font-size: 14px;
  margin-bottom: 20px;
}
/* 按钮 */
.actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}
</style>