# PDF文本分割器
import fitz 
import re

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from app.utils.splitters.chunk_builder import build_chunk
from app.utils.splitters.types import ChunkData
 

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    # 这个值大会造成大量的重复（重复召回），所以后面要做rerank重排序 
    chunk_overlap=120,
    # 语意切分优先级：段落 > 行 > 标点，减少无意义切割
    # 针对PDF的特殊分割配置，优先在段落、行、标点等位置进行切割，减少无意义的切割
    separators=[ 
        "\n\n",   # 段落
        "\n",     # 行
        "。",     # 中文句号
        ".",      # 英文句号
        "！",
        "？",
        ";",
        "；",
        "，",
        ",",
        " ",      # 空格
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
        # 清洗文本
        text = clean_pdf_text(text)

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
                        "chunk_size": 700,
                        "chunk_overlap": 120,
                        # 字符数统计
                        "char_count": len(chunk),
                        # 当前章节标题（如果有的话，PDF通常没有明确章节标题，这里暂时用页码占位，后续可以结合OCR或其他方法提取章节标题）
                        # "section_title": current_title,

                        # 文件路径（可选）
                        "file_path": file_path,
                    }
                )
            )

            global_chunk_index += 1

    doc.close()

    return final_chunks

# 彻底优化 fitz 提取
# 清洗函数
def clean_pdf_text(text: str):
    # 去掉多余空行
    text = re.sub(r'\n{2,}', '\n\n', text)

    # 修复中文断行
    text = re.sub(r'(?<!\n)\n(?!\n)', '', text)

    # 去掉多余空格
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()