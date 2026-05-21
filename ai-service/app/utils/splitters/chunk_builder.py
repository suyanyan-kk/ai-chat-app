from app.utils.splitters.types import ChunkData


def build_chunk(
    *,
    file_id: int,
    original_name: str,
    uuid_name: str,
    content: str,
    chunk_index: int,
    splitter: str,
    locator_type: str | None = None,
    locator_value: str | int | None = None,
    extra: dict | None = None
)-> ChunkData:

    metadata = {

        # =========================
        # source
        # =========================
        "file_id": file_id,
        "file_name": original_name,
        "file_type":uuid_name.split(".")[-1].lower(),
        "file_uuid_name": uuid_name,
        # =========================
        # chunk
        # =========================
        "chunk_index": chunk_index,
        # =========================
        # splitter
        # =========================
        "splitter": splitter,
        # =========================
        # locator
        # =========================
        "locator_type": locator_type,
        "locator_value": locator_value,
        # =========================
        # display
        # =========================
        "char_count": len(content),
    }

    # ⭐ extra 扁平展开
    if extra:
        metadata.update(extra)

    return ChunkData(
        content=content,
        metadata=metadata
    )