from app.utils.splitters.base_splitter import split_text
from app.utils.splitters.code_splitter import split_code
from app.utils.splitters.markdown_splitter import split_markdown
from app.utils.splitters.pdf_splitter import split_pdf
# 根据文件类型自动选择切片器
def split_by_file_type(file_id: int, filename: str, file_path: str, content: str):

    ext = filename.split(".")[-1].lower()
    
    print(f"文件类型: {ext}")   
    # markdown
    if ext in ["md", "markdown"]:
        return split_markdown(file_id, filename, content)

    # code
    elif ext in ["py", "js", "ts", "vue", "java"]:
        return split_code(file_id,filename, content)

    # pdf
    elif ext in ["pdf"]:
        return split_pdf(file_id, filename,file_path)
    # 普通文本
    elif ext in ["txt"]:
        return split_text(file_id,filename, content)

    # 默认
    return split_text(file_id, filename, content)
