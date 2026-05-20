from fastapi import APIRouter
from app.llm.services.chunk_service import (
    get_chunks_by_file,
    search_chunks
)

router = APIRouter(
    prefix="/chunk",
    tags=["Chunk调试"]
)

# 查看某个文件的chunk
@router.get("/list/{file_id}")
def chunk_list(file_id: str):

    data = get_chunks_by_file(file_id)

    return {
        "code": 0,
        "data": data
    }


# 测试向量召回
@router.get("/search")
def chunk_search(
    query: str,
    top_k: int = 5
):

    data = search_chunks(query, top_k)

    return {
        "code": 0,
        "data": data
    }