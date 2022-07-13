from flask import Flask, request
from flask_restx import Api, Resource, fields

from app.company.crunchbase import Crunchbase
from app.company.data import Company as MongoCompany

from bson import json_util
import json

app = Flask(__name__)
api = Api(app, version='0.1', title='Company API',
          description='Company data API')

ns = api.namespace('company', description='Company data')

policy_model = api.model('Policy', {
    'url': fields.Url(),
    'do_not_sell': fields.Boolean(),
    'third_party_data': fields.Boolean(),
    'profiling': fields.Boolean(),
    'opt_out_email': fields.List(fields.String),
    'opt_out_url': fields.Url()
})

company_model = api.model(
    'Company',
    {
        'name': fields.String(),
        'description': fields.String(),
        'uuid': fields.String(),
        'image': fields.String(),
        'website_url': fields.Url(),
        'policy': fields.Nested(policy_model)
    }
)


class CompanyDAO:

    @classmethod
    def get(cls, uuid):
        return MongoCompany.objects(uuid=uuid).first()

    @classmethod
    def create(cls, data):
        company = MongoCompany(**data)
        company.save()
        return company

    @classmethod
    def update(cls, uuid, data):
        return cls.create(data)

    @classmethod
    def delete(cls, uuid):
        company = cls.get(uuid)
        company.delete()


def mongo_to_dict(obj):
    raw = json_util.dumps(obj.to_mongo())
    return json.loads(raw)


def merge_object(mongo_obj, dict_obj):
    mongo_obj_dict = mongo_to_dict(mongo_obj)
    return {**dict_obj, **mongo_obj_dict}


@ns.route('/<string:uuid>')
@ns.response(404, 'Company with given uuid does not exist')
@ns.param('uuid', 'Company uuid')
class Company(Resource):
    def get(self, uuid):
        """Fetch company from database"""
        db_company = CompanyDAO.get(uuid)
        if db_company:
            return mongo_to_dict(db_company)
        cb_company = Crunchbase.get_company(uuid)
        if cb_company:
            return cb_company
        api.abort(404, f"Company does not exist")

    @ns.expect(company_model)
    def put(self, uuid):
        """Update company in database"""
        if not CompanyDAO.get(uuid):
            api.abort(404, f"Company does not exist")
        company = CompanyDAO.update(uuid, api.payload)
        return mongo_to_dict(company)

    def delete(self, uuid):
        """Delete company from database"""
        if not CompanyDAO.get(uuid):
            api.abort(404, f"Company does not exist")
        CompanyDAO.delete(uuid)
        return '', 204


@ns.route('/')
@ns.response(409, "Tried creating company that already exists")
class CompanyCreate(Resource):
    @ns.expect(company_model)
    def post(self):
        """Add company to database"""
        if CompanyDAO.get(api.payload['uuid']):
            api.abort(409, "Company already exists")
        company = CompanyDAO.create(api.payload)
        return mongo_to_dict(company), 201


@ns.route('/search')
@ns.response(400, "Missing query parameter")
class CompanySearch(Resource):
    def get(self):
        """Search for companies from crunchbase and prioritize data from database"""
        query = request.args.get('query')
        if query:
            cb_search = Crunchbase.search(query)
            for i, cb_company in enumerate(cb_search):
                db_company = CompanyDAO.get(cb_company['uuid'])
                if db_company is not None:
                    cb_search[i] = mongo_to_dict(db_company)
            return cb_search
        return api.abort(400, "Missing query parameter")


if __name__ == '__main__':
    from mongoengine import connect
    _username = 'azuma'
    _password = 'CotGiQnKX1hQGbkjw4JlIpEyE6mvqwto'
    connect('myFirstDatabase',
            host=f'mongodb+srv://{_username}:{_password}@cluster0.9amyl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    app.run(port=8008, debug=True)
