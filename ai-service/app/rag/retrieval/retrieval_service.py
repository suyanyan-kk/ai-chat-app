from collections import OrderedDict

from app.rag.hybrid.hybrid_service import (
    hybrid_retrieval_service 
)
from app.rag.rerank.rerank_service import (
    rerank_documents
)

from app.knowledgedb.db import ( 
    SessionLocal
)
from app.rag.query.query_analysis_service import (
    analyze_query
)
from app.knowledgedb import models
# =========================
# parent retrieval
# =========================
def get_parent_chunk(parent_id):

    db = SessionLocal()

    chunks = db.query(
        models.KnowledgeChunk
    ).all()

    for chunk in chunks:

        meta = chunk.meta_info or {}

        if (

            meta.get("chunk_type") == "parent"

            and

            meta.get("parent_id") == parent_id

        ):

            db.close()

            return chunk

    db.close()

    return None


# =========================
# retrieval build_rag_context
# =========================
def retrieval_pipeline( 

        query: str,

        recall_k: int = 20,

        rerank_top_k: int = 5
):
    # 分析查询
    db = SessionLocal()

    analysis = analyze_query(
        db,
        query
    )

    db.close()
    print("\n========== Query Analysis ==========\n")   
    print(f"Original Query: {analysis.original_query}")
    print(f"Rewritten Query: {analysis.rewritten_query}")
    print(f"Multi Queries: {analysis.multi_queries}")
    print(f"Metadata Filter: {analysis.metadata_filter}") 
    # =========================
    # 1 hybrid retrieval
    # ========================= 
    all_results = []
    # 多次检索，结果合并
    for q in analysis.multi_queries:
        results = (
            hybrid_retrieval_service.search( 

            query=q,

            top_k=recall_k,

            metadata_filter=analysis.metadata_filter
            )
        )
        all_results.extend(
        results
    )
    print("\n========== hybrid_results ==========\n")
   
    print(all_results)
    
    print(
        "\n========== Hybrid Recall ==========\n"
    )

    
    # 去重 因为同一个 Chunk 会被召回很多次。
    unique_results = {}
    for item in all_results:

        metadata = item["metadata"]

        doc_id = (

            metadata.get("file_id"),

            metadata.get("parent_id"),
        )

        if doc_id not in unique_results:

            unique_results[doc_id] = item

    hybrid_results = list(
        unique_results.values()
    )
    print("\n========== Unique Hybrid Results ==========\n")
    print(hybrid_results)
    # =========================
    # 2 rerank
    # =========================
    rerank_results = rerank_documents(

        query=query,

        documents=hybrid_results,

        top_n=rerank_top_k
    )

    print(
        "\n========== Rerank ==========\n"
    )

    # for item in rerank_results:

    #     print(
    #         item["content"][:100]
    #     )

    #     print(
    #         "rerank_score:",
    #         item.get("rerank_score")
    #     )

    #     print("\n----------------\n")

    # =========================
    # 3 parent retrieval
    # =========================
    final_results = []
    seen_parent_ids = set()
    for item in rerank_results:

        metadata = item["metadata"]

        chunk_type = metadata.get(
            "chunk_type"
        )

        # child -> parent
        if chunk_type == "child":

            parent_id = metadata.get(
                "parent_id"
            )

            parent_chunk = get_parent_chunk(
                parent_id
            )

            if parent_id in seen_parent_ids:
                continue 

            seen_parent_ids.add(
                parent_id
            )
            parent_chunk = get_parent_chunk(
                parent_id
            )
            if parent_chunk:
                final_results.append({

                    "content":
                        parent_chunk.content,

                    "metadata":
                        parent_chunk.meta_info,

                    "rerank_score":
                        item["rerank_score"]
                })

            else:

                parent_id = metadata.get(
                    "parent_id"
                )

                if parent_id in seen_parent_ids:

                    continue

                seen_parent_ids.add(
                    parent_id
                )

                final_results.append(
                    item
                )


    # =========================
    # 4 deduplicate
    # =========================
    dedup_results = list(

        OrderedDict(

            (
                item["content"],
                item
            )

            for item in final_results

        ).values()
    )

    # =========================
    # 5 build context
    # =========================
    context_list = []

    sources = []

    seen_sources = set()

    for item in dedup_results:

        metadata = item["metadata"]

        context_list.append(

            item["content"]
        )

        source_key = (

            metadata.get("file_id"),
        )

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

                "page":
                    metadata.get(
                        "page"
                    ),
            })

    # =========================
    # final context
    # =========================
    context = "\n\n".join(
        context_list
    )

    return {

        "context": context,

        "sources": sources,

        "chunks": dedup_results
    }







