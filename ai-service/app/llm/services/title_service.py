from ..chains import title_chain

def generate_title(message: str):
    return title_chain.invoke({
        "input": message
    })