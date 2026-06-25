<template>
  <div class="preview-wrap">
    <div class="preview-header">
      <h2>
        {{ currentDetail?.title || "资料预览" }}
      </h2>

      <p>{{ currentDetail?.description || "暂无描述" }}</p>
      <n-tag type="warning" v-if="currentDetail?.file?.embedding_status === 'pending'"> 等待向量化 </n-tag>

      <n-tag type="info" v-if="currentDetail?.file?.embedding_status === 'processing'"> 正在分析 </n-tag>

      <n-tag type="success" v-if="currentDetail?.file?.embedding_status === 'success'"> AI已就绪 </n-tag>

      <n-tag type="error" v-if="currentDetail?.file?.embedding_status === 'failed'"> 向量化失败 </n-tag>
    </div>

    <div class="preview-body">
      <div v-if="!file" class="preview-empty" role="status">
        <strong>该节点未关联文件</strong>
        <span>请重新上传文件，或修复该节点的文件关联。</span>
      </div>
      <!-- 图片 -->
      <img v-else-if="isImage" :src="previewUrl" class="image" />
      <!-- pdf -->
      <iframe
        v-else-if="isPdf && previewUrl"
        :key="previewUrl"
        :src="previewUrl"
        :title="file.original_name || currentDetail?.title || 'PDF 预览'"
        class="pdf"
      />
      <!-- markdown 内容 -->
      <div v-else-if="htmlContent" class="markdown-body" v-html="htmlContent" />
      <div v-else class="preview-empty" role="status">
        <strong>暂不支持预览此文件</strong>
        <span>{{ file.original_name || "文件信息不完整" }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import MarkdownIt from "markdown-it";
import { useRoute } from "vue-router";

import { storeToRefs } from "pinia";

import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";

const kbStore = useKnowledgeBaseStore();
const route = useRoute();

const { currentDetail } = storeToRefs(kbStore);
const file = computed(() => currentDetail.value?.file || null);

// markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

// markdown -> html
const htmlContent = computed(() => {
  return md.render(file.value?.content || "");
});

const fileUrl = computed(() => {
  const publicUrl = file.value?.url?.trim();

  if (publicUrl) return publicUrl;

  const uuidName = file.value?.uuid_name?.trim();

  if (uuidName) {
    return `/api/uploads/${encodeURIComponent(uuidName)}`;
  }

  return "";
});

const currentPage = computed(() => {
  const page = Array.isArray(route.query.page) ? route.query.page[0] : route.query.page;

  return page || "";
});

const previewUrl = computed(() => {
  if (!fileUrl.value) return "";
  if (!isPdf.value || !currentPage.value) return fileUrl.value;

  return `${fileUrl.value.split("#")[0]}#page=${encodeURIComponent(currentPage.value)}`;
});

const isImage = computed(() => {
  const type = file.value?.file_type?.toLowerCase().trim();
  const name = file.value?.original_name?.trim() || file.value?.uuid_name?.trim() || "";

  return ["png", "jpg", "jpeg", "gif"].includes(type) || /\.(png|jpg|jpeg|gif)$/i.test(name);
});

const isPdf = computed(() => {
  const type = file.value?.file_type?.toLowerCase().trim();
  const name = file.value?.original_name?.trim() || file.value?.uuid_name?.trim() || "";

  return type === "pdf" || /\.pdf$/i.test(name);
});
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

.preview-empty {
  min-height: 240px;
  display: grid;
  place-content: center;
  gap: 8px;
  border: 1px dashed rgba(255, 255, 255, 0.16);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.62);
  text-align: center;
}

.preview-empty strong {
  color: #fff;
  font-size: 16px;
}

.preview-empty span {
  font-size: 13px;
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

.image {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
}

.pdf {
  width: 100%;
  min-height: 70vh;
  border: 0;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
}
</style>
