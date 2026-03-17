<!-- src/views/about.vue -->
<template>
  <div class="about-page">

    <div class="about-visual">
      <div class="glow-ring"></div>
      <div class="glow-dot"></div>
    </div>
  </div>
</template>

<script setup>
// 无须脚本
</script>

<style scoped>
.about-page {
  min-height: 100%;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 32px;
  align-items: start;
}

</style>