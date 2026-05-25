from app.utils.splitters.common.semantic_base import (
    SemanticBaseSplitter
)


class SemanticChildSplitter(
    SemanticBaseSplitter
):

    def __init__(self):

        super().__init__(

            # 小检索块
            window_size=2,

            percentile=25,

            min_chunk_size=150,

            max_chunk_size=500
        )