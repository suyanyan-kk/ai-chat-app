# 固定长度切片
def split_text(
    text,
    chunk_size=500,# 切片大小，单位字符
    chunk_overlap=100# 相邻 chunk 重叠多少字符
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks

# 更高级做法
# 后面你会升级成：

# LangChain
# RecursiveCharacterTextSplitter

# LlamaIndex
# SentenceSplitter

# 按语义切片
# semantic chunking
