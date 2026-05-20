<template>
  <div class="page">

    <div class="header">
      <h2>Chunk 调试中心</h2>
    </div>

    <!-- 搜索 -->
    <div class="search-box">

      <n-input
        v-model:value="query"
        placeholder="输入问题测试召回..."
      />

      <n-button
        type="primary"
        @click="handleSearch"
      >
        搜索
      </n-button>

    </div>

    <!-- 结果 -->
    <div
      class="result-item"
      v-for="item in resultList"
      :key="item.id"
    >

      <div class="top">

        <div>
          Chunk ID:
          {{ item.id }}
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
          {{ item.metadata.file_name }}
        </div>

        <div>
          Chunk:
          {{ item.metadata.chunk_index }}
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from "vue"
import { useMessage } from "naive-ui"
import { getChunks, chunkSearch } from "@/api/modules/chunkSearch.js"

const message = useMessage()

const query = ref("")

const resultList = ref([])

const handleSearch = async () => {

  if (!query.value) {
    return message.warning("请输入问题")
  }

  const res = await chunkSearch(query.value, 10)
        if (res.code !== 0) {
          return message.error(res.data.message || "搜索失败")
        }else {
          message.success("搜索成功")
          resultList.value = res.data.data
        }
}
</script>

<style scoped>

.page{
  padding:20px;
}

.search-box{
  display:flex;
  gap:10px;
  margin-bottom:20px;
}

.result-item{
  padding:16px;
  border-radius:12px;
  background:#1e1e1e;
  margin-bottom:16px;
  border:1px solid #333;
}

.top{
  display:flex;
  justify-content:space-between;
  margin-bottom:10px;
}

.score{
  color:#18a058;
}

.content{
  line-height:1.8;
  white-space:pre-wrap;
  margin-bottom:12px;
}

.meta{
  display:flex;
  gap:20px;
  color:#999;
  font-size:13px;
}

</style>