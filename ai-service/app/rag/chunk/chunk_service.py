import uuid

from app.knowledgedb import models

from app.utils.parsers.parser_factory import ParserFactory

from app.utils.splitters.splitter_factory import SplitterFactory

from app.utils.splitters.chunk_builder import ChunkBuilder

from app.rag.vectorstore.chroma_service import (
    save_chunks_to_chroma
)


def create_chunks(
        db,
        file_id,
        original_name,
        uuid_name,
        file_path
):

    # 文件类型
    file_type = original_name.split(".")[-1].lower()

    source_info = {

        "file_id": file_id,

        "file_name": original_name,

        "uuid_name": uuid_name,

        "file_type": file_type
    }

    # 1 parser
    parser = ParserFactory.get_parser(file_type)

    parsed_docs = parser.parse(file_path)

    # 2 splitter
    splitter = SplitterFactory.get_splitter(file_type)

    # 3 chunk builder
    builder = ChunkBuilder(splitter)

    all_chunk_items = []

    # 4 build chunks
    for doc in parsed_docs:

        chunks = builder.build(

            text=doc["text"],

            source_info={

                **source_info,

                "page": doc.get("page")
            }
        )

        # 5 save mysql
        for index, chunk in enumerate(chunks):

            print(f"\n--- chunk {index} ---")
            print(chunk["text"])

            chunk_item = models.KnowledgeChunk(

                file_id=file_id,

                chunk_index=index,

                content=chunk["text"],

                meta_info=chunk["metadata"],

                embedding_status="pending",

                vector_id=str(uuid.uuid4())
            )

            all_chunk_items.append(chunk_item)

    # 6 批量保存
    db.add_all(all_chunk_items)

    db.commit()

    for item in all_chunk_items:

        db.refresh(item)

    # 7 save chroma
    save_chunks_to_chroma(all_chunk_items)

    return all_chunk_items



# 第一版
# from app.knowledgedb import models, schemas
# # from app.utils.chunk import split_text
# from app.utils.splitters.splitter_factory import split_by_file_type
# import json
# import uuid
# from app.rag.vectorstore.chroma_service import ( 
#     save_chunks_to_chroma
# )
# def create_chunks(db,file_id,original_name,uuid_name,file_path,text):

#     chunks = split_by_file_type(
#             file_id,
#             original_name,
#             uuid_name,
#             file_path,
#             text
#             )
#     print("\n========== chunk result ==========\n")

#     chunk_items = []
# # enumerate 函数可以同时获取列表的索引和内容，这里我们需要知道每个 chunk 的顺序，所以使用 enumerate 来获取 chunk_index和 chunk_text
#     for index, chunk in enumerate(chunks):
#         content = chunk.content
#         meta_info = chunk.metadata
#         meta_info["chunk_index"] = index  # 添加 chunk_index 到 meta_info 中，方便后续查询和调试
#         print(f"\n--- chunk {index} ---")
#         print(content)
#         print("长度:", len(content))
#         print("meta_info:", meta_info)
#         chunk_item = models.KnowledgeChunk(
#             file_id=file_id,
#             chunk_index=index,
#             content=content,
#             meta_info=meta_info,
#             embedding_status="pending",
#             vector_id=str(uuid.uuid4())
#         )

#         chunk_items.append(chunk_item)

#     db.add_all(chunk_items) #最后一次性添加所有 chunk_item，减少数据库交互次数，提高效率
#     db.commit()
#     for item in chunk_items:
#         db.refresh(item)
#     save_chunks_to_chroma(chunk_items)  