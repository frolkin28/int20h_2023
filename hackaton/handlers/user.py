import typing as t
from aiohttp import web

from hackaton.models.user import User
from hackaton.lib.auth import with_auth_user
from hackaton.lib.rest_utils import ok_response


@with_auth_user
async def get_user_data(_: web.Request, user: User) -> web.Response:
    return ok_response(payload=dict(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    ))
