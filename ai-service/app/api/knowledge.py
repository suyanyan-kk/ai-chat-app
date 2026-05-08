from fastapi import APIRouter,Depends,status,File,UploadFile
from uuid import uuid4
from sqlalchemy.orm import Session
from app.knowledgedb import models, schemas
from app.knowledgedb.db import SessionLocal, engine

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# 创建表（自动）如果表不存在 → 自动创建
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# 每次请求 → 创建一个数据库连接 → 用完关闭
# yield 生成器函数，第一次调用时执行到 yield 处暂停，返回 db 对象，第二次调用时继续执行 finally 块，关闭数据库连接
# Depends(get_db) 表示在每个接口函数中注入一个 db 参数，值由 get_db 函数提供，确保每次请求都有一个独立的数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. 读取（Read）
@router.get("/getKnowledge")
def get_all(db: Session = Depends(get_db)):
    # print(dir(db.query(models.Knowledge).all()),'1222')
    return db.query(models.Knowledge).all()


# 2. 创建（Create）
@router.post("/addKnowledge", status_code=status.HTTP_201_CREATED)
 #  ** （解构）把 data 对象的属性解构成一个个参数传给 Knowledge 构造函数
def create_knowledge(
    data: schemas.KnowledgeCreate,
    db: Session = Depends(get_db)
):
    item = models.Knowledge(**data.dict())
    # ORM = 把“数据库操作”变成“操作对象”
    # print(item.__dict__)
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "code": 0,
        "message": "创建成功",
        "data": item
    }
# 3. 更新（Update）
# data.dict(exclude_unset=True) 只更新传了的字段，没传的字段保持不变
@router.put("/updateKnowledge/{id}")
def update_knowledge(id: int, data: schemas.KnowledgeCreate, db: Session = Depends(get_db)):
    item = db.query(models.Knowledge).get(id)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    return item

# 4. 删除（Delete）
@router.delete("/deleteKnowledge/{id}", status_code=status.HTTP_200_OK)
def delete_knowledge(id: int, db: Session = Depends(get_db)):
   
    item = db.get(models.Knowledge, id)

    if not item:
        return {
            "code": 1,
            "message": "数据不存在"
        }
    db.delete(item)
    db.commit()
    return {
        "code": 0,
        "message": "删除成功",
    }

@router.post("/uploadKnowledgeFile")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
    ):
     # 1. 读取文件内容
    content = await file.read()
    
    # 2. 生成 uuid 文件名
    ext = file.filename.split(".")[-1]

    uuid_name = f"{uuid4()}.{ext}"
    
    # 3. 文件保存路径
    file_path = os.path.join(UPLOAD_DIR, uuid_name)
    
    # 4. 保存文件
    with open(file_path, "wb") as f:
        f.write(content)

    # 5. 提取文本（第一版先只支持 txt/md）
    text_content = ""

    try:
        text_content = content.decode("utf-8")
    except Exception:
        text_content = "暂不支持该文件解析"
    # 创建目录
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # 写文件表
    file_item = models.KnowledgeFile(
        original_name=file.filename,
        uuid_name=uuid_name,
        file_url=file_path,
        file_size=len(content),
        file_type=file.content_type,
        content= text_content
    )

    db.add(file_item)
    db.commit()
    db.refresh(file_item)
# 这里会生成id，前端可以把这个id 存到知识库节点的 file_id 字段里，后续需要使用这个文件时再根据 file_id 从知识文件表里查出文件信息
    return {
        "code": 0,
        "message": "创建成功",
        "data": file_item
    }

# 获取知识节点详情
@router.get("/getKnowledgeDetail/{id}")
def get_knowledge_detail(
    id: int,
    db: Session = Depends(get_db)
):

    # 1. 查询树节点
    knowledge = db.get(models.Knowledge, id)

    if not knowledge:
        return {
            "code": 1,
            "message": "节点不存在"
        }

    # 2. 基础树节点数据
    result = {
        "id": knowledge.id,
        "title": knowledge.title,
        "type": knowledge.type,
        "parent_id": knowledge.parent_id,
        "file_id": knowledge.file_id,
        "description": knowledge.description,
        "is_open": knowledge.is_open,
        "file": None
    }

    # 3. 如果是文件
    if knowledge.file_id:

        file_item = db.get(
            models.KnowledgeFile,
            knowledge.file_id
        )

        if file_item:

            result["file"] = {
                "id": file_item.id,
                "original_name": file_item.original_name,
                "uuid_name": file_item.uuid_name,
                "file_url": file_item.file_url,
                "file_size": file_item.file_size,
                "file_type": file_item.file_type,
                "content": file_item.content
            }

    return {
        "code": 0,
        "message": "获取成功",
        "data": result
    }