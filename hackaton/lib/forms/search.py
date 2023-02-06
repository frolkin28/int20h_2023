from marshmallow import Schema, fields, missing, validate

from hackaton.const import (
    PAGE_NUMBER_PARAM,
    SORT_PARAM,
    INGREDIENTS_IDS_PARAM,
    CREATED_BY_USER_IDS_PARAM,
    AREA_PARAM,
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

    # sort search result by 'field' (asc) or '-field' (desc)
    sort = ListOrOne(
        fields.Str(),
        attribute=SORT_PARAM,
        data_key=SORT_PARAM,
        validate=validate.ContainsOnly(RECIPE_SORT_CHOICES),
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