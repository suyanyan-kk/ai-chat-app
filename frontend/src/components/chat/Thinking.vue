<template>
  <div
    v-if="show"
    class="thinking"
    role="status"
    aria-live="polite"
  >
    <span class="thinking-dot" />
    <span class="thinking-text">正在思考</span>
    <span class="thinking-wave" aria-hidden="true">
      <i />
      <i />
      <i />
    </span>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean
})
</script>

<style scoped>
.thinking {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  margin: 2px 0 8px 2px;
  padding: 7px 10px;
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.055);
  color: rgba(230, 235, 255, 0.72);
  font-size: 12px;
  line-height: 1;
  letter-spacing: 0;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(10px);
}

.thinking-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #6edcff;
  box-shadow: 0 0 12px rgba(110, 220, 255, 0.75);
  animation: dot-pulse 1.4s ease-in-out infinite;
}

.thinking-text {
  white-space: nowrap;
}

.thinking-wave {
  display: inline-flex;
  align-items: flex-end;
  gap: 3px;
  height: 12px;
}

.thinking-wave i {
  display: block;
  width: 3px;
  height: 5px;
  border-radius: 999px;
  background: rgba(119, 103, 255, 0.78);
  animation: wave 0.9s ease-in-out infinite;
}

.thinking-wave i:nth-child(2) {
  animation-delay: 0.12s;
}

.thinking-wave i:nth-child(3) {
  animation-delay: 0.24s;
}

@keyframes dot-pulse {
  0%,
  100% {
    opacity: 0.55;
    transform: scale(0.86);
  }

  50% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes wave {
  0%,
  100% {
    height: 5px;
    opacity: 0.45;
  }

  50% {
    height: 11px;
    opacity: 1;
  }
}
</style>
