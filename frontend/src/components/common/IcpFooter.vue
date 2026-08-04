<template>
  <footer
    :class="['icp-footer', `icp-footer--${variant}`]"
    aria-label="备案信息"
  >
    <span>技术分享 · yanaihub.cn</span>
    <a
      href="https://beian.miit.gov.cn/"
      target="_blank"
      rel="noopener noreferrer"
    >
      京ICP备2026046046号-1
    </a>
  </footer>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: "dark",
    validator: (value) => ["dark", "light"].includes(value)
  }
});
</script>

<style scoped>
.icp-footer {
  width: 100%;
  min-height: 42px;
  padding: 10px 18px calc(10px + env(safe-area-inset-bottom));
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px 12px;
  text-align: center;
  font-size: 12px;
  line-height: 1.5;
  letter-spacing: 0;
}

.icp-footer a {
  color: inherit;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.18s ease, opacity 0.18s ease;
}

.icp-footer a:hover {
  opacity: 0.82;
}

.icp-footer--dark {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(8, 12, 27, 0.44);
  color: rgba(238, 241, 255, 0.58);
}

.icp-footer--dark a {
  color: rgba(238, 241, 255, 0.78);
}

.icp-footer--light {
  color: #667068;
}

.icp-footer--light a {
  color: #1f6d3d;
}

@media (max-width: 520px) {
  .icp-footer {
    min-height: 50px;
    padding-inline: 14px;
    gap: 2px 8px;
    font-size: 11px;
  }
}
</style>
