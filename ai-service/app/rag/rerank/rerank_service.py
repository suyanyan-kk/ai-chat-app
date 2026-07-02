import os

from functools import lru_cache
from langsmith import traceable


def is_rerank_enabled() -> bool:
    return os.getenv(
        "ENABLE_RERANK",
        "false"
    ).lower() in (
        "1",
        "true",
        "yes",
        "on"
    )


def get_doc_content(
    document
):
    if isinstance(
        document,
        dict
    ):
        return document.get(
            "content",
            ""
        )

    return getattr(
        document,
        "page_content",
        str(document)
    )


def fallback_rerank(
    documents: list,
    top_n: int = 5
):
    """
    rerank 关闭或模型加载失败时的降级逻辑。

    保证后续节点仍然可以读取 rerank_score，
    避免 KeyError('rerank_score')。
    """

    results = []

    for index, document in enumerate(
        documents[:top_n]
    ):
        if not isinstance(
            document,
            dict
        ):
            results.append(
                document
            )
            continue

        item = document.copy()

        fallback_score = (
            item.get("rerank_score")
            or item.get("rrf_score")
            or item.get("score")
            or item.get("vector_score")
            or item.get("bm25_score")
            or 0
        )

        item["rerank_score"] = float(
            fallback_score
        )

        item["rerank_disabled"] = True

        item["rerank_rank"] = index + 1

        results.append(
            item
        )

    return results


@lru_cache(maxsize=1)
def get_rerank_model():
    """
    延迟加载 rerank 模型。

    只有 ENABLE_RERANK=true 且真正执行 rerank 时，
    才会加载 CrossEncoder。
    """

    from sentence_transformers import CrossEncoder

    return CrossEncoder(
        "BAAI/bge-reranker-v2-m3"
    )


@traceable(name="rerank_documents")
def rerank_documents(
    query: str,
    documents: list,
    top_n: int = 5
):
    """
    Rerank 服务。

    - ENABLE_RERANK=false：直接降级返回 RRF 结果
    - ENABLE_RERANK=true：尝试加载 CrossEncoder
    - 模型加载失败：自动降级，不让后端崩溃
    """

    documents = documents or []

    if not documents:
        return []

    if not is_rerank_enabled():
        print("===== rerank disabled in rerank_service, fallback =====")

        return fallback_rerank(
            documents,
            top_n=top_n
        )

    try:
        model = get_rerank_model()

        pairs = []

        for document in documents:
            pairs.append([
                query,
                get_doc_content(
                    document
                )
            ])

        scores = model.predict(
            pairs
        )

        reranked = sorted(
            zip(
                documents,
                scores
            ),
            key=lambda item: float(
                item[1]
            ),
            reverse=True
        )

        results = []

        for index, (document, score) in enumerate(
            reranked[:top_n]
        ):
            if isinstance(
                document,
                dict
            ):
                item = document.copy()

                item["rerank_score"] = float(
                    score
                )

                item["rerank_disabled"] = False

                item["rerank_rank"] = index + 1

                results.append(
                    item
                )

            else:
                results.append(
                    document
                )

        return results

    except Exception as e:
        print("===== rerank failed, fallback to fusion results =====")
        print(e)

        return fallback_rerank(
            documents,
            top_n=top_n
        )
