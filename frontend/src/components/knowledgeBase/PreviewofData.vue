<template>
    <div>
      <h3>资料预览</h3>
      <div v-if="!kbStore.currentId" class="view-empty" >
        <ViewEmpty />
      </div>
      <div v-else>
        <!-- 这里可以根据 kbStore.currentId 显示对应的资料内容 -->
        <p>显示 ID 为 {{ kbStore.currentId }} 的资料内容...</p>
        <p>标题: {{ currentDetail?.title }}</p>
        <p>文件描述: {{ currentDetail?.description }}</p>
        <div v-if="currentDetail?.file_id">
          <p>文件 ID: {{ currentDetail.file_id }}</p>
          <div>文件内容: {{ currentDetail.file?.content }}</div>
        </div>
      </div>
    </div>
</template>
<script setup>
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";
import ViewEmpty from "@/components/knowledgeBase/viewEmpty.vue";
import { getKnowledgeDetail } from "@/api/modules/knowledge.js";
import { storeToRefs } from "pinia";
import { getKnowledge } from "@/api/modules/knowledge.js";
const kbStore = useKnowledgeBaseStore();
const { currentDetail } = storeToRefs(kbStore);

</script>