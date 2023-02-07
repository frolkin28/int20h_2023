import typing as t

from hackaton.const import SourceTypeEnum, DifficultyLevelEnum
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
    recipe.difficulty_level = calculate_difficulty_level(recipe)
    recipe.ingredients_ids = [
        ingredient_item.ingredient_id
        for ingredient_item in recipe.ingredients
    ]

    return recipe


def update_recipe(
    recipe: Recipe, data: t.Dict[str, t.Any]
) -> Recipe:
    recipe.update(data)
    recipe.difficulty_level = calculate_difficulty_level(recipe)
    recipe.ingredients_ids = [
        ingredient_item.ingredient_id
        for ingredient_item in recipe.ingredients
    ]

    return recipe


def calculate_difficulty_level(recipe: Recipe) -> int:
    instructions_len = len(recipe.instructions or '')

    if instructions_len <= 1000:
        return DifficultyLevelEnum.easy.value
    elif 1000 < instructions_len <= 2000:
        return DifficultyLevelEnum.medium.value
    else:
        return DifficultyLevelEnum.hard.value
