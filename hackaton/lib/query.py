from bson.objectid import ObjectId
from bson.errors import InvalidId

from hackaton.lib.payloads.auth import UserPayload
from hackaton.models.user import User
from hackaton.models.ingredient import Ingredient
from hackaton.models.ingredient_type import IngredientType
from hackaton.models.recipe import Recipe


async def create_user(user_payload: UserPayload) -> User:
    user_dict = user_payload.to_dict()
    user = User(**user_dict)
    await user.commit()
    return user


async def get_user_by_email(email: str) -> User | None:
    return await User.find_one({'email': email})


async def get_user_by_id(user_id: str | None) -> User | None:
    if not user_id:
        return None
    try:
        user = await User.find_one({'_id': ObjectId(user_id)})
    except InvalidId:
        return None

    return user


async def get_recipe_by_id(r_id: str) -> Recipe | None:
    try:
        record = await Recipe.find_one({'_id': ObjectId(r_id)})
    except InvalidId:
        return None

    return record


async def get_ingredient_by_id(ing_id: str) -> Recipe | None:
    try:
        record = await Ingredient.find_one({'_id': ObjectId(ing_id)})
    except InvalidId:
        return None

    return record


async def get_ingredient_types(limit: int = 10, offset: int = 0) -> list[IngredientType]:
    res = []
    async for record in IngredientType.find({}).skip(offset).limit(limit):
        res.append(record)
    return res
