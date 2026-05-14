from typing import TypedDict, Dict, Any


class ChunkData(TypedDict):
    file_id: int
    filename: str
    content: str
    meta_info: Dict[str, Any]

class ChunkDataPDF(TypedDict):
    file_id: int
    filename: str
    file_path: str
    meta_info: Dict[str, Any]
