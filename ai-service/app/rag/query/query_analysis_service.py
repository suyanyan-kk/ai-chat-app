from dataclasses import dataclass

from app.rag.config import (
    ENABLE_LLM_REWRITE,
    ENABLE_LLM_MULTI_QUERY
)

from app.rag.filter.metadata_filter import (
    build_metadata_filter
)

from app.rag.rewrite.rewrite_service import (
    rewrite_query
)

from app.rag.rewrite.multi_query_service import (
    generate_multi_queries
)

from app.rag.rewrite.llm_rewrite_service import (
    rewrite_query_llm
)

from app.rag.rewrite.llm_multi_query_service import (
    generate_multi_queries_llm
)


@dataclass
class QueryAnalysis:

    original_query: str

    rewritten_query: str

    multi_queries: list

    metadata_filter: dict | None


def analyze_query(
        db,
        query
):

    original_query = query

    metadata_filter = (
        build_metadata_filter(
            db,
            original_query
        )
    )

    # =====================
    # rewrite
    # =====================

    if ENABLE_LLM_REWRITE:

        rewritten_query = (
            rewrite_query_llm(
                original_query
            )
        )
        print(
            "LLM Rewrite Result:",
            rewritten_query
        )
    else:

        rewritten_query = (
            rewrite_query(
                original_query
            )
        )

    # =====================
    # multi query
    # =====================

    if ENABLE_LLM_MULTI_QUERY:

        multi_queries = (
            generate_multi_queries_llm(
                rewritten_query
            )
        )
        print(
            "LLM Multi-Query Result:",
            multi_queries
        )
    else:

        multi_queries = (
            generate_multi_queries(
                rewritten_query
            )
        )

    return QueryAnalysis(

        original_query=
            original_query,

        rewritten_query=
            rewritten_query,

        multi_queries=
            multi_queries,

        metadata_filter=
            metadata_filter
    )