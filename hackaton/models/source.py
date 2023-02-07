from umongo import EmbeddedDocument, fields

from hackaton.models import instance


@instance.register
class Source(EmbeddedDocument):
    class Meta:
        strict = False

    type = fields.StrField(required=True)
    id = fields.StrField()
