import argparse
import getpass

from app.auth.bootstrap import (
    initialize_auth,
)
from app.auth.service import (
    create_user,
)
from app.knowledgedb.db import (
    SessionLocal,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "创建首个 AI 项目管理员账号"
        )
    )
    parser.add_argument(
        "--email",
        required=True,
    )
    parser.add_argument(
        "--name",
        default="System Administrator",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    password = getpass.getpass(
        "管理员密码: "
    )
    password_confirm = getpass.getpass(
        "再次输入密码: "
    )

    if password != password_confirm:
        raise SystemExit(
            "两次输入的密码不一致"
        )

    if len(password) < 8:
        raise SystemExit(
            "密码至少需要 8 个字符"
        )

    initialize_auth()
    db = SessionLocal()

    try:
        try:
            user = create_user(
                db,
                email=args.email,
                password=password,
                display_name=args.name,
                role_code="admin",
                is_superuser=True,
            )
        except ValueError as error:
            raise SystemExit(
                str(error)
            ) from error
    finally:
        db.close()

    print(
        f"管理员已创建: {user.email}"
    )


if __name__ == "__main__":
    main()
