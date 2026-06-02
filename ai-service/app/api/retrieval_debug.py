from fastapi import APIRouter

from app.rag.retrieval.retrieval_debug import (
    retrieval_pipeline_debug
)
from pydantic import BaseModel

router = APIRouter(
    prefix="/debug",
    tags=["debug"]
)



class RetrievalRequest(BaseModel):
    query: str


@router.post("/retrieval")
def retrieval_debug(
        data: RetrievalRequest
):
    result = retrieval_pipeline_debug(
        query=data.query
    )
    return {
        "code": 0,
        "message": "调试成功",
        "data": result
    }