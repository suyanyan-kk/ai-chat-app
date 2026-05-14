# 接口数据格式
# Pydantic BaseModel = 用来定义“接口数据格式（入参/出参）”
from pydantic import BaseModel
# Optional 表示“可以为空”
from typing import Optional,Any
class KnowledgeCreate(BaseModel):
    title: str
    parent_id: Optional[int] = None
    type: str
    is_open: Optional[bool] = False
    description: Optional[str] = ""
    file_id: Optional[int] = None
    # file_url: Optional[str] = None


class KnowledgeOut(KnowledgeCreate):
    id: int
    class Config:
        # from_attributes=True 表示自动把 ORM （类） 对象转成 JSON
        from_attributes = True 

class KnowledgeFileOut(BaseModel):
    id: int
    original_name: str
    uuid_name: str
    file_url: str
    file_size: int
    file_type: str
    content: str
    embedding_status: str
    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    code: int
    message: str
    data: KnowledgeFileOut
    class Config:
        from_attributes = True

class ChunkOut(BaseModel):

    id: int
    chunk_index: int
    content: str
    meta_info: Any
    embedding_status: str
    class Config:
        from_attributes = True
class ApiResponse(BaseModel):
    code: int
    message: str

# class UploadResponse(ApiResponse):
#     data: KnowledgeFileOut
