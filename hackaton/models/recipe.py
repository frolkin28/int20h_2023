from umongo import Document, fields

from hackaton.models import instance
from hackaton.models.ingredient_item import IngredientItem
from hackaton.models.source import Source


@instance.register
class Recipe(Document):
    class Meta:
        strict = False

    doc_id = fields.ObjectIdField(attribute='_id')
    title = fields.StrField(required=True)
    description = fields.StrField()
    category = fields.StrField(required=True)
    instructions = fields.StrField()
    area = fields.StrField()
    img_url = fields.StrField()
    video_url = fields.StrField()
    source_url = fields.StrField()
    drink_alternate = fields.StrField()
    difficulty_level = fields.IntField()
    tags = fields.ListField(
        fields.StrField(),
        default=[]
    )
    ingredients = fields.ListField(
        fields.EmbeddedField(IngredientItem),
        default=[]
    )
    source = fields.EmbeddedField(Source, required=True)
