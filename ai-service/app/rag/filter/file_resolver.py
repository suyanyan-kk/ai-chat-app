from app.knowledgedb import models

def find_file_by_name(
        db,
        query
):

    files = db.query(
        models.KnowledgeFile
    ).all()

    query = query.lower()

    for file in files:

        filename = (
            file.original_name
            .split(".")[0]
            .lower()
        )

        if (

            filename in query

            or

            query in filename

        ):

            return file

    return None