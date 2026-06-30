# app/core/config.py

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv


# =========================
# Project Root
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]


# =========================
# Load Env
# =========================
#
# 本地开发时：
#   默认读取 ai-service/.env
#
# Docker / 线上时：
#   docker-compose 会通过 env_file 注入 .env.production
#
# 所以这里 load_dotenv 不会影响线上，只是方便本地开发。
# =========================

load_dotenv()


class Settings:
    """
    项目统一配置中心。

    以后所有路径、数据库连接、第三方 Key，
    都从这里读取，不要在业务代码里到处 os.getenv。
    """

    # =========================
    # App
    # =========================

    APP_ENV: str = os.getenv(
        "APP_ENV",
        "development"
    )
    # =========================
    # API Root Path
    # =========================
    #
    # 本地直接访问后端：
    #   ROOT_PATH=""
    #
    # Docker / 线上通过 Caddy 访问：
    #   ROOT_PATH="/api"
    # =========================

    ROOT_PATH: str = os.getenv(
        "ROOT_PATH",
        ""
    )
    # =========================
    # LLM
    # =========================

    DEEPSEEK_API_KEY: str | None = os.getenv(
        "DEEPSEEK_API_KEY"
    )

    DEEPSEEK_BASE_URL: str = os.getenv(
        "DEEPSEEK_BASE_URL",
        "https://api.deepseek.com"
    )

    # =========================
    # Weather
    # =========================

    OPENWEATHER_API_KEY: str | None = os.getenv(
        "OPENWEATHER_API_KEY"
    )

    # =========================
    # Database
    # =========================

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"
    )

    # =========================
    # Chroma
    # =========================

    CHROMA_PERSIST_DIR: str = os.getenv(
        "CHROMA_PERSIST_DIR",
        str(BASE_DIR / "chroma_db")
    )

    # =========================
    # Upload
    # =========================

    UPLOAD_DIR: str = os.getenv(
        "UPLOAD_DIR",
        str(BASE_DIR / "app" / "rag" / "uploads")
    )

    # =========================
    # LangSmith
    # =========================

    LANGCHAIN_TRACING_V2: str | None = os.getenv(
        "LANGCHAIN_TRACING_V2"
    )

    LANGCHAIN_API_KEY: str | None = os.getenv(
        "LANGCHAIN_API_KEY"
    )

    LANGCHAIN_PROJECT: str = os.getenv(
        "LANGCHAIN_PROJECT",
        "ai-service-dev"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()