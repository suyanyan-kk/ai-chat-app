from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_db"

client = PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="knowledge"
)

embedding_model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5"
)

# 获取文件所有chunk
def get_chunks_by_file(file_id: str):

    result = collection.get(
        where={
            "file_id": file_id
        },
        include=[
            "documents",
            "metadatas"
        ]
    )

    ids = result.get("ids", [])
    documents = result.get("documents", [])
    metadatas = result.get("metadatas", [])

    data = []

    for i in range(len(ids)):

        metadata = metadatas[i] or {}

        data.append({
            "id": ids[i],
            "content": documents[i],
            "length": len(documents[i]),
            "chunk_index": metadata.get("chunk_index"),
            "file_name": metadata.get("file_name"),
            "source": metadata.get("source"),
            "metadata": metadata
        })

    return data


# 测试向量召回
def search_chunks(
    query: str,
    top_k: int = 5
):

    embedding = embedding_model.encode(
        query
    ).tolist()

    result = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]
    ids = result["ids"][0]

    data = []

    for i in range(len(ids)):

        score = 1 - distances[i]

        data.append({
            "id": ids[i],
            "content": documents[i],
            "score": round(score, 4),
            "metadata": metadatas[i]
        })

    return data