# 接口数据格式
# Pydantic BaseModel = 用来定义“接口数据格式（入参/出参）”
from pydantic import BaseModel
# Optional 表示“可以为空”
from typing import Optional

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