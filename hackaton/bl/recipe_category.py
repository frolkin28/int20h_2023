import typing as t

from hackaton.const import SourceTypeEnum
from hackaton.models.recipe_category import RecipeCategory
from hackaton.models.source import Source


async def get_all_recipe_categories_by_source_type(
    source_type: SourceTypeEnum
) -> t.List[RecipeCategory]:
    cursor = RecipeCategory.find({
        'source.type': source_type.value,
    })

    return await cursor.to_list(length=None)


async def get_recipe_category_by_category_mealdb_id(
    category_mealdb_id: str
) -> t.Optional[RecipeCategory]:
    return await RecipeCategory.find_one({
        'source.type': SourceTypeEnum.mealdb.value,
        'source.id': category_mealdb_id,
    })


def create_recipe_category(
    data: t.Dict[str, t.Any], source: Source
) -> RecipeCategory:
    recipe_category = RecipeCategory(**data)
    recipe_category.source = source
    if recipe_category.title:
        recipe_category.title = recipe_category.title.lower()

    return recipe_category


def update_recipe_category(
    recipe_category: RecipeCategory, data: t.Dict[str, t.Any]
) -> RecipeCategory:
    recipe_category.update(data)
    if recipe_category.title:
        recipe_category.title = recipe_category.title.lower()

    return recipe_category
