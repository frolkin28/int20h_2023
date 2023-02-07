from umongo import Document, fields

from hackaton.models import instance
from hackaton.models.source import Source


@instance.register
class IngredientType(Document):
    class Meta:
        strict = False

    doc_id = fields.ObjectIdField(attribute='_id')
    title = fields.StrField(required=True)
    description = fields.StrField()
    source = fields.EmbeddedField(Source, required=True)
