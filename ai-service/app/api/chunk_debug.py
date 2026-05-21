from fastapi import APIRouter

from app.llm.services.chunk_service import (

    get_all_chunks,

    get_chunks_by_file,

    search_chunks
)

router = APIRouter(

    prefix="/chunk",

    tags=["Chunk调试"]
)


# 查看全部 chunk
@router.get("/all")
def chunk_all():

    data = get_all_chunks()

    return {
        "code": 0,
        "data": data
    }


# 查看某个文件 chunk
@router.get("/file/{file_id}")
def chunk_file(file_id: str):

    data = get_chunks_by_file(
        file_id
    )

    return {
        "code": 0,
        "data": data
    }


# chunk 检索调试
@router.get("/search")
def chunk_search(

    query: str,

    top_k: int = 5
):

    data = search_chunks(
        query,
        top_k
    )

    return {
        "code": 0,
        "data": data
    }