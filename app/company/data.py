from mongoengine import (
    Document,
    StringField,
    URLField,
    BooleanField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField
)


class Policy(EmbeddedDocument):
    url = URLField()
    do_not_sell = BooleanField()
    third_party_data = BooleanField()
    profiling = BooleanField()
    categories = ListField()
    opt_out_email = ListField()
    opt_out_url = URLField()


class Company(Document):
    uuid = StringField(required=True)
    name = StringField(required=True)
    description = StringField()
    image_url = StringField()
    website_url = URLField()
    EmbeddedDocumentField(Policy)
