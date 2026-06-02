from sqlalchemy import or_

from app.knowledgedb import models


def recall_file(
        db,
        keyword
):

    return (

        db.query(
            models.KnowledgeFile
        )

        .filter(

            models.KnowledgeFile
            .original_name
            .ilike(
                f"%{keyword}%"
            )

        )

        .first()
    )