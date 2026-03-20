from ..chains import simple_chain

def ask_llm(message: str):
    return simple_chain.invoke({
        "input": message
    })