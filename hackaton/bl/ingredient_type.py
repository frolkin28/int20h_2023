import typing as t

from hackaton.models.ingredient_type import IngredientType
from hackaton.models.source import Source


async def get_ingredient_type_by_title(
    ingredient_type_title: str
) -> t.Optional[IngredientType]:
    return await IngredientType.find_one({
        'title': ingredient_type_title,
    })


def create_ingredient_type(
    data: t.Dict[str, t.Any], source: Source
) -> IngredientType:
    ingredient_type = IngredientType(**data)
    ingredient_type.source = source
    if ingredient_type.title:
        ingredient_type.title = ingredient_type.title.lower()

    return ingredient_type


def update_ingredient_type(
    ingredient_type: IngredientType, data: t.Dict[str, t.Any]
) -> IngredientType:
    ingredient_type.update(data)
    if ingredient_type.title:
        ingredient_type.title = ingredient_type.title.lower()

    return ingredient_type