# 版本二 
# from app.rag.vectorstore.chroma_service import (
#     vector_store
# )

# from app.rag.rerank.rerank_service import (
#     rerank_documents
# )

# # =========================
# # 向量检索
# # =========================
# def similarity_search(
#         query: str,
#         k: int = 20
# ):

#     """
#     Chroma 向量召回
#     """
#     # LangChain
#     results = vector_store.similarity_search(

#         query=query,

#         k=k
#     )
#     print("\n========== 向量粗召回==========\n")
#     for item in results:
#         print("\n========== 向量粗召回检索结果 ==========\n")
#         print(item)
#     return results


# # =========================
# # rerank retrieval
# # =========================
# def rerank_search(
#         query: str,
#         recall_k: int = 20,
#         rerank_top_k: int = 5
# ):

#     """
#     先 embedding recall
#     再 rerank
#     """

#     # =========================
#     # 1 recall
#     # =========================
#     results = similarity_search(

#         query=query,

#         k=recall_k
#     )

#     # =========================
#     # 2 format docs
#     # =========================
#     candidates = []

#     for item in results:

#         candidates.append({

#             "content": item.page_content,

#             "metadata": item.metadata
#         })

#     # =========================
#     # 3 rerank
#     # =========================
#     rerank_results = rerank_documents(

#         query=query,

#         documents=candidates,

#         top_n=rerank_top_k
#     )

#     return rerank_results


# # =========================
# # 构建 RAG context
# # =========================
# def build_rag_context(

#         query: str,

#         recall_k: int = 20,

#         rerank_top_k: int = 5
# ):

#     """
#     构建最终 RAG context
#     """

#     # =========================
#     # rerank retrieval
#     # =========================
#     results = rerank_search(

#         query=query,

#         recall_k=recall_k,

#         rerank_top_k=rerank_top_k
#     )

#     print("\n========== RERANK 检索结果 ==========\n")

#     context_list = []

#     sources = []

#     # 去重
#     seen_sources = set()

#     for item in results:

#         print(
#             "rerank_score:",
#             item.get("rerank_score")
#         )

#         print(
#             item["content"]
#         )

#         print(
#             item["metadata"]
#         )

#         print("\n----------------\n")

#         # =========================
#         # context
#         # =========================
#         context_list.append(

#             item["content"]
#         )

#         # =========================
#         # metadata
#         # =========================
#         metadata = item["metadata"]

#         source_key = (

#             metadata.get("file_id"),
#         )

#         # =========================
#         # 去重
#         # =========================
#         if source_key not in seen_sources:

#             seen_sources.add(
#                 source_key
#             )

#             sources.append({

#                 "file_id":
#                     metadata.get(
#                         "file_id"
#                     ),

#                 "file_name":
#                     metadata.get(
#                         "file_name"
#                     ),

#                 "file_type":
#                     metadata.get(
#                         "file_type"
#                     ),
#             })

#     # =========================
#     # build context
#     # =========================
#     context = "\n\n".join(
#         context_list
#     )

#     return {

#         "context": context,

#         "sources": sources
#     }

# 版本一
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