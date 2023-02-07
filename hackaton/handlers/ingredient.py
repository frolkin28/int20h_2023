from http import client as httplib
from logging import getLogger

from aiohttp import web

from hackaton.const import SourceTypeEnum
from hackaton.models.source import Source
from hackaton.models.user import User
from hackaton.lib.auth import with_auth_user
from hackaton.bl.ingredient import create_ingredient
from hackaton.bl.ingredient import push_user_product
from hackaton.lib.query import get_ingredient_types
from hackaton.lib.payloads.indredient import IngredientPayload
from hackaton.lib.exceptions import SchemaValidationError
from hackaton.lib.rest_utils import error_response
from hackaton.lib.rest_utils import ok_response
from hackaton.lib.utils import serialize_mongo_records

log = getLogger(__name__)


@with_auth_user
async def add_ingredient(request: web.Request, user: User) -> web.Response:
    ingredient_data = await request.json()
    try:
        register_payload = IngredientPayload.load(ingredient_data)
    except SchemaValidationError as e:
        log.error(f'Invalid ingredient request data: {e.errors}')
        return error_response(code=httplib.BAD_REQUEST, errors=e.errors)

    source = Source(
        type=SourceTypeEnum.user.value,
        id=str(user.doc_id),
    )

    ingredient = create_ingredient(
        data=register_payload.to_dict(),
        source=source
    )
    await ingredient.commit()

    return ok_response(
        code=httplib.CREATED,
        payload={'ingredient_id': str(ingredient.doc_id)},
    )


@with_auth_user
async def add_user_product(request: web.Request, user: User) -> web.Response:
    request_data = await request.json()
    ingr_id = request_data.get('product_id')
    if not ingr_id:
        return error_response(
            code=httplib.BAD_REQUEST,
            errors_mapping={'message': 'Invalid payload'},
        )
    res = await push_user_product(request.app, user.doc_id, ingr_id)
    if not res:
        return error_response(
            code=httplib.CONFLICT,
            errors_mapping={'message': 'No such ingredient'},
        )
    return ok_response()


async def get_ingredient_type_list(request: web.Request) -> web.Response:
    limit = int(request.query.get('limit', 10))
    offset = int(request.query.get('offset', 0))
    ingr_types = await get_ingredient_types(limit, offset)
    return ok_response(payload=serialize_mongo_records(ingr_types))
