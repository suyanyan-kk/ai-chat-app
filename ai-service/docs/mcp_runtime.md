# MCP Runtime

## 1. 当前 MCP Server

当前项目已经接入 5 类 MCP Server：

| Server | Transport | 作用 |
|---|---|---|
| demo | stdio | 本地 MCP 测试工具 |
| filesystem | stdio | 访问本地安全目录 |
| github | stdio + docker | 访问 GitHub 仓库 / Issue / PR |
| postgres | stdio | 只读访问项目 PostgreSQL 数据库 |
| remote_http | streamable_http | 远程 HTTP MCP Server 测试 |

## 2. stdio MCP

stdio MCP 表示 MCP Client 启动一个本地子进程，然后通过标准输入/标准输出通信。

典型例子：

```text
npx @modelcontextprotocol/server-filesystem
docker run ghcr.io/github/github-mcp-server
python app/mcp_servers/demo_server.py
python app/mcp_servers/postgres_server.py
特点：

不需要端口
适合本地工具
适合命令行工具
server 不能随便 print 到 stdout
子进程启动失败时，常见错误是 Connection closed
3. Streamable HTTP MCP

Streamable HTTP MCP 表示 MCP Server 是一个独立 HTTP 服务，Client 通过 URL 连接。

当前项目示例：

http://127.0.0.1:8765/mcp

特点：

Server 独立运行
Client 通过 URL 连接
更接近生产环境部署方式
适合跨服务、跨机器调用
4. Tool 安全策略

当前项目不把所有 MCP tools 都交给 Agent，而是通过白名单过滤。

白名单位置：

app/agent/mcp/tools.py

核心变量：

SAFE_MCP_TOOL_NAMES

只允许只读或安全工具进入 Agent。

例如：

允许：
- read_file
- list_directory
- search_repositories
- get_file_contents
- pg_query_readonly
- remote_echo

禁止：
- delete_file
- push_files
- create_repository
- merge_pull_request
5. Agent 调用优先级

当前 Agent 工具调用优先级：

用户问题
  ↓
MCP Router 确定性路由
  ↓
RAG search_knowledge 兜底
  ↓
LLM 普通回答

原因：

MCP 工具是明确外部系统操作
RAG 是知识库检索兜底
防止用户要求调用 MCP 时，被 RAG 抢走
6. Sources 处理

RAG Tool 会返回：

{
  "context": "...",
  "sources": [...]
}

CustomToolNode 会把：

context → ToolMessage.content
sources → AgentState.sources

MCP Tool 通常返回普通字符串，不产生 sources。

所以：

RAG 回答有 sources
MCP 回答通常没有 sources
7. 调试命令

查看 MCP Server 配置：

uv run python -c "from app.agent.mcp.servers import MCP_SERVER_CONFIGS; print(MCP_SERVER_CONFIGS.keys())"

测试 MCP tools：

uv run python -m app.scripts.test_mcp_client

健康检查：

uv run python -m app.scripts.check_mcp_runtime

启动 Remote HTTP MCP：

uv run python app/mcp_servers/remote_http_server.py

启动 FastAPI：

uv run uvicorn app.main:app --reload
8. 当前 MCP Runtime 能力总结

当前项目已经完成：

stdio MCP 接入
Streamable HTTP MCP 接入
Filesystem MCP
GitHub MCP
PostgreSQL MCP
MCP Tool 白名单过滤
MCP Router 确定性调用
MCP + LangGraph Agent 集成
MCP + Streaming Runtime 集成
MCP 与 RAG sources 隔离

---

