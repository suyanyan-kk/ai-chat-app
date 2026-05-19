from langchain_chroma import Chroma

from app.rag.embedding.embedding_service import (
    embedding_model
)


"""
Chroma 向量数据库服务

作用：

chunk
↓
embedding
↓
vector storage
↓
similarity search
"""


# 创建 chroma 向量数据库
vector_store = Chroma(

    # chroma 数据库存储目录
    persist_directory="./chroma_db",

    # embedding 模型
    embedding_function=embedding_model 
)


def save_chunks_to_chroma(chunks): 

    """
    保存 chunk 到 chroma

    参数:
        chunks: chunk 数据列表
    """

    texts = []

    metadatas = []

    ids = []

    for chunk in chunks:

        # chunk 文本
        texts.append(
            chunk.content
        )

        # metadata
        metadatas.append({
            "file_id": chunk.file_id,
            "chunk_index": chunk.chunk_index,
            "chunk_id": chunk.id,
            "embedding_status": chunk.embedding_status
        })

        # 向量唯一 id/vector_id，后续更新向量状态和关联 chunk 时会用到
        ids.append(
            str(chunk.vector_id)
        )

    # 添加到 chroma
    vector_store.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids
    )

    print("保存到 Chroma 成功")
#    Chroma 实际存储长这样
# 你最终其实是：
# id: vector_id
#     "0b8e..."
# text:
#     "LangChain 是一个..."
# metadata:
# {
#     "file_id": 1,
#     "chunk_id": 22,
#     "chunk_index": 3
#     "embedding_status": "pending"
# } 
def show_all_vectors():

    result = vector_store.get(

        include=[
            "documents",
            "metadatas"
        ]
    )

    print("\n========== Chroma 数据 ==========\n")

    for i in range(len(result["ids"])):

        print(f"ID: {result['ids'][i]}")

        print(
            f"Document:\n{result['documents'][i]}"
        )

        print(
            f"Metadata:\n{result['metadatas'][i]}"
        )

        print("\n---------------------\n")


if __name__ == "__main__":

    show_all_vectors()
    #运行某个py的单独文件 要cd到-m后文件名的上一层 uv run python -m app.rag.vectorstore.chroma_service