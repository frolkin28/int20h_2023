from umongo import Document, fields

from hackaton.models import instance


@instance.register
class User(Document):
    class Meta:
        strict = False

    doc_id = fields.ObjectIdField(attribute='_id')
    email = fields.EmailField()
    password = fields.StrField()
    first_name = fields.StrField()
    last_name = fields.StrField()
