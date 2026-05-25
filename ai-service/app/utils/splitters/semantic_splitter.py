
from app.utils.splitters.common.semantic_base import (
    SemanticBaseSplitter
)


class SemanticSplitter(
    SemanticBaseSplitter
):

    def __init__(self):

        super().__init__(

            # 大结构
            window_size=5,#每次看前后5句 

            percentile=15,#最低15%的 similarity 认为可能是语义断层

            min_chunk_size=800,#避免：chunk 太小

            max_chunk_size=3000#避免：chunk 太大
        )

