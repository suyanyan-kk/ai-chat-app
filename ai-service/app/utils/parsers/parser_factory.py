from app.utils.parsers.pdf_parser import PDFParser
from app.utils.parsers.markdown_parser import MarkdownParser
from app.utils.parsers.word_parser import WordParser
from app.utils.parsers.text_parser import TextParser


class ParserFactory:

    @staticmethod
    def get_parser(file_type):

        mapping = {

            "pdf": PDFParser(),

            "md": MarkdownParser(),

            "docx": WordParser(),

            "txt": TextParser(),

            "py": TextParser(),

            "js": TextParser(),
        }

        return mapping[file_type]





# from app.utils.parsers.pdf_parser import parse_pdf
# from app.utils.parsers.docx_parser import parse_docx
# from app.utils.parsers.txt_parser import parse_text

# def parse_by_file_type(file_path, ext):
#     print(f"正在解析文件: {file_path}，文件类型: {ext}")
#     ext = ext.lower()

#     if ext == "pdf": 
#         return parse_pdf(file_path)

#     elif ext == "docx":
#         return parse_docx(file_path)

#     elif ext in ["txt", "md"]:
#         return parse_text(file_path)

#     else:
#         return "暂不支持该文件解析"
    

#   ["md", "markdown"]
#   ["py", "js", "ts", "vue", "java"]:
#   ["doc", "docx"]
#   ["pdf"]
#   ["txt"]
