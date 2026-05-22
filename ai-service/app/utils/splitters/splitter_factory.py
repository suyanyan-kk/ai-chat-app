from app.utils.splitters.base_splitter import split_text
from app.utils.splitters.code_splitter import split_code
from app.utils.splitters.markdown_splitter import split_markdown
from app.utils.splitters.pdf_splitter import split_pdf
from app.utils.splitters.word_splitter import split_word

 
# 根据文件类型自动选择切片器
def split_by_file_type(
    file_id: int, original_name: str, uuid_name: str, file_path: str, content: str
):
    
    ext = uuid_name.split(".")[-1].lower()

    print(f"文件类型: {ext}")
    # markdown
    if ext in ["md", "markdown"]:
        return split_markdown(file_id, original_name, uuid_name, content)

    # code
    elif ext in ["py", "js", "ts", "vue", "java"]:
        return split_code(file_id, original_name, uuid_name, content)
    # word
    elif ext in ["doc", "docx"]:

        return split_word(file_id, original_name, uuid_name, file_path)
    # pdf
    elif ext in ["pdf"]:
        return split_pdf(file_id, original_name, uuid_name, file_path)
    # 普通文本
    elif ext in ["txt"]:
        return split_text(file_id, original_name, uuid_name, content)

    # 默认
    return split_text(file_id, original_name, uuid_name, content)
