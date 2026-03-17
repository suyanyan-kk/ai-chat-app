<template>
  <button class="copy-btn" @click="handleCopy">
    {{ copied ? "✓" : "复制" }}
  </button>
</template>

<script setup>
import { ref } from "vue"

const props = defineProps({
  content: {
    type: String,
    default: ""
  }
})

const copied = ref(false)

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(props.content)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 1500)
  } catch (e) {
    console.error("复制失败", e)
  }
}
</script>

<style scoped>
.copy-btn {
  position: absolute;
  top: 8px;
  right: 8px;

  padding: 4px 8px;
  font-size: 12px;

  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.1);

  background: rgba(30,30,30,0.6);
  backdrop-filter: blur(8px);

  color: rgba(255,255,255,0.8);
  cursor: pointer;

  opacity: 0;
  transition: all 0.2s ease;
}

/* hover 才显示（高级感） */
pre:hover .copy-btn {
  opacity: 1;
}
</style>