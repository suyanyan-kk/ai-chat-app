<template>
  <div class="page">
    <div class="header">
      <h2>Retrieval 调试中心</h2>
    </div>

    <div class="search-box chat-input">
      <n-input
        v-model:value="query"
        placeholder="输入问题测试检索..."
        size="large"
        class="ask-input"
      />

      <div class="btn-group">
        <n-button type="primary" @click="handleDebug">
          开始调试
        </n-button>

        <!-- <n-button secondary type="primary">
          查看全部Chunk
        </n-button> -->

        <n-button secondary type="info" @click="handleClear">
          清空
        </n-button>
      </div>
    </div>

<div class="result">

  <!-- Query Rewrite -->
  <div class="debug-card">
    <h3>STEP 1 Query Rewrite</h3>

    <div class="block">
      <strong>原始问题：</strong>
      {{ debugData.original_query }}
    </div>

    <div class="block">
      <strong>改写结果：</strong>

      <div
        v-for="item in debugData.multi_queries"
        :key="item"
        class="query-tag"
      >
        {{ item }}
      </div>
    </div>
  </div>

  <!-- Recall -->
  <div class="debug-card">
    <h3>STEP 2 Multi Query Recall</h3>

    <div
      v-for="recall in debugData.all_recall_results"
      :key="recall.query"
      class="query-group"
    >
      <h4>
        Query:
        {{ recall.query }}
        ({{ recall.count }})
      </h4>

      <div
        class="result-item"
        v-for="item in recall.results"
        :key="item.metadata?.parent_id"
      >
        <div class="top">
          <span>
            {{ item.metadata?.file_name }}
          </span>

          <span class="score">
            RRF:
            {{ item.rrf_score?.toFixed(6) }}
          </span>
        </div>

        <div class="content">
          {{ item.content }}
        </div>

        <div class="meta">
          file_id:
          {{ item.metadata?.file_id }}

          |

          page:
          {{ item.metadata?.page }}

          |

          child:
          {{ item.metadata?.child_index }}

          <br />

          rerank:
          {{ item.rerank_score?.toFixed(6) }}
        </div>
      </div>
    </div>
  </div>

  <!-- Vector -->
  <div class="debug-card">
    <h3>STEP 3 Vector Recall</h3>

    <div
      class="query-group"
      v-for="vector,index in debugData.vector_results"
      :key="index"
    >
        <h4>
        Query:
        {{ vector.query }}
      </h4> 
        <div v-for="item in vector.vector_results" :key="item.metadata?.parent_id" class="result-item">
          <div class="top">
        <span>
          {{ vector.metadata?.file_name }}
        </span>

        <span class="score">
          VECTOR
        </span>
      </div>

      <div class="content">
        {{ item.content }}
      </div>

      <div class="meta">
        file_id:
        {{ item.metadata?.file_id }}

        |

        page:
        {{ item.metadata?.page }}

        |

        chunk:
        {{ item.metadata?.chunk_id }}
      </div>
        </div>
      
    </div>
  </div>

  <!-- BM25 -->
  <div class="debug-card">
    <h3>STEP 4 BM25 Recall</h3>

    <div
      class="query-group"
      v-for="bm25,index in debugData.bm25_results"
      :key="index"
    >
    <h4>
        Query:
        {{ bm25.query }}
      </h4>
      <div v-for="item in bm25.bm25_results" :key="item.metadata?.parent_id" class="result-item">
        <div class="top">
        <span>
          {{ item.metadata?.file_name }}
        </span>

        <span class="score">
          {{ item.bm25_score }}
        </span>
      </div>

      <div class="content">
        {{ item.content }}
      </div>

      <div class="meta">
        file_id:
        {{ item.metadata?.file_id }}

        |

        page:
        {{ item.metadata?.page }}
      </div>
      </div>

    </div>
  </div>

  <!-- Rerank -->
  <div class="debug-card">
    <h3>STEP 5 Rerank</h3>

    <div
      class="result-item"
      v-for="item in debugData.rerank"
      :key="item.metadata?.parent_id"
    >
      <div class="top">
        <span>
          {{ item.metadata?.file_name }}
        </span>

        <span class="score success">
          {{ item.rerank_score?.toFixed(6) }}
        </span>
      </div>

      <div class="content">
        {{ item.content }}
      </div>

      <div class="meta">

        file_id:
        {{ item.metadata?.file_id }}

        |

        page:
        {{ item.metadata?.page }}

        |

        parent:
        {{ item.metadata?.parent_id }}

        <br />

        rrf:
        {{ item.rrf_score?.toFixed(6) }}

        |

        bm25:
        {{ item.bm25_score }}
      </div>
    </div>
  </div>

