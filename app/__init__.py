from mongoengine import connect 
from flask import Flask, Blueprint
from os import urandom

api = Blueprint('api', __name__)
app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(32)

from app.utils.secrets import getSecrets
secrets = getSecrets()

connect(secrets['MONGO_DB_NAME'], host=secrets['MONGO_HOST'])

from .routes import *
app.register_blueprint(api, url_prefix='/api')
