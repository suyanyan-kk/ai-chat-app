from app.utils.splitters.common.semantic_base import (
    SemanticBaseSplitter
)


class SemanticParentSplitter(
    SemanticBaseSplitter
):

    def __init__(self):

        super().__init__(

            # 中语义块
            window_size=3,

            percentile=20,

            min_chunk_size=400,

            max_chunk_size=1200
        )