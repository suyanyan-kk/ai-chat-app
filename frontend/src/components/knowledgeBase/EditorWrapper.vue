<template>
  <div class="editor-page">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <div class="left">
        <div class="title">📝 Markdown 编辑器</div>

        <div class="file-name">
          {{ createFileData.title }}
        </div>
      </div>

      <div class="right">
        <div class="action-buttons">
          <!-- 保存 -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button circle secondary type="success" @click="handleSave">
                <template #icon>
                  <n-icon>
                    <SaveOutline />
                  </n-icon>
                </template>
              </n-button>
            </template>

            保存文件
          </n-tooltip>

          <!-- 清空 -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button circle secondary type="warning" @click="handleClear">
                <template #icon>
                  <n-icon>
                    <TrashOutline />
                  </n-icon>
                </template>
              </n-button>
            </template>

            清空内容
          </n-tooltip>

          <!-- 导出 PDF -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button circle secondary type="error" @click="exportPdf">
                <template #icon>
                  <n-icon>
                    <ReceiptOutline />
                  </n-icon>
                </template>
              </n-button>
            </template>

            导出 PDF
          </n-tooltip>

          <!-- 导出 Word -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button circle secondary type="info" @click="exportWord">
                <template #icon>
                  <n-icon>
                    <DocumentTextOutline />
                  </n-icon>
                </template>
              </n-button>
            </template>

            导出 Word
          </n-tooltip>

          <!-- 更多 -->
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-dropdown @select="handleSelectMore" :options="options" trigger="click">
                <n-button circle secondary  type="info">
                  <template #icon>
                    <n-icon>
                      <EllipsisHorizontal />
                    </n-icon>
                  </template>
                </n-button>
              </n-dropdown>
            </template>

            更多操作
          </n-tooltip>
        </div>
      </div>
    </div>

    <!-- 编辑器 -->
    <div class="editor-wrapper">
      <MdEditor
        v-model="content"
        :theme="theme"
        preview-theme="github"
        code-theme="atom"
        class="editor"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { MdEditor } from "md-editor-v3";
import "md-editor-v3/lib/style.css";
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";
import { addKnowledge, uploadFile } from "@/api/modules/knowledge";
import message from "@/utils/message";
import { Document, Packer, Paragraph } from "docx";
import jsPDF from "jspdf";
import { saveAs } from "file-saver";
import {
  ShareSocialOutline,
  SearchOutline,
  EllipsisHorizontal,
  SaveOutline,
  TrashOutline,
  DocumentTextOutline,
  ReceiptOutline,
} from "@vicons/ionicons5";
const store = useKnowledgeBaseStore();

const props = defineProps({
  createFileData: {
    type: Object,
    default: () => ({
      title: "未命名.md",
      description: "",
      file_type: "",
      type: "file",
      parent_id: null,
    }),
  },
});
const options = [
  {
    label: "分享",
    key: "share",
  },
  {
    label: "搜索",
    key: "search",
  },
];
function handleSelectMore(key) {
  console.log("选中的操作", key);

  if (key === "share") {
    message.info("分享功能开发中");
  }

  if (key === "search") {
    message.info("搜索功能开发中");
  }
}
/**
 * 导出word
 */
const exportWord = async () => {
  const doc = new Document({
    sections: [
      {
        children: [new Paragraph(content.value)],
      },
    ],
  });

  const blob = await Packer.toBlob(doc);

  saveAs(blob, `${props.createFileData.title}.docx`);
};

/**
 * 导出pdf
 */
const exportPdf = () => {
  // const element = document.querySelector(".md-editor-preview")

  // html2pdf().from(element).save()
  const pdf = new jsPDF();

  pdf.text(content.value, 10, 10);

  pdf.save(`${props.createFileData.title}.pdf`);
};
// markdown 内容
const content = ref(`
# 欢迎使用 AI Markdown 编辑器
这是一个支持：

- Markdown
- AI知识库
- 在线编辑
的编辑器。

---

## 代码示例

\`\`\`js
console.log("hello ai")
\`\`\`
`);

// 主题
const theme = ref("dark");

