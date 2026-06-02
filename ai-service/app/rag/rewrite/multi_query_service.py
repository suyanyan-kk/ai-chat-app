# V1 规则版
def generate_multi_queries(
        query: str
):

    queries = [query]

    query_lower = query.lower()

    # Vue
    if "vue" in query_lower:

        queries.extend([

            query.replace(
                "vue",
                "vue3"
            ),

            query + " 生命周期",

            query + " 组件通信",

            query + " Composition API",

        ])

    # React
    elif "react" in query_lower:

        queries.extend([

            query + " hooks",

            query + " useState",

            query + " useEffect",

        ])

    # Python
    elif "python" in query_lower:

        queries.extend([

            query + " 面向对象",

            query + " 继承",

            query + " 多态",

        ])

    # JavaScript
    elif (
        "javascript" in query_lower
        or
        "js" in query_lower
    ):

        queries.extend([

            query + " 循环",

            query + " for",

            query + " while",

            query + " Promise",

        ])
 
    return list(
        dict.fromkeys(queries)
    )