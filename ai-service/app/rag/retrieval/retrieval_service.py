from app.rag.vectorstore.chroma_service import (
    vector_store
)

from app.rag.rerank.rerank_service import (
    rerank_documents
)

# =========================
# 向量检索
# =========================
def similarity_search(
        query: str,
        k: int = 20
):

    """
    Chroma 向量召回
    """
    # LangChain
    results = vector_store.similarity_search(

        query=query,

        k=k
    )
    print("\n========== 向量粗召回==========\n")
    for item in results:
        print("\n========== 向量粗召回检索结果 ==========\n")
        print(item)
    return results


# =========================
# rerank retrieval
# =========================
def rerank_search(
        query: str,
        recall_k: int = 20,
        rerank_top_k: int = 5
):

    """
    先 embedding recall
    再 rerank
    """

    # =========================
    # 1 recall
    # =========================
    results = similarity_search(

        query=query,

        k=recall_k
    )

    # =========================
    # 2 format docs
    # =========================
    candidates = []

    for item in results:

        candidates.append({

            "content": item.page_content,

            "metadata": item.metadata
        })

    # =========================
    # 3 rerank
    # =========================
    rerank_results = rerank_documents(

        query=query,

        documents=candidates,

        top_n=rerank_top_k
    )

    return rerank_results


# =========================
# 构建 RAG context
# =========================
def build_rag_context(

        query: str,

        recall_k: int = 20,

        rerank_top_k: int = 5
):

    """
    构建最终 RAG context
    """

    # =========================
    # rerank retrieval
    # =========================
    results = rerank_search(

        query=query,

        recall_k=recall_k,

        rerank_top_k=rerank_top_k
    )

    print("\n========== RERANK 检索结果 ==========\n")

    context_list = []

    sources = []

    # 去重
    seen_sources = set()

    for item in results:

        print(
            "rerank_score:",
            item.get("rerank_score")
        )

        print(
            item["content"]
        )

        print(
            item["metadata"]
        )

        print("\n----------------\n")

        # =========================
        # context
        # =========================
        context_list.append(

            item["content"]
        )

        # =========================
        # metadata
        # =========================
        metadata = item["metadata"]

        source_key = (

            metadata.get("file_id"),
        )

        # =========================
        # 去重
        # =========================
        if source_key not in seen_sources:

            seen_sources.add(
                source_key
            )

            sources.append({

                "file_id":
                    metadata.get(
                        "file_id"
                    ),

                "file_name":
                    metadata.get(
                        "file_name"
                    ),

                "file_type":
                    metadata.get(
                        "file_type"
                    ),
            })

    # =========================
    # build context
    # =========================
    context = "\n\n".join(
        context_list
    )

    return {

        "context": context,

        "sources": sources
    }


# from app.rag.vectorstore.chroma_service import (
#     vector_store
# )

# # =========================
# # 向量检索
# # =========================
# # 查知识库，获取相关文本
# # k 是返回多少条相关文本
# # Chroma：会：
# # 1. query embedding
# # 2. 和所有 chunk 做相似度计算
# # 3. 排序
# # 4. 返回最相似的前 k 个
# def similarity_search(query: str, k: int = 3):

#     results = vector_store.similarity_search(
#         query=query,
#         k=k
#     )

#     return results


# # =========================
# # 构建 RAG 数据
# # =========================
# # 构建 RAG context
# def build_rag_context(query: str, k: int = 3):

#     """
#     构建 RAG context
#     """
#     results = similarity_search(query, k)
#     print("\n========== 检索结果 ==========\n")
#     context_list = []
#     sources = []
#     # 用于去重
#     seen_sources = set()
#     for item in results:
#         print(item.page_content)
#         print(item.metadata)
#         print("\n----------------\n")
#         # =========================
#         # context
#         # =========================
#         context_list.append(
#             item.page_content
#         )
#         # =========================
#         # sources
#         # =========================
#         metadata = item.metadata

#         source_key = (
#                 metadata.get("file_id"), 


#         )
#         # 去重
#         if source_key not in seen_sources:

#             seen_sources.add(source_key)

#             sources.append({
#                 "file_id":
#                     metadata.get("file_id"),

#                 "file_name":
#                     metadata.get("file_name"),

#                 "file_type": 
#                     metadata.get("file_type"),

#                 # "file_id": metadata.get("file_id"),
#                 # "uuid_name": metadata.get("uuid_name"),
#                 # "original_name": metadata.get("original_name"),
#                 # "file_type": metadata.get("file_type"),
#                 # "chunk_index": metadata.get("chunk_index"),
#                 # "char_count": metadata.get("char_count"),
#                 # "splitter": metadata.get("splitter"),
#                 # "extra": metadata.get("extra", {})
#             })
#     # 拼 prompt context
#     context = "\n\n".join(context_list)

#     return {
#         "context": context,
#         "sources": sources
#     }

# # if __name__ == "__main__":

# #     results = similarity_search(
# #         "Vue3 生命周期"
# #     )

# #     print("\n========== 检索结果 ==========\n")

# #     for item in results:

# #         print(item.page_content)

# #         print(item.metadata)

# #         print("\n----------------\n")