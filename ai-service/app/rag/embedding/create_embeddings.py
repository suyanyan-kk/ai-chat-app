from app.rag.embedding.embedding_service import embedding_model


def create_embeddings(chunks):

    texts = []

    for chunk in chunks:

        texts.append(chunk.content)
    
    #批量 embedding
    embeddings = embedding_model.embed_documents(texts)

    return embeddings 
# 这个函数接受一个 chunk 列表，提取每个 chunk 的文本内容，使用 embedding_model 的 embed_documents 方法批量生成 embedding，并返回 embedding 列表。
#返回二维数组 就是每个 chunk 对应一个 embedding 向量，embedding 向量的维度取决于所使用的 embedding 模型。
# 即矩阵
# [
#     [0.123, ...],
#     [0.888, ...]
# ]