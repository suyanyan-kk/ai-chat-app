import fitz


class PDFParser:

    def parse(self, file_path):

        doc = fitz.open(file_path)

        pages = []

        for page_number in range(len(doc)):

            page = doc[page_number]

            text = page.get_text()

            pages.append({

                "page": page_number + 1,

                "text": text
            })

        return pages






# import fitz

# def parse_pdf(file_path):

#     text = ""

#     doc = fitz.open(file_path)

#     for page in doc:
#         text += page.get_text()

#     doc.close()

#     return text