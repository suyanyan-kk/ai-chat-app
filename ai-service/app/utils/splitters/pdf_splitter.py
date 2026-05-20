import fitz

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from app.utils.splitters.chunk_builder import build_chunk
from app.utils.splitters.types import ChunkData


recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=[
        "\n\n",
        "\n",
        "。",
        "！",
        "？",
        ".",
        " "
    ]
)


def split_pdf(
    file_id: int,
    original_name: str,
    uuid_name: str,
    file_path: str,
) -> list[ChunkData]:

    doc = fitz.open(file_path)

    final_chunks = []

    global_chunk_index = 0

    for page_number in range(len(doc)):

        page = doc[page_number]

        text = page.get_text()

        # 空页跳过
        if not text.strip():
            continue

        chunks = recursive_splitter.split_text(text)

        for page_chunk_index, chunk in enumerate(chunks):

            final_chunks.append(
                build_chunk(
                    file_id=file_id,
                    original_name=original_name,
                    uuid_name=uuid_name,
                    content=chunk,
                    chunk_index=global_chunk_index,
                    splitter="pdf_recursive",
                    locator_type="page",
                    locator_value=page_number + 1,
                    extra={ 
                        "file_type": "pdf",
                        # PDF页码
                        "page": page_number + 1,
                        # 当前页内 chunk index
                        "page_chunk_index": page_chunk_index,
                        # section
                        "section": f"page_{page_number + 1}",
                        # splitter配置
                        "chunk_size": 300,
                        "chunk_overlap": 50,
                        # 文件路径（可选）
                        "file_path": file_path,
                    }
                )
            )

            global_chunk_index += 1

    doc.close()

    return final_chunks