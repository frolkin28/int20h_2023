import enum


MEALDB_API_HOST = 'https://www.themealdb.com/api/json/v1/1'


@enum.unique
class SourceTypeEnum(enum.Enum):
    mealdb = 'mealdb'
    user = 'user'


@enum.unique
class DifficultyLevelEnum(enum.Enum):
    easy = 1
    medium = 2
    hard = 3
