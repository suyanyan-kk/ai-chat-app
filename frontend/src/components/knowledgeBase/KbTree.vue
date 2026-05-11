<template>
  <div class="kb-node">
    <!-- 当前节点 -->
    <div class="node-row" @click="handleClick">
      <span> {{ node.type === "file" ? "📄" : "📁" }} {{ node.title }} </span>
      <div class="more-wrapper">
        <n-dropdown
          trigger="hover"
          placement="bottom-start"
          :options="options"
          @select="handleSelectNode($event, node)"
          size="large"
        >
          <n-button class="more-btn" :focusable="false" quaternary type="primary">
            更多
          </n-button>
        </n-dropdown>
      </div>
    </div>

    <!-- 子节点 -->
    <div v-if="children.length > 0 && node.is_open" class="children">
      <KbTree
        v-for="child in children"
        :key="child.id"
        :node="child"
        @select="handleChildSelect"
      />
    </div>
  </div>
  <!-- 新建弹窗组件 -->
  <KnowledgeModal v-model:show="showModal" :type="type" :parentId="node.id" />
</template>

<script setup>
import { ref, computed } from "vue";
import KnowledgeModal from "@/components/knowledgeBase/KnowledgeModal.vue";
import { useKnowledgeBaseStore } from "@/stores/modules/knowledgeBase";
import { deleteKnowledge, getKnowledgeDetail } from "@/api/modules/knowledge.js";
import message from "@/utils/message";
const options = [
  {
    label: "新增",
    key: "create",
    children: [
      {
        label: "目录",
        key: "addFolder",
      },
      {
        label: "创建文件",
        key: "createFile",
      },
    ],
  },
  {
    label: "删除",
    key: "delete",
  },
  {
    label: "置顶",
    key: "top",
  },
  {
    label: "重命名",
    key: "reName",
  },
  {
    label: "上传文件",
    key: "uploadFile",
  },

  {
    label: "更多",
    key: "more",
    children: [
      {
        label: "复制",
        key: "copy",
      },
      {
        label: "移动",
        key: "move",
      },
      {
        label: "下载",
        key: "download",
      },
      {
        label: "分享",
        key: "share",
      },
    ],
  },
];
const type = ref("file"); // 用于区分是新建文件还是目录
const store = useKnowledgeBaseStore();
const showModal = ref(false);
const props = defineProps({
  node: Object,
});
const emit = defineEmits(["select"]);
const children = computed(() => store.getChildren(props.node.id));

const handleChildSelect = (...args) => {
  emit("select", ...args);
};
function handleSelectNode(key, node) {
  console.log("选中了", key, node);
  if (key === "addFolder") {
    type.value = "folder";
    showModal.value = true;
    emit("select", "addFolder", props.node);
  } else if (key === "uploadFile") {
    type.value = "file";
    showModal.value = true;
    emit("select", "uploadFile", props.node);
  } else if (key === "createFile") {
    emit("select", "createFile", props.node);
  } else if (key === "delete") {
    // 删除
    remove(node.id);
  } else if (key === "reName") {
    // 重命名
    // const newTitle = prompt("请输入新的名称", node.title);
    // if (newTitle) {
    //   store.renameNode(node.id, newTitle);
    // }
  }
}

// 👉 点击文件夹展开/折叠
const handleClick = async () => {
  if (props.node.type === "folder") {
    store.toggleFolder(props.node.id);
  }
  const res = await getKnowledgeDetail(props.node.id);
  if (res.code === 0) {
    store.setCurrentId(props.node.id);
    store.getcurrentDetail(res.data);
    emit("select", "preview", props.node);
  } else {
    message.error("获取资料详情失败");
  }
};
const handleKnowledgeBaseModal = (type) => {
  showModal.value = true;
};
const remove = async (nodeId) => {
  const stutas = await deleteKnowledge(nodeId);
  if (stutas.code === 0) {
    message.success(stutas.message);
    store.deleteNode(nodeId);
  } else {
    message.error("删除失败");
  }
};
</script>

<style scoped>
/* 列表 */
.kb-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.kb-item {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: all 0.2s;
}

.kb-item:hover {
  border: 1px solid #4f8cff;
  box-shadow: 0 0 10px rgba(79, 140, 255, 0.3);
}
.node-row:hover {
  background: rgba(79, 140, 255, 0.08);
  border-radius: 6px;
}
.info h3 {
  margin: 0;
}

.info p {
  margin-top: 6px;
  color: #aaa;
  font-size: 13px;
}
.kb-node {
  margin-left: 10px;
}
.node-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
}

.children {
  margin-left: 16px;
  border-left: 1px dashed rgba(255, 255, 255, 0.1);
  padding-left: 10px;
}
</style>
