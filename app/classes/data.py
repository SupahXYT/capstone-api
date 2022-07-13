from werkzeug.security import generate_password_hash, check_password_hash
from scrape import company 
from shared_classes import Company
from mongoengine import (
    Document,
    EmailField,
    StringField,
    BooleanField,
    EnumField,
    URLField,
    ListField,
    ReferenceField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    signals
)


class TaskStatus:
    INACTIVE = -1
    SUBMITTED = 0
    APPROVED = 1
    REJECTED = 2


class QueueRequest(Document):
    uuid = StringField()

    @classmethod
    def find_policy(cls, sender, document, **kwargs):
        for request in cls.objects():
            print(f'getting company info {request.uuid}')
            scraper = company.PolicyFinder(request.uuid)

            company_obj = scraper.get_company()
            scraper.find_company()
            company_obj.policy = None
            company_obj.save()

            scraper.find_policy()
            scraper.get_policy().save()
            company.policy = scraper.get_policy()

            cls.objects(uuid=request.uuid).delete()


class User(Document):
    email = EmailField()
    password_hash = StringField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# all values are encrypted on the client side
class UserOptInfo(Document):
    user = ReferenceField(User)
    fname = StringField()
    lname = StringField()
    email = StringField()
    address1 = StringField()
    address2 = StringField()
    postal_code = StringField()
    city = StringField()
    region = StringField()
    country = StringField()
    maid = StringField() # mobile advertising identifier


class Task(Document):
    user = ReferenceField(User)
    company = ReferenceField(Company)
    status = IntField()


class NoUserTask(Document):
    company = ReferenceField(Company)
    uuid = StringField()
    status = IntField()

signals.post_save.connect(QueueRequest.find_policy, QueueRequest)
