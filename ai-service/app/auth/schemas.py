import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


class LoginRequest(BaseModel):
    email: str = Field(
        min_length=3,
        max_length=320,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("email")
    @classmethod
    def validate_email(
        cls,
        value: str,
    ) -> str:
        email = value.lower().strip()

        if not EMAIL_PATTERN.match(email):
            raise ValueError("邮箱格式不正确")

        return email


class RegisterRequest(LoginRequest):
    display_name: str = Field(
        min_length=1,
        max_length=100,
    )

    @field_validator("display_name")
    @classmethod
    def validate_display_name(
        cls,
        value: str,
    ) -> str:
        display_name = value.strip()

        if not display_name:
            raise ValueError("显示名称不能为空")

        return display_name

    @field_validator("password")
    @classmethod
    def validate_password_bytes(
        cls,
        value: str,
    ) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError(
                "密码不能超过 72 个 UTF-8 字节"
            )

        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    email: str
    display_name: str
    is_active: bool
    is_superuser: bool
    roles: list[str]
    permissions: list[str]


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class MessageResponse(BaseModel):
    code: int = 0
    message: str
