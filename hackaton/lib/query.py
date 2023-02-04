from bson.objectid import ObjectId
from logging import getLogger

from hackaton.lib.payloads.auth import UserPayload
from hackaton.models.user import User


log = getLogger(__name__)


async def create_user(user_payload: UserPayload) -> User:
    user_dict = user_payload.to_dict()
    user = User(**user_dict)
    await user.commit()
    return user


async def get_user_by_email(email: str) -> User | None:
    return await User.find_one({'email': email})


async def get_user_by_id(user_id: str | None) -> User | None:
    if not user_id:
        return False

    return await User.find_one({'_id': ObjectId(user_id)})
