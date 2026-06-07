from langchain.tools import tool

from sympy import sympify


@tool
def calculator(
    expression: str
) -> str:
    """
    数学计算工具
    """

    try:

        result = sympify(
            expression
        )

        return str(result)

    except Exception as e:

        return f"计算失败: {str(e)}"