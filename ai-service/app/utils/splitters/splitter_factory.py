from app.utils.splitters.base_splitter import split_text
from app.utils.splitters.code_splitter import split_code
from app.utils.splitters.markdown_splitter import split_markdown

# 根据文件类型自动选择切片器
def split_by_file_type(filename: str, content: str):

    ext = filename.split(".")[-1].lower()
    
    print(f"文件类型: {ext}")   
    # markdown
    if ext in ["md", "markdown"]:
        return split_markdown(content)

    # code
    elif ext in ["py", "js", "ts", "vue", "java"]:
        return split_code(content, ext)

    # 普通文本
    elif ext in ["txt"]:
        return split_text(content)

    # 默认
    return split_text(content)
