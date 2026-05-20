from app.knowledgedb import models, schemas
# from app.utils.chunk import split_text
from app.utils.splitters.splitter_factory import split_by_file_type
import json
import uuid
from app.rag.vectorstore.chroma_service import (
    save_chunks_to_chroma
)
def create_chunks(db,file_id,original_name,uuid_name,file_path,text):

    chunks = split_by_file_type(
            file_id,
            original_name,
            uuid_name,
            file_path,
            text
            )
    print("\n========== chunk result ==========\n")

    chunk_items = []
# enumerate 函数可以同时获取列表的索引和内容，这里我们需要知道每个 chunk 的顺序，所以使用 enumerate 来获取 chunk_index和 chunk_text
    for index, chunk in enumerate(chunks):
        content = chunk.content
        meta_info = chunk.metadata
        meta_info["chunk_index"] = index  # 添加 chunk_index 到 meta_info 中，方便后续查询和调试
        print(f"\n--- chunk {index} ---")
        print(content)
        print("长度:", len(content))
        print("meta_info:", meta_info)
        chunk_item = models.KnowledgeChunk(
            file_id=file_id,
            chunk_index=index,
            content=content,
            meta_info=meta_info,
            embedding_status="pending",
            vector_id=str(uuid.uuid4())
        )

        chunk_items.append(chunk_item)

    db.add_all(chunk_items) #最后一次性添加所有 chunk_item，减少数据库交互次数，提高效率
    db.commit()
    for item in chunk_items:
        db.refresh(item)
    save_chunks_to_chroma(chunk_items) 