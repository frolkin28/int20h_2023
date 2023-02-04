from passlib.hash import pbkdf2_sha256

from hackaton.models.user import User
from hackaton.lib.auth import check_password
from hackaton.lib.query import get_user_by_email
from hackaton.lib.query import create_user
from hackaton.lib.payloads.auth import UserPayload
from hackaton.lib.payloads.auth import LoginPayload
from hackaton.lib.exceptions import UserAlreadyExists


async def register_user(payload: UserPayload) -> User:
    existing_user = await get_user_by_email(payload.email)
    if existing_user:
        raise UserAlreadyExists
    payload.password = pbkdf2_sha256.hash(payload.password)
    return await create_user(payload)


async def login_user(payload: LoginPayload) -> str | None:
    user = await get_user_by_email(payload.email)
    if not user:
        return None

    if not check_password(payload.password, user.password):
        return None

    return str(user.doc_id)
