<template>
  <div v-if="visibleSources.length" class="sources">
    <div class="sources-title">引用来源</div>

    <button
      v-for="source in visibleSources"
      :key="sourceKey(source)"
      type="button"
      class="source"
      @click="openSource(source)"
    >
      <span class="source-name">{{ source.file_name || "未知文件" }}</span>
      <span v-if="formatSource(source)" class="source-meta">
        {{ formatSource(source) }}
      </span>
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"

const props = defineProps({
  sources: {
    type: Array,
    default: () => []
  }
})

const router = useRouter()

const visibleSources = computed(() => {
  return props.sources.filter(
    source => source?.file_id !== undefined && source?.file_id !== null
  )
})

const sourceKey = (source) => {
  return source.id ?? `${source.file_id}-${source.page ?? "file"}`
}

const formatSource = (source) => {
  if (source.page === undefined || source.page === null || source.page === "") {
    return ""
  }

  return `第 ${source.page} 页`
}

const openSource = (source) => {
  const query = {
    file_id: source.file_id
  }

  if (source.page !== undefined && source.page !== null && source.page !== "") {
    query.page = source.page
  }

  router.push({
    path: "/kb",
    query
  })
}
</script>

<style scoped>
.sources {
  width: 70%;
  margin-top: 10px;
  padding-left: 6px;
}

.sources-title {
  font-size: 12px;
  opacity: 0.6;
  margin-bottom: 8px;
}

.source {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 10px 12px;
  margin-bottom: 8px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.92);
  font: inherit;
  text-align: left;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.source:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-1px);
}

.source-name {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
  font-weight: 600;
}

.source-meta {
  flex-shrink: 0;
  font-size: 12px;
  opacity: 0.65;
}
</style>
