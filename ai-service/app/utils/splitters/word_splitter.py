from docx import Document

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from app.utils.splitters.chunk_builder import (
    build_chunk
)
 

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)


def split_word(
    file_id: int,
    original_name: str,
    uuid_name: str,
    file_path: str,
):

    doc = Document(file_path)

    final_chunks = []

    global_chunk_index = 0

    current_heading = "正文"

    for para in doc.paragraphs:

        text = para.text.strip()

        if not text:
            continue

        # Heading
        if para.style.name.startswith("Heading"):

            current_heading = text

            continue

        chunks = recursive_splitter.split_text(text)

        for paragraph_chunk_index, chunk in enumerate(chunks):

            final_chunks.append(

                build_chunk(

                    file_id=file_id,

                    original_name=original_name,

                    uuid_name=uuid_name,

                    content=chunk,

                    chunk_index=global_chunk_index,

                    splitter="word_recursive",

                    locator_type="heading",

                    locator_value=current_heading,

                    extra_metadata={

                        "paragraph_chunk_index":
                            paragraph_chunk_index
                    }
                )
            )

            global_chunk_index += 1

    return final_chunks