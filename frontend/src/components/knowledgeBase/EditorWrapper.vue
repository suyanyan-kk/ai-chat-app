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
        <!-- 图标按钮 -->
        <div class="action-buttons">
          <!-- 分享 -->
          <n-button circle secondary type="primary">
            <template #icon>
              <n-icon>
                <ShareSocialOutline />
              </n-icon>
            </template>
          </n-button>

          <!-- 查找 -->
          <n-button circle secondary type="info">
            <template #icon>
              <n-icon>
                <SearchOutline />
              </n-icon>
            </template>
          </n-button>

          <!-- 更多 -->
          <n-dropdown @select="handleSelectMore($event, node)" :options="options" trigger="click" >
            <n-button circle secondary>
              <template #icon>
                <n-icon>
                  <EllipsisHorizontal />
                </n-icon>
              </template>
            </n-button>
          </n-dropdown>
        </div>
      </div>
    </div>
    <!-- 操作按钮 -->
    <div class="editorBtn">
      <n-button ghost style="margin-right: 10px" @click="handleClear" color="#fff">
        清空
      </n-button>
      <n-button type="primary" @click="handleSave"> 保存 Markdown </n-button>
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
import "md-editor-v3/lib/style.css"
import html2pdf from "html2pdf.js"
import { saveAs } from "file-saver"
import { ShareSocialOutline, SearchOutline, EllipsisHorizontal } from "@vicons/ionicons5";
const store = useKnowledgeBaseStore();

const props = defineProps({
  createFileData: {
    type: Object,
    default: () => ({
      title: "未命名.md",
      description: "",
      parent_id: null,
      type: "file",
    }),
  },
});
const options = [
  {
    label: "导出pdf",
    key: "export-pdf",
  },
  {
    label: "导出word",
    key: "export-word",
  },
];
function handleSelectMore(key, node) {
  console.log("选中的导出", key, node);
  if (key === "export-pdf") {
    exportWord();
  } else if (key === "export-word") {
    exportPdf();
  }
}
/**
 * 导出word
 */
const exportWord = async () => {
  const doc = new Document({
    sections: [
      {
        children: [
          new Paragraph(content.value)
        ]
      }
    ]
  })

  const blob = await Packer.toBlob(doc)

  saveAs(blob, `${props.file.title}.docx`)
}

/**
 * 导出pdf
 */
const exportPdf = () => {
  const element = document.querySelector(".md-editor-preview")

  html2pdf().from(element).save()
}
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
.editorBtn {
  display: flex;
  margin: 10px;
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
