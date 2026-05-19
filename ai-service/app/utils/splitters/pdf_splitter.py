import fitz

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from app.utils.splitters.types import ChunkDataPDF


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

def split_pdf(file_id: int,filename: str,file_path: str,) -> list[ChunkDataPDF]:

    doc = fitz.open(file_path)
    final_chunks = []
    for page_number in range(len(doc)):

        page = doc[page_number]

        text = page.get_text()

        if not text.strip():
            continue

        chunks = recursive_splitter.split_text(text)

        for chunk_index, chunk in enumerate(chunks):

            final_chunks.append({
                "file_id": file_id,
                "filename": filename,
                "file_path": file_path,
                "content": chunk,
                "meta_info": {
                    "source": filename,
                    "file_type": "pdf",
                    "page": page_number + 1,
                    "section": f"page_{page_number + 1}",
                    "chunk_index": chunk_index,
                    "splitter": "pdf_recursive"
                }
            })

    doc.close()

    return final_chunks