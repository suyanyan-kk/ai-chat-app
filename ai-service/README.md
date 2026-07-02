<!--  启动服务 
uv run uvicorn app.main:app --reload
--reload 自动热更新
你应该会看到：

Uvicorn running on http://127.0.0.1:8000

打开浏览器：

http://127.0.0.1:8000

应该返回：

{"message":"AI Service is running"}

<!-- 打开浏览器：

http://127.0.0.1:8000

或者：

http://127.0.0.1:8000/docs

这个是 FastAPI 自动生成的接口文档。 -->

## 登录初始化

当前版本不开放自助注册。首次使用前，在 `ai-service` 目录执行：

## 本地：
```bash
./.venv/bin/python -m app.scripts.create_admin \
  --email admin@example.com \
  --name "System Administrator"
```
## 线上：
```bash
sudo docker exec -it ai_backend python -m app.scripts.create_admin \
  --email admin@yanaihub.cn \
  --name "System Administrator"
```

命令会在终端中安全地提示输入并确认管理员密码。创建后，可在前端
`http://127.0.0.1:5173/login` 登录。

也可以在 `.env` 中同时设置
`AUTH_BOOTSTRAP_ADMIN_EMAIL` 和 `AUTH_BOOTSTRAP_ADMIN_PASSWORD`，
由服务启动时自动创建首个管理员。生产环境应同时设置
`AUTH_COOKIE_SECURE=true`。


<!-- 目前RAG：

向量召回 + BM25 关键词召回 + RRF 融合 + Parent-Child Chunk + Sources 引用

只是暂时不开 CrossEncoder rerank。

线上轻量服务器版本默认关闭 rerank，避免大模型常驻占用内存。
系统保留 ENABLE_RERANK 开关，资源充足时可以启用 CrossEncoder rerank。
后续真正开启 rerank 的路线

等网站主流程稳定后，再单独做这一步：

1. 给 HuggingFace 模型缓存挂 Docker volume
2. 单独执行一次模型预下载脚本
3. 确认容器内能加载 BAAI/bge-reranker-v2-m3
4. 设置 ENABLE_RERANK=true
5. 重启 backend
6. 验证 RAG 检索质量 -->
