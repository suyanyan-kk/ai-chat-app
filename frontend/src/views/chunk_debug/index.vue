<template>
  <div class="page">
    <div class="header">
      <h2>Chunk 调试中心</h2>
    </div>

    <!-- 搜索 -->
    <div class="search-box chat-input">
      <n-input
        v-model:value="query"
        placeholder="输入问题测试召回..."
        size="large"
        rounded
        class="ask-input"
      />
      <div class="btn-group">
           <!-- 检索调试 -->
      <n-button type="primary" @click="handleSearch"> 检索调试搜索 </n-button>
      <!-- 查看某个文件 chunk -->

      <n-button trong secondary type="primary" @click="handleGetChunksID"> 查看某个文件 chunk </n-button>
      <!-- # 查看全部 chunk -->
      <n-button trong secondary type="primary" @click="handleGetAllChunks"> 查看全部 chunk </n-button>
      <!-- 清空 -->
      <n-button strong secondary type="info" @click="handleClear"> 清空 </n-button>
      </div>
 
    </div>

    <!-- 结果 -->
    <div class="result">
      <div class="result-list">
        <div class="result-item" v-for="item in resultList" :key="item.id">
          <div class="top">
            <div>
              文件 ID:
              {{ item.metadata?.file_id||'未知文件ID' }}
            </div>

            <div class="score">
              Score:
              {{ item.score }}
            </div>
          </div>

          <div class="content">
            {{ item.content }}
          </div>

          <div class="meta">
            <div>
              文件:
              {{ item.metadata.file_name||'未知文件' }}
            </div>

            <div>
              某个文件的切片ID Chunk Index:
              {{ item.metadata.chunk_index }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useMessage } from "naive-ui";
import { getChunksID, chunkSearch, getAllChunks } from "@/api/modules/chunkSearch.js";

const message = useMessage();

const query = ref("");

const resultList = ref([]);

// 查看某个文件 chunk
const handleGetChunksID = async () => {
  resultList.value = [];
  if (!query.value) {
    return message.warning("请输入文件ID");
  } 

  const res = await getChunksID(query.value);
  if (res.code !== 0) {
    return message.error(res.data.message || "获取文件chunk失败");
  } else {
    message.success("获取文件chunk成功");
    resultList.value = res.data;
  }
};

// 查看全部 chunk
const handleGetAllChunks = async () => {
  resultList.value = [];
  const res = await getAllChunks();
  if (res.code !== 0) {
    return message.error(res.data.message || "获取所有chunk失败");
  } else {
    message.success("获取所有chunk成功");
    resultList.value = res.data;
  }
};

const handleSearch = async () => {
  resultList.value = [];
  if (!query.value) {
    return message.warning("请输入问题");
  }

  const res = await chunkSearch(query.value, 10);
  if (res.code !== 0) {
    return message.error(res.data.message || "搜索失败");
  } else {
    message.success("搜索成功");
    resultList.value = res.data;
  }
};

const handleClear = () => {
  resultList.value = [];
  query.value = "";
};

</script>

<style scoped>
.page {
  padding: 20px;
}
.header{
  margin-bottom: 20px;
}
.chat-input {
  display: flex;
  gap: 12px;
  /* padding-top: 10px; */
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  color: rgba(244, 248, 255, 0.92);
}

.chat-input :deep(.n-input) {
  /* flex: 1; */
  width: 600px;
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
  color: rgba(244, 248, 255, 0.92);
  font-size: 1rem;
  outline: none;
  text-align: left;
}
.chat-input :deep(.n-input__input-el),
.chat-input :deep(.n-input__textarea-el) {
  color: rgba(244, 248, 255, 0.92) !important; /* 输入文字 */
  padding: 6px 5px !important;
  line-height: 1.9;
}

.chat-input :deep(.n-input__placeholder) {
  color: rgba(255, 255, 255, 0.4) !important; /* placeholder */
}

/* .chat-input input {
  flex: 1;
} */
.chat-input input:focus {
  border-color: rgba(130, 118, 255, 0.55);
  box-shadow: 0 0 0 2px rgba(130, 118, 255, 0.24);
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.btn-group{
  display: flex;
  gap: 10px;
}
.result {
  height: 75vh;
  overflow-y: auto;
}
.result-list {
  height: 100%;
}
.result-item {
  padding: 16px;
  border-radius: 12px;
  background: #1e1e1e;
  margin-bottom: 16px;
  border: 1px solid #333;
}

.top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.score {
  color: #18a058;
}

.content {
  line-height: 1.8;
  white-space: pre-wrap;
  margin-bottom: 12px;
}

.meta {
  display: flex;
  gap: 20px;
  color: #999;
  font-size: 13px;
}
</style>
