<template>
  <n-modal v-model:show="visible">
    <div class="modal">
      <!-- 标题 -->
      <h3 class="title">新建文件</h3>

      <!-- 文件名 -->
      <n-input
        v-model:value="createForm.title"
        placeholder="输入文件名称..."
        style="
          background: #111;
          border-radius: 10px;
          border: 1px solid rgba(255, 255, 255, 0.08);
          transition: all 0.2s ease;
        "
        class="input"
      />

      <!-- 描述 -->
      <n-input
        v-model:value="createForm.description"
        type="textarea"
        placeholder="输入文件描述..."
        style="
          background: #111;
          border-radius: 10px;
          border: 1px solid rgba(255, 255, 255, 0.08);
          transition: all 0.2s ease;
        "
        class="input"
      />

      <!-- 文件类型 -->
      <div class="type-section">
        <div class="type-title">文件类型</div>

        <div class="type-list">
          <div
            v-for="item in fileTypes"
            :key="item.value"
            :class="['type-card', createForm.file_type === item.value ? 'active' : '']"
            @click="selectType(item)"
          >
            <div class="type-icon">
              {{ item.icon }}
            </div>

            <div class="type-name">
              {{ item.label }}
            </div>
          </div>
        </div>
      </div>

      <!-- footer -->
      <div class="footer">
        <n-button ghost @click="close" color="#fff"> 取消 </n-button>

        <n-button type="primary" @click="handleSubmit"> 创建文件 </n-button>
      </div>
    </div>
  </n-modal>
</template>

<script setup>
import { ref, computed } from "vue";
import message from "@/utils/message";

const props = defineProps({
  show: Boolean,
});

const emit = defineEmits(["update:show", "submit"]);

const visible = computed({
  get: () => props.show,

  set: (val) => emit("update:show", val),
});

// 文件类型
const fileTypes = [
  {
    label: "Markdown",
    value: "md",
    icon: "📝",
  },

  {
    label: "Word",
    value: "docx",
    icon: "📘",
  },

  {
    label: "PDF",
    value: "pdf",
    icon: "📕",
  },

  {
    label: "Text",
    value: "txt",
    icon: "📄",
  },
];
// 表单
const createForm = ref({
  title: "",

  description: "",

  file_type: "md",
});

// 选择类型
const selectType = (item) => {
  createForm.value.file_type = item.value;
};

// 关闭
const close = () => {
  emit("update:show", false);

  createForm.value = {
    title: "",
    description: "",
    file_type: "md",
  };
};

// 提交
const handleSubmit = () => {
  if (!createForm.value.title) {
    message.warning("请输入文件名称");
    return;
  }

  emit("submit", { ...createForm.value });

  close();
};
</script>

<style scoped>
.modal {
  width: 460px;

  padding: 24px;

  border-radius: 16px;

  background: #0d1117;

  backdrop-filter: blur(10px);

  border: 1px solid rgba(255, 255, 255, 0.08);

  box-shadow: 0 0 40px rgba(0, 0, 0, 0.4);
}

/* 标题 */

.title {
  margin-bottom: 18px;

  color: #fff;

  font-size: 20px;

  font-weight: 700;
}

/* 输入框 */

.input {
  margin-bottom: 14px;
}

/* n-input 重写 */

.input :deep(.n-input) {
  background: #111;

  border-radius: 10px;

  border: 1px solid rgba(255, 255, 255, 0.08);

  transition: 0.2s;
}

/* input */

.input :deep(.n-input__input-el),
.input :deep(textarea) {
  color: #fff;

  background: transparent;
}

/* placeholder */

.input :deep(.n-input__placeholder) {
  color: #666;
}

/* hover */

.input :deep(.n-input:hover) {
  border-color: rgba(255, 255, 255, 0.08);
}

/* focus */

.input :deep(.n-input.n-input--focus) {
  border-color: #4f8cff;

  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.35);
}

/* textarea */

.input :deep(textarea) {
  min-height: 90px;
}

/* 类型区域 */

.type-section {
  margin-bottom: 18px;
}

.type-title {
  color: #aaa;

  font-size: 14px;

  margin-bottom: 12px;
}

/* 类型列表 */

.type-list {
  display: grid;

  grid-template-columns: repeat(2, 1fr);

  gap: 12px;
}

/* 卡片 */

.type-card {
  cursor: pointer;

  padding: 16px;

  border-radius: 12px;

  background: rgba(255, 255, 255, 0.03);

  border: 1px solid rgba(255, 255, 255, 0.08);

  transition: 0.2s;
}

.type-card:hover {
  transform: translateY(-2px);

  border-color: rgba(9, 255, 116, 0.5);

  box-shadow: 0 0 20px rgba(79, 140, 255, 0.12);
}

/* 激活 */

.active {
  border-color: rgba(9, 255, 116, 0.5);

  background: transparent;

  box-shadow: 0 0 20px rgba(9, 255, 116, 0.12);
}

.type-icon {
  font-size: 26px;

  margin-bottom: 10px;
}

.type-name {
  color: #fff;

  font-size: 14px;

  font-weight: 600;
}

/* footer */

.footer {
  display: flex;

  justify-content: flex-end;

  gap: 12px;
}
</style>
