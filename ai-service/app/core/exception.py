# 全局异常处理
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger

# 自定义业务异常
class AppException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code

# 注册异常处理
def register_exception(app):

    # 👉 业务异常
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.error(f"[业务异常] {exc.message}")

        return JSONResponse(
            status_code=exc.code,
            content={
                "code": exc.code,
                "message": exc.message
            }
        )

    # 👉 全局异常（兜底）
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"[系统异常] {str(exc)}")

        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "服务器内部错误"
            }
        )