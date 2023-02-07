from hackaton.bl.recipe import calculate_difficulty_level
from hackaton.models.recipe import Recipe


async def calculate_difficulty_level_for_all_recipes() -> None:
    async for recipe in Recipe.find({}):
        recipe.difficulty_level = calculate_difficulty_level(recipe)
        await recipe.commit()


async def add_ingredients_ids_field_for_all_recipes() -> None:
    async for recipe in Recipe.find({}):
        recipe.ingredients_ids = [
            ingredient_item.ingredient_id
            for ingredient_item in recipe.ingredients
        ]
        await recipe.commit()
