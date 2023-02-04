import asyncio
import logging
import typing as t

from aiohttp import web

from hackaton.bl.ingredient import get_ingredient_by_ingredient_title
from hackaton.bl.recipe import (
    get_recipe_by_recipe_mealdb_id,
    create_recipe,
    update_recipe,
)
from hackaton.bl.recipe_category import get_all_recipe_categories_by_source_type
from hackaton.const import MEALDB_API_HOST, SourceTypeEnum
from hackaton.exceptions import MealDBMigrationException
from hackaton.models.recipe import Recipe
from hackaton.models.recipe_category import RecipeCategory
from hackaton.models.source import Source

log = logging.getLogger(__name__)


async def _parse_recipe_ingredients_data(
    mealdb_recipe_data: t.Dict[str, t.Any]
) -> t.List[t.Dict[str, t.Any]]:
    ingredient_titles = {}
    ingredient_measures = {}

    for key, value in mealdb_recipe_data.items():
        if key.startswith('strIngredient') and value:
            split_key = key.split('strIngredient')
            ingredient_titles[split_key[1]] = value
        if key.startswith('strMeasure') and value:
            split_key = key.split('strMeasure')
            ingredient_measures[split_key[1]] = value

    ingredient_items = []
    for ingredient_key, ingredient_title in ingredient_titles.items():
        if not ingredient_measures.get(ingredient_key):
            continue

        ingredient_item = {
            'ingredient_title': ingredient_title,
            'measure': ingredient_measures[ingredient_key],
        }
        ingredient = await get_ingredient_by_ingredient_title(ingredient_title)
        if ingredient:
            ingredient_item['ingredient_id'] = str(ingredient.doc_id)

        ingredient_items.append(ingredient_item)

    return ingredient_items


async def _parse_recipe_data(
    mealdb_recipe_data: t.Dict[str, t.Any]
) -> t.Dict[str, t.Any]:
    tags_data = mealdb_recipe_data.get('strTags') or ''
    tags = [tag.strip() for tag in tags_data.split(',')]
    result = {
        'title': mealdb_recipe_data.get('strMeal'),
        'category': mealdb_recipe_data.get('strCategory'),
        'area': mealdb_recipe_data.get('strArea'),
        'instructions': mealdb_recipe_data.get('strInstructions'),
        'drink_alternate': mealdb_recipe_data.get('strDrinkAlternate'),
        'img_url': mealdb_recipe_data.get('strMealThumb'),
        'tags': tags or None,
        'video_url': mealdb_recipe_data.get('strYoutube'),
        'source_url': mealdb_recipe_data.get('strSource'),
        'ingredients': await _parse_recipe_ingredients_data(mealdb_recipe_data),
    }

    return {k: v for k, v in result.items() if v}


async def _migrate_recipe(
    app: web.Application, recipe_short_data: t.Dict[str, t.Any]
) -> None:
    recipe_mealdb_id = recipe_short_data['idMeal']

    recipe_data = await get_recipe_data(app, recipe_mealdb_id)
    if not recipe_data:
        log.error(f'fail to get {recipe_mealdb_id=} from mealdb API')
        return

    old_recipe: t.Optional[Recipe] = (
        await get_recipe_by_recipe_mealdb_id(recipe_mealdb_id)
    )

    parsed_data = await _parse_recipe_data(recipe_data)

    if old_recipe:
        recipe = update_recipe(old_recipe, data=parsed_data)
        await recipe.commit()
        recipe_doc_id = str(recipe.doc_id)
        log.info(f'update recipe {recipe_mealdb_id=} {recipe_doc_id=}')
    else:
        source = Source(
            type=SourceTypeEnum.mealdb.value,
            id=recipe_mealdb_id,
        )
        recipe = create_recipe(data=parsed_data, source=source)
        await recipe.commit()
        log.info(f'insert recipe {recipe_mealdb_id=}')


async def migrate_recipes_by_category(
    app: web.Application, recipe_category: RecipeCategory
):
    recipe_category_doc_id = str(recipe_category.doc_id)
    log.info(
        f'---- migrate_recipes_by_category '
        f'{recipe_category.title=} {recipe_category_doc_id=} '
        f'STARTED ----'
    )
    recipes = await get_recipes_data_by_recipe_category_title(
        app, recipe_category_title=recipe_category.title
    )

    for recipe_short_data in recipes:
        await _migrate_recipe(app, recipe_short_data)

    log.info(
        f'---- migrate_recipes_by_category '
        f'{recipe_category.title=} {recipe_category_doc_id=} '
        f'FINISHED ----'
    )


async def migrate_recipes_by_categories(app: web.Application):
    log.info('==== migrate_recipes_by_categories STARTED ====')
    recipe_categories = (
        await get_all_recipe_categories_by_source_type(
            source_type=SourceTypeEnum.mealdb
        )
    )

    tasks = []
    for recipe_category in recipe_categories:
        tasks.append(
            migrate_recipes_by_category(app, recipe_category)
        )

    await asyncio.gather(*tasks)

    log.info('==== migrate_recipes_by_categories FINISHED ====')


async def get_recipes_data_by_recipe_category_title(
    app: web.Application, recipe_category_title: str
) -> t.List[t.Dict[str, t.Any]]:
    url = f'{MEALDB_API_HOST}/filter.php?c={recipe_category_title}'
    api_response = None
    try:
        async with app['session'].get(url) as resp:
            api_response = await resp.json()
            resp.raise_for_status()

            return api_response.get('meals', [])
    except Exception as error:
        raise MealDBMigrationException(
            f'Error while get_recipes_data_by_recipe_category_title, '
            f'{api_response=}: {error=}'
        )


async def get_recipe_data(
    app: web.Application, recipe_mealdb_id: str
) -> t.Dict[str, t.Any]:
    url = f'{MEALDB_API_HOST}/lookup.php?i={recipe_mealdb_id}'
    api_response = None
    try:
        async with app['session'].get(url) as resp:
            api_response = await resp.json()
            resp.raise_for_status()

            meals = api_response.get('meals')
            return meals and meals[0]
    except Exception as error:
        raise MealDBMigrationException(
            f'Error while get_recipes_data_by_recipe_category_title, '
            f'{api_response=}: {error=}'
        )
