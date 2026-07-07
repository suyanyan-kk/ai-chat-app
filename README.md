
## 启动方式

### 前端
cd frontend
npm install
npm run dev

### 后端
cd ai-service
uv run uvicorn app.main:app --reload
### docker build
cd /Users/suyanyan/Documents/study/AI/AI_PY_Project

docker compose -f docker-compose.prod.yml up -d --build

# AI 知识库问答与 Agent 系统

> 一个基于 **Vue3 + FastAPI + LangChain/LangGraph + ChromaDB + PostgreSQL + Docker/Jenkins** 构建的企业级 RAG Agent 问答系统。

本项目从零实现了一个完整的 AI 应用系统，覆盖知识库文件上传、文档解析、语义切片、向量检索、BM25 混合检索、Rerank、来源引用、Agent 工具调用、流式输出、前后端交互、容器化部署与 Jenkins 自动化发布。

---

## 1. 项目定位

本项目的目标不是简单调用大模型接口，而是构建一个接近真实企业场景的 AI 知识库问答系统。

系统支持用户上传知识库文件，后端对文件进行解析、切片、向量化存储，并通过 RAG Workflow 完成多阶段检索与上下文构建。最终由 Agent 调用知识库工具、天气工具、时间工具、计算器工具等完成问题回答，并在前端以流式方式展示答案、工具调用状态和来源引用。

项目核心能力包括：

```text
文件上传
  ↓
文档解析
  ↓
语义切片 / Parent-Child Chunk
  ↓
向量存储
  ↓
混合检索
  ↓
Rerank
  ↓
RAG Workflow
  ↓
Agent 工具调用
  ↓
流式回答
  ↓
来源引用
  ↓
Docker 部署
  ↓
Jenkins 自动发布
```

---

## 2. 技术栈

### 前端

- Vue3
- Vite
- Pinia
- Naive UI
- Markdown 渲染
- Fetch + ReadableStream 流式响应
- 组件化聊天 UI
- 知识库管理 UI
- Chunk 调试页面
- Retrieval Debug 页面

### 后端

- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- ChromaDB
- LangChain 0.3
- LangGraph 0.6
- LangSmith
- sentence-transformers
- rank-bm25
- jieba
- PyMuPDF
- python-docx

### AI / RAG

- DeepSeek Chat Model
- HuggingFace Embedding Model
- Chroma 向量检索
- BM25 关键词检索
- RRF 多路召回融合
- Rerank 重排序
- Parent-Child Chunk
- Query Analysis
- Sources 来源引用
- LangGraph Workflow
- LangGraph Agent

### 部署与工程化

- Docker
- Docker Compose
- Caddy
- Jenkins
- Gitee / GitHub
- SSH 自动部署
- PostgreSQL Docker Volume 持久化
- 生产环境 `.env.production`

---

## 3. 系统架构

```text
用户浏览器 / iPad / PC
        ↓
Vue3 Frontend
        ↓
Caddy Reverse Proxy
        ↓
FastAPI Backend
        ↓
LangGraph Agent Runtime
        ↓
Tools
 ┌───────────────┬───────────────┬──────────────┬───────────────┐
 │ search_knowledge │ get_weather │ calculator │ get_current_time │
 └───────────────┴───────────────┴──────────────┴───────────────┘
        ↓
RAG Workflow
        ↓
ChromaDB + PostgreSQL
```

---

## 4. 核心功能

### 4.1 用户认证与基础系统

系统已经具备基础用户登录能力，支持管理员账号创建和前端登录访问。

主要能力：

- 用户登录
- 登录状态管理
- 前端请求拦截
- Token / Session 管理
- 线上环境可访问

---

### 4.2 知识库文件上传

系统支持用户上传知识库文件，后端保存文件并进行解析。

支持的文件类型包括：

- PDF
- Word
- Markdown
- Text
- Code / 普通文本类文件

处理流程：

```text
上传文件
  ↓
保存原始文件
  ↓
解析文本内容
  ↓
生成 KnowledgeFile 记录
  ↓
生成 KnowledgeChunk 记录
  ↓
写入 Chroma 向量库
```

