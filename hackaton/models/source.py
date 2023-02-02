from umongo import EmbeddedDocument, fields

from hackaton.models import instance


@instance.register
class Source(EmbeddedDocument):
    class Meta:
        strict = False

    type = fields.StrField()
    id = fields.StrField()
