import typing as t
from bson.objectid import ObjectId

from aiohttp import web

from hackaton.const import SourceTypeEnum
from hackaton.models.ingredient import Indredient
from hackaton.models.source import Source
from hackaton.lib.query import get_ingredient_by_id


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


async def push_user_product(app: web.Application, user_id: ObjectId, ingredient_id: str) -> bool:
    ingr = await get_ingredient_by_id(ingredient_id)
    if not ingr:
        return False

    await app['mongo_db'].user.update_one(
        {'_id': user_id},
        {'$push': {'product_ids': ingredient_id}},
    )
    return True
