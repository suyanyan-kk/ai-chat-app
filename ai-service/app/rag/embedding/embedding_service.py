from langchain_huggingface import HuggingFaceEmbeddings


"""
embedding 模型服务

作用：
文本 -> embedding 向量

这里使用：
BAAI/bge-small-zh-v1.5

这是一个中文效果非常好的 embedding 模型
"""


# 创建 embedding 模型
embedding_model = HuggingFaceEmbeddings( 

    # embedding 模型名称
    model_name="BAAI/bge-small-zh-v1.5",

    # 模型初始化参数
    model_kwargs={

        # 使用 cpu
        # Mac M芯片如果支持 mps
        # 可以改成:
        # "device": "mps"

        "device": "cpu"
    },

    # encode 参数
    encode_kwargs={

        # 向量归一化
        # 对 cosine similarity 更友好
        "normalize_embeddings": True
    }
)


def embed_query(query: str):

    """
    用户问题 embedding

    参数:
        query: 用户问题

    返回:
        embedding 向量
    """

    return embedding_model.embed_query(query)


def embed_documents(texts: list[str]):

    """
    文档批量 embedding

    参数:
        texts: chunk 文本列表

    返回:
        embedding 向量列表
    """

    return embedding_model.embed_documents(texts)


if __name__ == "__main__":

    result = embed_query(
        "Vue3 生命周期"
    )

    print(result)