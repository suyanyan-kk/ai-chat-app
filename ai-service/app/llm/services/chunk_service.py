from app.rag.vectorstore.chroma_service import (
    vector_store
)

"""
Chunk 调试服务
"""


# 查看所有 chunk
def get_all_chunks():

    result = vector_store.get(

        include=[
            "documents",
            "metadatas"
        ]
    )

    ids = result.get("ids", [])

    documents = result.get(
        "documents",
        []
    )

    metadatas = result.get(
        "metadatas",
        []
    )

    data = []

    for i in range(len(ids)):

        metadata = metadatas[i] or {}

        data.append({

            "id": ids[i],

            "content": documents[i],

            "length": len(documents[i]),

            "metadata": metadata
        })

    return data


# 根据 file_id 查看 chunk
def get_chunks_by_file(file_id):

    result = vector_store.get(

        where={
            "file_id": int(file_id)
        },
        include=[
            "documents",
            "metadatas"
        ]
    )

    ids = result.get("ids", [])

    documents = result.get(
        "documents",
        []
    )

    metadatas = result.get(
        "metadatas",
        []
    )

    data = []

    for i in range(len(ids)):

        metadata = metadatas[i] or {}

        data.append({

            "id": ids[i],

            "content": documents[i],

            "length": len(documents[i]),

            "metadata": metadata
        })

    return data


# chunk 向量搜索调试
def search_chunks(
    query,
    top_k=5
):

    docs = vector_store.similarity_search_with_score(

        query=query,

        k=top_k
    )

    data = []

    for doc, score in docs:

        data.append({

            "content": doc.page_content,

            "score": round(score, 4),

            "metadata": doc.metadata
        })

    return data