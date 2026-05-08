<template>
  <n-modal v-model:show="visible">
    <div class="modal">
      <h3 class="title">
        {{ type === "file" ? "新建文件" : "新建目录" }}
      </h3>

      <n-input
        v-model:value="localForm.title"
        placeholder="输入标题..."
        style="
          background: #111;
          border-radius: 10px;
          border: 1px solid rgba(255, 255, 255, 0.08);
          transition: all 0.2s ease;
        "
        class="input"
      />

      <n-input
        v-model:value="localForm.description"
        type="textarea"
        style="
          color: #fff;
          background: transparent;
          border: 1px solid rgba(255, 255, 255, 0.08);
        "
        placeholder="输入描述内容..."
        class="input"
      />
      <!-- 🔥 新增：上传区域（仅新建文件时显示） -->
      <div v-if="type === 'file'" class="upload">
        <n-upload
          multiple
          style="width: 100%"
          :default-upload="false"
          :on-change="handleFileChange"
          :show-file-list="true"
          accept=".pdf,.txt,.md,.doc,.docx"
          v-model:file-list="fileList"
          :on-drop="handleDrop"
        >
          <n-upload-dragger>
            <div class="upload-box">
              <div class="icon">📄</div>
              <p>点击或拖拽文件上传</p>
              <span>支持 PDF / TXT / MD / DOCX</span>
            </div>
          </n-upload-dragger>
        </n-upload>
      </div>
      <div class="footer">
        <n-button ghost @click="close" color="#fff">取消</n-button>
        <n-button type="primary" @click="handleSubmit"> 确认 </n-button>
      </div>
    </div>
  </n-modal>
</template>

<script setup>
import { ref, watch, computed } from "vue";
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";
import { addKnowledge,uploadFile } from "@/api/modules/knowledge.js";
import message from "@/utils/message";
const store = useKnowledgeBaseStore();

const props = defineProps({
  show: Boolean,
  form: Object,
  node: Object,
  type: String, // 这个 type 是为了区分是从目录新建还是从文件新建，因为文件没有 parentId 这个字段，所以需要区分开来
  parentId: [String, Number, null],
});

const localForm = ref({
  title: "",
  file_id: null,
  // type: 'folder'|| "file",
  description: "",
  content: "",
});
const fileList = ref([]);
const visible = computed({
  get: () => props.show,
  set: (val) => emit("update:show", val),
});
const emit = defineEmits(["update:show"]);

const handleDrop = (e) => {
  console.log("拖拽触发", e);
};
// 文件变化
const handleFileChange = async ({ fileList: files }) => {
  // 目前只支持上传一个文件，所以我们直接取第一个文件来处理
  fileList.value = files
  const file = files[0]?.file

  if (!file) {
    console.log("没有获取到文件")
    return
  }
 const res = await uploadFile(files[0].file);
  if (res.code === 0) {
    localForm.value.file_id = res.data.id;
    message.success("文件上传成功");
    console.log("文件上传成功，内容已获取", res.data);
  } else {
    message.error("文件上传失败");
    console.log("文件上传失败: " + res.message);
  }
  console.log("文件列表更新", fileList.value);
};
const close = () => {
  emit("update:show", false);
  localForm.value = {};
  fileList.value = [];
};

const handleSubmit = async(data) => {
  if (!localForm.value.title) {
    // 这里可以使用你项目中的消息提示组件
    message.warning("标题不能为空");
    return;
  }
  if (props.type === "file" && fileList.value.length === 0 && !localForm.value.file_id) {
    message.warning("请上传文件");
    return;
  }
  const payload = {
    title: localForm.value.title,
    description: localForm.value.description,
    type: props.type,
    parent_id: props.type === "folder" ? null : props.parentId,
    file_id: localForm.value.file_id,
    content: props.type === "folder" ? null:localForm.value.content,

  };
  // console.log(props.parentId, "1232144");
  addHandleSubmit(payload)
    .then(() => {
      // 提交成功后的操作，例如刷新列表等
      message.success("提交成功");
    })
    .catch((err) => {
      message.error("提交失败", err);
    });
  close();
};

const addHandleSubmit = async (data) => {
  // ✅ 新增目录（调用接口版）
  try {
    const res = await addKnowledge(data);
   if (res.code === 0) {
      // 更新本地
      const newNode = res.data;
      store.addNode(newNode); // ✅ 将新节点添加到 Pinia 状态中
      console.log("新增成功");
      return newNode;
    } else {
      console.log("新增失败: " + res.message);
      return;
    }
  } catch (err) {
    console.error("新增失败", err);
    throw err;
  }
};
</script>

<style scoped>
.modal {
  width: 420px;
  padding: 24px;
  border-radius: 14px;
  background: #0d1117;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.title {
  margin-bottom: 15px;
  color: #fff;
}
/* 输入框容器 */
.input {
  margin-bottom: 12px;
}

/* 🔥 核心：重写 n-input */
.input :deep(.n-input) {
  background: #111; /* 深色背景 */
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.2s ease;
}

/* 输入框内部（真正的 input） */
.input :deep(.n-input__input-el),
.input :deep(textarea) {
  color: #fff;
  background: transparent; /* 去掉内部白底 */
}

/* placeholder */
.input :deep(.n-input__placeholder) {
  color: #666;
}

/* hover */
.input :deep(.n-input:hover) {
  border-color: rgba(79, 140, 255, 0.5);
}

/* focus（科技感重点✨） */
.input :deep(.n-input.n-input--focus) {
  border-color: #4f8cff;
  box-shadow: 0 0 0 1px rgba(79, 140, 255, 0.4);
}

/* textarea 高度 */
.input :deep(textarea) {
  min-height: 100px;
}
/* 上传区域 */
.upload {
  margin-bottom: 16px;
}
/* 🔥 让 trigger 撑满 */
.upload :deep(.n-upload-trigger .n-upload-dragger) {
  width: 100%;
}

/* 🔥 让内部包裹层也撑满 */
.upload :deep(.n-upload-trigger .n-upload-dragger > *) {
  width: 100%;
}

/* 🔥 如果你用的是自定义 upload-box */
/* 上传盒子 */
.n-upload-dragger {
  padding: 20px;
  text-align: center;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px dashed rgba(255, 255, 255, 0.15);
  cursor: pointer;
  transition: all 0.2s;
}

.n-upload-dragger:hover {
  border-color: #4f8cff;
  background: rgba(79, 140, 255, 0.05);
}
.upload :deep(.n-upload-dragger) {
  border: 1px dashed rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  transition: all 0.2s;
}

.upload :deep(.n-upload-dragger:hover) {
  border-color: #4f8cff;
}

.upload :deep(.n-upload-dragger--dragover) {
  border-color: #4f8cff;
  background: rgba(79, 140, 255, 0.08);
}
/* 图标 */
.icon {
  font-size: 24px;
  margin-bottom: 6px;
}

/* 文本 */
.n-upload-dragger p {
  margin: 0;
  color: #ddd;
}

.n-upload-dragger span {
  font-size: 12px;
  color: #777;
}
/* 科技风按钮区 */
.footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
