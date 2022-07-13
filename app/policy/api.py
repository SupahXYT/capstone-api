from flask import Flask, request
from flask_restx import Api, Resource, fields
from app.policy.scrape import PolicyWrapper

app = Flask(__name__)
api = Api(app, version='0.1',
          description='Privacy policy scraper service')

ns = api.namespace('policy', description='Privacy policy')


@ns.route('')
class Policy(Resource):
    def get(self):
        """Fetch the privacy policy of a website from given url"""
        url = request.args.get('url')
        if url is None:
            api.abort(400, "Missing website url")
        with PolicyWrapper() as policy:
            return policy.get_policy(url)


if __name__ == '__main__':
    app.run(debug=True)