</div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useMessage } from "naive-ui";
import { retrievalDebug } from "@/api/modules/retrievalDebug.js";

const message = useMessage();

const query = ref("");

const debugData = ref({
  original_query: "",
  multi_queries: [],

  all_recall_results: [],

  vector_results: [],
  bm25_results: [],

  rerank: []
});

const handleDebug = async () => {
  const res = await retrievalDebug(query.value);

  if (res.code !== 0) {
    return message.error("调试失败");
  }

  debugData.value = res.data;

  message.success("调试成功");
};

const handleClear = () => {
  query.value = "";

  debugData.value = {
    original_query: "",
    multi_queries: [],

    all_recall_results: [],

    vector_results: [],
    bm25_results: [],

    rerank: []
  };
};
</script>
<style scoped>

.page {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
.chat-input {
  display: flex;
  gap: 12px;
  /* padding-top: 10px; */
  flex-direction: row;
  align-items: center;
  justify-content: center;
  color: rgba(244, 248, 255, 0.92);
}

.chat-input :deep(.n-input) {
  /* flex: 1; */
  width: 600px;
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
  color: rgba(244, 248, 255, 0.92);
  font-size: 1rem;
  outline: none;
  text-align: left;
}
.chat-input :deep(.n-input__input-el),
.chat-input :deep(.n-input__textarea-el) {
  color: rgba(244, 248, 255, 0.92) !important; /* 输入文字 */
  padding: 6px 5px !important;
  line-height: 1.9;
}

.chat-input :deep(.n-input__placeholder) {
  color: rgba(255, 255, 255, 0.4) !important; /* placeholder */
}

/* .chat-input input {
  flex: 1;
} */
.chat-input input:focus {
  border-color: rgba(130, 118, 255, 0.55);
  box-shadow: 0 0 0 2px rgba(130, 118, 255, 0.24);
}
.ask-input {
  width: 600px;
}

.btn-group {
  display: flex;
  gap: 10px;
}

.result {
  height: 75vh;
  overflow-y: auto;
}

.debug-card {
  background: #1e1e1e;

  border: 1px solid #333;

  border-radius: 12px;

  padding: 16px;

  margin-bottom: 20px;
}

.debug-card h3 {
  margin-bottom: 12px;
}

.result-item {
  padding: 12px;

  margin-bottom: 12px;

  border-radius: 8px;

  background: #262626;
}

.top {
  display: flex;

  justify-content: space-between;

  margin-bottom: 10px;
}

.score {
  color: #f0a020;
}

.success {
  color: #18a058;
}

.content {
  line-height: 1.8;

  white-space: pre-wrap;
}

pre {
  white-space: pre-wrap;

  word-break: break-word;
}

.block {
  margin-bottom: 10px;
}
.meta {
  margin-top: 10px;

  color: #999;

  font-size: 12px;

  line-height: 1.8;
}

.query-group {
  margin-bottom: 24px;
}

.query-group h4 {
  color: #18a058;

  margin-bottom: 12px;
}

.query-tag {
  display: inline-block;

  padding: 4px 10px;

  margin-right: 10px;

  margin-top: 8px;

  border-radius: 6px;

  background: rgba(24, 160, 88, 0.15);

  color: #18a058;
}
</style>