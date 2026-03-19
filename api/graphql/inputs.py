from strawberry.experimental.pydantic import input as pydantic_input
import strawberry

from api.schemas import (
    RegisterSchema,
    PasswordChangeSchema,
    PasswordResetSchema,
    TwoFactorAuthSchema
)

@pydantic_input(RegisterSchema)
class RegisterInput:
    to_email: strawberry.auto
    link: strawberry.auto

@pydantic_input(PasswordChangeSchema)
class PasswordChangeInput:
    to_email: strawberry.auto

@pydantic_input(PasswordResetSchema)
class PasswordResetInput:
    to_email: strawberry.auto
    link: strawberry.auto
    expiresAt: strawberry.auto

@pydantic_input(TwoFactorAuthSchema)
class TwoFactorAuthInput:
    to_email: strawberry.auto
    code: strawberry.auto
    expiresAt: strawberry.auto






