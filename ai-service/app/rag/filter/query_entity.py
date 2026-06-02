import re


STOP_WORDS = [

    "帮我",

    "总结",

    "讲了什么",

    "文档",

    "文件",

    "资料",

    "那个",

    "一下",

    "看看",

]


def extract_entity(query: str):

    text = query.lower()

    for word in STOP_WORDS:

        text = text.replace(
            word,
            ""
        )

    text = text.strip()

    return text