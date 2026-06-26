from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router
from app.api.title import router as title_router
from app.api.health import router as health_router
from app.api.knowledge import router as knowledge_router
from app.auth.bootstrap import initialize_auth
from app.auth.dependencies import get_current_user
from app.auth.router import router as auth_router

from app.core.exception import register_exception
from app.core.logger import logger
import uvicorn
from app.api.chunk_debug import router as chunk_router
from app.api.retrieval_debug import router as debug_router
app = FastAPI()

UPLOAD_DIR = Path(__file__).resolve().parent / "rag" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 请求: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 响应: {response.status_code}")
    return response

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 注册异常处理
register_exception(app)
# 注册路由
app.include_router(auth_router)
app.include_router(health_router)
protected_dependencies = [
    Depends(get_current_user)
]
app.include_router(
    chat_router,
    dependencies=protected_dependencies,
)
app.include_router(
    title_router,
    dependencies=protected_dependencies,
)
app.include_router(
    knowledge_router,
    dependencies=protected_dependencies,
)
app.include_router(
    chunk_router,
    dependencies=protected_dependencies,
)
app.include_router(
    debug_router,
    dependencies=protected_dependencies,
)


@app.on_event("startup")
def startup():
    initialize_auth()


def dev():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
logger.info("🚀 服务启动成功")
