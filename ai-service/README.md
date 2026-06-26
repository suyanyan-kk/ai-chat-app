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

```bash
./.venv/bin/python -m app.scripts.create_admin \
  --email admin@example.com \
  --name "System Administrator"
```

命令会在终端中安全地提示输入并确认管理员密码。创建后，可在前端
`http://127.0.0.1:5173/login` 登录。

也可以在 `.env` 中同时设置
`AUTH_BOOTSTRAP_ADMIN_EMAIL` 和 `AUTH_BOOTSTRAP_ADMIN_PASSWORD`，
由服务启动时自动创建首个管理员。生产环境应同时设置
`AUTH_COOKIE_SECURE=true`。
