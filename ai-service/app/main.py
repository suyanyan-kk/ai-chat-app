from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.title import router as title_router
from app.api.health import router as health_router

import uvicorn

app = FastAPI()

# 注册路由
app.include_router(chat_router)
app.include_router(title_router)
app.include_router(health_router)

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def dev():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)