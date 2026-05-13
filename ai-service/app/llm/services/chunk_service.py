from app.knowledgedb import models, schemas
from app.utils.chunk import split_text

def create_chunks(
    db,
    file_id,
    text
):

    chunks = split_text(text)

    chunk_items = []

    for index, chunk_text in enumerate(chunks):

        chunk_item = models.KnowledgeChunk(
            file_id=file_id,
            chunk_index=index,
            content=chunk_text,
            embedding_status="pending"
        )

        chunk_items.append(chunk_item)

    db.add_all(chunk_items) #最后一次性添加所有 chunk_item，减少数据库交互次数，提高效率

    db.commit()