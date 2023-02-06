from marshmallow import Schema
from marshmallow import fields
from marshmallow import pre_dump


class IngredientItemSchema(Schema):
    ingredient_id = fields.Str()
    ingredient_title = fields.Str()
    measure = fields.Str()


class SourceSchema(Schema):
    type = fields.Str()
    id = fields.Str()


class RecipeSchema(Schema):
    id = fields.Str(attribute='doc_id')
    title = fields.Str()
    description = fields.Str()
    category = fields.Str()
    instructions = fields.Str()
    area = fields.Str()
    img_url = fields.Str()
    video_url = fields.Str()
    source_url = fields.Str()
    drink_alternate = fields.Str()
    difficulty_level = fields.Str()
    tags = fields.List(
        fields.Str(),
        default=[]
    )
    ingredients = fields.List(
        fields.Nested(IngredientItemSchema),
        default=[]
    )
    source = fields.Nested(SourceSchema)
