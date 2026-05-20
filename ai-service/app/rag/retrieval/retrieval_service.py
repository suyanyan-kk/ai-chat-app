from app.rag.vectorstore.chroma_service import (
    vector_store
)

# =========================
# 向量检索
# =========================
# 查知识库，获取相关文本
# k 是返回多少条相关文本
# Chroma：会：
# 1. query embedding
# 2. 和所有 chunk 做相似度计算
# 3. 排序
# 4. 返回最相似的前 k 个
def similarity_search(query: str, k: int = 3):

    results = vector_store.similarity_search(
        query=query,
        k=k
    )

    return results


# =========================
# 构建 RAG 数据
# =========================
# 构建 RAG context
def build_rag_context(query: str, k: int = 3):

    """
    构建 RAG context
    """
    results = similarity_search(query, k)
    print("\n========== 检索结果 ==========\n")
    context_list = []
    sources = []
    # 用于去重
    seen_sources = set()
    for item in results:
        print(item.page_content)
        print(item.metadata)
        print("\n----------------\n")
        # =========================
        # context
        # =========================
        context_list.append(
            item.page_content
        )
        # =========================
        # sources
        # =========================
        metadata = item.metadata

        source_key = (
                metadata.get("source_id"),

                metadata.get("locator_type"),

                metadata.get("locator_value"),
        )
        # 去重
        if source_key not in seen_sources:

            seen_sources.add(source_key)

            sources.append({
                "source_id":
                    metadata.get("source_id"),

                "source_name":
                    metadata.get("source_name"),

                "source_type":
                    metadata.get("source_type"),

                "locator_type":
                    metadata.get("locator_type"),

                "locator_value":
                    metadata.get("locator_value"),

                # "file_id": metadata.get("file_id"),
                # "uuid_name": metadata.get("uuid_name"),
                # "original_name": metadata.get("original_name"),
                # "file_type": metadata.get("file_type"),
                # "chunk_index": metadata.get("chunk_index"),
                # "char_count": metadata.get("char_count"),
                # "splitter": metadata.get("splitter"),
                # "extra": metadata.get("extra", {})
            })
    # 拼 prompt context
    context = "\n\n".join(context_list)

    return {
        "context": context,
        "sources": sources
    }

# if __name__ == "__main__":

#     results = similarity_search(
#         "Vue3 生命周期"
#     )

#     print("\n========== 检索结果 ==========\n")

#     for item in results:

#         print(item.page_content)

#         print(item.metadata)

#         print("\n----------------\n")