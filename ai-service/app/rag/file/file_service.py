
import os

from uuid import uuid4

from app.knowledgedb import models

from app.rag.chunk.chunk_service import create_chunks


BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)


async def save_upload_file(file, db):

    print("save_upload_file:", file.filename)

    # 1 读取文件
    content = await file.read()

    # 2 文件后缀
    ext = file.filename.split(".")[-1].lower()

    # 3 uuid文件名
    uuid_name = f"{uuid4()}.{ext}"

    # 4 创建上传目录
    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    # 5 文件路径
    file_path = os.path.join(
        UPLOAD_DIR,
        uuid_name
    )

    # 6 保存文件
    with open(file_path, "wb") as f:

        f.write(content)

    # 7 创建文件记录
    file_item = models.KnowledgeFile(

        original_name=file.filename,

        uuid_name=uuid_name,

        file_url=file_path,

        file_size=len(content),

        # 文件扩展名
        file_type=ext,

        # 不再提前解析
        content="",

        embedding_status="pending"
    )

    db.add(file_item)

    db.commit()

    db.refresh(file_item)

    # 8 创建 chunks
    create_chunks(

        db=db,

        file_id=file_item.id,

        original_name=file.filename,

        uuid_name=uuid_name,

        file_path=file_path
    )

    return file_item
