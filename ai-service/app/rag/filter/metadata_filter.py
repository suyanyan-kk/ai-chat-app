# from app.rag.filter.file_resolver import find_file_by_name
from app.rag.filter.query_entity import (
    extract_entity
)

from app.rag.filter.file_recall import (
    recall_file
)

def build_metadata_filter(
        db,
        query
):

    keyword = extract_entity(
        query
    )

    if not keyword:

        return None

    file = recall_file(
        db,
        keyword
    )

    if not file:

        return None
    print(f"Metadata filter hit: {file.original_name}")
    print(f"Metadata filter hit id: {file.id}")
    return {

        "file_id": file.id
    }