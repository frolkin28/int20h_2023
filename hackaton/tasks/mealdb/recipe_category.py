import asyncio
import logging
import typing as t

from aiohttp import web

from hackaton.bl.recipe_category import (
    get_recipe_category_by_category_mealdb_id,
    create_recipe_category,
    update_recipe_category,
)
from hackaton.const import MEALDB_API_HOST, SourceTypeEnum
from hackaton.exceptions import MealDBMigrationException
from hackaton.models.recipe_category import RecipeCategory
from hackaton.models.source import Source

log = logging.getLogger(__name__)


def _parse_recipe_category_data(
    mealdb_category_data: t.Dict[str, t.Any]
) -> t.Dict[str, t.Any]:
    return {
        'title': mealdb_category_data.get('strCategory'),
        'description': mealdb_category_data.get('strCategoryDescription'),
        'img_url': mealdb_category_data.get('strCategoryThumb'),
    }


async def _migrate_recipe_category(category: t.Dict[str, t.Any]) -> None:
    category_mealdb_id = category['idCategory']
    old_category: t.Optional[RecipeCategory] = (
        await get_recipe_category_by_category_mealdb_id(category_mealdb_id)
    )

    parsed_data = _parse_recipe_category_data(category)

    if old_category:
        category = update_recipe_category(old_category, data=parsed_data)
        await category.commit()
        category_doc_id = str(category.doc_id)
        log.info(
            f'update recipe category '
            f'{category_mealdb_id=} {category_doc_id=}'
        )
    else:
        source = Source(
            type=SourceTypeEnum.mealdb.value,
            id=category_mealdb_id,
        )
        category = create_recipe_category(data=parsed_data, source=source)
        await category.commit()
        log.info(f'insert recipe category {category_mealdb_id=}')


async def migrate_recipe_categories(app: web.Application):
    log.info('==== migrate_recipe_categories STARTED ====')
    recipe_categories = await get_categories_data(app)

    tasks = []
    for category in recipe_categories:
        # await _migrate_recipe_category(category)
        tasks.append(_migrate_recipe_category(category))

    await asyncio.gather(*tasks)

    log.info('==== migrate_recipe_categories FINISHED ====')


async def get_categories_data(app: web.Application) -> t.List[t.Dict[str, t.Any]]:
    url = f'{MEALDB_API_HOST}/categories.php'
    api_response = None
    try:
        async with app['session'].get(url) as resp:
            api_response = await resp.json()
            resp.raise_for_status()

            return api_response.get('categories', [])
    except Exception as error:
        raise MealDBMigrationException(
            f'Error while get_categories_data, {api_response=}: {error=}'
        )