---

### 4.3 Chunk 管理

本项目没有停留在简单的固定长度切片，而是实现了较完整的 Chunk 管理方案。

已完成能力：

- Recursive Chunk
- Markdown 结构化切片
- PDF 按页切片
- Parent-Child Chunk
- metadata 统一管理
- chunk 调试接口
- 根据 file_id 查询 chunk
- 向量召回调试

核心 metadata 包括：

```text
file_id
file_name
file_type
chunk_id
chunk_type
parent_id
parent_index
child_index
page
splitter
embedding_status
```

Parent-Child Chunk 的作用：

```text
Child Chunk：用于精准召回
Parent Chunk：用于提供更完整上下文
```

这样可以兼顾召回准确率和回答上下文完整性。

---

## 5. RAG Workflow

本项目的 RAG 不是一个单独的 retrieval 函数，而是通过 LangGraph 编排成完整 Workflow。

当前 RAG 流程：

```text
query_analysis
  ↓
vector_retrieval
  ↓
bm25_retrieval
  ↓
rrf_fusion
  ↓
rerank
  ↓
parent_chunk
  ↓
build_context
```

### 5.1 query_analysis

负责对用户问题进行分析，为后续检索提供更好的查询条件。

主要职责：

- 保留原始问题
- 生成改写后的问题
- 支持多查询扩展
- 支持 metadata filter

---

### 5.2 vector_retrieval

基于 ChromaDB 进行向量召回。

流程：

```text
query
  ↓
embedding
  ↓
Chroma similarity_search
  ↓
vector_results
```

向量检索适合处理语义相似的问题，例如用户表达和文档原文不完全一致的情况。

---

### 5.3 bm25_retrieval

基于 BM25 进行关键词召回。

BM25 更适合处理：

- 专有名词
- 文件名
- 明确关键词
- 短文本精确匹配

在企业知识库中，纯向量检索容易漏掉关键词强相关内容，所以 BM25 是非常重要的补充。

---

### 5.4 rrf_fusion

RRF 用于融合向量检索和 BM25 检索结果。

```text
vector_results
      ↓
   RRF Fusion
      ↑
bm25_results
```

通过多路召回融合，可以降低单一检索方式带来的偏差。

---

### 5.5 rerank

Rerank 用于对召回结果进行二次排序，提高最终进入上下文的内容质量。

生产环境中已经支持 Rerank 开关：

```env
ENABLE_RERANK=false
```

当线上服务器资源不足或模型下载受限时，可以关闭 Rerank，并使用 fallback 逻辑保证系统稳定运行。

---

### 5.6 parent_chunk

根据召回到的 child chunk 找到对应 parent chunk。

作用：

```text
召回阶段：用 child chunk 保证精度
生成阶段：用 parent chunk 保证上下文完整
```

---

### 5.7 build_context

最终构建 LLM 所需上下文，并生成 sources 来源引用。

输出内容：

```text
context：提供给 LLM 的知识库上下文
sources：前端展示的来源引用
chunks：调试用的最终 chunk 列表
```

---

## 6. Sources 来源引用设计

本项目支持回答后的来源引用展示。

sources 字段包括：

```text
file_id
file_name
file_type
page
```

来源引用链路：

```text
RAG build_context
  ↓
生成 sources
  ↓
search_knowledge Tool 返回 { context, sources }
  ↓
CustomToolNode 解析 ToolMessage
  ↓
context 写回 ToolMessage.content
  ↓
sources 写入 AgentState.sources
  ↓
Streaming updates 推送给前端
  ↓
前端 SourceList 展示来源
```

这个设计避免了把 sources 临时塞进事件流，而是让 sources 成为 Graph State 的一部分，更符合企业级状态管理思路。

---

## 7. Agent 工具调用系统

本项目基于 LangGraph 实现了 Agent Runtime。

当前工具：

| 工具 | 作用 |
|---|---|
| search_knowledge | 查询企业知识库 |
| get_weather | 查询城市天气 |
| get_current_time | 获取当前时间 |
| calculator | 数学计算 |

Agent 流程：

