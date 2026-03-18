<!-- src/views/langchainPractice.vue -->
<template>
  <div class="langchainPractice-page">
    <n-collapse class="collapse" v-model:value="activeNames">
      <n-collapse-item title="使用提示词模版" name="1">
        使用提示词模版
        <template #header-extra> ChatPromptTemplate </template>
      </n-collapse-item>
      <n-collapse-item title="李四" name="2">
        一周小结：勤奋是获取成功的唯一捷径
        <template #header-extra> 本周工作日工作时长：62 小时 </template>
      </n-collapse-item>
    </n-collapse>
  </div>
</template>

<script setup>
import { ref } from "vue";
const activeNames = ref(["1"]);
</script>

<style scoped>
.langchainPractice-page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: start;
    padding: 24px;
    min-height: 100%;
    color: blueviolet;
}
.collapse{
    width: 100%;
    height: 100%;
    color: blueviolet;
    font-size: .4em;
}
</style>
