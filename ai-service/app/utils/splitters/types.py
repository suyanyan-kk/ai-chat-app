from dataclasses import dataclass, field
from typing import Any


@dataclass
class ChunkData:

    # chunk文本
    content: str

    # metadata
    metadata: dict[str, Any] = field(default_factory=dict)