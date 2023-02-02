from umongo import Document, fields

from hackaton.models import instance
from hackaton.models.source import Source


@instance.register
class Indredient(Document):
    class Meta:
        strict = False

    doc_id = fields.ObjectIdField(attribute='_id')
    title = fields.StrField()
    description = fields.StrField()
    source = fields.EmbeddedField(Source)
    type = fields.StrField()
