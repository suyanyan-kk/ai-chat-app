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