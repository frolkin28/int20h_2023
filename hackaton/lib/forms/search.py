from marshmallow import Schema, fields, missing, validate

from hackaton.const import (
    PAGE_NUMBER_PARAM,
    SORT_PARAM,
    INGREDIENTS_IDS_PARAM,
    CREATED_BY_USER_IDS_PARAM,
    AREA_PARAM,
    INGREDIENT_TYPE_PARAM,
    RECIPE_CATEGORY_PARAM,
    PAGE_SIZE_PARAM,
    QUERY_STRING_PARAM,
)
from hackaton.lib.forms import ListOrOne


RECIPE_SORT_FIELDS = [
    'difficulty_level',
]
RECIPE_SORT_CHOICES = (
    RECIPE_SORT_FIELDS[:] + [f"-{field}" for field in RECIPE_SORT_FIELDS]
)


class SearchRecipeSchema(Schema):

    # page number
    page_number = fields.Int(
        attribute=PAGE_NUMBER_PARAM,
        data_key=PAGE_NUMBER_PARAM,
        missing=missing,
    )

    # page size
    page_size = fields.Int(
        attribute=PAGE_SIZE_PARAM,
        data_key=PAGE_SIZE_PARAM,
        missing=missing,
    )

    # sort search result by 'field' (asc) or '-field' (desc)
    sort = ListOrOne(
        fields.Str(),
        attribute=SORT_PARAM,
        data_key=SORT_PARAM,
        validate=validate.ContainsOnly(RECIPE_SORT_CHOICES),
        missing=missing,
    )

    # search string from user
    query_string = fields.Str(
        attribute=QUERY_STRING_PARAM,
        data_key=QUERY_STRING_PARAM,
        missing=missing,
    )

    ingredients = ListOrOne(
        fields.Str(),
        attribute=INGREDIENTS_IDS_PARAM,
        data_key=INGREDIENTS_IDS_PARAM,
        missing=missing,
    )

    created_by_user_ids = ListOrOne(
        fields.Str(),
        attribute=CREATED_BY_USER_IDS_PARAM,
        data_key=CREATED_BY_USER_IDS_PARAM,
        missing=missing,
    )

    area = ListOrOne(
        fields.Str(),
        attribute=AREA_PARAM,
        data_key=AREA_PARAM,
        missing=missing,
    )

    recipe_category = ListOrOne(
        fields.Str(),
        attribute=RECIPE_CATEGORY_PARAM,
        data_key=RECIPE_CATEGORY_PARAM,
        missing=missing,
    )


class SearchIngredientSchema(Schema):

    # page number
    page_number = fields.Int(
        attribute=PAGE_NUMBER_PARAM,
        data_key=PAGE_NUMBER_PARAM,
        missing=missing,
    )

    # page size
    page_size = fields.Int(
        attribute=PAGE_SIZE_PARAM,
        data_key=PAGE_SIZE_PARAM,
        missing=missing,
    )

    # search string from user
    query_string = fields.Str(
        attribute=QUERY_STRING_PARAM,
        data_key=QUERY_STRING_PARAM,
        missing=missing,
    )

    created_by_user_ids = ListOrOne(
        fields.Str(),
        attribute=CREATED_BY_USER_IDS_PARAM,
        data_key=CREATED_BY_USER_IDS_PARAM,
        missing=missing,
    )

    ingredients = ListOrOne(
        fields.Str(),
        attribute=INGREDIENTS_IDS_PARAM,
        data_key=INGREDIENTS_IDS_PARAM,
        missing=missing,
    )

    ingredient_type = ListOrOne(
        fields.Str(),
        attribute=INGREDIENT_TYPE_PARAM,
        data_key=INGREDIENT_TYPE_PARAM,
        missing=missing,
    )
