import enum


MEALDB_API_HOST = 'https://www.themealdb.com/api/json/v1/1'

PAGE_NUMBER_PARAM = "page"
PAGE_SIZE_PARAM = "page_size"
SORT_PARAM = "sort"
QUERY_STRING_PARAM = "query"

INGREDIENTS_IDS_PARAM = 'ingredients_ids'
CREATED_BY_USER_IDS_PARAM = 'created_by_user_ids'
AREA_PARAM = 'area'
RECIPE_CATEGORY_PARAM = 'recipe_category'

INGREDIENT_TYPE_PARAM = 'ingredient_type'


@enum.unique
class SourceTypeEnum(enum.Enum):
    mealdb = 'mealdb'
    user = 'user'
    migration = 'migration'


@enum.unique
class DifficultyLevelEnum(enum.Enum):
    easy = 1
    medium = 2
    hard = 3
