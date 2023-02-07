from http import client as httplib
from logging import getLogger

from aiohttp import web
from marshmallow import ValidationError

from hackaton.const import SourceTypeEnum
from hackaton.models.source import Source
from hackaton.models.user import User
from hackaton.lib.auth import with_auth_user
from hackaton.lib.exceptions import SchemaValidationError
from hackaton.lib.payloads.recipe import RecipeCategoryPayload
from hackaton.lib.query import create_recipe_category, get_recipe_by_id
from hackaton.lib.rest_utils import error_response
from hackaton.lib.rest_utils import ok_response
from hackaton.lib.utils import serialize_mongo_record


log = getLogger(__name__)


async def recipe_view(request: web.Request) -> web.Response:
    recipe_id = request.match_info['id']
    recipe = await get_recipe_by_id(recipe_id)
    if not recipe:
        return error_response(code=httplib.NOT_FOUND)

    recipe_data = serialize_mongo_record(recipe)
    return ok_response(payload=recipe_data)


@with_auth_user
async def create_recipe_category_handler(
    request: web.Request,
    user: User,
) -> web.Response:
    request_data = await request.json()
    try:
        payload = RecipeCategoryPayload().load(request_data)
    except ValidationError as e:
        log.error(
            f'Invalid recipe category creation request data: {e.messages}'
        )
        return error_response(
            code=httplib.BAD_REQUEST,
            errors_mapping=e.messages,
        )
    source = Source(
        type=SourceTypeEnum.user.value,
        id=str(user.doc_id),
    )

    recipe_category = await create_recipe_category(payload, source)
    return ok_response(payload=serialize_mongo_record(recipe_category))
