def parse_text(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()