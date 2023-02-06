import logging
import typing as t

from aiohttp import web
from marshmallow import ValidationError

from hackaton.bl.search import RecipeSearchMongoExecutor
from hackaton.config import CONFIG
from hackaton.lib.forms.search import (
    SearchRecipeSchema,
)
from hackaton.lib.rest_utils import error_response, ok_response

log = logging.getLogger(__name__)


async def search_recipe(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except Exception as e:
        return error_response(
            web.HTTPUnprocessableEntity.status,
            errors_mapping={'error': str(e)}
        )

    schema = SearchRecipeSchema()
    try:
        result = schema.load(payload)
    except ValidationError as e:
        log.info(f"Errors during search request: {e.messages}")
        result = e.valid_data

    app = request.app

    search_executor = RecipeSearchMongoExecutor(
        db=app['db_recipe'],
        filter_data=result,
        debug=CONFIG['is_debug']
    )
    search_result = await search_executor.get_result() or []
    pager = await search_executor.get_pager()

    recipes = list()
    for recipe in search_result:
        recipes.append(
            prepare_recipe_data(recipe)
        )

    return ok_response(
        payload={
            "currentPage": pager.page,
            "nextPage": pager.next_page,
            "prevPage": pager.previous_page,
            "pageAmount": pager.page_count,
            "totalHits": pager.item_count,
            "recipes": recipes,
        },
    )


def prepare_recipe_data(
    data: t.Dict[str, t.Any],
) -> t.Dict[str, t.Any]:
    doc_id = str(data.pop('_id'))
    data['_id'] = doc_id

    return data
