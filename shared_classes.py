from mongoengine import (
    Document, 
    StringField,
    URLField,
    BooleanField,
    ListField,
    ReferenceField,
    EmailField
)


class Policy(Document):
    uuid = StringField()
    url = URLField()
    do_not_sell = BooleanField()
    third_party_data = BooleanField()
    profiling = BooleanField()
    categories = ListField()
    opt_out_email = ListField()
    opt_out_url = StringField()


class Company(Document):
    name = StringField()
    uuid = StringField()
    desc = StringField()
    image = StringField()
    url = StringField()
    policy = ReferenceField(Policy)


class DataBroker(Document):
    name = StringField()
    website = URLField()
    email = EmailField()

