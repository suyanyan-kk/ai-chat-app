from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.title import router as title_router
from app.api.health import router as health_router
from app.core.exception import register_exception
from app.core.logger import logger
import uvicorn

app = FastAPI()
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 请求: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 响应: {response.status_code}")
    return response

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 注册异常处理
register_exception(app)
# 注册路由
app.include_router(chat_router)
app.include_router(title_router)
app.include_router(health_router)
def dev():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
logger.info("🚀 服务启动成功")