// 清空
const handleClear = () => {
  content.value = "";
};
const handleSave = async () => {
  try {
    // 1. blob
    const blob = new Blob(
      [content.value],

      {
        type: "text/markdown",
      }
    );

    // 2. 转 file
    const file = new File(
      [blob],

      props.createFileData.title.endsWith(".md")
        ? props.createFileData.title
        : `${props.createFileData.title}.md`,

      {
        type: "text/markdown",
      }
    );

    // 3. 上传
    const res = await uploadFile(file);
    if (res.code === 0) {
      console.log("文件信息", res.data);
      await submitData(res.data.id);
    } else {
      message.error("文件上传失败");
    }
  } catch (err) {
    message.error("文件上传失败", err);
  }
};
const submitData = async (fileId) => {
  // 这里可以调用接口提交数据，data 包含 title、description、file_type 和 content 等信息
  const payloadMd = {
    title: props.createFileData.title,
    description: props.createFileData.description,
    type: props.createFileData.type,
    parent_id: props.createFileData.parent_id,
    file_id: fileId,
  };
  try {
    const addRes = await addKnowledge(payloadMd);
    if (addRes.code === 0) {
      // 更新本地
      const newNode = addRes.data;
      store.addNode(newNode); // ✅ 将新节点添加到 Pinia 状态中
      message.success("保存成功");
      return newNode;
    } else {
      message.error("保存失败: " + addRes.message);
      return;
    }
  } catch (err) {
    message.error("保存失败", err);
    throw err;
  }
  // 在这里可以调用接口提交数据，例如：
  // await api.createFile(payload);
};
// 保存 markdown 实体文件
// const handleSave = () => {

//   // 创建 blob
//   const blob = new Blob(

//     [content.value],

//     {
//       type: "text/markdown;charset=utf-8"
//     }

//   )

//   // 创建下载链接
//   const url =
//     window.URL.createObjectURL(blob)

//   // 创建 a 标签
//   const a =
//     document.createElement("a")

//   a.href = url

//   a.download =
//     props.createFileData.title.endsWith(".md")
//       ? props.createFileData.title
//       : `${props.createFileData.title}.md`

//   document.body.appendChild(a)

//   a.click()

//   document.body.removeChild(a)

//   window.URL.revokeObjectURL(url)

//   message.success(
//     "Markdown 文件已生成"
//   )

// }
</script>

<style scoped>
.editor-page {
  height: 100%;

  display: flex;

  flex-direction: column;

  overflow: hidden;
}

/* 顶部工具栏 */

.toolbar {
  height: 64px;

  padding: 0 20px;

  display: flex;

  justify-content: space-between;

  align-items: center;

  border-bottom: 1px solid rgba(255, 255, 255, 0.08);

  background: rgba(255, 255, 255, 0.02);

  backdrop-filter: blur(10px);
}

/* 左侧 */

.left {
  display: flex;

  align-items: center;

  gap: 14px;
}

.title {
  font-size: 18px;

  font-weight: 700;

  color: #fff;
}

.file-name {
  font-size: 13px;

  color: #888;
}

/* 右侧 */

.right {
  display: flex;

  gap: 12px;
}
.action-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}
:deep(.n-tooltip) {
  border-radius: 10px;
}
.action-buttons :deep(.n-button) {
  backdrop-filter: blur(10px);
  transition: all 0.2s ease;
}

.action-buttons :deep(.n-button:hover) {
  transform: translateY(-2px);
}
/* 编辑器区域 */

.editor-wrapper {
  flex: 1;

  overflow: hidden;
}

/* 编辑器 */

.editor {
  height: 100%;
}

/* md-editor 深色主题重写 */

:deep(.md-editor) {
  background: transparent;
}

/* 工具栏 */

:deep(.md-editor-toolbar) {
  background: rgba(255, 255, 255, 0.03);

  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

/* 编辑区域 */

:deep(.md-editor-input-wrapper),
:deep(.md-editor-preview-wrapper) {
  background: transparent;
}

/* textarea */

:deep(.md-editor-input) {
  color: #e6edf3;

  font-size: 15px;

  line-height: 1.8;
}

/* 预览 */

:deep(.md-editor-preview) {
  background: transparent;

  color: #e6edf3;
}

/* 分割线 */

:deep(.md-editor-resize-operate) {
  background: rgba(255, 255, 255, 0.08);
}

/* 工具栏按钮 */

:deep(.md-editor-toolbar-item) {
  color: #aaa;
}

:deep(.md-editor-toolbar-item:hover) {
  color: #4f8cff;

  background: rgba(79, 140, 255, 0.08);
}

/* 滚动条 */

:deep(::-webkit-scrollbar) {
  width: 8px;

  height: 8px;
}

:deep(::-webkit-scrollbar-thumb) {
  background: rgba(255, 255, 255, 0.12);

  border-radius: 10px;
}
</style>
