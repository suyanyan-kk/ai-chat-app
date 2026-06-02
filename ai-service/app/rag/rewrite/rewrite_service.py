REWRITE_MAP = {

    "js": "javascript",

    "py": "python",

    "vue": "vue3",

    "reactjs": "react",

}

def rewrite_query( 
        query: str
):

    query = query.lower()

    for old, new in REWRITE_MAP.items():

        query = query.replace(
            old,
            new
        )
    print(f"Rewritten query: {query}")
    return query