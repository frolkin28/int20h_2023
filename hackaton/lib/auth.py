import typing as t
from functools import wraps
from http import client as httplib


from aiohttp import web
from aiohttp_security import authorized_userid
from aiohttp_security.abc import AbstractAuthorizationPolicy
from hackaton.models.user import User
from hackaton.lib.rest_utils import error_response
from passlib.hash import pbkdf2_sha256

from hackaton.lib.query import get_user_by_id


TFunc = t.TypeVar('TFunc', bound=t.Callable[..., t.Any])


class MongoAuthorizationPolicy(AbstractAuthorizationPolicy):
    async def authorized_userid(self, identity: str) -> str | None:
        '''Retrieve authorized user id.'''
        user = await get_user_by_id(identity)
        if not user:
            return None

        return str(user.doc_id)

    async def permits(self, *args, **kwargs) -> bool:
        '''Check user permissions.'''
        return True


def check_password(user_pwd: str, hashed_pwd: str) -> bool:
    return pbkdf2_sha256.verify(user_pwd, hashed_pwd)


def login_required(func: TFunc) -> TFunc:
    @wraps(func)
    async def wrapper(
        request: web.Request,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> t.Any:
        user_id = await authorized_userid(request)
        if not user_id:
            return error_response(code=httplib.UNAUTHORIZED)
        return await func(request, *args, **kwargs)

    return t.cast(TFunc, wrapper)


def with_auth_user(func: TFunc) -> TFunc:
    @wraps(func)
    async def wrapper(
        request: web.Request,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> t.Any:
        user = await get_current_user(request)
        if not user:
            return error_response(code=httplib.UNAUTHORIZED)
        return await func(request, user, *args, **kwargs)

    return t.cast(TFunc, wrapper)


async def get_current_user(request: web.Request) -> User | None:
    user_id = await authorized_userid(request)
    return await get_user_by_id(user_id)
