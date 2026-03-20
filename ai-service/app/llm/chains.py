# 所有Chain
from langchain_core.output_parsers import StrOutputParser
from .model import model
from .prompts import chat_prompt, title_prompt, simple_prompt

parser = StrOutputParser()

chat_chain = chat_prompt | model | parser
title_chain = title_prompt | model | parser
simple_chain = simple_prompt | model | parser