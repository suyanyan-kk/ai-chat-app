<template>
  <n-modal v-model:show="visible">
    <div class="modal">
      <h3 class="title">
        {{ isEdit ? "编辑资料" : "新建资料" }}
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
      <!-- 🔥 新增：上传区域（仅新建显示） -->
      <div v-if="!isEdit" class="upload">
        <n-upload
          multiple
          style="width: 100%;"
          :default-upload="false"
          :on-change="handleFileChange"
          :show-file-list="true"
          accept=".pdf,.txt,.md,.doc,.docx"
          v-model:file-list="fileList"
          :on-drop="handleDrop"
        >
         <n-upload-dragger >
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

const store = useKnowledgeBaseStore();

const props = defineProps({
  show: Boolean,
  form: Object,
  isEdit: Boolean,
  node: Object,
  parentId: [String, Number,null],
});
watch(
  () => props.node,
  (node) => {
    if (node&&props.isEdit) { // 编辑回显数据
      localForm.value = JSON.parse(JSON.stringify(node))
    }
  },
  {
    immediate: true
  }
)
const localForm = ref({
    title: '',
    type: 'folder'|| "file",
    parentId:'' ,
    description:'',
    content: ''
});
const fileList = ref([]);
const visible = computed({
  get: () => props.show,
  set: (val) => emit("update:show", val),
});
const emit = defineEmits(["update:show",]);

const handleDrop = (e) => {
  console.log("拖拽触发", e)
}
// 文件变化
const handleFileChange = ({ fileList: files }) => {
  fileList.value = files;
};
const close = () => {
  emit("update:show", false);
  localForm.value = {};
  fileList.value = []; 
};

const handleSubmit = (data) => {
    // 新增和编辑共用一个接口，后端根据是否有 id 来判断
  if(!props.isEdit) {
    addHandleSubmit(data)
  }else{
    editHandleSubmit(data)
  }
  close();
};
const editHandleSubmit = async (data) => {
  store.updateNode(data.id, {
    title: localForm.value.title,
    description: localForm.value.description,
    content: localForm.value.content
  })
  // store.buildTree
}
const addHandleSubmit = async () => {
  debugger
  console.log(props.parentId, '1232144')
  store.addNode({
    title: localForm.value.title,
    type: localForm.value.type || "file",
    parentId: props.parentId || null,
    description:localForm.value.description,
    content: localForm.value.content
  })
  //  store.buildTree

}
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
.upload :deep(.n-upload-trigger  .n-upload-dragger> *) {
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
