<template>
  <!-- <div class="kb-page"> -->
  <!-- 头部 -->
  <!-- <div class="kb-header">
      <div>
        <h2>📚 资料库</h2>
        <p class="sub">Knowledge Base</p>
      </div>
    </div> -->
  <!-- </div> -->
  <div class="kb-box">
    <div class="box-list">
      <!-- 搜索 -->
      <div class="search-box">
        <n-input v-model:value="keyword" placeholder="🔍 搜索资料..." clearable />
      </div>
      <!-- 列表 @load="handleLoad"-->
      <n-infinite-scroll style="height: 65vh" :distance="10">
        <KbTree v-for="item in list" :key="item.id" :node="item" @select="handleSelect" />
      </n-infinite-scroll>
    </div>
    <div class="box-view">
      <component :is="currentComponent" v-bind="currentComponentProps" />
    </div>
    <CreateFileModal v-model:show="showCreateFile" @createSubmit="handleCreateFile" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import KbTree from "@/components/knowledgeBase/KbTree.vue";
import PreviewofData from "@/components/knowledgeBase/PreviewofData.vue";
import EditorWrapper from "@/components/knowledgeBase/EditorWrapper.vue";
import ViewEmpty from "@/components/knowledgeBase/ViewEmpty.vue";
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";
import { storeToRefs } from "pinia";
import { getKnowledge, getKnowledgeDetailByFileId } from "@/api/modules/knowledge.js";
import CreateFileModal from "@/components/knowledgeBase/CreateFileModal.vue";
import ChunkPreview from "@/components/knowledgeBase/ChunkPreview.vue";
import { useRoute } from "vue-router";

const route = useRoute();
// 当前视图：预览、编辑等addFile
const currentView = ref("empty");
const loading = ref(false);
const hasLoadedList = ref(false);
const kbStore = useKnowledgeBaseStore();
const keyword = ref("");
// 表单数据 俩种响应式
const { buildTree } = storeToRefs(kbStore);
const list = buildTree;
const componentMap = {
  preview: PreviewofData,
  createFile: EditorWrapper,
  chunkPreview: ChunkPreview,
  empty: ViewEmpty,
};

const currentComponent = computed(() => {
  return componentMap[currentView.value] || ViewEmpty;
});

const currentComponentProps = computed(() => {
  switch (currentView.value) {
    case "createFile":
      return {
        createFileData: createFileData.value,
      };

    default:
      return {};
  }
});

const handleSelect = (operationType, node) => {
  console.log("选中节点：", node);
  if (operationType === "createFile") {
    showCreateFile.value = true;
    createFileData.value.parent_id = node.id;
    createFileData.value.type = "file";
  } else if (operationType === "chunkFile") {
    // 处理文件切片逻辑
    currentView.value = "chunkPreview";
  } else {
    currentView.value = "preview";
  }
  // 在这里可以根据需要处理选中节点的逻辑，比如展示详情等
};
const showCreateFile = ref(false);

const createFileData = ref({
  title: "",
  description: "",
  file_type: "",
  type: "",
  parent_id: null,
});
const handleCreateFile = (data) => {
  // debugger
  createFileData.value.title = data.title;
  createFileData.value.description = data.description;
  createFileData.value.file_type = data.file_type;
  currentView.value = "createFile";
};
const openParentFolder = (parentId) => {
  if (!parentId) return;

  const parent = kbStore.getNodeById(Number(parentId));

  if (parent && !parent.is_open) {
    kbStore.toggleFolder(parent.id);
  }
};

const openKnowledgeByFileId = async (fileId) => {
  if (!fileId) return;

  const res = await getKnowledgeDetailByFileId(fileId);

  if (res.code === 0) {
    openParentFolder(res.data?.parent_id);
    handleSelect("preview", res.data);
    kbStore.setCurrentId(res.data.id);
    kbStore.getcurrentDetail(res.data);
  }
};

// const items = ref(Array.from({ length: 10 }, (_, i) => mock(i)));

// const noMore = computed(() => items.value.length > 16);
// async function handleLoad() {
//   if (loading.value || noMore.value)
//     return;
//   loading.value = true;
//   await new Promise((resolve) => setTimeout(resolve, 1e3));
//   items.value.push(...[mock(items.value.length), mock(items.value.length + 1)]);
//   loading.value = false;
// }
watch(
  () => route.query.file_id,
  async (fileId) => {
    if (!hasLoadedList.value) return;

    await openKnowledgeByFileId(fileId);
  },
  {
    immediate: true,
  }
);
onMounted(async () => {
  const knowledgeList = await getKnowledge();
  kbStore.setList(knowledgeList);
  hasLoadedList.value = true;
  await openKnowledgeByFileId(route.query.file_id);
});
</script>

<style scoped>
.kb-page {
  padding: 20px;
  color: #fff;
}
.box-view {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 15px;
  box-sizing: border-box;
}
.kb-box {
  height: 100%;
  display: flex;
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
  color: #fff;
}
.box-list {
  width: 300px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 15px;
  box-sizing: border-box;
}
.text {
  text-align: center;
}
/* .list{
  max-height: 70vh;
  overflow-y: auto; 

} */
/* 头部 */
.kb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sub {
  font-size: 12px;
  color: #888;
}

/* 科技按钮 */
.btn-primary {
  position: relative;
  overflow: hidden;
  /* color: #fff; */
}

.btn-primary:hover {
  color: #6edcff;
}
.btn-primary {
  outline: none !important;
}
.btn-primary:focus,
.btn-primary:focus-visible {
  outline: none !important;
  box-shadow: none !important;
}
/* 🔥 针对 Naive UI 内部按钮 */
.btn-primary :deep(.n-button:focus),
.btn-primary :deep(.n-button:focus-visible) {
  box-shadow: none !important;
  outline: none !important;
}
/* 🔥 再补一刀（有些主题用这个类） */
.btn-primary :deep(.n-button--focus) {
  box-shadow: none !important;
}
.btn-primary:hover::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: 1px solid rgba(110, 220, 255, 0.6);
  box-shadow: 0 0 10px rgba(110, 220, 255, 0.4);
  pointer-events: none;
}

/* 搜索框科技风 */
.search-box {
  width: 100%;
  margin: 15px 0;
}

.search-box :deep(.n-input) {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  backdrop-filter: blur(6px);
}
</style>