```text
START
  ↓
agent
  ↓
判断是否需要工具
  ↓
tools
  ↓
agent
  ↓
END
```

Agent 使用 `model.bind_tools()` 绑定工具，并通过 LangGraph 条件边判断是否进入工具节点。

---

## 8. CustomToolNode 设计

项目中自定义了 `CustomToolNode`，用于增强官方 ToolNode。

它的职责：

1. 执行官方 ToolNode
2. 解析工具返回结果
3. 识别 RAG Tool 返回的 JSON
4. 将 `context` 写回 ToolMessage
5. 将 `sources` 写入 Graph State
6. 兼容同步 `invoke` 和异步 `ainvoke`

这个设计解决了 RAG 工具返回结构化数据的问题：

```json
{
  "context": "知识库上下文",
  "sources": [
    {
      "file_id": 1,
      "file_name": "xxx.pdf",
      "file_type": "pdf",
      "page": 1
    }
  ]
}
```

最终 Agent 看到的是 context，前端拿到的是 sources。

---

## 9. Streaming Runtime

系统支持流式回答。

当前推荐路线：

```python
 graph.astream(stream_mode=["messages", "updates"])
```

其中：

```text
messages → token 流
updates  → state 更新，例如 sources
```

前端消费的事件协议：

```text
start       回答开始
tool_start  工具开始调用
tool_end    工具调用结束
sources     来源引用更新
stream      token 增量输出
end         回答结束
```

这种设计把模型 token 和业务状态更新分成两条线：

```text
token 流：负责实时展示回答
state 流：负责展示 sources、工具状态等业务信息
```

---

## 10. LangSmith 链路追踪

项目已经接入 LangSmith，用于 RAG Workflow 追踪和调试。

已追踪节点：

- rag_workflow
- build_context

LangSmith 可以帮助分析：

- 用户问题如何被改写
- 向量检索召回了什么
- BM25 召回了什么
- RRF 融合结果是否合理
- Rerank 是否生效
- 最终 context 是否正确
- LLM 回答是否基于知识库内容

---

## 11. 前端页面能力

前端已经具备 AI 产品化页面结构。

主要页面：

```text
登录页
聊天页
知识库管理页
Chunk 调试页
Retrieval Debug 页
```

主要组件：

```text
ChatMessage
SourceList
Thinking
ToolStatus
KbTree
ChunkPreview
KnowledgeModal
```

前端核心能力：

- 流式输出展示
- Markdown 渲染
- 来源引用展示
- 工具调用状态展示
- 知识库树管理
- Chunk 预览
- Retrieval 调试
- 登录状态管理

---

## 12. 数据存储设计

系统使用 PostgreSQL 存储业务数据，使用 ChromaDB 存储向量数据。

### PostgreSQL

用于存储：

```text
用户信息
知识库节点
文件信息
chunk 元数据
权限相关数据
```

### ChromaDB

用于存储：

```text
chunk content
embedding vector
metadata
```

### Docker Volume 持久化

线上 PostgreSQL 使用 Docker Volume 持久化，容器重启后数据不会丢失。

本地可以通过 SSH 隧道使用 DBeaver 连接线上 PostgreSQL。

---

## 13. 线上部署

项目已经完成线上部署。

部署结构：

```text
Tencent Cloud / Ubuntu Server
        ↓
Docker Compose
        ↓
backend container
frontend container
postgres container
caddy container
```

Caddy 路由：

```text
/       → Vue 前端
/api/*  → FastAPI 后端
```

生产环境配置：

```text
.env.production
DATABASE_URL
DEEPSEEK_API_KEY
OPENWEATHER_API_KEY
LANGCHAIN_API_KEY
CHROMA_PERSIST_DIR
UPLOAD_DIR
ROOT_PATH
ENABLE_RERANK
```

---

## 14. Jenkins 自动化发布

项目已经完成 Jenkins 自动化部署，并成功看到：

```text
Finished: SUCCESS
```

当前发布流程：

```text
本地开发
  ↓
git push origin main
  ↓
git push gitee main
  ↓
Jenkins 从 Gitee 拉取 main
  ↓
rsync 上传代码到服务器
  ↓
Docker Compose build
  ↓
Docker Compose up -d
  ↓
Health Check
  ↓
发布成功
```

