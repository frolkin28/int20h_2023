from http import client as httplib
from logging import getLogger

from aiohttp import web
from aiohttp_security import remember
from aiohttp_security import forget

from hackaton.bl.auth import register_user
from hackaton.bl.auth import login_user
from hackaton.lib.auth import login_required
from hackaton.lib.exceptions import SchemaValidationError
from hackaton.lib.exceptions import UserAlreadyExists
from hackaton.lib.payloads.auth import UserPayload
from hackaton.lib.payloads.auth import LoginPayload
from hackaton.lib.rest_utils import error_response
from hackaton.lib.rest_utils import ok_response


log = getLogger(__name__)


async def register(request: web.Request) -> web.Response:
    user_data = await request.json()
    try:
        register_payload = UserPayload.load(user_data)
    except SchemaValidationError as e:
        log.error(f'Invalid register data: {e.errors}')
        return error_response(code=httplib.BAD_REQUEST, errors=e.errors)

    try:
        user = await register_user(register_payload)
    except UserAlreadyExists:
        return error_response(
            code=httplib.CONFLICT,
            errors={'message': 'User already exists'},
        )
    return ok_response(
        code=httplib.CREATED,
        payload={'user_id': str(user.doc_id)},
    )


async def login(request: web.Request) -> web.Response:
    user_data = await request.json()
    try:
        login_payload = LoginPayload.load(user_data)
    except SchemaValidationError as e:
        log.error(f'Invalid login data: {e.errors}')
        return error_response(code=httplib.BAD_REQUEST, errors=e.errors)

    user_identity = await login_user(login_payload)
    if not user_identity:
        return error_response(code=httplib.UNAUTHORIZED)

    response = ok_response()
    await remember(request, response, user_identity)
    return response


async def logout(request: web.Request) -> web.Response:
    response = ok_response()
    await forget(request, response)
    return response
