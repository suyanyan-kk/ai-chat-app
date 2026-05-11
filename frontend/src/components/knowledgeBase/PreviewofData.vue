<template>
  <div class="preview-wrap">
    <div class="preview-header">
      <h2>
        {{ currentDetail?.title || "资料预览" }}
      </h2>

      <p>{{ currentDetail?.file?.description || "暂无描述" }}</p>
    </div>

   
    <div class="preview-body">
      <!-- markdown 内容 -->
      <div class="markdown-body" v-html="htmlContent" />
           <!-- 图片 -->
    <img
      v-if="isImage"
      :src="currentDetail?.file?.url"
      class="image"
    />
    <!-- pdf -->
    <iframe
      v-else-if="isPdf"
      :src="currentDetail?.file?.url"
      class="pdf"
    />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import MarkdownIt from "markdown-it";

import { storeToRefs } from "pinia";

import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";

const kbStore = useKnowledgeBaseStore();

const { currentDetail } = storeToRefs(kbStore);

// markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

// markdown -> html
const htmlContent = computed(() => {
  return md.render(currentDetail.value?.file?.content || "");
});
const isImage = computed(() => {
  return /\.(png|jpg|jpeg|gif)$/i.test(currentDetail.value?.file?.original_name)
})

const isPdf = computed(() => {
  return /\.pdf$/i.test(currentDetail.value?.file?.original_name)
})
</script>

<style scoped>
.preview-wrap {
  height: 100%;
  display: flex;
  flex-direction: column;

  background: transparent;
}

.preview-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.preview-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;

  color: #fff;
}

.preview-body {
  flex: 1;
  overflow-y: auto;

  padding: 32px;

  background: transparent;
}

/* markdown */

.markdown-body {
  background: transparent;

  color: #fff;

  line-height: 1.8;

  font-size: 15px;
}

/* 标题 */

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
  color: #fff;

  margin-top: 28px;

  margin-bottom: 16px;

  font-weight: 700;
}

/* 段落 */

.markdown-body :deep(p) {
  color: #fff;

  margin: 12px 0;
}

/* 行内代码 */

.markdown-body :deep(code) {
  background: rgba(0, 0, 0, 0.06);

  color: #c7254e;

  padding: 2px 6px;

  border-radius: 6px;
}

/* 代码块 */

.markdown-body :deep(pre) {
  background: rgba(0, 0, 0, 0.04);

  color: #fff;

  padding: 16px;

  border-radius: 12px;

  overflow-x: auto;
}

/* 引用 */

.markdown-body :deep(blockquote) {
  border-left: 4px solid #ccc;

  padding-left: 16px;

  color: #fff;

  margin: 16px 0;
}

/* 链接 */

.markdown-body :deep(a) {
  color: #3b82f6;

  text-decoration: none;
}

/* 图片 */

.markdown-body :deep(img) {
  max-width: 100%;

  border-radius: 12px;

  margin: 16px 0;
}
</style>
