from app.utils.parsers.pdf_parser import parse_pdf
from app.utils.parsers.docx_parser import parse_docx
from app.utils.parsers.txt_parser import parse_text

def parse_by_file_type(file_path, ext):
    print(f"正在解析文件: {file_path}，文件类型: {ext}")
    ext = ext.lower()

    if ext == "pdf":
        return parse_pdf(file_path)

    elif ext == "docx":
        return parse_docx(file_path)

    elif ext in ["txt", "md"]:
        return parse_text(file_path)

    else:
        return "暂不支持该文件解析"