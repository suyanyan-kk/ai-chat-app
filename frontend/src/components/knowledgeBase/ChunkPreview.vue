<template>
  <div class="chunk-page">
    <!-- 顶部 -->
    <div class="page-header">
      <div>
        <h2>🧩 Chunk Preview</h2>
        <p class="sub">查看文件切片结果与 metadata</p>
      </div>

      <div class="stats">共 {{ chunkList.length }} 个 Chunk</div>
    </div>

    <!-- 空状态 -->
    <div v-if="!chunkList.length" class="empty">暂无 Chunk 数据</div>

    <!-- Chunk 列表 -->
    <div v-for="item in chunkList" :key="item.id" class="chunk-card">
      <!-- 卡片头部 -->
      <div class="chunk-top">
        <div class="left">
        
          <div class="chunk-index">#chunk_index：{{ item.chunk_index }}</div>
          <div class="chunk-index">#file_id：{{ item.file_id }}</div>

          <div class="section">
            {{ item.meta_info.section }}
          </div>
        </div>

        <div class="status" :class="item.embedding_status">
          {{ item.embedding_status }}
        </div>
      </div>

      <!-- 内容 -->
      <div class="content-wrapper">
        <pre class="chunk-content"
          >{{ item.content }}
        </pre>
      </div>

      <!-- metadata -->
      <div class="meta-box">
        <div class="meta-item">
          <span class="label">Source</span>
          <span class="value">
            {{ item.meta_info.source }}
          </span>
        </div>

        <div class="meta-item">
          <span class="label">File Type</span>
          <span class="value">
            {{ item.meta_info.file_type }}
          </span>
        </div>

        <div class="meta-item">
          <span class="label">Splitter</span>
          <span class="value">
            {{ item.meta_info.splitter }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getChunks } from "@/api/modules/knowledge.js";
import { storeToRefs } from "pinia";

import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";

const kbStore = useKnowledgeBaseStore();

const { currentId } = storeToRefs(kbStore);

const chunkList = ref([]);

async function loadChunks(fileId) {
  const res = await getChunks(fileId);

  chunkList.value = res.data;
}

onMounted(() => {
  loadChunks(currentId.value);
});
</script>

<style scoped>
.chunk-page {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
  background: #f6f8fb;
} /* 顶部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.page-header h2 {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  color: #1f2937;
}
.sub {
  margin-top: 6px;
  color: #6b7280;
  font-size: 14px;
}
.stats {
  background: white;
  border-radius: 12px;
  padding: 10px 16px;
  font-size: 14px;
  color: #374151;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
} /* 空状态 */
.empty {
  padding: 60px 0;
  text-align: center;
  color: #9ca3af;
  font-size: 15px;
} /* 卡片 */
.chunk-card {
  background: white;
  border-radius: 18px;
  padding: 18px;
  margin-bottom: 20px;
  border: 1px solid #eef2f7;
  transition: all 0.2s ease;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}
.chunk-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
} /* 顶部 */
.chunk-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.chunk-index {
  background: #111827;
  color: white;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}
.section {
  font-size: 15px;
  font-weight: 600;
  color: #374151;
} /* 状态 */
.status {
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}
.pending {
  background: #fef3c7;
  color: #92400e;
}
.success {
  background: #dcfce7;
  color: #166534;
}
.failed {
  background: #fee2e2;
  color: #991b1b;
} /* 内容 */
.content-wrapper {
  margin-bottom: 16px;
}
.chunk-content {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.8;
  background: #f9fafb;
  border-radius: 14px;
  padding: 16px;
  font-size: 14px;
  color: #1f2937;
  overflow-x: auto;
} /* metadata */
.meta-box {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.meta-item {
  background: #f3f4f6;
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.label {
  color: #6b7280;
}
.value {
  color: #111827;
  font-weight: 500;
}
</style>
