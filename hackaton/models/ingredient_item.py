from umongo import EmbeddedDocument, fields

from hackaton.models import instance


@instance.register
class IngredientItem(EmbeddedDocument):
    class Meta:
        strict = False

    ingredient_id = fields.StrField()
    ingredient_title = fields.StrField()
    measure = fields.StrField()
