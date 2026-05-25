import os

from uuid import uuid4

from app.knowledgedb import models

from app.rag.chunk.chunk_service import (
    create_chunks
)

from app.utils.parsers.parser_factory import (
    ParserFactory
)

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)


async def save_upload_file(file, db):

    print("save_upload_file:", file.filename)

    # =========================
    # 1 read file
    # =========================
    content = await file.read()

    # =========================
    # 2 file ext
    # =========================
    ext = file.filename.split(".")[-1].lower()

    # =========================
    # 3 uuid file name
    # =========================
    uuid_name = f"{uuid4()}.{ext}"

    # =========================
    # 4 create upload dir
    # =========================
    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    # =========================
    # 5 file path
    # =========================
    file_path = os.path.join(
        UPLOAD_DIR,
        uuid_name
    )

    # =========================
    # 6 save file
    # =========================
    with open(file_path, "wb") as f:

        f.write(content)

    # =========================
    # 7 parser
    # =========================
    parser = ParserFactory.get_parser(ext)

    parsed_docs = parser.parse(file_path)

    # =========================
    # 8 full content
    # =========================
    full_content = "\n".join(

        doc["text"]

        for doc in parsed_docs
    )

    # =========================
    # 9 create file record
    # =========================
    file_item = models.KnowledgeFile(

        original_name=file.filename,

        uuid_name=uuid_name,

        file_url=file_path,

        file_size=len(content),

        file_type=ext,

        # 前端全文展示
        content=full_content,

        embedding_status="pending"
    )

    db.add(file_item)

    db.commit()

    db.refresh(file_item)

    # =========================
    # 10 create chunks
    # =========================
    create_chunks(

        db=db,

        file_id=file_item.id,

        original_name=file.filename,

        uuid_name=uuid_name,

        parsed_docs=parsed_docs 
    )

    return file_item