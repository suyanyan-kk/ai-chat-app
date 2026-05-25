import uuid

from app.knowledgedb import models

from app.utils.splitters.splitter_factory import (
    SplitterFactory
)

from app.utils.splitters.chunk_builder import (
    ChunkBuilder
)

from app.rag.vectorstore.chroma_service import (
    save_chunks_to_chroma
)


def create_chunks(
        db,
        file_id,
        original_name,
        uuid_name,
        parsed_docs,
):

    # =========================
    # file type
    # =========================
    file_type = original_name.split(".")[-1].lower()

    source_info = {

        "file_id": file_id,

        "file_name": original_name,

        "uuid_name": uuid_name,

        "file_type": file_type,
    }

    # =========================
    # splitter
    # =========================
    splitter = SplitterFactory.get_splitter(
        file_type
    )

    # =========================
    # builder
    # =========================
    builder = ChunkBuilder(splitter)

    all_chunk_items = []

    global_chunk_index = 0

    # =========================
    # build chunks
    # =========================
    for doc_index, doc in enumerate(parsed_docs):

        chunks = builder.build(

            text=doc["text"],

            source_info={

                **source_info,

                "page": doc.get("page"),

                "doc_index": doc_index,
                
            }
        )

        for chunk in chunks:

            metadata = chunk["metadata"]

            chunk_type = metadata.get("chunk_type")

            parent_index = metadata.get("parent_index")

            child_index = metadata.get("child_index")

            structure_index = metadata.get("structure_index")
            vector_id = (
                f"file_{file_id}_"

                f"chunk_{global_chunk_index}"
            )
        

            # =========================
            # debug
            # =========================
            print(f"\n--- chunk {global_chunk_index} ---")

            print("vector_id:",vector_id)

            print("splitter:",metadata.get("splitter"))

            print(
                "semantic_layer:",
                metadata.get(
                    "semantic_layer"
                )
            )

            print("chunk_type:",chunk_type)

            print("page:",metadata.get("page"))

            print(chunk["text"])

            print("\n=====================\n")

            # =========================
            # PostgreSQL
            # =========================
            chunk_item = models.KnowledgeChunk(

                file_id=file_id,

                chunk_index=global_chunk_index,

                content=chunk["text"],

                meta_info=metadata,

                embedding_status="pending",

                vector_id=vector_id
            )

            all_chunk_items.append(
                chunk_item
            )

            global_chunk_index += 1

    # =========================
    # batch save
    # =========================
    db.add_all(all_chunk_items)

    db.commit()

    for item in all_chunk_items:

        db.refresh(item)

    # =========================
    # save chroma
    # =========================
    save_chunks_to_chroma(
        all_chunk_items
    )

    return all_chunk_items

# parent
# file_8_s_0_p_0
# child
# file_8_s_0_p_0_c_2

# file_3_s_2_p_1_c_5
# 文件3
# 结构2
# parent1
# child5