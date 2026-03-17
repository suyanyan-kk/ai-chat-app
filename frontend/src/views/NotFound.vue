<!-- src/views/NotFound.vue -->
<template>
  <div class="not-found">
    <h1>404 - 页面未找到</h1>
    <p>抱歉，你访问的页面不存在。</p>
    <router-link to="/">返回首页</router-link>
  </div>
</template>

<script setup>
// 可选：添加页面逻辑
</script>

<style scoped>
.not-found {
  text-align: center;
  padding: 2rem;
}
.not-found h1 {
  font-size: 2rem;
  color: #ff6b6b;
}
.not-found p {
  margin: 1rem 0;
}
</style>