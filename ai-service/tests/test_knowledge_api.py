import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.knowledge import get_db, router
from app.auth.dependencies import get_current_user
from app.auth.models import AuthUser
from app.auth.service import (
    create_user,
    ensure_default_roles_and_permissions,
)
from app.knowledgedb import models
from app.knowledgedb.db import Base


class KnowledgeApiTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.TestSession = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        Base.metadata.create_all(bind=self.engine)

        db = self.TestSession()
        try:
            ensure_default_roles_and_permissions(db)
            self.user_a = create_user(
                db,
                email="owner-a@example.com",
                password="Correct-Horse-42",
                display_name="Owner A",
                is_superuser=True,
            )
            self.user_b = create_user(
                db,
                email="owner-b@example.com",
                password="Correct-Horse-42",
                display_name="Owner B",
                is_superuser=True,
            )
            self.user_a_id = self.user_a.id
            self.user_b_id = self.user_b.id
        finally:
            db.close()

        self.current_user_id = self.user_a_id
        app = FastAPI()

        def override_db():
            db = self.TestSession()
            try:
                yield db
            finally:
                db.close()

        def override_current_user():
            db = self.TestSession()
            try:
                return db.get(AuthUser, self.current_user_id)
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_db
        app.dependency_overrides[get_current_user] = (
            override_current_user
        )
        app.include_router(router)
        self.client = TestClient(app)

    def tearDown(self):
        self.engine.dispose()

    def add_folder(self, title):
        return self.client.post(
            "/addKnowledge",
            json={"title": title, "type": "folder"},
        )

    def test_queries_only_return_current_users_records(self):
        own_response = self.add_folder("owner-a-folder")
        self.assertEqual(own_response.status_code, 201)
        own_id = own_response.json()["data"]["id"]

        self.current_user_id = self.user_b_id
        other_response = self.add_folder("owner-b-folder")
        self.assertEqual(other_response.status_code, 201)
        other_id = other_response.json()["data"]["id"]

        self.current_user_id = self.user_a_id
        listed = self.client.get("/getKnowledge")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(
            [item["id"] for item in listed.json()],
            [own_id],
        )

        hidden_detail = self.client.get(
            f"/getKnowledgeDetail/{other_id}"
        )
        self.assertEqual(hidden_detail.json()["code"], 1)

        hidden_chunks = self.client.get("/chunks/999")
        self.assertEqual(hidden_chunks.json()["data"], [])

    def test_writes_cannot_target_another_users_records(self):
        self.current_user_id = self.user_b_id
        other = self.add_folder("owner-b-folder").json()["data"]

        db = self.TestSession()
        try:
            other_file = models.KnowledgeFile(
                user_id=self.user_b_id,
                original_name="private.md",
                uuid_name="private.md",
                file_url="/tmp/private.md",
                file_size=1,
                file_type="md",
                content="private",
            )
            db.add(other_file)
            db.commit()
            other_file_id = other_file.id
        finally:
            db.close()

        self.current_user_id = self.user_a_id
        update = self.client.put(
            f"/updateKnowledge/{other['id']}",
            json={"title": "changed", "type": "folder"},
        )
        self.assertEqual(update.status_code, 404)

        delete = self.client.delete(
            f"/deleteKnowledge/{other['id']}"
        )
        self.assertEqual(delete.json()["code"], 1)

        foreign_parent = self.client.post(
            "/addKnowledge",
            json={
                "title": "child",
                "type": "folder",
                "parent_id": other["id"],
            },
        )
        self.assertEqual(foreign_parent.status_code, 400)

        foreign_file = self.client.post(
            "/addKnowledge",
            json={
                "title": "private.md",
                "type": "file",
                "file_id": other_file_id,
            },
        )
        self.assertEqual(foreign_file.status_code, 400)

    def test_created_node_is_bound_to_current_user(self):
        response = self.add_folder("owned")
        self.assertEqual(response.status_code, 201)

        db = self.TestSession()
        try:
            item = db.get(
                models.Knowledge,
                response.json()["data"]["id"],
            )
            self.assertEqual(item.user_id, self.user_a_id)
        finally:
            db.close()


if __name__ == "__main__":
    unittest.main()
