from app.rag.vectorstore.chroma_service import (
    vector_store
)

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

# 构建 RAG context
def build_context(query: str, k: int = 3):

    """
    构建 RAG context
    """
    results = similarity_search(query, k)
    print("\n========== 检索结果 ==========\n")
    context_list = []

    for item in results:
        print(item.page_content)
        print(item.metadata)
        print("\n----------------\n")
        context_list.append(
            item.page_content
        )
    # 拼 prompt
    context = "\n\n".join(context_list)

    return context

# if __name__ == "__main__":

#     results = similarity_search(
#         "Vue3 生命周期"
#     )

#     print("\n========== 检索结果 ==========\n")

#     for item in results:

#         print(item.page_content)

#         print(item.metadata)

#         print("\n----------------\n")