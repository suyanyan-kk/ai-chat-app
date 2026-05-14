from typing import TypedDict, Dict, Any


class ChunkData(TypedDict):
    content: str
    meta_info: Dict[str, Any]