Jenkins 已解决的问题：

- GitHub 拉取超时，改用 Gitee
- Jenkinsfile Groovy 语法修复
- SSH 私钥认证问题
- docker compose 权限问题
- 前端 Linux 大小写构建问题
- Docker 构建与线上部署流程打通

---

## 15. 当前项目亮点

### 15.1 从前端到 AI 应用闭环

项目不仅实现 AI 后端能力，还完成了 Vue3 前端产品化界面。

覆盖：

```text
问答 UI
知识库 UI
流式回答
来源引用
工具状态
调试页面
```

---

### 15.2 RAG 不是简单 Demo

项目完成了比较完整的企业级 RAG 链路：

```text
Query Analysis
Vector Recall
BM25 Recall
RRF Fusion
Rerank
Parent Chunk
Context Build
Sources
```

---

### 15.3 Agent 与 RAG 结合

RAG 不是单独接口，而是被封装成 Agent Tool。

Agent 可以根据用户问题自动选择：

```text
知识库查询
天气查询
时间查询
数学计算
```

---

### 15.4 Sources 进入 Graph State

来源引用不是临时拼接，而是进入 AgentState，支持 streaming updates 推送给前端。

---

### 15.5 已完成生产化部署

项目已经不是本地 Demo，而是完成：

```text
Docker Compose
Caddy
PostgreSQL Volume
Jenkins CI/CD
线上访问
```

---

## 16. 当前阶段成果

项目目前已经完成三个大阶段。

### 第一阶段：RAG 基础能力

- 文件上传
- 文档解析
- 文档切片
- 向量入库
- 基础检索
- 来源引用

### 第二阶段：RAG 工程化

- Parent-Child Chunk
- Metadata 管理
- BM25 混合检索
- RRF 融合
- Rerank
- LangGraph RAG Workflow
- LangSmith 追踪

### 第三阶段：AI 应用生产化

- Agent 工具调用
- 流式输出
- 前端 AI 产品化页面
- Docker 容器化
- Caddy 反向代理
- Jenkins 自动部署
- Gitee 发布链路

---

## 17. 后续规划

### 17.1 代码清理

统一 Streaming Runtime：

```text
agent_chat_stream
  ↓
graph.astream(stream_mode=["messages", "updates"])
  ↓
route_graph_stream
  ↓
chat_service
```

逐步归档旧的 `astream_events` 解析逻辑。

---

### 17.2 RAG 质量增强

计划继续优化：

- Metadata Filter
- 多知识库隔离
- 用户权限隔离
- 文件级权限
- Query Rewrite 评估
- Multi Query 评估
- Rerank 线上优化
- 召回评测集

---

### 17.3 Memory Runtime

后续计划实现：

- 短期对话记忆
- 长期用户记忆
- 会话摘要
- 历史压缩
- 多轮 RAG 查询改写

---

### 17.4 MCP Runtime

后续计划接入 MCP：

```text
理解 MCP
  ↓
选择 MCP Server
  ↓
接入 MCP Client
  ↓
MCP Tools 转 LangChain Tool
  ↓
加入 Agent tools
  ↓
验证 ToolNode / Streaming / Sources 兼容
```

---

### 17.5 生产安全增强

后续计划补充：

- 域名绑定
- HTTPS
- Caddy 自动证书
- PostgreSQL 端口仅本机监听
- Docker Volume 备份
- 日志轮转
- 环境变量安全管理

---

## 18. 阶段性总结

本项目已经从本地 AI Demo 升级为一个具备完整链路的 AI 应用系统。

当前已经完成：

```text
AI 能力：RAG + Agent + Tool Calling
工程能力：前后端分离 + 状态管理 + 流式协议
数据能力：PostgreSQL + ChromaDB + Docker Volume
部署能力：Docker Compose + Caddy + Jenkins
调试能力：Chunk Debug + Retrieval Debug + LangSmith
```

下一阶段重点将从“能跑通”转向“更稳定、更准确、更安全、更适合面试展示”。
