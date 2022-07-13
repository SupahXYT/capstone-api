from flask import Flask
from flask_restx import Api, Resource, fields

# from app.gateway.authentication import User
import crunchbase_service

app = Flask(__name__)
api = Api(app, version='0.1', title='CMT API',
          description='The PMT (Privacy Management Tool) API gateway')

crunchbase_ns = api.namespace('crunchbase', description='crunchbase lookup api')

crunchbase = api.model('Crunchbase', {
    'uuid': fields.String(readonly=True, description="UUID of the organization")
})


@crunchbase_ns.route('/<string:uuid>')
class CrunchbaseSearch(Resource):
    def get(self, uuid):
        return crunchbase_service.CrunchbaseService.get_company(uuid)


if __name__ == '__main__':
    app.run()