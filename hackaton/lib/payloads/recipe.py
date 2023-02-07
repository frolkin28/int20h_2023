from marshmallow import Schema
from marshmallow import fields


class RecipeCategoryPayload(Schema):
    title = fields.Str(required=True)
    description = fields.Str(max=2000)
    img_url = fields.Str(max=1000)
