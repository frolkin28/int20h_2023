import logging
import typing as t

from aiohttp import web

from hackaton.bl.ingredient import (
    get_ingredient_by_ingredient_mealdb_id,
    create_ingredient,
    update_ingredient,
)
from hackaton.bl.ingredient_type import (
    get_ingredient_type_by_title,
    create_ingredient_type,
    update_ingredient_type,
)
from hackaton.const import MEALDB_API_HOST, SourceTypeEnum
from hackaton.lib.exceptions import MealDBMigrationException
from hackaton.models.ingredient import Ingredient
from hackaton.models.source import Source

log = logging.getLogger(__name__)


def _parse_ingredient_data(
    mealdb_ingredient_data: t.Dict[str, t.Any]
) -> t.Dict[str, t.Any]:
    result = {
        'title': mealdb_ingredient_data.get('strIngredient'),
    }
    if mealdb_ingredient_data.get('strDescription'):
        result['description'] = mealdb_ingredient_data['strDescription']
    if mealdb_ingredient_data.get('strType'):
        result['type'] = mealdb_ingredient_data['strType']

    return result


async def _migrate_ingredient_type(ingredient_type_title: str) -> None:
    old_ingredient_type = await get_ingredient_type_by_title(
        ingredient_type_title
    )

    parsed_data = {'title': ingredient_type_title}
    if old_ingredient_type:
        ingredient_type = update_ingredient_type(
            old_ingredient_type, data=parsed_data
        )
        await ingredient_type.commit()
        ingredient_type_doc_id = str(ingredient_type.doc_id)
        log.info(
            f'update ingredient_type '
            f'{ingredient_type_title=} {ingredient_type_doc_id=}'
        )
    else:
        source = Source(
            type=SourceTypeEnum.mealdb.value
        )
        ingredient_type = create_ingredient_type(
            data=parsed_data, source=source
        )
        await ingredient_type.commit()
        log.info(f'insert ingredient_type {ingredient_type_title=}')


async def _migrate_ingredient(ingredient: t.Dict[str, t.Any]) -> None:
    ingredient_mealdb_id = ingredient['idIngredient']
    old_ingredient: t.Optional[Ingredient] = (
        await get_ingredient_by_ingredient_mealdb_id(ingredient_mealdb_id)
    )

    parsed_data = _parse_ingredient_data(ingredient)

    if old_ingredient:
        ingredient = update_ingredient(old_ingredient, data=parsed_data)
        await ingredient.commit()
        ingredient_doc_id = str(ingredient.doc_id)
        log.info(
            f'update ingredient '
            f'{ingredient_mealdb_id=} {ingredient_doc_id=}'
        )
    else:
        source = Source(
            type=SourceTypeEnum.mealdb.value,
            id=ingredient_mealdb_id,
        )
        ingredient = create_ingredient(data=parsed_data, source=source)
        await ingredient.commit()
        log.info(f'insert ingredient {ingredient_mealdb_id=}')

    if ingredient.type:
        await _migrate_ingredient_type(ingredient.type)


async def migrate_ingredients(app: web.Application):
    log.info('==== migrate_ingredients STARTED ====')
    ingredients = await get_ingredients_data(app)

    for ingredient in ingredients:
        await _migrate_ingredient(ingredient)

    log.info('==== migrate_ingredients FINISHED ====')


async def get_ingredients_data(
    app: web.Application
) -> t.List[t.Dict[str, t.Any]]:
    url = f'{MEALDB_API_HOST}/list.php?i=list'
    api_response = None
    try:
        async with app['session'].get(url) as resp:
            api_response = await resp.json()
            resp.raise_for_status()

            return api_response.get('meals', [])
    except Exception as error:
        raise MealDBMigrationException(
            f'Error while get_ingredients_data, {api_response=}: {error=}'
        )
