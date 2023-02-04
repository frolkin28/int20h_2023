import typing as t

from hackaton.const import SourceTypeEnum
from hackaton.models.recipe import Recipe
from hackaton.models.source import Source


async def get_recipe_by_recipe_mealdb_id(
    category_mealdb_id: str
) -> t.Optional[Recipe]:
    return await Recipe.find_one({
        'source.type': SourceTypeEnum.mealdb.value,
        'source.id': category_mealdb_id,
    })


def create_recipe(
    data: t.Dict[str, t.Any], source: Source
) -> Recipe:
    recipe = Recipe(**data)
    recipe.source = source

    return recipe


def update_recipe(
    recipe: Recipe, data: t.Dict[str, t.Any]
) -> Recipe:
    recipe.update(data)

    return recipe
