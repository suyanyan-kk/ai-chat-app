from sentence_transformers import (
    CrossEncoder
)

# =========================
# rerank model
# =========================
rerank_model = CrossEncoder(

    "BAAI/bge-reranker-v2-m3"
)


# =========================
# rerank
# =========================
def rerank_documents(
        query,
        documents,
        top_n=5
):

    """
    documents:

    [
        {
            "content": "...",
            "metadata": {...}
        }
    ]
    """

    if not documents:

        return []

    # =========================
    # build pairs
    # =========================
    """
    输入模型的 sentence_pairs 长这个样子的：
    [
        ["Vue3 生命周期", "Vue3 生命周期包括 mounted"],
        ["Vue3 生命周期", "Python 是解释型语言"],
    ]
    """
    sentence_pairs = [

        [query, doc["content"]]

        for doc in documents
    ]

    # =========================
    # predict 
    # 让 rerank 模型给每一对：[query, content]打相关性分数。
    # =========================
    """    
    score 越高，相关性越强
        scores = [
            0.98,
            0.02
        ]
    """
    scores = rerank_model.predict(
        sentence_pairs
    )

    # =========================
    # merge
    # =========================
    results = []

    for doc, score in zip(
            documents,
            scores
    ):

        doc["rerank_score"] = float(score)

        results.append(doc)

    # =========================
    # sort
    # =========================
    results.sort(

        key=lambda x: x["rerank_score"],

        reverse=True
    )

    # =========================
    # top n
    # =========================
    return results[:top_n]

