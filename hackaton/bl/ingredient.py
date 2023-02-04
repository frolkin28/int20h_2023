import typing as t

from hackaton.const import SourceTypeEnum
from hackaton.models.ingredient import Indredient
from hackaton.models.source import Source


async def get_ingredient_by_ingredient_mealdb_id(
    category_mealdb_id: str
) -> t.Optional[Indredient]:
    return await Indredient.find_one({
        'source.type': SourceTypeEnum.mealdb.value,
        'source.id': category_mealdb_id,
    })


async def get_ingredient_by_ingredient_title(
    ingredient_title: str
) -> t.Optional[Indredient]:
    return await Indredient.find_one({
        'title': ingredient_title,
    })


def create_ingredient(
    data: t.Dict[str, t.Any], source: Source
) -> Indredient:
    ingredient = Indredient(**data)
    ingredient.source = source

    return ingredient


def update_ingredient(
    ingredient: Indredient, data: t.Dict[str, t.Any]
) -> Indredient:
    ingredient.update(data)

    return ingredient
