import unittest

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.dependencies import (
    get_auth_db,
    get_current_user,
)
from app.auth.models import AuthUser
from app.auth.router import router
from app.auth.service import (
    create_user,
    ensure_default_roles_and_permissions,
)
from app.knowledgedb.db import Base


class AuthApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite://",
            connect_args={
                "check_same_thread": False
            },
            poolclass=StaticPool,
        )
        cls.TestSession = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=cls.engine,
        )
        Base.metadata.create_all(
            bind=cls.engine
        )

        db = cls.TestSession()

        try:
            ensure_default_roles_and_permissions(
                db
            )
            create_user(
                db,
                email="admin@example.com",
                password="Correct-Horse-42",
                display_name="Test Admin",
                role_code="admin",
                is_superuser=True,
            )
        finally:
            db.close()

        app = FastAPI()

        def override_auth_db():
            test_db = cls.TestSession()

            try:
                yield test_db
            finally:
                test_db.close()

        app.dependency_overrides[
            get_auth_db
        ] = override_auth_db
        app.include_router(router)

        @app.get("/protected")
        def protected(
            user: AuthUser = Depends(
                get_current_user
            ),
        ):
            return {
                "user_id": user.id
            }

        cls.client = TestClient(app)

    def test_login_refresh_logout_flow(self):
        login_response = self.client.post(
            "/auth/login",
            json={
                "email": "admin@example.com",
                "password": "Correct-Horse-42",
            },
        )

        self.assertEqual(
            login_response.status_code,
            200,
        )
        self.assertEqual(
            login_response.headers[
                "cache-control"
            ],
            "no-store",
        )
        login_data = login_response.json()
        old_access_token = login_data[
            "access_token"
        ]

        self.assertIn(
            "admin",
            login_data["user"]["roles"],
        )
        self.assertIn(
            "mcp.manage",
            login_data["user"][
                "permissions"
            ],
        )
        self.assertIn(
            "ai_refresh_token",
            self.client.cookies,
        )

        me_response = self.client.get(
            "/auth/me",
            headers={
                "Authorization": (
                    f"Bearer {old_access_token}"
                )
            },
        )

        self.assertEqual(
            me_response.status_code,
            200,
        )

        protected_response = self.client.get(
            "/protected",
            headers={
                "Authorization": (
                    f"Bearer {old_access_token}"
                )
            },
        )
        self.assertEqual(
            protected_response.status_code,
            200,
        )

        refresh_response = self.client.post(
            "/auth/refresh"
        )

        self.assertEqual(
            refresh_response.status_code,
            200,
        )
        new_access_token = refresh_response.json()[
            "access_token"
        ]
        self.assertNotEqual(
            old_access_token,
            new_access_token,
        )

        old_token_response = self.client.get(
            "/auth/me",
            headers={
                "Authorization": (
                    f"Bearer {old_access_token}"
                )
            },
        )
        self.assertEqual(
            old_token_response.status_code,
            401,
        )

        new_token_response = self.client.get(
            "/auth/me",
            headers={
                "Authorization": (
                    f"Bearer {new_access_token}"
                )
            },
        )
        self.assertEqual(
            new_token_response.status_code,
            200,
        )

        logout_response = self.client.post(
            "/auth/logout"
        )
        self.assertEqual(
            logout_response.status_code,
            200,
        )

        refresh_after_logout = self.client.post(
            "/auth/refresh"
        )
        self.assertEqual(
            refresh_after_logout.status_code,
            401,
        )

    def test_wrong_password_does_not_leak_user_state(self):
        response = self.client.post(
            "/auth/login",
            json={
                "email": "admin@example.com",
                "password": "Wrong-Password-42",
            },
        )

        self.assertEqual(
            response.status_code,
            401,
        )
        self.assertEqual(
            response.json()["detail"],
            "邮箱或密码错误",
        )

    def test_register_creates_member_and_session(self):
        response = self.client.post(
            "/auth/register",
            json={
                "email": "learner@example.com",
                "password": "Learning-Password-42",
                "display_name": "New Learner",
            },
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(
            data["user"]["email"],
            "learner@example.com",
        )
        self.assertEqual(
            data["user"]["display_name"],
            "New Learner",
        )
        self.assertEqual(
            data["user"]["roles"],
            ["member"],
        )
        self.assertIn(
            "knowledge.write",
            data["user"]["permissions"],
        )
        self.assertFalse(data["user"]["is_superuser"])
        self.assertIn("access_token", data)
        self.assertIn("ai_refresh_token", self.client.cookies)

        me_response = self.client.get(
            "/auth/me",
            headers={
                "Authorization": (
                    f"Bearer {data['access_token']}"
                )
            },
        )
        self.assertEqual(me_response.status_code, 200)

    def test_register_rejects_duplicate_email(self):
        response = self.client.post(
            "/auth/register",
            json={
                "email": "admin@example.com",
                "password": "Another-Password-42",
                "display_name": "Duplicate Admin",
            },
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["detail"],
            "该邮箱已存在",
        )

    def test_register_validates_trimmed_name_and_password(self):
        blank_name = self.client.post(
            "/auth/register",
            json={
                "email": "blank-name@example.com",
                "password": "Valid-Password-42",
                "display_name": "   ",
            },
        )
        self.assertEqual(blank_name.status_code, 422)

        short_password = self.client.post(
            "/auth/register",
            json={
                "email": "short-password@example.com",
                "password": "short",
                "display_name": "Learner",
            },
        )
        self.assertEqual(short_password.status_code, 422)

    def test_protected_route_requires_login(self):
        response = self.client.get(
            "/protected"
        )

        self.assertEqual(
            response.status_code,
            401,
        )


if __name__ == "__main__":
    unittest.main()
