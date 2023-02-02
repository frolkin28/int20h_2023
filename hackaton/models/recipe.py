from umongo import Document, fields

from hackaton.models import instance


@instance.register
class Recipe(Document):
    # inherit Document to create collection in mongo
    class Meta:
        strict = False

    doc_id = fields.ObjectIdField(attribute='_id')
    name = fields.StrField()